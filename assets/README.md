---
title: "Assets"
kind: map
created: "2026-08-28"
tags:
  - archive-navigation
  - directory-index
aliases:
  - "Assets index"
---

# Assets (`assets`)

## Purpose

Assets hold durable local attachments required by the research archive.

## What belongs here

Put lawfully retained images, PDFs, diagrams, datasets, logs, binaries, and
other non-Markdown artifacts here when a canonical external link is
insufficient. Record source, creator, license, provenance, and use.

## Index

### Subdirectories

- [C kernel feasibility](c-kernel-feasibility/README.md) — original C ABI, compile/link and missing-helper research probes with transcripts; no boot or privileged execution.
- [Zig kernel feasibility](zig-kernel-feasibility/README.md) — original hosted ABI and compile/link research fixtures, reproduction script and observed output; no boot or physical qualification claim.

### Files

- [Minimal T7500 / Intel x86-64 QEMU configuration intent](qemu-minimal-x86-64.json) —
  project-authored companion to the [active target specification](../20-notes/proof-of-concept-requirements/dell-precision-t7500-target-and-minimal-qemu-profile.md),
  created 2026-09-06 for future tests. It is not QEMU readconfig syntax, a
  launcher or an executed run manifest; unresolved pins remain null. No
  third-party binary or downloaded attachment is included.

## Maintaining this index

Index every direct asset with its provenance and purpose. Add a descriptive
subdirectory with its own README when a related asset group needs structure.
