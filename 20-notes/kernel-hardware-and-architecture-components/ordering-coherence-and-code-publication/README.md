---
title: "Ordering, coherence and code publication: internal-service research"
kind: map
created: "2026-09-08"
tags:
  - architecture-support
  - archive-navigation
  - directory-index
aliases: []
---

# Ordering, coherence and code publication: internal-service research

## Purpose

This directory decomposes [component 4: Ordering, coherence and code publication](../ordering-coherence-and-code-publication.md) into 7 independently reviewable architecture services. Seven distinct services separate ordinary synchronization, device completion, maintenance planning, sealing, publication, membership catch-up and retirement. Visibility, execution eligibility and reclamation are deliberately not one notion of completion.

This is full-system architecture research, not a delivery plan or evidence of implementation. The parent component remains authoritative for the integrated protocol; local state sketches below are projections, not replacements for its complete transitions and completion predicates.

## What belongs here

Service-level syntheses belong here when they identify a distinct owner or contract, state transitions, failure behavior, alternatives, architecture-specific obligations and falsification criteria. Counts follow the actual responsibility boundaries.

Keep one owning aggregate for each resource. Views do not create duplicate authority. At-most-once terminalization is a safety property; eventual completion additionally needs progress and recovery assumptions. Zig representations do not by themselves enforce linear ownership: protected state validates generations, authority and single-consumer transitions.

## Index

### Subdirectories

- None.

### Documents

- [Ordinary-memory synchronization](ordinary-memory-synchronization.md) — The ordinary-memory contract should begin with the source language and then justify its lowering to hardware. Successful execution on a strongly ordered processor is not evidence that a shared protocol is race-free or portable.
- [Typed MMIO ordering and completion](typed-mmio-ordering-and-completion.md) — An MMIO write can be ordered with other accesses without having reached its device. The service should expose those effects separately and require a device-safe completion recipe.
- [Cache-maintenance planner](cache-maintenance-planner.md) — Cache maintenance should be selected from a semantic request with explicit ownership, aliases and participating agents. A range flush API that omits those dimensions cannot explain what has become visible.
- [Executable image sealing](executable-image-sealing.md) — Sealing should close every path that can modify the executable extent before binding the image identity. Removing one writable mapping is not proof that the physical bytes are immutable.
- [Executable publication transaction](executable-publication-transaction.md) — Executable publication should admit an immutable image only while all affected execution is controlled, then commit after translation and instruction-fetch obligations are complete. Installing an executable mapping is an intermediate effect.
- [Publication membership and catch-up](publication-membership-and-catch-up.md) — A frozen publication target set is safe only if CPUs outside it cannot later execute with stale fetch state. Persistent generation evidence must connect publication to CPU joining, migration and return admission.
- [Executable retirement and quarantine](executable-retirement-and-quarantine.md) — Retiring an executable image requires excluding future entry and proving that current execution and retained references no longer depend on it. Waiting a fixed interval or unmapping one address does not establish that result.

## Maintaining this index

Inventory every direct service report and preserve links to the parent component. Update the [architecture map](../../../10-maps/kernel-hardware-and-architecture-support.md) and [component directory index](../README.md) when boundaries change. Do not weaken the parent's integrated protocol merely to simplify one service.

The [research journal](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) records exact source provenance, access limitations and cross-service findings. All verification cases in these reports are proposed and not run.
