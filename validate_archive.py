#!/usr/bin/env python3
"""Validate the Atom OS Research archive's structural invariants."""

from __future__ import annotations

import copy
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlsplit

try:
    import jsonschema
    import yaml
except ModuleNotFoundError as error:
    print(
        f"Missing validation dependency: {error.name}. "
        "Run `python3 -m pip install -r requirements-validation.txt`.",
        file=sys.stderr,
    )
    raise SystemExit(2) from error


ROOT = Path(__file__).resolve().parent
SCHEMA_PATH = ROOT / "frontmatter.schema.json"
ARCHIVE_DIRECTORIES = {
    "00-inbox",
    "10-maps",
    "20-notes",
    "30-sources",
    "40-inquiries",
    "50-journal",
    "90-archive",
    "assets",
    "templates",
}
IGNORED_NAMES = {
    ".DS_Store",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
}
REQUIRED_README_HEADINGS = {
    "Purpose",
    "What belongs here",
    "Index",
    "Maintaining this index",
}
KNOWLEDGE_FILENAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
JOURNAL_FILENAME = re.compile(
    r"^\d{4}-\d{2}-\d{2}(?:-[a-z0-9]+(?:-[a-z0-9]+)*)?\.md$"
)
DEEP_DIVE_JOURNAL_FILENAME = re.compile(
    r"^\d{4}-\d{2}-\d{2}(?:-[a-z0-9]+)*-deep-dive\.md$"
)
PLACEHOLDER = re.compile(
    r"\{(?:title|question|YYYY-MM-DD|author|directory title|directory-name)\}"
)
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


class StringDateLoader(yaml.SafeLoader):
    """A safe YAML loader that does not coerce ISO dates to Python dates."""


StringDateLoader.yaml_implicit_resolvers = copy.deepcopy(
    yaml.SafeLoader.yaml_implicit_resolvers
)
for initial, resolvers in list(StringDateLoader.yaml_implicit_resolvers.items()):
    StringDateLoader.yaml_implicit_resolvers[initial] = [
        (tag, expression)
        for tag, expression in resolvers
        if tag != "tag:yaml.org,2002:timestamp"
    ]


def relative(path: Path) -> str:
    """Return a stable repository-relative display path."""

    try:
        value = path.resolve().relative_to(ROOT)
    except ValueError:
        return str(path)
    return "." if value == Path(".") else value.as_posix()


def is_ignored(path: Path) -> bool:
    """Return whether a path is repository machinery rather than archive data."""

    try:
        parts = path.resolve().relative_to(ROOT).parts
    except ValueError:
        parts = path.parts
    return any(part in IGNORED_NAMES or part.startswith(".") for part in parts)


def visible_children(directory: Path) -> list[Path]:
    """Return direct archive children, excluding repository machinery."""

    return sorted(
        (
            child
            for child in directory.iterdir()
            if not is_ignored(child) and child.name != "README.md"
        ),
        key=lambda child: child.name,
    )


def archive_directories() -> list[Path]:
    """Return the root and every non-generated archive directory."""

    return [
        ROOT,
        *sorted(
            (
                path
                for path in ROOT.rglob("*")
                if path.is_dir() and not is_ignored(path)
            ),
            key=lambda path: path.as_posix(),
        ),
    ]


def completed_markdown_files() -> list[Path]:
    """Return completed knowledge documents and directory READMEs."""

    files: list[Path] = []
    for top_name in sorted(ARCHIVE_DIRECTORIES):
        top = ROOT / top_name
        if not top.is_dir():
            continue
        for path in sorted(top.rglob("*.md")):
            if is_ignored(path):
                continue
            if top_name == "templates" and path.name != "README.md":
                continue
            if top_name == "00-inbox" and path.name != "README.md":
                continue
            files.append(path)
    return files


