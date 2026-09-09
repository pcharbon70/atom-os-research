---
title: "Query frontiers, redaction, and continuation tokens"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Query frontiers, redaction, and continuation tokens

This study decomposes [Typed commands, queries, events, and protocol contracts](../typed-commands-queries-events-and-protocol-contracts.md).

Research question: How does a query expose freshness without accidentally granting write authority or leaking another scope?

## Research basis and status

Overeem and colleagues report practitioner experience with event evolution and recovery costs, not universal event-sourcing benefits. [1](../../../30-sources/overeem-et-al-2021-event-sourced-systems.md).

WAI-ARIA defines semantic roles, states and relationships; vocabulary conformance alone does not establish usable or authorized interaction. [2](../../../30-sources/w3c-2023-wai-aria-1-2.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own query consistency profiles and result descriptors: authoritative revision or
causal frontier, projection generation, completeness, redaction policy and
continuation identity. Store and identity services supply enforceable read facets.
An object appearing in a result does not authorize a later command.

### Admission, transitions and completion

Bind a query to current realm and policy, validate a requested minimum frontier or
maximum staleness, and select a compatible projection. Return explicit stale or
incomplete status when the profile allows it; otherwise refuse. Pagination pins or
explicitly relaxes the read frontier and binds continuation tokens to query digest,
scope, generation and resource limit.

### Failure and adversarial behavior

A token copied between tenants can become a deputy if the next page trusts embedded
names. Cache keys omitting policy generation can disclose fields after revocation. A
changed projection may reuse row offsets with different meaning; restart pagination
rather than silently skipping or repeating protected records.

### Alternatives and unresolved tradeoffs

Snapshot pagination provides stronger repeatability but consumes retention and
storage. Live pagination is cheaper if callers accept moving results.
Read-your-writes can use a commit frontier without forcing every query into globally
linearizable execution.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Revoke read authority between pages and mutate the projection generation; continuation must respect both transitions.
- Issue a command from a stale query result; the command boundary must independently validate authority and expected revision.

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

1. [Event-sourced systems study](../../../30-sources/overeem-et-al-2021-event-sourced-systems.md).
2. [WAI-ARIA 1.2](../../../30-sources/w3c-2023-wai-aria-1-2.md).
