# Atom OS Research Archive

This repository researches and develops a new kernel and operating system
informed by the principles of Erlang/OTP and the BEAM virtual machine. The goal
is to carry ideas such as cheap isolated processes, asynchronous messaging,
supervision, fault containment, responsiveness, and distribution into the
system architecture without tying the project to one existing BEAM
implementation. The platform is required to run compiled BEAM code and retain
automatic process-local tracing garbage collection; the exact compatible
runtime and versioned OTP profile remain implementation questions.

The current proof of concept builds a minimal bootable OS whose first delivery
is an interactive CLI. Graphical UI and desktop work are outside its scope.
AtomVM has been rejected as an implementation foundation; its archived research
is retained for provenance. The CLI can be native during bring-up, with the
required unprivileged BEAM runtime and tracing GC integrated in a later
milestone. See the [readiness assessment](20-notes/proof-of-concept-research-readiness.md)
for the staged acceptance criteria.

The [implementation planning area](60-planning/README.md) defines the
milestone-directory and phased-plan convention. The
[proof-of-concept planning stream](60-planning/01-proof-of-concept/README.md)
connects M0–M4 to that structure; detailed phase plans are not yet authored.

The initial physical target is the **Dell Precision T7500**, using
**Intel Xeon / Intel 64 (x86-64)**. The [active target profile](20-notes/proof-of-concept-requirements/dell-precision-t7500-target-and-minimal-qemu-profile.md)
defines a Nehalem-class, one-CPU, 128 MiB serial QEMU fixture and the remaining
installed-unit inventory. The AMD-processor assumption has been corrected;
its former profile is archived. RISC-V/OpenSBI remains comparative research,
not the first implementation path.

Start at the [home map](10-maps/home.md). Repository-wide authoring and
maintenance conventions are defined in [`AGENTS.md`](AGENTS.md).

## Structure

- [`00-inbox/`](00-inbox/README.md) — unprocessed captures
- [`10-maps/`](10-maps/README.md) — curated paths through subjects and questions
- [`20-notes/`](20-notes/README.md) — ideas developed in the author's own words
- [`30-sources/`](30-sources/README.md) — reading notes and bibliographic records
- [`40-inquiries/`](40-inquiries/README.md) — active research questions
- [`50-journal/`](50-journal/README.md) — dated observations and experiments
- [`60-planning/`](60-planning/README.md) — milestone-scoped phased implementation plans
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
4. For every deep dive, record an exhaustive journal source manifest that
   separates newly introduced sources from reused sources.
5. Develop selective maps when conceptual clusters emerge.
6. Translate near-term milestones into described, integration-gated phase plans
   in `60-planning/`; keep plans distinct from implementation evidence.
7. Preserve superseded work in `90-archive/` when its context remains useful.
8. Update affected indexes and validate in the same change.

## Validation

Install the pinned dependencies once, then run the archive checks:

```bash
python3 -m pip install -r requirements-validation.txt
python3 validate_archive.py
python3 -m unittest test_validate_archive.py
```

The validator checks metadata, placeholders, filenames, local links,
directory inventories, conceptual connections, deep-dive source-manifest
structure and classification, and duplicate source identifiers.
Planning notes are included in metadata and navigation checks. The described
task hierarchy and adequacy of phase-ending integration tests are review
requirements, not currently automated checks.

## Repository files

- [`AGENTS.md`](AGENTS.md) — research, authoring, and maintenance instructions
- [`frontmatter.schema.json`](frontmatter.schema.json) — metadata schema
- [`requirements-validation.txt`](requirements-validation.txt) — validator dependencies
- [`test_validate_archive.py`](test_validate_archive.py) — focused validator tests
- [`validate_archive.py`](validate_archive.py) — deterministic archive checks
