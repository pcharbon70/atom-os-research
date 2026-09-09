---
title: "Bounded envelope decoding and critical extensions"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Bounded envelope decoding and critical extensions

This study decomposes [Typed commands, queries, events, and protocol contracts](../typed-commands-queries-events-and-protocol-contracts.md).

Research question: How does an untrusted message become one unambiguous typed application request?

## Research basis and status

RFC 9413 warns that indiscriminate permissive parsing can preserve ambiguity and obstruct protocol evolution. [1](../../../30-sources/thomson-schinazi-2023-maintaining-robust-protocols.md).

Liskov and Wing treat substitution as preservation of behavioral properties, beyond compatible representation. [2](../../../30-sources/liskov-wing-1994-behavioral-subtyping.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own protocol identifiers, version negotiation, command/query/event classification,
bounded decoders and canonical request digests. Envelopes include target lifecycle,
authenticated realm binding, operation identity, expected revision and deadline
where relevant. Correlation and trace strings are diagnostic input, not identity
evidence.

### Admission, transitions and completion

Check size, depth, field cardinality, primitive ranges and critical variants before
allocating domain objects or resolving expensive references. Normalize only under a
pinned schema. Hash the canonical semantic request with its protocol version and
scope. Preserve explicitly permitted optional fields across promised round trips;
reject unknown critical meaning.

### Failure and adversarial behavior

Two decoders can interpret duplicate fields, missing defaults or malformed text
differently. Signing bytes does not resolve that semantic disagreement. A permissive
compatibility shim must not turn an unknown effect class into a known command. Error
responses must avoid disclosing protected targets through parser-versus-policy
distinctions.

### Alternatives and unresolved tradeoffs

Exact-version profiles reduce ambiguity but increase upgrade coordination.
Negotiated profiles permit longer compatibility windows at the price of permanent
fixture coverage. A generated decoder is useful only if resource bounds and
behavioral rejection rules are also reviewed.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Differentially decode duplicate fields, unknown enums and extreme nesting; accepted messages must have one digest and meaning.
- Send a correctly signed but unsupported critical command; it must fail before operation admission.

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

1. [RFC 9413](../../../30-sources/thomson-schinazi-2023-maintaining-robust-protocols.md).
2. [Behavioral subtyping](../../../30-sources/liskov-wing-1994-behavioral-subtyping.md).
