---
title: "Application-service admission and use-case coordination"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Application-service admission and use-case coordination

This study decomposes [Bounded contexts, domain model, and application services](../bounded-contexts-domain-model-and-application-services.md).

Research question: How does a use case coordinate work without becoming the hidden owner of every business rule?

## Research basis and status

Evans separates domain rules from application coordination; this is a pattern vocabulary, not a recovery proof. [1](../../../30-sources/evans-2015-domain-driven-design-reference.md).

RIFL couples mutations to retained completion records; its guarantees require participating storage and recoverable request identity. [2](../../../30-sources/lee-et-al-2015-rifl.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own the use-case protocol, request-to-operation binding, current progress and
dependency calls. Aggregate code owns synchronous invariants; Layer 4 issues
authority and supplies durable transactions. The application service must identify
where responsibility moves from a transient request handler into a durable owner.

### Admission, transitions and completion

Decode and validate scope, authenticate the realm binding, obtain narrow action
authority, then bind operation identity before delegating consequential work. A
short use case can execute one aggregate decision and commit. A multi-stage use case
becomes a durable workflow; it must not rely on a stack frame surviving remote
calls. Return an outcome whose receipt names the actual completed scope.

### Failure and adversarial behavior

Retrying a whole handler after reply loss can repeat a committed first step. An
application service must recover the existing operation, not allocate fresh
identities because its actor restarted. Domain rejection and policy denial are
independently meaningful but must be redacted where their distinction would disclose
protected object existence.

### Alternatives and unresolved tradeoffs

Putting all rules in service scripts makes reuse and invariant review difficult.
Putting network calls inside aggregates blocks serialization and hides distributed
failure. Prefer thin coordination plus explicit stateful workflow only where
accepted responsibility outlives one local commit.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Crash after first aggregate commit but before handler reply; recovery must report or continue the same operation.
- Present valid domain input with revoked authority, and authorized input violating an invariant; neither may commit.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Invariant catalog and coordination selection](../invariants-transactions-and-concurrency-policy/invariant-catalog-and-coordination-selection.md) — a cross-component contract this service must preserve.
- [Operation identity and honest outcome ledgers](../typed-commands-queries-events-and-protocol-contracts/operation-identity-and-honest-outcome-ledgers.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [DDD Reference](../../../30-sources/evans-2015-domain-driven-design-reference.md).
2. [RIFL](../../../30-sources/lee-et-al-2015-rifl.md).
