---
title: "Deadline terminalization and cancellation"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - raw-time-and-deadline-programming
aliases: []
---

# Deadline terminalization and cancellation

Every accepted deadline should have one retained terminal decision even if notifications are lost. Cancellation chooses an outcome through the same protected record as firing, rebasing and channel failure.

## Scope and research question

How can a caller determine what happened when expiry, cancellation and replacement race?

This report refines [component 6: Raw time and deadline programming](../raw-time-and-deadline-programming.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

A DeadlineToken binds channel/CPU/programming identities, clock era, source/conversion generations and caller operation. Its protected terminal slot admits Fired, Cancelled, Rebased, RebaseFailed, EraDiscontinuity or ChannelFailed. Channel health is separate. A sealed record is immutable and pollable until acknowledged; notification is only a bounded hint.

### Protocol and publication points

Open → exactly one selected terminal → retained observation → consumer acknowledgement → safe slot reuse. Fire/cancel/rebase/failure compete on one generation-bound arbitration point. Hardware cancellation must establish the channel post-state but cannot rewrite a token already fired. Rebase seals the old token and identifies the replacement; it does not mutate old identity in place.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

A late interrupt may refer to an earlier compare value; it is not itself authority to complete the current token. Returning cancellation success before defining which outcome won creates duplicate or lost effects. Catastrophic failure can prevent eventual observation; at-most-once sealing safety must not be advertised as unconditional liveness or durability.

### Alternatives and tradeoffs

Callbacks alone are convenient but obscure lost-notification and reentrancy behavior. Retained results consume bounded storage and need acknowledgement/backpressure. A polling inspection path preserves outcome discoverability without pretending the system survives every failure.

### Cross-architecture realization

Comparator and pending-state effects differ across backends. The channel protocol tolerates spurious/stale interrupts while requiring exact current-state validation. Real-time response additionally depends on scheduling and interrupt availability.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Enumerate fire/cancel/rebase/failure interleavings and require at most one terminal per exact token.
- Drop all EventSink notifications and retrieve the retained outcome through inspection.
- Recycle channel generations and replay old interrupts/results; they must not alter the new token.

Terminalization linearizability, result-pool exhaustion and liveness under the stated failure model remain unverified.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Counter and clock-domain qualification](counter-and-clock-domain-qualification.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Tock HIL design](../../../30-sources/tock-project-2026-hil-design.md) — Submission, returned ownership and asynchronous completion contracts.
- [Linux low-level core APIs](../../../30-sources/linux-kernel-community-2026-low-level-core-apis.md) — Engineering precedent; Linux contracts are not Atom proofs.
- [RISC-V privileged architecture](../../../30-sources/risc-v-international-2026-privileged-architecture.md) — Privilege and trap semantics qualified by extensions.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
