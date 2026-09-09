---
title: "Directed compatibility and behavioral fixture matrices"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Directed compatibility and behavioral fixture matrices

This study decomposes [Application evolution, schema compatibility, and migration](../application-evolution-schema-compatibility-and-migration.md).

Research question: Which old/new combinations preserve the application's observable contract?

## Research basis and status

Liskov and Wing treat substitution as preservation of behavioral properties, beyond compatible representation. [1](../../../30-sources/liskov-wing-1994-behavioral-subtyping.md).

RFC 9413 warns that indiscriminate permissive parsing can preserve ambiguity and obstruct protocol evolution. [2](../../../30-sources/thomson-schinazi-2023-maintaining-robust-protocols.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own a directed compatibility matrix across commands, outcomes, events, states,
snapshots, workflows, extensions and configuration. Each allowed pair names
behavioral properties and fixture evidence. A reader range does not automatically
authorize the same writer range or a changed security policy.

### Admission, transitions and completion

Compare preconditions, guarantees, duplicate and timeout semantics, redaction,
invariants and permitted histories. Generate old/new request and durable-state
fixtures, including unknown critical fields. Reject unsupported pairs before
publication; keep unresolved compatibility explicit rather than deriving it from a
semantic-version number.

### Failure and adversarial behavior

An added optional field can encode a new constraint that old writers ignore. A
renamed result can make old clients retry a committed action. Mixed-generation
behavior may fail only after several calls, so single-message decoding tests cannot
close the matrix.

### Alternatives and unresolved tradeoffs

Exact-generation replacement reduces compatibility combinations but may require
downtime or draining. Broad version windows improve availability at a sustained test
and retention cost. Behavioral adapters can bridge some pairs, but cannot
manufacture missing authority or evidence.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Run every allowed producer/consumer pair through complete pending-to-terminal histories.
- Introduce a structurally readable field that changes an invariant; demonstrate that the old writer is excluded or safely adapted.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Retention, erasure, and recovery dependency closure](../durable-state-journals-snapshots-and-projections/retention-erasure-and-recovery-dependency-closure.md) — a cross-component contract this service must preserve.
- [Compensation, pivots, and manual repair](../workflows-process-managers-timers-and-compensation/compensation-pivots-and-manual-repair.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [Behavioral subtyping](../../../30-sources/liskov-wing-1994-behavioral-subtyping.md).
2. [RFC 9413](../../../30-sources/thomson-schinazi-2023-maintaining-robust-protocols.md).
