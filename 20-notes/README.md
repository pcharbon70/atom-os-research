---
title: "Notes"
kind: map
created: "2026-08-28"
tags:
  - archive-navigation
  - directory-index
aliases:
  - "Notes index"
---

# Notes (`20-notes`)

## Purpose

Notes preserve ideas, arguments, models, and syntheses in the author's own
words.

## What belongs here

Put independently useful conclusions and developing interpretations here.
Source summaries belong in `30-sources`; unresolved workbenches belong in
`40-inquiries`.

## Index

### Subdirectories

- [Kernel hardware and architecture components](kernel-hardware-and-architecture-components/README.md) —
  contains the eleven detailed component-level implementation syntheses for
  the kernel hardware and architecture support layer.
- [Managed actor runtime components](managed-actor-runtime-components/README.md) —
  contains the thirteen detailed component-level implementation syntheses for
  the managed actor runtime layer.
- [Minimal privileged kernel components](minimal-privileged-kernel-components/README.md) —
  contains the eleven detailed component-level implementation syntheses for
  the capability-microkernel layer.

### Documents

- [AtomVM as an operating-system foundation](atomvm-as-an-operating-system-foundation.md) — assesses the
  current runtime boundary, empirical limits, missing OS responsibilities, and
  a proposed minimal-substrate architecture.
- [BEAM, ERTS, and OTP principles for a new operating system](beam-erts-and-otp-principles-for-a-new-operating-system.md) —
  separates the three layers, makes compiled-BEAM compatibility and
  process-local tracing collection explicit, identifies needed security and
  resource-control changes, and proposes a layered architecture.
- [Managed actor runtime layer](managed-actor-runtime-layer.md) — develops the
  unprivileged BEAM-compatible runtime contract, thirteen component design,
  critical execution paths, implementation stages, and conformance,
  responsiveness, overload, and fault evaluation plan.
- [Kernel hardware and architecture support layer](kernel-hardware-and-architecture-support-layer.md) —
  develops the kernel-level contracts for privileged entry, execution context,
  translation, ordering and code publication, interrupts, time, logical CPUs,
  protected I/O, faults, and a portable typed facade.
- [Minimal privileged kernel layer](minimal-privileged-kernel-layer.md) —
  proposes a capability microkernel with explicit object memory, first-class
  execution-stop domains, bounded IPC and CPU budgets, revocation anchors,
  structured fault routes, and quiescence- or quarantine-gated recovery, with
  each component linked to its detailed evidence and implementation report.

## Maintaining this index

Index every direct note and describe its claim or role. Keep maturity values
honest and connect each note to evidence, related notes, or a map.
