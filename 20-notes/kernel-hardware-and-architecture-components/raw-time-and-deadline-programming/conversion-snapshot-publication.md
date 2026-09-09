---
title: "Conversion snapshot publication and lifetime"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - raw-time-and-deadline-programming
aliases: []
---

# Conversion snapshot publication and lifetime

A time reader must use one matched source/anchor/scale snapshot whose storage remains valid throughout the read. A generation retry is a consistency check, not a memory-lifetime mechanism.

## Scope and research question

How can interruptible readers remain safe while conversion snapshots are replaced or recycled?

This report refines [component 6: Raw time and deadline programming](../raw-time-and-deadline-programming.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

Publish immutable conversion records through a protected reference/epoch scheme with explicit reuse eligibility. The record contains source identity, clock era, conversion generation, anchor, mask, scale and validity horizon. Reader admission pins both record and source. An NMI-safe path needs preallocated storage and a progress argument that does not depend on the interrupted writer running.

### Protocol and publication points

Construct unused record → publish complete generation → readers acquire a valid lifetime guard → sample/convert/revalidate → release guard → retire old record only after readers drain. If using a latch or sequence-counter variant, separately prove its data-access legality, writer serialization and dynamic pointer lifetime. A bounded reader may fail with quality-unavailable rather than retry indefinitely.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

A reader that interrupts an odd-state writer can spin forever. Double buffering alone is unsafe if a delayed reader survives enough updates to see its slot reused. Non-atomic racing field accesses remain a source-language problem even when a later version mismatch is detected.

### Alternatives and tradeoffs

A lock is simple where readers cannot interrupt their holder. Immutable records with safe reclamation suit read-mostly paths but need bounded capacity and exhaustion policy. Latches address specific interruption patterns, not arbitrary object lifetime.

### Cross-architecture realization

The publication protocol must be valid in the language memory model before ISA lowering. Per-CPU copies can reduce contention but require a clear relation to the same clock domain and conversion-generation contract.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Interrupt the writer at every step with each admitted reader context.
- Suspend a reader across multiple replacements and attempted buffer reuse.
- Corrupt or retire the source pointer independently from the snapshot and require lifetime protection to prevent access.

A wait-free or bounded-failure critical reader and safe finite-pool reclamation remain unproved.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Clock continuity and era transitions](clock-continuity-and-era-transitions.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Sequence counters and sequential locks](../../../30-sources/linux-kernel-community-2026-sequence-counter-contracts.md) — Reader consistency does not establish pointer lifetime or bounded progress.
- [Timecounters](../../../30-sources/kamp-2002-timecounters.md) — Wrap-aware conversion and matched source/anchor publication.
- [Zig language reference](../../../30-sources/zig-project-2026-language-reference-0-16.md) — Lifetime discipline, atomics and assembly remain explicit obligations.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
