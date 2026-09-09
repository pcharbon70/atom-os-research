---
title: "Causal frontiers, tombstones, and peer retirement"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Causal frontiers, tombstones, and peer retirement

This study decomposes [Offline collaboration, replication, and conflict semantics](../offline-collaboration-replication-and-conflict-semantics.md).

Research question: When can collaborative history be collected without resurrecting deleted content?

## Research basis and status

CRDT convergence follows stated algebra and delivery assumptions, not arbitrary invariant or authorization correctness. [1](../../../30-sources/shapiro-et-al-2011-conflict-free-replicated-data-types.md).

Local-first research argues for locally usable user-owned documents; its scope is not arbitrary scarce-resource or external-effect transactions. [2](../../../30-sources/kleppmann-et-al-2019-local-first-software.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own admitted peer membership, causal frontiers, tombstones, rejected-operation
retention and replica retirement generations. A deleted element's metadata can
remain necessary to reject a delayed dependent edit. Layer 4 provides storage and
authenticated peer identity, not the domain's forgetting rule.

### Admission, transitions and completion

Track sufficient stable frontiers for the chosen replication profile. Compact only
after all permitted future operations are either represented or excluded by an
enforced retirement policy. A retired peer re-enters through a fresh snapshot and
generation; its old operations are rejected or offered as new user-reviewed drafts,
never merged blindly.

### Failure and adversarial behavior

An indefinitely offline peer can prevent safe collection under an unlimited-return
promise. A malicious peer can withhold acknowledgment or create unbounded causal
references. Bound admitted membership and metadata, and state the
availability-versus-retention tradeoff before accepting offline work.

### Alternatives and unresolved tradeoffs

Permanent tombstones simplify safety but impose growing cost and privacy exposure.
Expiring peer membership enables bounded history at the price of rejecting old work.
Snapshot exchange reduces transfer cost only if it retains required attribution and
rejection barriers.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Delete content, collect under a retirement certificate and reconnect the old peer; no resurrection may occur.
- Withhold one peer's frontier and flood dependencies; compaction must not fake stability and admission must remain bounded.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Escrow rights conservation and transfer](../invariants-transactions-and-concurrency-policy/escrow-rights-conservation-and-transfer.md) — a cross-component contract this service must preserve.
- [Directed compatibility and behavioral fixture matrices](../application-evolution-schema-compatibility-and-migration/directed-compatibility-and-behavioral-fixture-matrices.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [CRDTs](../../../30-sources/shapiro-et-al-2011-conflict-free-replicated-data-types.md).
2. [Local-First Software](../../../30-sources/kleppmann-et-al-2019-local-first-software.md).
