---
title: "Privileged entry, exit and execution context: internal-service research"
kind: map
created: "2026-09-08"
tags:
  - architecture-support
  - archive-navigation
  - directory-index
aliases: []
---

# Privileged entry, exit and execution context: internal-service research

## Purpose

This directory decomposes [component 2: Privileged entry, exit and execution context](../privileged-entry-exit-and-execution-context.md) into 6 independently reviewable architecture services. Separate early admission, semantic frames, return authority, context ownership, nested failure and transition security. All six share the parent entry state; none duplicates component 9's capture or disposition owner.

This is full-system architecture research, not a delivery plan or evidence of implementation. The parent component remains authoritative for the integrated protocol; local state sketches below are projections, not replacements for its complete transitions and completion predicates.

## What belongs here

Service-level syntheses belong here when they identify a distinct owner or contract, state transitions, failure behavior, alternatives, architecture-specific obligations and falsification criteria. Counts follow the actual responsibility boundaries.

Keep one owning aggregate for each resource. Views do not create duplicate authority. At-most-once terminalization is a safety property; eventual completion additionally needs progress and recovery assumptions. Zig representations do not by themselves enforce linear ownership: protected state validates generations, authority and single-consumer transitions.

## Index

### Subdirectories

- None.

### Documents

- [Early vector and stack admission](early-vector-stack-admission.md) — Early entry must establish a safe stack and CPU-local identity before invoking ordinary kernel code. Hardware-provided entry state is only the beginning of this protocol.
- [Frame normalization and bounded dispatch](frame-normalization-and-dispatch.md) — The normalized entry frame should preserve origin and validity without making captured bytes into return authority. Dispatch begins only after entry state is coherent and stays separate from scheduling and device policy.
- [Validated less-privileged return](validated-user-return.md) — Returning to a less-privileged domain should consume an exact current return authority, not replay an arbitrary saved register block. The last transition remains faultable and must have its own failure route.
- [Extended-state ownership and context transfer](extended-state-ownership-transfer.md) — Execution context is the complete enabled architectural state belonging to an execution domain, not a fixed integer-register array. Its transfer must prevent a new domain from observing another domain's residual state.
- [Nested-event and terminal handoff](nested-event-and-terminal-handoff.md) — Nesting control should distinguish ordinary reentry from a state in which only minimal terminal capture is safe. It must preserve component 9's evidence and disposition protocol rather than create a competing fault handler.
- [Transition-security profile](transition-security-profile.md) — Architectural state restoration and protection-domain isolation are related but distinct. A transition-security profile should state what residual microarchitectural exposure is addressed and what remains outside its claim.

## Maintaining this index

Inventory every direct service report and preserve links to the parent component. Update the [architecture map](../../../10-maps/kernel-hardware-and-architecture-support.md) and [component directory index](../README.md) when boundaries change. Do not weaken the parent's integrated protocol merely to simplify one service.

The [research journal](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) records exact source provenance, access limitations and cross-service findings. All verification cases in these reports are proposed and not run.
