---
title: "Raw time and deadline programming: internal-service research"
kind: map
created: "2026-09-08"
tags:
  - architecture-support
  - archive-navigation
  - directory-index
aliases: []
---

# Raw time and deadline programming: internal-service research

## Purpose

This directory decomposes [component 6: Raw time and deadline programming](../raw-time-and-deadline-programming.md) into 6 independently reviewable architecture services. Six services distinguish source quality, arithmetic, snapshot lifetime, continuity, hardware programming and terminal outcomes. Diagnostic sampling and delay bounds are part of source qualification; timer queues, civil time and scheduling policy remain above this component.

This is full-system architecture research, not a delivery plan or evidence of implementation. The parent component remains authoritative for the integrated protocol; local state sketches below are projections, not replacements for its complete transitions and completion predicates.

## What belongs here

Service-level syntheses belong here when they identify a distinct owner or contract, state transitions, failure behavior, alternatives, architecture-specific obligations and falsification criteria. Counts follow the actual responsibility boundaries.

Keep one owning aggregate for each resource. Views do not create duplicate authority. At-most-once terminalization is a safety property; eventual completion additionally needs progress and recovery assumptions. Zig representations do not by themselves enforce linear ownership: protected state validates generations, authority and single-consumer transitions.

## Index

### Subdirectories

- None.

### Documents

- [Counter and clock-domain qualification](counter-and-clock-domain-qualification.md) — A readable counter is not automatically a portable clock. Its rate, scope, continuity and observation ordering must be qualified independently.
- [Counter extension and checked conversion](counter-extension-and-conversion.md) — Counter extension is a bounded arithmetic inference over a known sampling interval. It cannot recover an arbitrary number of missed wraps or silently turn overflow into a plausible timestamp.
- [Conversion snapshot publication and lifetime](conversion-snapshot-publication.md) — A time reader must use one matched source/anchor/scale snapshot whose storage remains valid throughout the read. A generation retry is a consistency check, not a memory-lifetime mechanism.
- [Clock continuity and era transitions](clock-continuity-and-era-transitions.md) — Recalibration should preserve a clock's continuity when evidence supports it; a genuine discontinuity should create a new era and explicitly resolve old-era obligations. These are different operations.
- [Absolute deadline channel programming](absolute-deadline-programming.md) — A TimerChannel should own one precisely identified hardware programming obligation. It does not own the scheduler's queue of deadlines, and successful register programming is not equivalent to a future timely callback.
- [Deadline terminalization and cancellation](deadline-terminalization-and-cancellation.md) — Every accepted deadline should have one retained terminal decision even if notifications are lost. Cancellation chooses an outcome through the same protected record as firing, rebasing and channel failure.

## Maintaining this index

Inventory every direct service report and preserve links to the parent component. Update the [architecture map](../../../10-maps/kernel-hardware-and-architecture-support.md) and [component directory index](../README.md) when boundaries change. Do not weaken the parent's integrated protocol merely to simplify one service.

The [research journal](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) records exact source provenance, access limitations and cross-service findings. All verification cases in these reports are proposed and not run.
