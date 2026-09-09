---
title: "Projection checkpoints, rebuild, and publication"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Projection checkpoints, rebuild, and publication

This study decomposes [Durable state, journals, snapshots, and projections](../durable-state-journals-snapshots-and-projections.md).

Research question: How can a derived view be rebuilt and switched without claiming false freshness?

## Research basis and status

Overeem and colleagues report practitioner experience with event evolution and recovery costs, not universal event-sourcing benefits. [1](../../../30-sources/overeem-et-al-2021-event-sourced-systems.md).

The early Elm paper demonstrates asynchronous view composition, not durable application outcomes or protected presentation. [2](../../../30-sources/czaplicki-chong-2013-asynchronous-frp-guis.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own projection definition, input frontiers, checkpoint, output generation, redaction
dimensions and completeness. Projection state is derived unless a separate
application decision says otherwise. Its offset must describe exactly the input
reflected in its output, not merely messages received.

### Admission, transitions and completion

Apply an input idempotently with its checkpoint in one qualified transaction, or use
a recovery protocol proving equivalent coupling. Rebuild into a private generation
from available authoritative input, catch up through a declared frontier, validate
and request publication. Queries name the generation and consistency profile; old
continuation tokens cannot silently address the new layout.

### Failure and adversarial behavior

A crash between row update and offset advancement can duplicate or skip
materialization. Loss of source history makes some rebuilds impossible. A projection
rebuilt under obsolete redaction policy is not safe merely because its content
frontier is current. Recompute or filter under current read authority before
disclosure.

### Alternatives and unresolved tradeoffs

Incremental projection lowers routine cost but has more checkpoint states than
on-demand queries. Full rebuild is simpler only when source retention and bounded
catch-up exist. Coalescing is acceptable for disposable views, not for required
outcome or audit records.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Crash between output and checkpoint writes and compare with a clean reference rebuild.
- Replace a projection while queries paginate and policy changes; reject stale tokens and disclose the precise available frontier.

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
2. [Asynchronous FRP](../../../30-sources/czaplicki-chong-2013-asynchronous-frp-guis.md).