def parse_frontmatter(path: Path) -> tuple[dict[str, object], str]:
    """Parse one completed Markdown file into metadata and body."""

    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing opening YAML frontmatter delimiter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("missing closing YAML frontmatter delimiter")
    metadata = yaml.load(text[4:end], Loader=StringDateLoader)
    if not isinstance(metadata, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return metadata, text[end + 5 :]


def link_destination(raw: str) -> str:
    """Remove optional Markdown angle brackets and link titles."""

    value = raw.strip()
    if value.startswith("<"):
        close = value.find(">")
        return value[1:close] if close >= 0 else value[1:]
    return value.split(maxsplit=1)[0]


def local_link_target(source: Path, raw: str) -> tuple[Path, str] | None:
    """Resolve a Markdown destination, returning None for external links."""

    destination = link_destination(raw)
    parsed = urlsplit(destination)
    if parsed.scheme or parsed.netloc:
        return None
    decoded_path = unquote(parsed.path)
    target = source if not decoded_path else source.parent / decoded_path
    return target.resolve(), unquote(parsed.fragment)


def github_heading_anchors(markdown: str) -> set[str]:
    """Approximate GitHub heading IDs, including duplicate suffixes."""

    anchors: set[str] = set()
    occurrences: defaultdict[str, int] = defaultdict(int)
    for line in markdown.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        heading = re.sub(r"<[^>]+>", "", match.group(1))
        heading = re.sub(r"[`*_~]", "", heading).strip().lower()
        slug = re.sub(r"[^\w\- ]", "", heading, flags=re.UNICODE)
        slug = re.sub(r"\s+", "-", slug)
        suffix = occurrences[slug]
        occurrences[slug] += 1
        anchors.add(slug if suffix == 0 else f"{slug}-{suffix}")
    return anchors


def markdown_without_hidden_content(markdown: str) -> str:
    """Remove HTML comments and fenced code before structural Markdown checks."""

    markdown = re.sub(
        r"<!--.*?-->",
        lambda match: "\n" * match.group(0).count("\n"),
        markdown,
        flags=re.DOTALL,
    )
    visible: list[str] = []
    fence_character: str | None = None
    fence_length = 0
    for line in markdown.splitlines():
        fence = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if fence_character is None:
            if fence:
                fence_character = fence.group(1)[0]
                fence_length = len(fence.group(1))
                visible.append("")
            else:
                visible.append(line)
            continue
        if fence and fence.group(1)[0] == fence_character and len(
            fence.group(1)
        ) >= fence_length:
            fence_character = None
            fence_length = 0
        visible.append("")
    return "\n".join(visible)


def markdown_heading_section(
    markdown: str, level: int, heading: str
) -> str | None:
    """Return content below one heading through the next peer or ancestor."""

    lines = markdown_without_hidden_content(markdown).splitlines()
    marker = f"{'#' * level} {heading}"
    starts = [index for index, line in enumerate(lines) if line.strip() == marker]
    if len(starts) != 1:
        return None
    start = starts[0] + 1
    end = len(lines)
    for index in range(start, len(lines)):
        match = re.match(r"^\s{0,3}(#{1,6})\s+", lines[index])
        if match and len(match.group(1)) <= level:
            end = index
            break
    return "\n".join(lines[start:end])


def markdown_list_items(markdown: str) -> list[str]:
    """Return top-level hyphen list items with wrapped continuation text."""

    items: list[str] = []
    current: list[str] | None = None
    for line in markdown_without_hidden_content(markdown).splitlines():
        bullet = re.match(r"^\s{0,3}-\s+(.*)$", line)
        if bullet:
            if current is not None:
                items.append(" ".join(current))
            current = [bullet.group(1).strip()]
            continue
        if current is None:
            continue
        if re.match(r"^\s{0,3}#{1,6}\s+", line):
            items.append(" ".join(current))
            current = None
            continue
        if line.strip():
            current.append(line.strip())
    if current is not None:
        items.append(" ".join(current))
    return items


def markdown_without_sections(
    markdown: str, level: int, excluded_headings: set[str]
) -> str:
    """Remove named heading sections through their next peer or ancestor."""

    kept: list[str] = []
    skipping = False
    for line in markdown_without_hidden_content(markdown).splitlines():
        match = re.match(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if match and len(match.group(1)) <= level:
            skipping = (
                len(match.group(1)) == level
                and match.group(2).strip() in excluded_headings
            )
        if not skipping:
            kept.append(line)
    return "\n".join(kept)


def validate() -> tuple[list[str], dict[str, int]]:
    """Run all checks and return errors plus summary counts."""

    errors: list[str] = []
    counts: defaultdict[str, int] = defaultdict(int)

    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
    except (OSError, json.JSONDecodeError, jsonschema.SchemaError) as error:
        return [f"{relative(SCHEMA_PATH)}: invalid JSON Schema: {error}"], counts

    validator = jsonschema.Draft202012Validator(
        schema, format_checker=jsonschema.FormatChecker()
    )
    records: dict[Path, tuple[dict[str, object], str]] = {}

    for top_name in sorted(ARCHIVE_DIRECTORIES):
        if not (ROOT / top_name).is_dir():
            errors.append(f"{top_name}/: missing canonical archive directory")

    for path in completed_markdown_files():
        counts["completed_documents"] += 1
        try:
            metadata, body = parse_frontmatter(path)
        except (OSError, ValueError, yaml.YAMLError) as error:
            errors.append(f"{relative(path)}: {error}")
            continue
        records[path.resolve()] = (metadata, body)
        schema_errors = validator.iter_errors(metadata)
        for schema_error in sorted(
            schema_errors, key=lambda item: list(item.absolute_path)
        ):
            location = ".".join(str(part) for part in schema_error.absolute_path)
            errors.append(
                f"{relative(path)}: frontmatter {location or '<root>'}: "
                f"{schema_error.message}"
            )

        h1 = re.search(r"^#\s+(.+?)\s*$", body, flags=re.MULTILINE)
        title = str(metadata.get("title", ""))
        if h1 is None:
            errors.append(f"{relative(path)}: missing H1")
        elif path.name == "README.md":
            if not h1.group(1).replace("`", "").startswith(title):
                errors.append(
                    f"{relative(path)}: H1 {h1.group(1)!r} does not match title "
                    f"{title!r}"
                )
        elif h1.group(1) != title:
            errors.append(
                f"{relative(path)}: H1 {h1.group(1)!r} does not match title {title!r}"
            )

        if path.name == "README.md":
            continue
        kind = metadata.get("kind")
        filename_pattern = JOURNAL_FILENAME if kind == "journal" else KNOWLEDGE_FILENAME
        if not filename_pattern.fullmatch(path.name):
            errors.append(
                f"{relative(path)}: filename does not follow the convention for {kind}"
            )
        top_name = path.relative_to(ROOT).parts[0]
        destinations = {
            "map": "10-maps",
            "note": "20-notes",
            "source": "30-sources",
            "inquiry": "40-inquiries",
            "journal": "50-journal",
        }
        expected = destinations.get(kind)
        if top_name not in {"90-archive", "assets"} and expected and top_name != expected:
            errors.append(f"{relative(path)}: kind {kind!r} belongs in {expected}/")

    for path in sorted(ROOT.rglob("*.md")):
        if is_ignored(path):
            continue
        if path.parent == ROOT / "templates" or path == ROOT / "AGENTS.md":
            continue
        if path.parent == ROOT / "00-inbox" and path.name != "README.md":
            continue
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if PLACEHOLDER.search(line):
                errors.append(
                    f"{relative(path)}:{line_number}: unresolved template placeholder"
                )

    links_by_source: defaultdict[Path, set[Path]] = defaultdict(set)
    incoming_from_conceptual: defaultdict[Path, set[Path]] = defaultdict(set)
    for path in sorted(ROOT.rglob("*.md")):
        if is_ignored(path):
            continue
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for raw in MARKDOWN_LINK.findall(line):
                resolved = local_link_target(path, raw)
                if resolved is None:
                    continue
                target, fragment = resolved
                counts["local_links"] += 1
                if link_destination(raw).startswith("/"):
                    errors.append(
                        f"{relative(path)}:{line_number}: local link must be relative: {raw}"
                    )
                    continue
                if not target.exists():
                    errors.append(
                        f"{relative(path)}:{line_number}: missing local link target: {raw}"
                    )
                    continue
                links_by_source[path.resolve()].add(target)
                if target.suffix.lower() == ".md" and fragment:
                    anchors = github_heading_anchors(target.read_text(encoding="utf-8"))
                    if fragment not in anchors:
                        errors.append(
                            f"{relative(path)}:{line_number}: missing heading fragment "
                            f"#{fragment} in {relative(target)}"
                        )

                source_record = records.get(path.resolve())
                source_is_conceptual = path == ROOT / "README.md" or (
                    source_record is not None
                    and path.name != "README.md"
                    and source_record[0].get("kind") == "map"
                )
                if source_is_conceptual:
                    incoming_from_conceptual[target].add(path.resolve())

    introduced_by_source: defaultdict[Path, list[Path]] = defaultdict(list)
    for path, (metadata, body) in sorted(
        records.items(), key=lambda item: relative(item[0])
    ):
        is_deep_dive_journal = (
            metadata.get("kind") == "journal"
            and DEEP_DIVE_JOURNAL_FILENAME.fullmatch(path.name) is not None
        )
        if metadata.get("kind") != "journal":
            continue

        visible_body = markdown_without_hidden_content(body)
        manifest_heading_count = len(
            re.findall(
                r"^\s{0,3}##\s+Source manifest\s*#*\s*$",
                visible_body,
                flags=re.MULTILINE,
            )
        )
        if is_deep_dive_journal:
            counts["deep_dive_journals"] += 1
        if not manifest_heading_count:
            if is_deep_dive_journal:
                errors.append(f"{relative(path)}: missing unique ## Source manifest")
            continue
        if manifest_heading_count != 1:
            errors.append(f"{relative(path)}: missing unique ## Source manifest")
            continue

        manifest = markdown_heading_section(body, 2, "Source manifest")
        if manifest is None:
            errors.append(f"{relative(path)}: missing unique ## Source manifest")
            continue

        expected_categories = {"Newly introduced sources", "Reused sources"}
        actual_categories = set(
            re.findall(
                r"^\s{0,3}###\s+(.+?)\s*#*\s*$",
                manifest,
                flags=re.MULTILINE,
            )
        )
        for unexpected in sorted(actual_categories - expected_categories):
            errors.append(
                f"{relative(path)}: unexpected source-manifest category: {unexpected}"
            )

        classified: dict[str, set[Path]] = {}
        for heading in ("Newly introduced sources", "Reused sources"):
            section = markdown_heading_section(manifest, 3, heading)
            if section is None:
                errors.append(f"{relative(path)}: missing unique ### {heading}")
                continue

            targets: list[Path] = []
            items = markdown_list_items(section)
            if items == ["None."]:
                classified[heading] = set()
                continue
            if not items:
                errors.append(
                    f"{relative(path)}: ### {heading} must list source notes or - None."
                )
                classified[heading] = set()
                continue
            if "None." in items or "None" in items:
                errors.append(
                    f"{relative(path)}: ### {heading} must use exactly - None. alone"
                )

            for item in items:
                raw_links = MARKDOWN_LINK.findall(item)
                if len(raw_links) != 1:
                    errors.append(
                        f"{relative(path)}: each ### {heading} item must contain "
                        "exactly one inline source-note link"
                    )
                    continue
                raw = raw_links[0]
                resolved = local_link_target(path, raw)
                if resolved is None:
                    errors.append(
                        f"{relative(path)}: {heading} entry must link a local "
                        f"source note: {raw}"
                    )
                    continue
                target, _fragment = resolved
                target_record = records.get(target)
                if target_record is None or target_record[0].get("kind") != "source":
                    errors.append(
                        f"{relative(path)}: {heading} link is not a source note: {raw}"
                    )
                    continue
                targets.append(target)
                if not re.search(r"\)\s+—\s+\S", item):
                    errors.append(
                        f"{relative(path)}: {heading} entry lacks an em-dash role "
                        f"description for {relative(target)}"
                    )
            if len(targets) != len(items):
                errors.append(
                    f"{relative(path)}: every ### {heading} list item must be valid"
                )
            if len(targets) != len(set(targets)):
                errors.append(
                    f"{relative(path)}: duplicate source within ### {heading}"
                )
            classified[heading] = set(targets)

        introduced = classified.get("Newly introduced sources", set())
        reused = classified.get("Reused sources", set())
        if is_deep_dive_journal:
            counts["introduced_source_classifications"] += len(introduced)
            counts["reused_source_classifications"] += len(reused)
        for target in sorted(introduced & reused):
            errors.append(
                f"{relative(path)}: source classified as both introduced and reused: "
                f"{relative(target)}"
            )
        for target in introduced:
            if is_deep_dive_journal:
                introduced_by_source[target].append(path)
            target_metadata = records[target][0]
            if target_metadata.get("created") != metadata.get("created"):
                errors.append(
                    f"{relative(path)}: introduced source has different creation date: "
                    f"{relative(target)}"
                )
        for target in reused:
            target_metadata = records[target][0]
            target_created = str(target_metadata.get("created", ""))
            journal_created = str(metadata.get("created", ""))
            if target_created > journal_created:
                errors.append(
                    f"{relative(path)}: reused source was created after the session: "
                    f"{relative(target)}"
                )

        substantive_body = markdown_without_sections(
            body, 2, {"Threads", "Follow-ups"}
        )
        all_linked_sources: set[Path] = set()
        for raw in MARKDOWN_LINK.findall(substantive_body):
            resolved = local_link_target(path, raw)
            if resolved is None:
                continue
            target, _fragment = resolved
            target_record = records.get(target)
            if target_record is not None and target_record[0].get("kind") == "source":
                all_linked_sources.add(target)
        for target in sorted(all_linked_sources - introduced - reused):
            errors.append(
                f"{relative(path)}: linked source missing from source manifest: "
                f"{relative(target)}"
            )

    deep_dive_journals = {
        path
        for path, (metadata, _body) in records.items()
        if metadata.get("kind") == "journal"
        and DEEP_DIVE_JOURNAL_FILENAME.fullmatch(path.name) is not None
    }
    sources_readme = (ROOT / "30-sources" / "README.md").resolve()
    sources_readme_record = records.get(sources_readme)
    if sources_readme_record is not None:
        provenance = markdown_heading_section(
            sources_readme_record[1], 2, "Research provenance"
        )
        if provenance is None:
            errors.append(
                "30-sources/README.md: missing unique ## Research provenance"
            )
        else:
            journal_links: list[Path] = []
            for raw in MARKDOWN_LINK.findall(provenance):
                resolved = local_link_target(sources_readme, raw)
                if resolved is None:
                    continue
                target, _fragment = resolved
                target_record = records.get(target)
                if target_record is not None and target_record[0].get("kind") == "journal":
                    if DEEP_DIVE_JOURNAL_FILENAME.fullmatch(target.name) is not None:
                        journal_links.append(target)
            if len(journal_links) != len(set(journal_links)):
                errors.append(
                    "30-sources/README.md: duplicate deep-dive journal in "
                    "## Research provenance"
                )
            for missing in sorted(deep_dive_journals - set(journal_links)):
                errors.append(
                    "30-sources/README.md: deep-dive journal missing from research "
                    f"provenance: {relative(missing)}"
                )

    for source, journals in sorted(
        introduced_by_source.items(), key=lambda item: relative(item[0])
    ):
        if len(journals) > 1:
            joined = ", ".join(relative(path) for path in sorted(journals))
            errors.append(
                f"{relative(source)}: introduced by multiple deep-dive journals: {joined}"
            )

    counts["sources_without_deep_dive_origin"] = sum(
        1
        for path, (metadata, _body) in records.items()
        if metadata.get("kind") == "source" and path not in introduced_by_source
    )

    for directory in archive_directories():
        counts["directories"] += 1
        readme = directory / "README.md"
        if not readme.is_file():
            errors.append(f"{relative(directory)}: missing README.md")
            continue
        text = readme.read_text(encoding="utf-8")
        headings = set(re.findall(r"^##\s+(.+?)\s*$", text, flags=re.MULTILINE))
        if directory != ROOT:
            for missing in sorted(REQUIRED_README_HEADINGS - headings):
                errors.append(f"{relative(readme)}: missing section ## {missing}")
            if not re.search(r"^###\s+Subdirectories\s*$", text, flags=re.MULTILINE):
                errors.append(f"{relative(readme)}: missing ### Subdirectories")
            if not re.search(
                r"^###\s+(?:Documents|Files|Templates)\s*$",
                text,
                flags=re.MULTILINE,
            ):
                errors.append(
                    f"{relative(readme)}: missing ### Documents, ### Files, or "
                    "### Templates"
                )

        indexed_targets = links_by_source.get(readme.resolve(), set())
        for child in visible_children(directory):
            expected = child / "README.md" if child.is_dir() else child
            if expected.resolve() not in indexed_targets:
                errors.append(
                    f"{relative(readme)}: unindexed direct child {child.name!r}"
                )

    completed_paths = set(records)
    for path, (metadata, _body) in sorted(
        records.items(), key=lambda item: relative(item[0])
    ):
        if path.name == "README.md":
            continue
        outgoing = {
            target
            for target in links_by_source.get(path, set())
            if target == ROOT / "README.md" or target in completed_paths
        }
        if not outgoing and not incoming_from_conceptual.get(path):
            errors.append(f"{relative(path)}: no conceptual body link or incoming map link")

    identifiers: dict[str, defaultdict[str, list[Path]]] = {
        key: defaultdict(list) for key in ("citation_key", "doi", "url")
    }
    for path, (metadata, _body) in records.items():
        if metadata.get("kind") != "source":
            continue
        counts["source_documents"] += 1
        for key, values in identifiers.items():
            value = metadata.get(key)
            if value:
                values[str(value).casefold()].append(path)
    for key, values in identifiers.items():
        for value, paths in sorted(values.items()):
            if len(paths) > 1:
                joined = ", ".join(relative(path) for path in sorted(paths))
                errors.append(f"duplicate {key} {value!r}: {joined}")

    return sorted(set(errors)), counts


def main() -> int:
    errors, counts = validate()
    if errors:
        print(f"Archive validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Archive validation passed: "
        f"{counts['completed_documents']} completed documents, "
        f"{counts['directories']} directories, "
        f"{counts['local_links']} local links, and "
        f"{counts['source_documents']} source notes checked; "
        f"{counts['deep_dive_journals']} deep-dive source manifests classify "
        f"{counts['introduced_source_classifications']} introduced and "
        f"{counts['reused_source_classifications']} reused source uses; "
        f"{counts['sources_without_deep_dive_origin']} source notes entered "
        "outside a deep-dive manifest."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
