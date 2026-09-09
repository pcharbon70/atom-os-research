---
title: "Passivation, tombstones, and retained responsibility"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Passivation, tombstones, and retained responsibility

This study decomposes [Durable domain identity, aggregate actors, and lifecycle](../durable-domain-identity-aggregate-actors-and-lifecycle.md).

Research question: When may an aggregate release memory or destroy state without losing ownership of unresolved work?

## Research basis and status

RIFL couples mutations to retained completion records; its guarantees require participating storage and recoverable request identity. [1](../../../30-sources/lee-et-al-2015-rifl.md).

Crash-only design puts authoritative state outside replaceable components; restarting cannot repair every corruption or ambiguous effect. [2](../../../30-sources/candea-fox-2003-crash-only-software.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own the passivation decision, durable lifecycle tombstone and inventory of pending
commands, workflows and effects. Volatile inactivity is not absence of durable
responsibility. Layer 4 owns storage retention and teardown mechanisms; Layer 5
states which records still make an outcome recoverable.

### Admission, transitions and completion

Close new admission, complete or durably hand off accepted work, checkpoint where
required, invalidate the activation route and release volatile state. Destruction
additionally records final revision, lifecycle generation, references and retention
obligations. Compaction may replace detailed results with sufficient tombstones, but
expired operation identities must fail closed once their full outcome record is
gone.

### Failure and adversarial behavior

A quiet mailbox can coexist with an in-flight store commit or external request.
Premature passivation can lose the only live lookup path. A delayed retry after
result expiry must not become a new command. Key reuse waits for an explicit
old-generation rejection policy, not an arbitrary sleep.

### Alternatives and unresolved tradeoffs

Never passivating avoids some transitions but gives unbounded memory with entity
growth. Retaining every detailed outcome forever avoids some ambiguity but creates
unbounded durable cost. Bounded admission epochs plus carefully scoped tombstones
trade availability of old results against safe refusal.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Passivate at each commit/reply boundary and recover the same operation result.
- Expire outcome retention, then replay old IDs and reuse entity keys; no new execution may arise from forgotten identity.

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

1. [RIFL](../../../30-sources/lee-et-al-2015-rifl.md).
2. [Crash-only software](../../../30-sources/candea-fox-2003-crash-only-software.md).
