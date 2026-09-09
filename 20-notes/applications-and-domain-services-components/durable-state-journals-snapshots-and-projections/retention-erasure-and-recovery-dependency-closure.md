---
title: "Retention, erasure, and recovery dependency closure"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Retention, erasure, and recovery dependency closure

This study decomposes [Durable state, journals, snapshots, and projections](../durable-state-journals-snapshots-and-projections.md).

Research question: What must remain reachable before history, outcomes or private data can be collected?

## Research basis and status

Overeem and colleagues report practitioner experience with event evolution and recovery costs, not universal event-sourcing benefits. [1](../../../30-sources/overeem-et-al-2021-event-sourced-systems.md).

Local-first research argues for locally usable user-owned documents; its scope is not arbitrary scarce-resource or external-effect transactions. [2](../../../30-sources/kleppmann-et-al-2019-local-first-software.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own retention classes and a dependency inventory spanning source events,
authoritative snapshots, outcome tombstones, workflow compensation parameters,
projections, exports and backups. Generic deletion and key management belong to
Layer 4. This is a technical privacy and recovery model, not a claim of legal
compliance.

### Admission, transitions and completion

Classify data as authoritative, derived, accepted responsibility or historical
evidence. Compute which retained readers and workflows still need it. Stage deletion
or transformation with an auditable policy decision, preserve required nonsecret
identity barriers and verify resulting recovery. Deleting a key affects only copies
exclusively protected by that key; plaintext caches and exported replicas require
separate treatment.

### Failure and adversarial behavior

A retention job can destroy the only evidence that prevents a delayed retry, or
erase compensation inputs before a workflow finishes. Conversely, keeping immutable
history forever can violate the application's promised data lifecycle. Surface
irreconcilable retention/recovery requirements instead of quietly prioritizing one.

### Alternatives and unresolved tradeoffs

Selective payload separation and encrypted fields can reduce retained sensitive
content while preserving structural history, but add key and schema dependencies.
Detailed outcomes may compact to minimal expired-ID barriers. Indefinite retention
is not a substitute for a defined retry horizon.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Delete a subject payload while an unresolved workflow, backup and projection reference it; enumerate each retained or removed copy.
- Expire detailed outcomes and replay old requests; collection must not re-enable forgotten operations.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Aggregate commit bundles and revision validation](../invariants-transactions-and-concurrency-policy/aggregate-commit-bundles-and-revision-validation.md) — a cross-component contract this service must preserve.
- [Shadow migration checkpoints and validation](../application-evolution-schema-compatibility-and-migration/shadow-migration-checkpoints-and-validation.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [Event-sourced systems study](../../../30-sources/overeem-et-al-2021-event-sourced-systems.md).
2. [Local-First Software](../../../30-sources/kleppmann-et-al-2019-local-first-software.md).
