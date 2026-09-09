---
title: "Counter extension and checked conversion"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - raw-time-and-deadline-programming
aliases: []
---

# Counter extension and checked conversion

Counter extension is a bounded arithmetic inference over a known sampling interval. It cannot recover an arbitrary number of missed wraps or silently turn overflow into a plausible timestamp.

## Scope and research question

How can raw wrapping counts become a timescale with a declared numerical error and validity horizon?

This report refines [component 6: Raw time and deadline programming](../raw-time-and-deadline-programming.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

Conversion state binds source, mask, anchor ticks/time, multiplier, shift, validity horizon and error bounds. Use checked widened arithmetic or a proved multiword operation. Distinct Duration and compatible instant types prevent accidental cross-era subtraction. Deadline conversion additionally declares rounding direction and hardware minimum/maximum lead.

### Protocol and publication points

Acquire a consistent live snapshot → sample its source → compute masked delta → validate elapsed-range assumptions → convert with checked product/shift → return value and quality. Refresh the anchor before wrap ambiguity. Source or conversion changes publish a matched snapshot; a reader must not combine old ticks with a new scale.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Two different elapsed durations can have the same masked delta after missed wraps. A 128-bit intermediate may introduce a compiler helper whose behavior is outside a critical-context contract. Rounding down a deadline can violate a no-early-fire promise unless the programming contract explicitly accounts for it. Saturating arithmetic must return its degraded status.

### Alternatives and tradeoffs

Floating-point conversion is convenient but imports state and rounding obligations into privileged paths. Fixed-point conversion has predictable cost but needs a proved range. Frequent anchors reduce ambiguity while increasing update work.

### Cross-architecture realization

The arithmetic model is portable; widths, access atomicity and counter frequency are profile inputs. No backend may choose a longer horizon merely because ordinary workloads rarely delay readers that long.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Use tiny-width model counters to exercise every wrap boundary and missed-multiple-wrap case.
- Check maximum products, signed/unsigned conversion and deadline rounding around one-tick boundaries.
- Compare against an exact arithmetic oracle and verify the declared maximum error over the validity horizon.

The arithmetic proof, helper closure and worst-case anchor servicing assumptions remain open.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Conversion snapshot publication and lifetime](conversion-snapshot-publication.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Timecounters](../../../30-sources/kamp-2002-timecounters.md) — Wrap-aware conversion and matched source/anchor publication.
- [Zig language reference](../../../30-sources/zig-project-2026-language-reference-0-16.md) — Lifetime discipline, atomics and assembly remain explicit obligations.
- [High-resolution timekeeping research](../../../30-sources/terraneo-cattaneo-2026-high-resolution-timekeeping.md) — Separating shared timekeeping from per-CPU preemption.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
