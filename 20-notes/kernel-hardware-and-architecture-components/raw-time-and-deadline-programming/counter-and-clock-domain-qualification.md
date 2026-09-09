---
title: "Counter and clock-domain qualification"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - raw-time-and-deadline-programming
aliases: []
---

# Counter and clock-domain qualification

A readable counter is not automatically a portable clock. Its rate, scope, continuity and observation ordering must be qualified independently.

## Scope and research question

What comparisons and timeout decisions are justified by a particular raw source?

This report refines [component 6: Raw time and deadline programming](../raw-time-and-deadline-programming.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

ClockProfile records width, nominal/rate evidence, scope, comparability, suspend behavior, access privilege, read ordering and known failure modes. RawTicks binds source and CPU/scope generation. Distinguish local monotonic samples from globally comparable instants with bounded skew. Diagnostic sampling can expose an unqualified value with that status; correctness-sensitive callers cannot silently treat it as qualified time.

### Protocol and publication points

Discovered → access verified → width/rate characterized → continuity/scope evaluated → profile admitted → health monitored. Rate stability does not prove equal reset values across CPUs. Source-health failure withdraws its promise and initiates the explicit continuity/era protocol. Ordered reads for accounting have separate semantics from cheap diagnostic samples.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Migration can turn local monotonic counters into backward global time. Deep power states, reset or an external execution environment may change assumptions. A monotonic clamp can hide error and accumulate unbounded skew. Repeated reads cannot reconstruct elapsed wraps that were never observed.

### Alternatives and tradeoffs

A single global source simplifies comparability but can be slow or contended. Per-CPU sources are cheap but require explicit domains and migration policy. A compatibility floor may be justified only with recorded clamping and an error budget, not as automatic repair.

### Cross-architecture realization

TSC-like, architectural generic counters and RISC-V time sources differ in access and invariance promises. Counters and programmable event devices need not be the same hardware. Bounded instruction sequences do not guarantee access latency through firmware or interconnect failure.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Inject rate changes, backward steps, source reset and unsynchronized CPU offsets.
- Read multipart counters at rollover and verify the chosen stable-read algorithm.
- Attempt a cross-domain comparison without a conversion/qualification witness and reject it.

Quantitative skew, health thresholds and admissible diagnostic/real-time sampling contexts remain profile-specific.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Counter extension and checked conversion](counter-extension-and-conversion.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Timecounters](../../../30-sources/kamp-2002-timecounters.md) — Wrap-aware conversion and matched source/anchor publication.
- [Linux low-level core APIs](../../../30-sources/linux-kernel-community-2026-low-level-core-apis.md) — Engineering precedent; Linux contracts are not Atom proofs.
- [High-resolution timekeeping research](../../../30-sources/terraneo-cattaneo-2026-high-resolution-timekeeping.md) — Separating shared timekeeping from per-CPU preemption.
- [Time protection](../../../30-sources/ge-et-al-2019-time-protection.md) — Temporal isolation exceeds timer precision.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
