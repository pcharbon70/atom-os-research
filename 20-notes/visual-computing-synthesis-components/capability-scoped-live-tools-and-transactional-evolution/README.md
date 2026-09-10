---
title: "Capability-scoped live tools and transactional evolution: internal services"
kind: map
created: "2026-09-10"
tags:
  - capability-security
  - live-programming
  - visual-computing
aliases: []
---

# Capability-scoped live tools and transactional evolution: internal services

## Purpose

Separate inspection, pure evaluation, tracing/debugging, transactional
publication, and reusable-tool distribution.

This directory decomposes [Capability-scoped live tools and transactional evolution](../capability-scoped-live-tools-and-transactional-evolution.md).

## What belongs here

Keep tool authority, isolated worker state, transition records, migration
limits, recovery alternatives, and unexecuted falsifiers here. Live feedback
does not imply immediate or unrestricted commit. The [session
manifest](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md)
records provenance.

## Index

### Subdirectories

- None yet.

### Documents

- [Inspection facets, redaction, and copied state](inspection-facets-redaction-and-copied-state.md) — What can a tool observe without acquiring mutation or transitive authority?
- [Pure-evaluation sandbox and resource bounds](pure-evaluation-sandbox-and-resource-bounds.md) — How can exploratory execution remain deterministic and effect-free?
- [Tracing, debugging, safe points, and lease expiry](tracing-debugging-safe-points-and-lease-expiry.md) — How can live observation and control avoid permanently destabilizing targets?
- [Changeset validation, migration, and atomic publication](changeset-validation-migration-and-atomic-publication.md) — What evidence and state machine make a live change recoverable?
- [Tool packaging, provenance, rollout, and recovery](tool-packaging-provenance-rollout-and-recovery.md) — How do reusable tools move from local experiment to confined release?

## Maintaining this index

Inventory every direct child and preserve the separation among observation,
execution, control, commit, and publication powers. Link claimed results only
to actual execution evidence.
