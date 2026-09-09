---
title: "Application evolution, schema compatibility, and migration: internal services"
kind: map
created: "2026-09-09"
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
  - directory-index
aliases: []
---

# Application evolution, schema compatibility, and migration: internal services

## Purpose

Separate directed compatibility, safe intermediate schemas, private migration,
in-flight handoff and irreversible retirement.

This directory decomposes [Application evolution, schema compatibility, and migration](../application-evolution-schema-compatibility-and-migration.md)
into 5 separately reviewable research responsibilities. These are service
contracts, not a mandate for one actor, protected domain or deployable package
per document.

## What belongs here

Keep owned state, authority boundaries, transition and completion semantics,
failure cases, alternatives and falsifiers here. Primary findings remain in
source notes; the [session manifest](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md)
records exact provenance. This is full-system architecture research, not
implementation delivery or a proof-of-concept gate.

Layer 5 declares domain meaning and required evidence. Layer 4 supplies generic
policy and durability services; Layers 2–3 enforce protection, resources and
managed execution. Proposed guarantees remain conditional on those contracts.

## Index

### Subdirectories

- None yet.

### Documents

- [Directed compatibility and behavioral fixture matrices](directed-compatibility-and-behavioral-fixture-matrices.md) — Which old/new combinations preserve the application's observable contract?
- [Expand-contract transitions and old-writer exclusion](expand-contract-transitions-and-old-writer-exclusion.md) — When is it safe to remove the old representation or protocol?
- [Shadow migration checkpoints and validation](shadow-migration-checkpoints-and-validation.md) — How can data conversion be interrupted without damaging the source or guessing progress?
- [Workflow-generation handoff and publication fences](workflow-generation-handoff-and-publication-fences.md) — How do accepted operations cross a release boundary without acquiring two owners or none?
- [Rollback cutoffs, canaries, and retirement evidence](rollback-cutoffs-canaries-and-retirement-evidence.md) — When does rollback cease to mean restoring a valid prior application generation?

## Maintaining this index

Inventory every direct child and update the parent report, component index and
relevant map when a responsibility changes. Keep counts needs-based: split only
where distinct state, trust or completion obligations justify it. Preserve
unexecuted tests and unresolved choices as such.

Continue through the [application topic map](../../../10-maps/applications-and-domain-services.md)
and [open inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md);
neither literature coverage nor this decomposition closes architectural
qualification.
