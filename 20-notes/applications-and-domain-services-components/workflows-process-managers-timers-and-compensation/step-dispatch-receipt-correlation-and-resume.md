---
title: "Step dispatch, receipt correlation, and resume"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Step dispatch, receipt correlation, and resume

This study decomposes [Workflows, process managers, timers, and compensation](../workflows-process-managers-timers-and-compensation.md).

Research question: How is a workflow step retried without creating another business action?

## Research basis and status

Featonby's operational account uses caller request identity, parameter checks and retained results; retention and endpoint participation remain explicit limits. [1](../../../30-sources/featonby-2021-idempotent-apis.md).

Durable Functions formalizes restricted history replay; arbitrary nondeterminism and external effects remain outside that abstraction. [2](../../../30-sources/burckhardt-et-al-2021-durable-functions.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own a step record containing stable logical operation ID, request digest, step
generation, target port, expected revision and receipt profile. Attempt IDs
distinguish transport tries only. Layer 4 may schedule retries, but Layer 5 defines
which result allows this workflow to advance.

### Admission, transitions and completion

Commit the step intent before dispatch. Recover or query the same target operation
after uncertainty, retain its authenticated receipt and only then advance the
workflow revision. If parameters must change, create an explicit superseding step
with linked intent; never reuse the old logical ID with a different digest.

### Failure and adversarial behavior

A reply from a prior step generation may be genuine but no longer authorize
advancement. A receipt for queue acceptance does not prove an external action
committed. Lost workflow replies must not cause the caller to start another workflow
when an earlier one is already responsible.

### Alternatives and unresolved tradeoffs

An idempotent participating endpoint supports automatic resume. A queryable but weak
endpoint requires reconciliation rules; an unqueryable endpoint may force manual
repair. The coordinator must advertise these differences instead of presenting every
step as a transparent function call.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Deliver a late successful receipt after cancellation and replacement; preserve the old effect evidence without advancing the wrong step.
- Duplicate dispatch around a coordinator crash; one stable target operation must be recovered.

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

1. [Idempotent APIs](../../../30-sources/featonby-2021-idempotent-apis.md).
2. [Durable Functions semantics](../../../30-sources/burckhardt-et-al-2021-durable-functions.md).
