#!/usr/bin/env python3
"""Focused tests for Atom OS Research archive validation."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import jsonschema

from validate_archive import (
    ARCHIVE_DIRECTORIES,
    DEEP_DIVE_JOURNAL_FILENAME,
    ROOT,
    completed_markdown_files,
    github_heading_anchors,
    link_destination,
    local_link_target,
    markdown_heading_section,
    markdown_list_items,
    markdown_without_sections,
    parse_frontmatter,
    validate,
)


class FrontmatterSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        schema = json.loads((ROOT / "frontmatter.schema.json").read_text(encoding="utf-8"))
        cls.validator = jsonschema.Draft202012Validator(
            schema, format_checker=jsonschema.FormatChecker()
        )

    def test_accepts_valid_note(self) -> None:
        metadata = {
            "title": "Example",
            "kind": "note",
            "created": "2026-08-28",
            "maturity": "seed",
            "tags": ["atom-vm"],
            "aliases": [],
        }
        self.assertEqual([], list(self.validator.iter_errors(metadata)))

    def test_rejects_note_without_maturity(self) -> None:
        metadata = {
            "title": "Example",
            "kind": "note",
            "created": "2026-08-28",
            "tags": [],
            "aliases": [],
        }
        self.assertNotEqual([], list(self.validator.iter_errors(metadata)))

    def test_rejects_uncontrolled_tag_spelling(self) -> None:
        metadata = {
            "title": "Example",
            "kind": "map",
            "created": "2026-08-28",
            "tags": ["Not Kebab Case"],
            "aliases": [],
        }
        self.assertNotEqual([], list(self.validator.iter_errors(metadata)))


class PlanningArchiveTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        for name in sorted(ARCHIVE_DIRECTORIES):
            directory = self.root / name
            directory.mkdir()
            self.write_readme(directory)
        (self.root / "README.md").write_text(
            "# Test archive\n\n"
            + "\n".join(
                f"- [{name}]({name}/README.md)" for name in sorted(ARCHIVE_DIRECTORIES)
            )
            + "\n",
            encoding="utf-8",
        )
        self.milestone = self.root / "60-planning" / "m0-prototype-contract"
        self.milestone.mkdir()
        self.write_readme(self.milestone)
        self.write_readme(self.milestone.parent)
        root_patch = patch("validate_archive.ROOT", self.root)
        root_patch.start()
        self.addCleanup(root_patch.stop)

    def write_readme(self, directory: Path, kind: str = "map") -> None:
        children = sorted(directory.iterdir())
        directories = [child for child in children if child.is_dir()]
        documents = [
            child for child in children if child.is_file() and child.name != "README.md"
        ]
        metadata = (
            "---\ntitle: Test index\n"
            f"kind: {kind}\n"
            'created: "2026-09-06"\ntags: []\naliases: []\n'
        )
        if kind == "note":
            metadata += "maturity: developing\n"
        body = (
            "---\n\n# Test index\n\n## Purpose\n\nTest fixture.\n\n"
            "## What belongs here\n\nFixture documents.\n\n"
            "## Index\n\n### Subdirectories\n\n"
            + ("\n".join(f"- [{child.name}]({child.name}/README.md)" for child in directories)
               or "- None.")
            + "\n\n### Documents\n\n"
            + ("\n".join(f"- [{child.name}]({child.name})" for child in documents)
               or "- None.")
            + "\n\n## Maintaining this index\n\nKeep fixture links current.\n"
        )
        if directory.name == "30-sources":
            body += "\n## Research provenance\n\n- None.\n"
        (directory / "README.md").write_text(metadata + body, encoding="utf-8")

    def write_note(self, directory: Path, maturity: str | None = "developing") -> Path:
        path = directory / "phase-01-contract.md"
        metadata = (
            "---\ntitle: Contract phase\nkind: note\n"
            'created: "2026-09-06"\ntags: [implementation-plan]\naliases: []\n'
        )
        if maturity is not None:
            metadata += f"maturity: {maturity}\n"
        path.write_text(
            metadata + "---\n\n# Contract phase\n\n[Milestone index](README.md).\n",
            encoding="utf-8",
        )
        self.write_readme(directory)
        return path

    def test_planning_note_and_map_readmes_are_validated(self) -> None:
        path = self.write_note(self.milestone)
        self.assertIn(path, completed_markdown_files())
        self.assertIn(self.milestone / "README.md", completed_markdown_files())
        errors, _counts = validate()
        self.assertEqual([], errors)

    def test_planning_note_frontmatter_is_checked(self) -> None:
        self.write_note(self.milestone, maturity=None)
        errors, _counts = validate()
        self.assertTrue(
            any(
                error.startswith("60-planning/m0-prototype-contract/phase-01-contract.md: frontmatter")
                for error in errors
            ),
            errors,
        )

    def test_note_is_still_allowed_in_notes(self) -> None:
        self.write_note(self.root / "20-notes")
        errors, _counts = validate()
        self.assertEqual([], errors)

    def test_note_is_forbidden_in_unrelated_destination(self) -> None:
        self.write_note(self.root / "30-sources")
        errors, _counts = validate()
        self.assertIn(
            "30-sources/phase-01-contract.md: kind 'note' belongs in 20-notes/ or 60-planning/",
            errors,
        )

    def test_planning_readme_requires_map_kind(self) -> None:
        self.write_readme(self.milestone, kind="note")
        errors, _counts = validate()
        self.assertIn(
            "60-planning/m0-prototype-contract/README.md: directory README must use kind 'map'",
            errors,
        )

    def test_source_is_not_allowed_in_planning(self) -> None:
        path = self.write_note(self.milestone, maturity=None)
        path.write_text(
            path.read_text(encoding="utf-8").replace("kind: note\n", "kind: source\n"),
            encoding="utf-8",
        )
        errors, _counts = validate()
        self.assertIn(
            "60-planning/m0-prototype-contract/phase-01-contract.md: kind 'source' belongs in 30-sources/",
            errors,
        )


class MarkdownTests(unittest.TestCase):
    def test_heading_anchors_include_duplicate_suffixes(self) -> None:
        anchors = github_heading_anchors("# A Title\n\n## Repeat\n\n## Repeat\n")
        self.assertEqual({"a-title", "repeat", "repeat-1"}, anchors)

    def test_link_destination_removes_title_and_angle_brackets(self) -> None:
        self.assertEqual("notes/a.md", link_destination('notes/a.md "title"'))
        self.assertEqual("notes/a file.md", link_destination("<notes/a file.md>"))

    def test_external_link_has_no_local_target(self) -> None:
        self.assertIsNone(local_link_target(ROOT / "README.md", "https://example.com"))

    def test_heading_section_keeps_nested_headings(self) -> None:
        markdown = (
            "## Source manifest\n\n"
            "### Newly introduced sources\n\n"
            "#### Foundations\n\n- [One](../30-sources/one.md)\n\n"
            "### Reused sources\n\n- None.\n\n"
            "## Threads\n"
        )
        manifest = markdown_heading_section(markdown, 2, "Source manifest")
        self.assertIsNotNone(manifest)
        assert manifest is not None
        introduced = markdown_heading_section(
            manifest, 3, "Newly introduced sources"
        )
        self.assertIn("#### Foundations", introduced or "")
        self.assertNotIn("### Reused sources", introduced or "")

    def test_heading_section_requires_unique_heading(self) -> None:
        markdown = "## Evidence\n\n## Evidence\n"
        self.assertIsNone(markdown_heading_section(markdown, 2, "Evidence"))

    def test_heading_section_ignores_comments_and_fences(self) -> None:
        markdown = (
            "<!-- ## Source manifest -->\n"
            "```markdown\n## Source manifest\n```\n"
            "## Source manifest\n\nVisible\n\n## Threads\n"
        )
        self.assertEqual(
            "\nVisible\n",
            markdown_heading_section(markdown, 2, "Source manifest"),
        )

    def test_list_items_join_wrapped_role_descriptions(self) -> None:
        markdown = (
            "#### Foundation\n\n"
            "- [One](../30-sources/one.md)\n"
            "  — a wrapped role description.\n"
            "- [Two](../30-sources/two.md) — another role.\n"
        )
        self.assertEqual(
            [
                "[One](../30-sources/one.md) — a wrapped role description.",
                "[Two](../30-sources/two.md) — another role.",
            ],
            markdown_list_items(markdown),
        )

    def test_removes_prospective_source_sections(self) -> None:
        markdown = (
            "## Evidence\n\nKeep\n\n"
            "## Threads\n\nRemove\n\n### Nested\n\nRemove too\n\n"
            "## Outcome\n\nKeep again\n"
        )
        visible = markdown_without_sections(markdown, 2, {"Threads", "Follow-ups"})
        self.assertIn("Keep", visible)
        self.assertIn("Keep again", visible)
        self.assertNotIn("Remove", visible)

    def test_deep_dive_filename_detection(self) -> None:
        self.assertIsNotNone(
            DEEP_DIVE_JOURNAL_FILENAME.fullmatch("2026-09-04-auth-deep-dive.md")
        )
        self.assertIsNotNone(
            DEEP_DIVE_JOURNAL_FILENAME.fullmatch("2026-09-04-deep-dive.md")
        )
        self.assertIsNone(
            DEEP_DIVE_JOURNAL_FILENAME.fullmatch("2026-09-04-research.md")
        )


class FrontmatterParsingTests(unittest.TestCase):
    def test_dates_remain_strings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "example.md"
            path.write_text(
                "---\ntitle: Example\nkind: map\ncreated: 2026-08-28\n"
                "tags: []\naliases: []\n---\n# Example\n",
                encoding="utf-8",
            )
            metadata, body = parse_frontmatter(path)
        self.assertEqual("2026-08-28", metadata["created"])
        self.assertIn("# Example", body)


if __name__ == "__main__":
    unittest.main()
