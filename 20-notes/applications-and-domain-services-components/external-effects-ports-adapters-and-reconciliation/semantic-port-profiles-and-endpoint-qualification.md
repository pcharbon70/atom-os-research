---
title: "Semantic port profiles and endpoint qualification"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Semantic port profiles and endpoint qualification

This study decomposes [External effects, ports, adapters, and reconciliation](../external-effects-ports-adapters-and-reconciliation.md).

Research question: Which completion guarantees can a particular external endpoint honestly support?

## Research basis and status

Cockburn places technology adapters outside semantic ports; the pattern does not guarantee effect safety. [1](../../../30-sources/cockburn-2005-hexagonal-architecture.md).

Featonby's operational account uses caller request identity, parameter checks and retained results; retention and endpoint participation remain explicit limits. [2](../../../30-sources/featonby-2021-idempotent-apis.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own a semantic port profile containing operation meaning, endpoint generation,
idempotency and lookup behavior, ordering, authority, deadlines and receipt
evidence. Layer 4 supplies network, device and secret facilities. HTTP status,
packet acknowledgment or device interrupt is evidence only for its named transport
or hardware stage.

### Admission, transitions and completion

Qualify endpoints as participating atomic stores, retained-idempotency services,
queryable weak services, unqueryable actuators or human-mediated processes. Test
stable-ID and changed-payload behavior, retention expiry and status authorization.
Admit only the effect class supported by this profile; expose unsupported
exactly-once expectations before accepting responsibility.

### Failure and adversarial behavior

An adapter can report success while a downstream processor is still pending.
Endpoint changes can shorten retention or alter meanings. A timeout during provider
failover cannot authorize replay to a different endpoint unless operation identity
and results migrate under an explicit contract.

### Alternatives and unresolved tradeoffs

A generic transport adapter is reusable but cannot supply business completion
semantics. Port-specific adapters cost maintenance yet make receipts and repair
intelligible. Conservative refusal may be necessary for high-consequence effects
without a qualified reconciliation path.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Drop the reply after endpoint acceptance and separately after commit; document the strongest recoverable conclusion in each case.
- Change endpoint generation while a request is unknown; prevent blind dispatch to a new provider.

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

1. [Hexagonal Architecture](../../../30-sources/cockburn-2005-hexagonal-architecture.md).
2. [Idempotent APIs](../../../30-sources/featonby-2021-idempotent-apis.md).
