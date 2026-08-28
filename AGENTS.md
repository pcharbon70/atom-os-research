# Repository instructions

These instructions apply to the entire repository. This is a Markdown research
archive, not a conventional software project. Preserve room for exploratory
thought while keeping provenance, navigation, and document structure reliable.

Follow an explicit user request when it conflicts with this file. Otherwise,
use these conventions for every document and organizational change.

## Project goal

This project researches how `atom-vm` can serve as the actual foundation for a
new operating-system design, rather than merely running as an application on
top of an existing operating system.

Keep research and implementation work oriented toward making `atom-vm` the
system's foundational execution environment. Relevant areas include boot and
bring-up, hardware abstraction and drivers, scheduling, memory management,
isolation and capabilities, persistence, networking, tooling, and the path from
a research prototype to a bootable system.

Distinguish clearly among:

- behavior already provided by `atom-vm`;
- behavior inherited from a host operating system or platform port;
- behavior an `atom-vm`-based operating system would need to own;
- evidence demonstrated by an experiment; and
- proposed architecture that remains unverified.

## Archive principles

- Folders describe what a document is doing; maps, links, and tags describe
  what it is about.
- Prefer a small stable top-level structure over speculative subject folders.
- Preserve provenance. Separate a source's claims, our synthesis, local
  experimental evidence, and unresolved questions.
- Keep navigation useful at two levels: directory READMEs are complete local
  inventories, while maps are selective conceptual paths.
- Treat `frontmatter.schema.json` as the authoritative metadata contract.
- Keep related changes atomic: change a document and every affected index,
  link, and map together.

## Canonical structure

```text
00-inbox/       Unprocessed, temporary captures
10-maps/        Curated paths through subjects and questions
20-notes/       Ideas and syntheses in the author's own words
30-sources/     Reading notes and bibliographic records
40-inquiries/   Active questions and research workbenches
50-journal/     Dated observations and research-session evidence
90-archive/     Inactive or superseded material worth retaining
assets/         Images, PDFs, diagrams, datasets, and attachments
templates/      Starting points for documents and directory indexes
```

Do not add or rename a top-level directory unless the user asks or a repeated,
demonstrated need makes the existing structure inadequate. Organize subjects
through tags, links, and maps first.

## Sources of truth

Use these files for different decisions:

1. `frontmatter.schema.json` defines valid metadata fields and values.
2. `templates/` defines the minimum starting structure for each artifact.
3. The root `README.md` explains the archive to human readers.
4. Each directory's `README.md` describes and inventories that directory.
5. `10-maps/` provides curated thematic navigation.
6. `validate_archive.py` performs deterministic structural checks.

If documentation and the filesystem disagree, inspect the intended change and
bring them back into sync. Never preserve a stale index merely because it was
previously written.

## Directory README invariant

Every archive directory, including a future nested directory, must contain a
`README.md`. Create it from `templates/directory-readme.md` as part of creating
the directory.

Directory READMEs must:

- use valid frontmatter with `kind: map` (the root README is the exception);
- include `## Purpose`, `## What belongs here`, `## Index`, and
  `## Maintaining this index`;
- list `### Subdirectories` and then `### Documents`, `### Files`, or
  `### Templates` under the index;
- inventory every direct child except the README itself;
- link entries relatively and explain their role;
- state an explicit empty state when a category has no entries; and
- link a child directory through its README rather than its bare path.

Whenever content is added, moved, renamed, archived, or removed, update every
affected directory README, map, and meaningful body link in the same change.
Do not index `.git`, generated caches, editor state, or similar machinery.

## Frontmatter contract

Every durable knowledge document and directory README begins with YAML
frontmatter that validates against `frontmatter.schema.json`:

```yaml
---
title: "A human-readable title"
kind: note
created: "2026-08-28"
tags: []
aliases: []
---
```

Additional requirements depend on `kind`:

- `note` requires `maturity: seed | developing | stable`.
- `inquiry` requires `status: open | paused | resolved`.
- `source` may use `authors`, `published`, `citation_key`, `container`,
  `edition`, `isbn`, `doi`, `url`, and `accessed`.
- `map` and `journal` use the common fields.

Quote dates in `YYYY-MM-DD` form. Use the archive document's creation date,
not its subject's publication date. Use lowercase kebab-case tags, YAML lists
for tags and aliases, `[]` for an intentionally empty list, and `null` for an
unknown nullable value. Never invent missing source metadata. Do not add an
`updated` field by hand; revision control records history.

