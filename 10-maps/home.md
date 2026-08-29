---
title: "Atom OS Research"
kind: map
created: "2026-08-28"
tags:
  - beam
  - operating-systems
  - otp
aliases:
  - "Home"
---

# Atom OS Research

This is the selective entry point to research on a new kernel and operating
system informed by Erlang/OTP and BEAM principles. See the [archive
guide](../README.md) for the repository structure and working conventions.

## Research objective

Determine which actor, isolation, scheduling, recovery, upgrade, and
distribution principles should shape the kernel and wider system, then
establish a credible path from research prototypes to a bootable system. The
project is not committed to BEAM bytecode compatibility or to any existing VM.

## Active inquiries

- [Which BEAM, ERTS, and OTP principles belong in a new
  kernel?](../40-inquiries/which-beam-erts-and-otp-principles-belong-in-the-kernel.md) —
  compares compatibility and clean-slate paths and defines the experiments
  needed to place mechanisms at the right system layer.
- [Can AtomVM serve as the kernel-facing runtime of a new embedded operating
  system?](../40-inquiries/can-atomvm-serve-as-a-kernel-facing-runtime.md) —
  retains AtomVM as one concrete implementation case and defines its boot,
  substrate, resource, fault, trust, and lifecycle evidence requirements.

## Topic maps

- [BEAM, ERTS, and OTP](beam-erts-and-otp.md) — separates the instruction
  machine, runtime mechanisms, and OTP policy, then routes through current
  documentation, source, foundational papers, scalability evidence, and the OS
  design synthesis.
- [AtomVM foundation](atomvm-foundation.md) — routes through the current
  architecture, measurements, and open questions for one compact BEAM
  implementation.

## Recently developed

- [BEAM, ERTS, and OTP principles for a new operating
  system](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md) —
  proposes a layered design that adopts actor-friendly kernel mechanisms,
  ERTS-like managed execution, and user-space OTP recovery policy while
  strengthening security and resource control.
- [2026-08-28 BEAM, ERTS, and OTP deep
  dive](../50-journal/2026-08-28-beam-erts-and-otp-deep-dive.md) — records the
  pinned OTP 29.0.5 source audit, literature search, practitioner survey, and
  evidence limits.
- [AtomVM as an operating-system
  foundation](../20-notes/atomvm-as-an-operating-system-foundation.md) —
  assesses one possible compact execution nucleus and its native isolation
  limits.

## Unsettled threads

- Decide whether the first prototype should run unmodified ERTS, execute BEAM
  bytecode in a new runtime, or adopt only the architectural principles.
- Define kernel-level capability, quota, mailbox-pressure, and failure-domain
  semantics that are stronger than ordinary Erlang process isolation.
- Measure reduction-style accounting against wall-clock latency, interrupt
  pre-emption, native work, and priority inversion.
- Demonstrate boot, driver-fault containment, crash-consistent persistence,
  authenticated distribution, atomic update/rollback, and retained diagnostics.
