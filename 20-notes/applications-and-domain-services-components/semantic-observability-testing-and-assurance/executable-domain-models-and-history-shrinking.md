---
title: "Executable domain models and history shrinking"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Executable domain models and history shrinking

This study decomposes [Semantic observability, testing, and assurance](../semantic-observability-testing-and-assurance.md).

Research question: What oracle can detect incorrect histories rather than merely compare implementation outputs with themselves?

## Research basis and status

QuickCheck supplies generated properties and shrinking; an incomplete oracle or input distribution can miss failures. [1](../../../30-sources/claessen-hughes-2000-quickcheck.md).

AWS reports design errors found with small executable specifications; models remain distinct from implementation evidence. [2](../../../30-sources/newcombe-et-al-2015-aws-formal-methods.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own an independent reference state machine, safety and liveness properties,
operation generators, history shrinkers and assumption register. The model describes
domain commitments and permitted uncertainty. It must not simply invoke the
production implementation's transition code and call agreement independent evidence.

### Admission, transitions and completion

Generate valid and adversarial commands, retries, stale generations, policy changes
and migrations. Compare observable histories with the reference model. Classify
coverage by important transitions and failure windows. Shrink while preserving
causality and required preconditions so a reduced failure remains a possible
execution. Record seeds, model versions and minimal counterexamples.

### Failure and adversarial behavior

An oracle omitting compensation or expiration may approve unsafe results. Unbounded
liveness cannot be established by finite random tests. A model checker proves only
the modeled bounded or symbolic property under its assumptions; tests are still
needed to connect those actions to the real runtime and stores.

### Alternatives and unresolved tradeoffs

Small targeted models are more reviewable than a monolithic simulation of the OS.
Differential tests add useful comparison where implementations share a contract, but
shared bugs remain possible. Prioritize models around identity retention, fencing,
migration and irreversible effects.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Seed known duplicate-execution and stale-writer bugs and require the model campaign to find them.
- Shrink a failure containing a lost receipt and policy change; retain the causal conditions that make its result invalid.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Operation identity and honest outcome ledgers](../typed-commands-queries-events-and-protocol-contracts/operation-identity-and-honest-outcome-ledgers.md) — a cross-component contract this service must preserve.
- [Semantic admission classes and protected recovery reserve](../cross-layer-placement-tenancy-overload-and-recovery-topology/semantic-admission-classes-and-protected-recovery-reserve.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [QuickCheck](../../../30-sources/claessen-hughes-2000-quickcheck.md).
2. [AWS formal methods](../../../30-sources/newcombe-et-al-2015-aws-formal-methods.md).
