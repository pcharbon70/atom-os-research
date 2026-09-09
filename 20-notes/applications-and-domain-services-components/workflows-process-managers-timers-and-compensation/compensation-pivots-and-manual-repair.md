---
title: "Compensation, pivots, and manual repair"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Compensation, pivots, and manual repair

This study decomposes [Workflows, process managers, timers, and compensation](../workflows-process-managers-timers-and-compensation.md).

Research question: How can interrupted work be amended without pretending its visible effects never happened?

## Research basis and status

Sagas permit visible intermediate commits and semantic compensation; they do not supply outer transaction isolation. [1](../../../30-sources/garcia-molina-salem-1987-sagas.md).

Liskov and Wing treat substitution as preservation of behavioral properties, beyond compatible representation. [2](../../../30-sources/liskov-wing-1994-behavioral-subtyping.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own compensation meaning, original step parameters, pivot classification,
compensation operation identity and repair responsibility. Compensation is a new
domain action under current authority. A refund, release or correction is not a
physical restoration of a prior snapshot.

### Admission, transitions and completion

Record which committed steps require amendment and their dependency order. Before
the irreversible pivot, execute permitted compensations; after it, follow explicit
roll-forward or repair policy. Retain original code and parameters while any
compensation can be needed. Report terminated workflows with surviving effects and
unresolved obligations, not simply failed.

### Failure and adversarial behavior

A compensation can be refused, uncertain or permanently impossible. Repeated
attempts must use its stable operation identity. Operator assignment may end
automated work but does not close the business obligation; the repair case remains
attributable and queryable until its domain closure criteria are met.

### Alternatives and unresolved tradeoffs

Automatic reversal is appropriate only where the domain provides a valid operation
after intervening work. Manual repair offers flexibility but requires narrow
authority, evidence and an operational owner. Generic reverse-order execution is
insufficient for parallel dependency graphs.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Fail compensation after an earlier visible commit and verify that the history retains both facts.
- Revoke the initiator before repair; test the explicit policy for delegated completion authority without reviving the user's old grant.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Effect reconciliation and unqueryable repair](../external-effects-ports-adapters-and-reconciliation/effect-reconciliation-and-unqueryable-repair.md) — a cross-component contract this service must preserve.
- [Workflow-generation handoff and publication fences](../application-evolution-schema-compatibility-and-migration/workflow-generation-handoff-and-publication-fences.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [Sagas](../../../30-sources/garcia-molina-salem-1987-sagas.md).
2. [Behavioral subtyping](../../../30-sources/liskov-wing-1994-behavioral-subtyping.md).
