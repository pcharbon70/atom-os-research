# Atom OS Research Archive

This repository researches and develops a new kernel and operating system
informed by the principles of Erlang/OTP and the BEAM virtual machine. The goal
is to carry ideas such as cheap isolated processes, asynchronous messaging,
supervision, fault containment, responsiveness, and distribution into the
system architecture without tying the project to one existing BEAM
implementation.

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

The central question is which BEAM and OTP principles belong in the kernel,
which belong in a managed runtime or system-service layer, and which existing
implementation choices should be replaced. Research covers boot and bring-up,
hardware abstraction, execution and scheduling, memory and resource
management, isolation and capabilities, persistence, drivers, networking,
updates, distribution, and system tooling.

Research must distinguish a principle from a particular implementation. A
result demonstrated inside Linux, macOS, an RTOS, or another host is evidence
about a hosted arrangement unless it also identifies the services supplied by
that host. Existing systems such as Erlang/OTP, AtomVM, GRiSP, LING, or newer
bare-metal experiments are evidence and design material, not predetermined
foundations.

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
