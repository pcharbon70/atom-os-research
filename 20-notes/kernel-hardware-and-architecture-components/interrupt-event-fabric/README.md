---
title: "Interrupt event fabric: internal-service research"
kind: map
created: "2026-09-08"
tags:
  - architecture-support
  - archive-navigation
  - directory-index
aliases: []
---

# Interrupt event fabric: internal-service research

## Purpose

This directory decomposes [component 5: Interrupt event fabric](../interrupt-event-fabric.md) into 6 independently reviewable architecture services. Six services separate source identity, electrical/controller flow, bounded evidence, binding lifetime, accounting and polling handoff. Kernel IPI transport remains owned by component 7 and consumes this fabric rather than duplicating a second request protocol.

This is full-system architecture research, not a delivery plan or evidence of implementation. The parent component remains authoritative for the integrated protocol; local state sketches below are projections, not replacements for its complete transitions and completion predicates.

## What belongs here

Service-level syntheses belong here when they identify a distinct owner or contract, state transitions, failure behavior, alternatives, architecture-specific obligations and falsification criteria. Counts follow the actual responsibility boundaries.

Keep one owning aggregate for each resource. Views do not create duplicate authority. At-most-once terminalization is a safety property; eventual completion additionally needs progress and recovery assumptions. Zig representations do not by themselves enforce linear ownership: protected state validates generations, authority and single-consumer transitions.

## Index

### Subdirectories

- None.

### Documents

- [Controller and source normalization](controller-and-source-normalization.md) — Interrupt source identity should be scoped to a discovered controller and source incarnation. A vector number is neither global identity nor authority to bind or complete an interrupt.
- [Interrupt flow-state machines](interrupt-flow-state-machines.md) — Controller completion, device-cause clearing and rearming are different transitions. The fabric should choose a closed flow plan rather than let an arbitrary driver callback define privileged acknowledgement order.
- [Bounded hard-path recording](bounded-hard-path-recording.md) — The hard path should record bounded, generation-tagged evidence that work is pending. It should not promise one message for every physical event or invoke the ordinary driver inline.
- [Binding, routing and teardown](binding-routing-and-teardown.md) — Changing a destination or CPU route should be an explicit lifetime transition. Replacing a pointer is insufficient while hard-path code, old notifications or device remapping can still name the previous binding.
- [Interrupt accounting and quarantine](interrupt-accounting-and-quarantine.md) — Interrupts need an admission and recovery budget independent of the failing driver. A source that exhausts its account must not be able to refill itself or monopolize the CPU while reporting its own failure.
- [Polling and interrupt handoff](polling-and-interrupt-handoff.md) — Polling should be an explicit bounded ownership mode with a loss-aware transition back to interrupts. It is a scheduling and workload tradeoff, not an unconditional optimization.

## Maintaining this index

Inventory every direct service report and preserve links to the parent component. Update the [architecture map](../../../10-maps/kernel-hardware-and-architecture-support.md) and [component directory index](../README.md) when boundaries change. Do not weaken the parent's integrated protocol merely to simplify one service.

The [research journal](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) records exact source provenance, access limitations and cross-service findings. All verification cases in these reports are proposed and not run.
