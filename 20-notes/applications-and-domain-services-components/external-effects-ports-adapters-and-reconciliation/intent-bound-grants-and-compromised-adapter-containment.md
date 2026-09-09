---
title: "Intent-bound grants and compromised-adapter containment"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Intent-bound grants and compromised-adapter containment

This study decomposes [External effects, ports, adapters, and reconciliation](../external-effects-ports-adapters-and-reconciliation.md).

Research question: What prevents a compromised adapter from using its legitimate access for a different effect?

## Research basis and status

The archived WASI design principles favor explicit imports and resource handles; correct host enforcement is still assumed. [1](../../../30-sources/wasi-project-2026-design-principles.md).

Wedge demonstrates reduced-privilege compartments in Linux applications; it does not validate Atom OS isolation costs. [2](../../../30-sources/bittau-et-al-2008-wedge.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own the intended action, target, quantity, payload digest, originating commit and
repair policy. Layer 4 derives a narrow invocation grant, and the effect sink
validates it. Protection separates memory, but a compromised adapter can still
misuse any authority it actually holds.

### Admission, transitions and completion

Bind the grant to an authenticated committed intent, exact endpoint generation,
operation ID, request digest, limits and revocation policy. The sink checks these
before admission and atomically records use where one-shot semantics are promised.
The adapter may translate representation only within the qualified equivalence; it
cannot choose another payee, device or amount.

### Failure and adversarial behavior

If the adapter holds a general endpoint credential and the provider cannot enforce
intent bindings, compromise may permit arbitrary actions within that credential's
scope. Record this residual trust explicitly. Local process isolation, code
signatures and redacted logs do not remove it; an independent validating broker
helps only if the adapter cannot bypass the broker.

### Alternatives and unresolved tradeoffs

Per-intent grants minimize delegated power but increase issuance and sink-validation
cost. Long-lived narrow credentials are operationally simpler yet create a larger
residual effect domain. Select the profile from consequence and actual provider
capabilities, not from the word sandbox.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Compromise the adapter in a model and mutate target, amount, digest or generation; the enforcing sink must reject each unauthorized variation.
- Attempt a direct provider call bypassing the broker; either prove it unavailable or record the adapter as trusted for that credential scope.

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

1. [WASI Design Principles](../../../30-sources/wasi-project-2026-design-principles.md).
2. [Wedge](../../../30-sources/bittau-et-al-2008-wedge.md).
