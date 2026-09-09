---
title: "Snapshot validation and authority promotion"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Snapshot validation and authority promotion

This study decomposes [Durable state, journals, snapshots, and projections](../durable-state-journals-snapshots-and-projections.md).

Research question: When is a checkpoint a disposable cache, and when has pruning made it authoritative?

## Research basis and status

ARIES makes recovery depend on durable ordering metadata; its storage log is not a domain-event model. [1](../../../30-sources/mohan-et-al-1992-aries.md).

Overeem and colleagues report practitioner experience with event evolution and recovery costs, not universal event-sourcing benefits. [2](../../../30-sources/overeem-et-al-2021-event-sourced-systems.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own snapshot identity, source-prefix commitment, through-position, schema and
reducer generation, checksum and retention relationship. A snapshot is normally
derived from retained history. Once necessary history is removed, that snapshot and
its suffix become an authoritative recovery base with stronger preservation
obligations.

### Admission, transitions and completion

Build privately from a verified frontier, validate state and replay equivalence, and
publish a checkpoint reference atomically. Before pruning, establish recoverability
from every retained backup and promised reader. Record an explicit promotion
decision and immutable dependency set; do not let a generic cache collector delete
the now-authoritative checkpoint.

### Failure and adversarial behavior

A valid checksum says bytes match the recorded digest, not that the reducer produced
correct state. A snapshot ahead of the retained outcome ledger may misrepresent
accepted operations. If both checkpoint and required history are lost, report
unrecoverable state rather than fabricate an empty aggregate.

### Alternatives and unresolved tradeoffs

Frequent checkpoints reduce replay latency but increase write amplification and
retention complexity. Keeping complete history allows fallback at privacy and
capacity cost. Compare measured recovery budgets and failure domains, not only
nominal snapshot size.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Corrupt or replace a derived checkpoint and verify fallback to retained history.
- Prune a history prefix, then remove the promoted checkpoint in a test store; recovery must detect the missing authoritative dependency.

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

1. [ARIES](../../../30-sources/mohan-et-al-1992-aries.md).
2. [Event-sourced systems study](../../../30-sources/overeem-et-al-2021-event-sourced-systems.md).
