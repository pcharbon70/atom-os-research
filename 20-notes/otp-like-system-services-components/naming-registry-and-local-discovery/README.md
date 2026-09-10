---
title: "Naming, registry, and local discovery: internal services"
kind: map
created: "2026-09-10"
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Naming, registry, and local discovery: internal services

## Purpose

Separate namespace authority, unique publication, watch continuity and bounded
candidate views.

This directory decomposes [Naming, registry, and local discovery](../naming-registry-and-local-discovery.md).
These are logical responsibilities, not a requirement for one process per study.

## What belongs here

Keep owned state, authority, transition evidence, failure cases, alternatives
and unexecuted verification obligations here. This is full-system Layer 4
architecture research, not a PoC, QEMU profile or implementation plan. Layers
2–3 supply enforcement and managed execution; Layer 5 supplies domain meaning.
The [session manifest](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) records provenance.

## Index

### Subdirectories

- None yet.

### Documents

- [Namespace reservation and authority-safe resolution](namespace-reservation-and-authority-safe-resolution.md) — What does resolving a name authorize, and who may reserve it?
- [Binding publication, owner death, and shard handoff](binding-publication-owner-death-and-shard-handoff.md) — How can replacement and owner cleanup avoid deleting a successor's binding?
- [Snapshot/watch continuity and overflow recovery](snapshot-watch-continuity-and-overflow-recovery.md) — How can bounded subscribers reconstruct state without silently missing changes?
- [Group candidate caches and bounded history](group-candidate-caches-and-bounded-history.md) — How should non-unique discovery remain useful without becoming an ownership oracle?

## Maintaining this index

Inventory every direct child. Keep the parent report, component index, topic
map and inquiry connected when responsibilities change. Decompose according
to distinct state, authority and completion needs, not a fixed document quota.
Writing these studies does not validate their proposed guarantees.
