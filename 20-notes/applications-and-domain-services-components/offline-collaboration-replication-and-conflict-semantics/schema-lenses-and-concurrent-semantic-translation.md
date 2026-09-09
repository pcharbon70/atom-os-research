---
title: "Schema lenses and concurrent semantic translation"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Schema lenses and concurrent semantic translation

This study decomposes [Offline collaboration, replication, and conflict semantics](../offline-collaboration-replication-and-conflict-semantics.md).

Research question: Can old and new offline clients collaborate without silently changing the meaning of edits?

## Research basis and status

Cambria demonstrates schema lenses but explicitly leaves semantic reassignment and missing external data beyond mechanical translation. [1](../../../30-sources/litt-et-al-2020-cambria.md).

Liskov and Wing treat substitution as preservation of behavioral properties, beyond compatible representation. [2](../../../30-sources/liskov-wing-1994-behavioral-subtyping.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own writer-schema identity, reader-schema compatibility, transformation graph, loss
declarations and interpretation version. Store original attributable operations
rather than converting away their provenance. A lens can translate representation; a
different domain action requires explicit application logic and authority.

### Admission, transitions and completion

Resolve a bounded trusted transformation path, interpret records in the reader's
schema and preserve required unknown information. Test mixed old/new writes, not
only static round trips. Record the schema under which each operation was authored.
When translation lacks required facts or changes action meaning, retain a conflict
or require authorized reapplication.

### Failure and adversarial behavior

A rename handled independently by two clients can alternate deletion and recreation
of fields. Several transformation paths can disagree. A default cannot reconstruct a
removed fact, and a field edit cannot safely stand in for reassignment of a
referenced entity. Loading a lens is also loading executable or interpreted behavior
with resource and trust requirements.

### Alternatives and unresolved tradeoffs

On-read translation preserves original writes but increases reader cost. Canonical
migration simplifies active readers but needs coordination with old peers. Neither
approach proves behavioral equivalence; maintain explicit unsupported version pairs
and repair paths.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Replay concurrent edits across branched schema versions and compare all declared transformation paths.
- Translate a reference change requiring unavailable external facts; preserve uncertainty rather than synthesize a privileged action.

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

1. [Project Cambria](../../../30-sources/litt-et-al-2020-cambria.md).
2. [Behavioral subtyping](../../../30-sources/liskov-wing-1994-behavioral-subtyping.md).
