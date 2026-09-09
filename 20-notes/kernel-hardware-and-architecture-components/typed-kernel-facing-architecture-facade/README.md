---
title: "Typed kernel-facing architecture facade: internal-service research"
kind: map
created: "2026-09-08"
tags:
  - architecture-support
  - archive-navigation
  - directory-index
aliases: []
---

# Typed kernel-facing architecture facade: internal-service research

## Purpose

This directory decomposes [component 10: Typed kernel-facing architecture facade](../typed-kernel-facing-architecture-facade.md) into 6 independently reviewable architecture services. Separate object identity, admission, asynchronous custody, backend profiles, completion composition and conformance. These six services expose existing component authority rather than introducing a second hardware-management layer.

This is full-system architecture research, not a delivery plan or evidence of implementation. The parent component remains authoritative for the integrated protocol; local state sketches below are projections, not replacements for its complete transitions and completion predicates.

## What belongs here

Service-level syntheses belong here when they identify a distinct owner or contract, state transitions, failure behavior, alternatives, architecture-specific obligations and falsification criteria. Counts follow the actual responsibility boundaries.

Keep one owning aggregate for each resource. Views do not create duplicate authority. At-most-once terminalization is a safety property; eventual completion additionally needs progress and recovery assumptions. Zig representations do not by themselves enforce linear ownership: protected state validates generations, authority and single-consumer transitions.

## Index

### Subdirectories

- None.

### Documents

- [Canonical object and lifetime registry](canonical-object-and-lifetime-registry.md) — The facade should expose one canonical object model with generation-checked views. A convenient wrapper must never become an independent owner of a resource already governed by another component.
- [Authorization and execution-context admission](authorization-and-context-admission.md) — Permission to perform an operation and ability to perform it safely in the current context are independent admission checks. Exceptional execution must not silently widen authority.
- [Split-phase operation and terminal ownership](split-phase-operation-and-terminal-ownership.md) — Asynchronous acceptance transfers responsibility, not merely control flow. Every accepted operation needs a durable owner and an at-most-once terminal transition, including cancellation and caller failure.
- [Feature profiles and backend binding](feature-profiles-and-backend-binding.md) — A backend profile is a semantic promise, not a bag of available instructions. Static binding should reduce dispatch complexity without hiding unsupported or weaker behavior.
- [Cross-component completion composition](cross-component-completion-composition.md) — The facade should compose completion evidence structurally while preserving its scope. A single unqualified Done value cannot safely represent every memory, CPU, device and diagnostic obligation.
- [Conformance, observation and escape hatches](conformance-observation-and-escape-hatches.md) — Conformance should compare observable effects and failure behavior, not merely compile matching function signatures. Escape hatches require narrower review and cannot silently become the normal interface.

## Maintaining this index

Inventory every direct service report and preserve links to the parent component. Update the [architecture map](../../../10-maps/kernel-hardware-and-architecture-support.md) and [component directory index](../README.md) when boundaries change. Do not weaken the parent's integrated protocol merely to simplify one service.

The [research journal](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) records exact source provenance, access limitations and cross-service findings. All verification cases in these reports are proposed and not run.
