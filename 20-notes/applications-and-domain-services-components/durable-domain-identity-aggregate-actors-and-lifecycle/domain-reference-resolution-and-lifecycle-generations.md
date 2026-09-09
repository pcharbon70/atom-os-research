---
title: "Domain-reference resolution and lifecycle generations"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Domain-reference resolution and lifecycle generations

This study decomposes [Durable domain identity, aggregate actors, and lifecycle](../durable-domain-identity-aggregate-actors-and-lifecycle.md).

Research question: How does a domain reference survive runtime replacement without reviving a deleted entity?

## Research basis and status

Evans separates domain rules from application coordination; this is a pattern vocabulary, not a recovery proof. [1](../../../30-sources/evans-2015-domain-driven-design-reference.md).

The 2014 Orleans report separates logical actor identity from activation; its cloud model is not the BEAM process contract. [2](../../../30-sources/bernstein-et-al-2014-orleans.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own DomainRef as context, business-tenant designation, entity type, key and semantic
lifecycle generation. Keep mutable security-realm assignments in separately
authenticated bindings. A PID, activation lease, storage location or route is a
temporary resolution result, never part of the entity's durable identity.

### Admission, transitions and completion

Resolve only after validating the caller's current binding and requested action.
Return a generation-bound route or typed absent, deleted, unavailable or denied
result under disclosure policy. Entity creation allocates its own lifecycle
generation. Restart may change every execution identifier without changing that
semantic generation; destruction and permitted key reuse must distinguish the
successor.

### Failure and adversarial behavior

A cached route may reach a live actor for an obsolete entity. Validate DomainRef and
lifecycle generation at the sink, not just the directory. Missing activation is not
entity absence. An administrator moving data between realms must not accidentally
create new business identity or authorize old realm holders against the destination.

### Alternatives and unresolved tradeoffs

Embedding location in identity simplifies direct lookup but complicates movement and
recovery. Eternal globally unique keys avoid reuse ambiguity but do not eliminate
deletion, privacy or storage costs. Research whether readable aliases can remain
entirely outside the durable key.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Move an entity between runtime domains and security bindings; identity remains stable while old authority fails.
- Delete and recreate a user-visible key; replay old commands, routes and workflow references and require lifecycle rejection.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Aggregate commit bundles and revision validation](../invariants-transactions-and-concurrency-policy/aggregate-commit-bundles-and-revision-validation.md) — a cross-component contract this service must preserve.
- [Workflow-generation handoff and publication fences](../application-evolution-schema-compatibility-and-migration/workflow-generation-handoff-and-publication-fences.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [DDD Reference](../../../30-sources/evans-2015-domain-driven-design-reference.md).
2. [Orleans virtual actors](../../../30-sources/bernstein-et-al-2014-orleans.md).
