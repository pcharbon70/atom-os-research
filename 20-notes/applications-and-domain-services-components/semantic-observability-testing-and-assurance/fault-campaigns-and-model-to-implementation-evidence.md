---
title: "Fault campaigns and model-to-implementation evidence"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Fault campaigns and model-to-implementation evidence

This study decomposes [Semantic observability, testing, and assurance](../semantic-observability-testing-and-assurance.md).

Research question: How will a plausible architecture be tested against failures its abstract model cannot represent?

## Research basis and status

AWS reports design errors found with small executable specifications; models remain distinct from implementation evidence. [1](../../../30-sources/newcombe-et-al-2015-aws-formal-methods.md).

Crash-only design puts authoritative state outside replaceable components; restarting cannot repair every corruption or ambiguous effect. [2](../../../30-sources/candea-fox-2003-crash-only-software.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own a qualification matrix connecting every claimed boundary to an observable case,
implementation revision, environment and evidence artifact. Distinguish
deterministic actor schedules from real storage, native-code, network, power and
resource failures. No tests described in this research have been executed as
architecture qualification.

### Admission, transitions and completion

Map model actions to instrumented admission, commit, dispatch, receipt, publication
and teardown points. Inject failures before and after each, then query state and
outcomes through public contracts. Preserve raw histories, seeds and limitations.
Compare the actual substrate's behavior with modeled assumptions and reopen claims
when it diverges.

### Failure and adversarial behavior

A simulated atomic store cannot validate power-loss durability. Killing one actor
cannot exercise runtime-memory corruption. Green tests can omit the exact stale
fence or mixed-schema path used in production. Failed or blocked cases must remain
visible; a documentation review is not a pass.

### Alternatives and unresolved tradeoffs

Deterministic simulation is efficient for searching interleavings; physical and
infrastructure campaigns test model fidelity at higher cost. Neither replaces the
other. Qualification should start with narrow complete contracts, then compose them
with adversarial cross-boundary scenarios.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Run paired simulated and real-store commit interruption cases and document any differing possible histories.
- Exhaust ordinary resources while an effect is indeterminate and an update is draining; verify reserved reconciliation and honest unresolved status.

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

1. [AWS formal methods](../../../30-sources/newcombe-et-al-2015-aws-formal-methods.md).
2. [Crash-only software](../../../30-sources/candea-fox-2003-crash-only-software.md).
