# Atom OS Research Archive

This repository researches how `atom-vm` could become the foundational
execution environment for a new operating system, rather than an application
hosted by an existing OS.

Start at the [home map](10-maps/home.md). Repository-wide authoring and
maintenance conventions are defined in [`AGENTS.md`](AGENTS.md).

## Structure

- [`00-inbox/`](00-inbox/README.md) — unprocessed captures
- [`10-maps/`](10-maps/README.md) — curated paths through subjects and questions
- [`20-notes/`](20-notes/README.md) — ideas developed in the author's own words
- [`30-sources/`](30-sources/README.md) — reading notes and bibliographic records
- [`40-inquiries/`](40-inquiries/README.md) — active research questions
- [`50-journal/`](50-journal/README.md) — dated observations and experiments
- [`90-archive/`](90-archive/README.md) — inactive or superseded material
- [`assets/`](assets/README.md) — durable research attachments
- [`templates/`](templates/README.md) — document and directory scaffolds

Folders describe what a document is doing. Links, maps, and tags describe what
it is about. Directory READMEs are complete local inventories; maps remain
selective conceptual paths.

## Research boundary

The central test is whether `atom-vm` can own the responsibilities required of
the system foundation: boot and bring-up, hardware abstraction, execution and
scheduling, memory and resource management, isolation, persistence, drivers,
networking, and system tooling.

Research should make host dependencies visible. A result demonstrated inside
Linux, macOS, or another host is evidence about a hosted port unless it also
shows which services can be replaced or moved beneath `atom-vm`.

## Frontmatter

Every completed knowledge document begins with YAML frontmatter:

```yaml
---
title: "A human-readable title"
kind: note
created: "2026-08-28"
maturity: seed
tags:
  - example-topic
aliases: []
---
```

[`frontmatter.schema.json`](frontmatter.schema.json) is the authoritative
metadata contract. Document kinds are `note`, `source`, `inquiry`, `map`, and
`journal`. Notes require `maturity: seed | developing | stable`; inquiries
require `status: open | paused | resolved`.

## Working rhythm

1. Capture temporary material in `00-inbox/`.
2. Promote useful material with the closest template.
3. Connect every durable document to another document or a map.
4. Develop maps when clusters emerge.
5. Preserve superseded work in `90-archive/` when its context remains useful.
6. Update affected indexes and validate in the same change.

## Validation

Install the pinned dependencies once, then run the archive checks:

```bash
python3 -m pip install -r requirements-validation.txt
python3 validate_archive.py
python3 -m unittest test_validate_archive.py
```

The validator checks metadata, placeholders, filenames, local links,
directory inventories, conceptual connections, and duplicate source
identifiers.

## Repository files

- [`AGENTS.md`](AGENTS.md) — research, authoring, and maintenance instructions
- [`frontmatter.schema.json`](frontmatter.schema.json) — metadata schema
- [`requirements-validation.txt`](requirements-validation.txt) — validator dependencies
- [`test_validate_archive.py`](test_validate_archive.py) — focused validator tests
- [`validate_archive.py`](validate_archive.py) — deterministic archive checks
