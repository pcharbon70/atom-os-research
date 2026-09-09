---
title: "Clock continuity and era transitions"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - raw-time-and-deadline-programming
aliases: []
---

# Clock continuity and era transitions

Recalibration should preserve a clock's continuity when evidence supports it; a genuine discontinuity should create a new era and explicitly resolve old-era obligations. These are different operations.

## Scope and research question

How does the system avoid inventing elapsed time after source replacement, suspend or reset?

This report refines [component 6: Raw time and deadline programming](../raw-time-and-deadline-programming.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

ClockEra names one continuity claim. ConversionSnapshotGeneration names a representation change within it. Maintain compatible MonotonicInstant and DeadlineTarget types and a ledger of open deadline tokens. A source-switch record contains old/new observations, uncertainty and continuity justification. Civil-time correction remains a higher-level policy.

### Protocol and publication points

For continuous replacement, sample the old timeline, establish a compatible new anchor and atomically publish a new conversion generation without changing era. For unproved continuity, close old-era admission, create the new era and terminally resolve every still-open old-era token as EraDiscontinuity. Rebase of an armed token competes through its exact terminal slot and links any replacement token.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Changing source and scale separately can produce enormous fabricated jumps. A system resume timestamp does not automatically prove elapsed duration. Silently clamping or translating an old deadline can make it expire in an unrelated era. Concurrent channel failure must not overwrite an already sealed discontinuity or fired result.

### Alternatives and tradeoffs

Always advancing era simplifies safety but burdens consumers during benign recalibration. Preserving era without evidence is convenient but corrupts timeout meaning. Explicit continuity evidence allows selective preservation while keeping uncertainty visible.

### Cross-architecture realization

Source reset and suspend properties depend on the platform and retained execution environment, not just the ISA timer instruction. Active-monotonic and suspend-inclusive domains require separate promises.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Switch sources with known offsets and verify monotonic continuity within declared uncertainty.
- Resume with unknown elapsed time and reject ordinary old/new-era subtraction.
- Race discontinuity with fire, cancel and rebase; preserve one exact terminal per accepted token.

System-wide old-era token enumeration and continuity proofs under concurrent source changes remain open.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Absolute deadline channel programming](absolute-deadline-programming.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Timecounters](../../../30-sources/kamp-2002-timecounters.md) — Wrap-aware conversion and matched source/anchor publication.
- [Linux low-level core APIs](../../../30-sources/linux-kernel-community-2026-low-level-core-apis.md) — Engineering precedent; Linux contracts are not Atom proofs.
- [High-resolution timekeeping research](../../../30-sources/terraneo-cattaneo-2026-high-resolution-timekeeping.md) — Separating shared timekeeping from per-CPU preemption.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
