---
title: "Effect reconciliation and unqueryable repair"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Effect reconciliation and unqueryable repair

This study decomposes [External effects, ports, adapters, and reconciliation](../external-effects-ports-adapters-and-reconciliation.md).

Research question: How can the system preserve useful truth when no component knows whether an effect happened?

## Research basis and status

Featonby's operational account uses caller request identity, parameter checks and retained results; retention and endpoint participation remain explicit limits. [1](../../../30-sources/featonby-2021-idempotent-apis.md).

Sagas permit visible intermediate commits and semantic compensation; they do not supply outer transaction isolation. [2](../../../30-sources/garcia-molina-salem-1987-sagas.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own the reconciliation case: logical operation, intent digest, last proven stage,
endpoint evidence, authorized lookup routes, age and repair owner. Unknown is a
first-class state, not a transient error to hide. Reconciliation capacity must
survive adapter restart and ordinary overload.

### Admission, transitions and completion

Query the qualified endpoint by stable identity, validate evidence and advance the
outcome monotonically. Retry the same operation only when its idempotency contract
still applies. For an unqueryable actuator or human action, seek independent
feedback or create a bounded repair case. A manual decision records its evidence and
uncertainty rather than retroactively inventing a receipt.

### Failure and adversarial behavior

Silence cannot prove absence. A duplicate physical action can be worse than an
unresolved request. Human assignment or notification does not mean the person
completed the task. Repair can require a new compensating action with distinct
identity; it must retain the relationship to the uncertain original.

### Alternatives and unresolved tradeoffs

Automatic retry favors liveness when duplicate suppression is trustworthy.
Conservative no-retry favors safety for irreversible unqueryable effects.
Domain-specific reconciliation may establish stronger conclusions than generic
transport logic, but its evidence quality must be evaluated.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Simulate execution with lost response and no lookup support; the outcome must stay indeterminate instead of becoming not committed.
- Restart the repair owner and exhaust ordinary queues; accepted cases remain discoverable with bounded reserved progress.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Step dispatch, receipt correlation, and resume](../workflows-process-managers-timers-and-compensation/step-dispatch-receipt-correlation-and-resume.md) — a cross-component contract this service must preserve.
- [Semantic admission classes and protected recovery reserve](../cross-layer-placement-tenancy-overload-and-recovery-topology/semantic-admission-classes-and-protected-recovery-reserve.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [Idempotent APIs](../../../30-sources/featonby-2021-idempotent-apis.md).
2. [Sagas](../../../30-sources/garcia-molina-salem-1987-sagas.md).