The root `README.md`, `AGENTS.md`, validation scripts, and validation
requirements are repository documentation or tooling and do not use archive
frontmatter. Template placeholders are exempt until copied and filled. A
transient inbox capture may be incomplete, but it must validate before
promotion. Binary assets do not use frontmatter; document them in their local
directory README.

## Document roles and templates

| Artifact | Destination | Template | Intended result |
| --- | --- | --- | --- |
| Directory index | Any archive directory's `README.md` | `templates/directory-readme.md` | An exhaustive local inventory |
| Conceptual map | `10-maps/` | `templates/map.md` | A selective route through related work |
| Note | `20-notes/` | `templates/note.md` | An idea, argument, model, or synthesis |
| Source note | `30-sources/` | `templates/source.md` | A bibliographic record and evidence-focused analysis |
| Inquiry | `40-inquiries/` | `templates/inquiry.md` | A live question, hypotheses, findings, and outcome |
| Journal entry | `50-journal/` | `templates/journal.md` | A dated observation or reproducible research-session record |

Copy the closest template, replace every placeholder, and adapt its headings
only as the material requires. Do not add a document kind when an existing role
plus links or tags expresses the same work.

## Filenames and paths

- Use lowercase kebab-case Markdown filenames.
- Name notes and maps for their subject, not their creation date.
- Name inquiries as concise questions in kebab case.
- Name journal entries `YYYY-MM-DD.md`; add a short suffix if needed.
- Prefer `<author>-<year>-<short-title>.md` or
  `<lead-author>-et-al-<year>-<short-title>.md` for source notes.
- Use relative Markdown links for local documents and assets.
- Before moving a file, find and repair every incoming link.

## Producing research

Before creating a durable document, read this file, the root README, the
destination README, the relevant template, and the schema. Search for an
existing document that already serves the need. Add a meaningful body
connection or place the document on a relevant map, then update the destination
README in the same change.

A deep dive should preserve both its evidence trail and resulting model.
Unless the user requests another shape, create or update this connected bundle:

1. a synthesis note in `20-notes/`;
2. a source note in `30-sources/` for each substantively used primary work;
3. an inquiry in `40-inquiries/` while the central question remains open;
4. a topic map in `10-maps/`;
5. the home map when the topic belongs at the archive entry point;
6. journal evidence for material local experiments; and
7. every affected directory README.

Research method:

- Define the question, scope, terminology, and an operational standard for the
  conclusion.
- Search current sources when facts, software, papers, standards, or product
  behavior may have changed.
- Prefer primary papers, official specifications, and official project
  documentation. Use surveys to locate primary evidence or context.
- Record exact authorship, title, year, venue, DOI or canonical URL, and access
  date when available.
- Read enough of a source to support the claim for which it is cited. Search
  snippets and abstracts are not evidence for detailed claims.
- Distinguish reported results from interpretation, extrapolation, proposal,
  and cross-source synthesis.
- Compare approaches and include negative results, limitations, evaluation
  weaknesses, and unresolved questions.
- Preserve experimental method, versions, commands, output, and artifacts in a
  journal entry.
- For OS claims, identify the trust boundary, privilege level, hardware or
  simulator target, host dependencies, failure model, and reproducibility
  conditions.

## Maps, inquiries, and lifecycle

- Maps are curated explanations, not file dumps.
- Keep the home map selective: major active inquiries, topic maps, and
  developed syntheses belong there.
- Promote independently useful conclusions from inquiries or journals to
  notes.
- Move dormant or superseded work to `90-archive/` rather than silently
  deleting useful context. Record why and link replacements.
- Do not call a note `stable` or inquiry `resolved` merely because a writing
  pass is complete; evidence must support the lifecycle state.

## Verification and handoff

Before reporting archive work complete:

1. inspect repository status when version control is present and preserve
   unrelated changes;
2. run `python3 validate_archive.py` from the repository root;
3. run `python3 -m unittest test_validate_archive.py` when validation code or
   schema behavior changes;
4. verify newly introduced external citations against primary sources;
5. run `git diff --check` when this is a Git worktree; and
6. review the complete change for stale paths and accidental rewrites.

Do not commit, push, open a pull request, or publish unless the user asks. In
the final handoff, summarize documents created or changed, indexes updated,
validation performed, and whether changes remain uncommitted.
