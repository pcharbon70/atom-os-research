---
title: "Normalized boot handoff and feature discovery: internal-service research"
kind: map
created: "2026-09-08"
tags:
  - architecture-support
  - archive-navigation
  - directory-index
aliases: []
---

# Normalized boot handoff and feature discovery: internal-service research

## Purpose

This directory decomposes [component 0: Normalized boot handoff and feature discovery](../normalized-boot-handoff-and-feature-discovery.md) into 6 independently reviewable architecture services. Separate provider lifetime, parsing, physical-resource reconciliation, discovery, and final publication. These six boundaries prevent a successful provider transaction from being mistaken for validated kernel facts.

This is full-system architecture research, not a delivery plan or evidence of implementation. The parent component remains authoritative for the integrated protocol; local state sketches below are projections, not replacements for its complete transitions and completion predicates.

## What belongs here

Service-level syntheses belong here when they identify a distinct owner or contract, state transitions, failure behavior, alternatives, architecture-specific obligations and falsification criteria. Counts follow the actual responsibility boundaries.

Keep one owning aggregate for each resource. Views do not create duplicate authority. At-most-once terminalization is a safety property; eventual completion additionally needs progress and recovery assumptions. Zig representations do not by themselves enforce linear ownership: protected state validates generations, authority and single-consumer transitions.

## Index

### Subdirectories

- None.

### Documents

- [Provider handoff adapter](provider-handoff-adapter.md) — The adapter should terminate one precisely versioned provider contract and produce owned input for normalization. It is a privileged boundary translator, not a firmware compatibility layer that remains callable indefinitely.
- [Bounded envelope parser](bounded-envelope-parser.md) — The envelope parser should convert an addressable byte extent into structurally valid records without dereferencing provider pointers or performing hardware effects. Structural validity remains separate from whether a record's claims are true.
- [Memory extent reconciler](memory-extent-reconciler.md) — The reconciler should produce a conservative, disjoint physical-memory ledger while preserving the provenance and release conditions of every restriction. Unknown space must never become RAM merely because no reservation describes it.
- [CPU feature admission](cpu-feature-admission.md) — CPU discovery should publish evidence about a particular CPU incarnation, separately from the set of features the kernel requires or chooses to enable. A firmware topology entry is a candidate, not proof that its execution environment is safe.
- [Static mechanism discovery](static-mechanism-discovery.md) — Static discovery should describe topology, controllers, counters and retained firmware gates without initializing them. This prevents a descriptive table from becoming authority to issue interrupts, reset devices or execute arbitrary firmware policy.
- [Snapshot sealing and custody](snapshot-sealing-and-custody.md) — BootSnapshot should be the immutable publication boundary for validated boot facts. Sealing must close mutable input dependencies and retain the evidence needed to explain each fact, without presenting a digest as authentication.

## Maintaining this index

Inventory every direct service report and preserve links to the parent component. Update the [architecture map](../../../10-maps/kernel-hardware-and-architecture-support.md) and [component directory index](../README.md) when boundaries change. Do not weaken the parent's integrated protocol merely to simplify one service.

The [research journal](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) records exact source provenance, access limitations and cross-service findings. All verification cases in these reports are proposed and not run.
