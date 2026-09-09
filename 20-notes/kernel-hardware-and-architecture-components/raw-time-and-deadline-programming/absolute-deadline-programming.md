---
title: "Absolute deadline channel programming"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - raw-time-and-deadline-programming
aliases: []
---

# Absolute deadline channel programming

A TimerChannel should own one precisely identified hardware programming obligation. It does not own the scheduler's queue of deadlines, and successful register programming is not equivalent to a future timely callback.

## Scope and research question

How is a deadline admitted without losing an expiry that races the programming sequence?

This report refines [component 6: Raw time and deadline programming](../raw-time-and-deadline-programming.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

Bind channel identity and CPU incarnation, programming generation, source/era/conversion generations, absolute target, lead/range limits and preallocated terminal slot. The channel retains an interrupt-binding generation, while component 5 owns controller operations. Remote programming uses component 7's request fabric rather than writing another CPU's local state implicitly.

### Protocol and publication points

Reserve result capacity → validate target and current conversion → serialize local channel state → accept token → compute/program compare → re-read time and pending condition → Armed or DuePending. If the target passed during programming, retain a due observation rather than wait for an interrupt that may not arrive. Long-range deadlines require an explicit intermediate wake strategy above or within a declared channel profile.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

An accepted token cannot disappear because programming failed; it must retain a typed failure outcome or unresolved ownership. A compare update may leave a stale interrupt pending. A remote request arriving after CPU restart must not program the replacement channel. Channel disable and token completion are separate state transitions.

### Alternatives and tradeoffs

Relative delays are simple but accumulate scheduling/programming error when retried. Absolute targets preserve intent while requiring careful era and conversion handling. One channel can serve many software timers only through a separately owned multiplexer.

### Cross-architecture realization

APIC-like, Arm generic-timer and RISC-V supervisor/firmware timer mechanisms differ in programming and pending-bit semantics. The normalized operation preserves absolute intent and observable outcome without promising identical hardware behavior.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Advance time across the target between conversion and register write.
- Inject maximum-range, too-close and stale-conversion targets with declared rejection or due outcomes.
- Deliver a remote programming request after CPU incarnation replacement and reject it.

Minimum-lead bounds, delayed programming effects and the complete channel-admission algorithm need profile tests.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Deadline terminalization and cancellation](deadline-terminalization-and-cancellation.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Linux low-level core APIs](../../../30-sources/linux-kernel-community-2026-low-level-core-apis.md) — Engineering precedent; Linux contracts are not Atom proofs.
- [RISC-V privileged architecture](../../../30-sources/risc-v-international-2026-privileged-architecture.md) — Privilege and trap semantics qualified by extensions.
- [High-resolution timekeeping research](../../../30-sources/terraneo-cattaneo-2026-high-resolution-timekeeping.md) — Separating shared timekeeping from per-CPU preemption.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
