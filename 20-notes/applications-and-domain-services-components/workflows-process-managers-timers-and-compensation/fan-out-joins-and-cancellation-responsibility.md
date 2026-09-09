---
title: "Fan-out, joins, and cancellation responsibility"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Fan-out, joins, and cancellation responsibility

This study decomposes [Workflows, process managers, timers, and compensation](../workflows-process-managers-timers-and-compensation.md).

Research question: When may a parallel workflow finish while child work is still running?

## Research basis and status

Workflow Patterns distinguishes branch, join and cancellation semantics; it does not provide durable effect execution. [1](../../../30-sources/van-der-aalst-et-al-2003-workflow-patterns.md).

Sagas permit visible intermediate commits and semantic compensation; they do not supply outer transaction isolation. [2](../../../30-sources/garcia-molina-salem-1987-sagas.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own child identities, join policy, required versus optional participants,
cancellation state and the inventory of accepted child responsibilities. A
first-success join is not equivalent to all-success; dynamic fan-out must have a
durable bound or an explicit closed membership frontier.

### Admission, transitions and completion

Persist each admitted child and its stable step identity before launching it.
Evaluate joins against recorded outcomes and the declared membership set.
Cancellation closes new child admission and requests the allowed stop behavior;
already accepted effects remain pending until terminal evidence or durable transfer
to another owner.

### Failure and adversarial behavior

Duplicate child completions can satisfy a naïve counter twice. Late children can
complete after a parent claims termination. An unbounded fan-out can consume the
resources needed to collect results or compensate. Reserve completion and
cancellation capacity before admitting the set.

### Alternatives and unresolved tradeoffs

Parallelism can reduce latency when branches are independent, but increases recovery
and compensation states. Sequential execution is preferable for tightly coupled
irreversible work. Choreographed joins are possible only if their membership and
ownership rules remain explicit and recoverable.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Duplicate and reorder child results around a coordinator restart; join membership must count each child once.
- Cancel after one child commits and another becomes indeterminate; parent status must retain both responsibilities.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Effect reconciliation and unqueryable repair](../external-effects-ports-adapters-and-reconciliation/effect-reconciliation-and-unqueryable-repair.md) — a cross-component contract this service must preserve.
- [Workflow-generation handoff and publication fences](../application-evolution-schema-compatibility-and-migration/workflow-generation-handoff-and-publication-fences.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [Workflow Patterns](../../../30-sources/van-der-aalst-et-al-2003-workflow-patterns.md).
2. [Sagas](../../../30-sources/garcia-molina-salem-1987-sagas.md).
