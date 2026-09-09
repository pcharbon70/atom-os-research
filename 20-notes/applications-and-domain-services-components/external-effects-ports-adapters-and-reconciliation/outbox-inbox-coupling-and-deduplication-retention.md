---
title: "Outbox, inbox coupling, and deduplication retention"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Outbox, inbox coupling, and deduplication retention

This study decomposes [External effects, ports, adapters, and reconciliation](../external-effects-ports-adapters-and-reconciliation.md).

Research question: How do committed domain changes cross a message boundary without losing or duplicating accepted intent?

## Research basis and status

ARIES makes recovery depend on durable ordering metadata; its storage log is not a domain-event model. [1](../../../30-sources/mohan-et-al-1992-aries.md).

RIFL couples mutations to retained completion records; its guarantees require participating storage and recoverable request identity. [2](../../../30-sources/lee-et-al-2015-rifl.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own semantic effect intents and inbox request-to-outcome bindings. An outbox records
accepted dispatch responsibility, not proof of external execution. Layer 4 provides
the atomic store and bounded relay. Outbox IDs, payload digests and originating
revisions remain stable across retries and movement.

### Admission, transitions and completion

Commit state, outcome and outbox together in the local atomic scope. Claim and
dispatch an intent with a generation-bound relay token. At a participating
recipient, commit inbox identity and business mutation atomically; acknowledge only
the named durable stage. Retain records through the advertised retry horizon and
reject expired identities thereafter.

### Failure and adversarial behavior

A relay can publish successfully and crash before marking the outbox delivered;
duplicates are expected. A consumer that records inbox acknowledgment before
mutation loses work, while the reverse order permits duplicates. A nonparticipating
downstream effect still requires its own intent and reconciliation.

### Alternatives and unresolved tradeoffs

A database-backed outbox avoids assuming an atomic database-plus-network send but
adds lag and storage. A true transactional broker may combine scopes only when every
participant's failure contract is qualified. At-least-once transport is acceptable
when domain admission provides the needed identity barrier.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Crash at every source commit, send, recipient commit and acknowledgment point; compare business execution count with durable identities.
- Collect an inbox record and deliver a delayed old message; fail closed rather than silently execute again.

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

1. [ARIES](../../../30-sources/mohan-et-al-1992-aries.md).
2. [RIFL](../../../30-sources/lee-et-al-2015-rifl.md).
