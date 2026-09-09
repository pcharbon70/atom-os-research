---
title: "Deterministic event reducers and replay firewalls"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Deterministic event reducers and replay firewalls

This study decomposes [Durable state, journals, snapshots, and projections](../durable-state-journals-snapshots-and-projections.md).

Research question: How can history reconstruct truth without repeating real-world actions?

## Research basis and status

Durable Functions formalizes restricted history replay; arbitrary nondeterminism and external effects remain outside that abstraction. [1](../../../30-sources/burckhardt-et-al-2021-durable-functions.md).

Overeem and colleagues report practitioner experience with event evolution and recovery costs, not universal event-sourcing benefits. [2](../../../30-sources/overeem-et-al-2021-event-sourced-systems.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own event decoding, reducer generation, deterministic inputs and replay progress. A
reducer maps a valid prior state and committed fact to a new state; it has no live
network, device, secret or command-publication imports. Randomness, time and
external observations needed for meaning must be recorded as facts.

### Admission, transitions and completion

Read a bounded history segment under a compatible reader, verify stream identity and
positions, apply pure transformations and checkpoint progress. Keep recovery replay
distinct from an outbox relay: the relay resumes already recorded effect intent by
stable ID; replay never creates a fresh intent from observing an old event.

### Failure and adversarial behavior

Calling an old event handler that also sends email can duplicate every historical
notification. Querying today's exchange rate during replay can change a previously
committed amount. Unknown critical events, broken causal order or invariant
violations require quarantine, not best-effort skipping.

### Alternatives and unresolved tradeoffs

Pure reducers make repeatability auditable but can increase event design effort.
Snapshot-only recovery is faster when its authority and retention are explicit.
Sandboxed replay supplements code review but still needs resource bounds; a pure
function can diverge or allocate without limit.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Run identical histories with different clocks, randomness and denied I/O; semantic state must be identical.
- Replay through a deliberate effect-call trap; any attempted dispatch is a failure even if the destination is mocked.

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

1. [Durable Functions semantics](../../../30-sources/burckhardt-et-al-2021-durable-functions.md).
2. [Event-sourced systems study](../../../30-sources/overeem-et-al-2021-event-sourced-systems.md).
