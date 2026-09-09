---
title: "Event publication and behavioral history contracts"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Event publication and behavioral history contracts

This study decomposes [Typed commands, queries, events, and protocol contracts](../typed-commands-queries-events-and-protocol-contracts.md).

Research question: When does a message represent an authoritative fact, and what must a compatible consumer preserve?

## Research basis and status

Liskov and Wing treat substitution as preservation of behavioral properties, beyond compatible representation. [1](../../../30-sources/liskov-wing-1994-behavioral-subtyping.md).

RFC 9413 warns that indiscriminate permissive parsing can preserve ambiguity and obstruct protocol evolution. [2](../../../30-sources/thomson-schinazi-2023-maintaining-robust-protocols.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own domain-event and integration-event schemas, causal provenance, per-stream
ordering and supported consumer histories. A domain fact is emitted only from a
committed transition. A public integration event is an intentionally narrowed
export, not the full internal record, storage WAL, audit entry or trace span.

### Admission, transitions and completion

Bind event identity to its originating commit and subject reference, then retain
publication intent for an idempotent relay. Consumers validate schema, source scope,
sequence or causal context and their own admission authority. Compatibility compares
permitted histories, outcomes and invariant implications; successful decoding is
only the structural check.

### Failure and adversarial behavior

Republishing reconstructed historical facts as fresh events can trigger duplicate
work. A relay acknowledgment proves only its named stage. Unknown critical outcome
variants must not default to failure and induce retries. A causation ID links
observations but cannot authorize consumption or prove a principal's identity.

### Alternatives and unresolved tradeoffs

Session-state monitors can enforce narrow high-consequence conversations, but
introduce their own generation, restart and resource state. Simple event schemas
suffice for independent notifications. Whole-system session typing is not assumed
and would require separate toolchain and failure-model research.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Replay an event stream into a projection and an effect consumer; only the latter's explicitly admitted intent path may cause an effect.
- Run old/new consumer histories containing pending and indeterminate outcomes; no version may reinterpret known commitment as retryable absence.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Semantic port profiles and endpoint qualification](../external-effects-ports-adapters-and-reconciliation/semantic-port-profiles-and-endpoint-qualification.md) — a cross-component contract this service must preserve.
- [Directed compatibility and behavioral fixture matrices](../application-evolution-schema-compatibility-and-migration/directed-compatibility-and-behavioral-fixture-matrices.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [Behavioral subtyping](../../../30-sources/liskov-wing-1994-behavioral-subtyping.md).
2. [RFC 9413](../../../30-sources/thomson-schinazi-2023-maintaining-robust-protocols.md).
