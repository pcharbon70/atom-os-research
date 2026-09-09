---
title: "Replicated-type specifications and intent preservation"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Replicated-type specifications and intent preservation

This study decomposes [Offline collaboration, replication, and conflict semantics](../offline-collaboration-replication-and-conflict-semantics.md).

Research question: Which concurrent edits should be equivalent, and which must remain visible conflicts?

## Research basis and status

CRDT convergence follows stated algebra and delivery assumptions, not arbitrary invariant or authorization correctness. [1](../../../30-sources/shapiro-et-al-2011-conflict-free-replicated-data-types.md).

OpSets makes replicated meaning explicit through sequential interpretation; convergence can still permit undesirable user-visible ordering. [2](../../../30-sources/kleppmann-et-al-2018-opsets.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own a sequential reference meaning, admitted operations, causal relationships and
merge algebra for each collaborative type. A text sequence, annotation set and
object ownership field need not share a consistency profile. Converged bytes are one
requirement among intent, invariants and disclosure.

### Admission, transitions and completion

Specify representative concurrent histories, including insertion groups,
move/delete, overwrite and undo. Integrate only validated operations and interpret
them deterministically under a pinned type version. Preserve alternatives or
explicit conflict objects where no automatic rule matches intended meaning. Commands
with scarce or irreversible consequences leave the content merge path.

### Failure and adversarial behavior

A last-writer-wins register may converge while losing an intentional edit. A move
can create an illegal parent cycle despite individually valid operations. Clock
order cannot substitute for causal context. User repair is itself an operation with
identity and current authorization, not an untracked database patch.

### Alternatives and unresolved tradeoffs

CRDTs suit data whose declared operations meet the algebra. Application-defined
merge permits richer semantics but increases proof and testing burden. Central
sequencing is a valid choice for nonmergeable decisions even inside an otherwise
local-first document.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Generate concurrent grouped insertions and move/delete histories; compare convergence and intended sequential meaning separately.
- Construct cross-field invariant violations from individually valid edits; reject the profile or add coordination rather than accepting mere convergence.

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
2. [OpSets](../../../30-sources/kleppmann-et-al-2018-opsets.md).
