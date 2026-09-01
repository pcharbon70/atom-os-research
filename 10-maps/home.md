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
platform must run compiled BEAM code with BEAM-compatible process semantics,
including automatic process-local tracing garbage collection, without making
one existing VM implementation the kernel foundation.

## Active inquiries

- [What contract should the minimal privileged kernel
  provide?](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) —
  defines falsifiable capability, domain, IPC, CPU-budget, fault, teardown,
  recovery-independence, portability, and BEAM-compatibility criteria.
- [What contract should the kernel hardware and architecture layer
  provide?](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) —
  defines falsifiable authority, completion, isolation, ordering, portability,
  failure, and performance criteria for the privileged mechanism boundary.
- [Which BEAM, ERTS, and OTP principles belong in a new
  kernel?](../40-inquiries/which-beam-erts-and-otp-principles-belong-in-the-kernel.md) —
  defines the experiments needed to place required BEAM-compatible runtime
  mechanisms at the right system layer and choose between runtime strategies.
- [Can AtomVM serve as the kernel-facing runtime of a new embedded operating
  system?](../40-inquiries/can-atomvm-serve-as-a-kernel-facing-runtime.md) —
  retains AtomVM as one concrete implementation case and defines its boot,
  substrate, resource, fault, trust, and lifecycle evidence requirements.

## Topic maps

- [Minimal privileged kernel](minimal-privileged-kernel.md) — routes through
  the capability, protected-domain, bounded-IPC, temporal-authority, failure,
  driver-containment, teardown, and assurance evidence for the layer above
  architecture support.
- [Kernel hardware and architecture
  support](kernel-hardware-and-architecture-support.md) — routes through the
  kernel-level evidence for entry/context, translation, ordering and code
  publication, interrupts, time, CPU lifecycle, protected I/O, and faults while
  excluding board and physical-component engineering.
- [BEAM, ERTS, and OTP](beam-erts-and-otp.md) — separates the instruction
  machine, runtime mechanisms, and OTP policy, then routes through current
  documentation, source, foundational papers, scalability evidence, and the OS
  design synthesis.
- [AtomVM foundation](atomvm-foundation.md) — routes through the current
  architecture, measurements, and open questions for one compact BEAM
  implementation.

## Recently developed

- [Minimal privileged kernel
  layer](../20-notes/minimal-privileged-kernel-layer.md) — proposes a capability
  microkernel with explicit object resources, coordinated execution-stop
  domains, bounded invocation and CPU budgets, typed fault routes, and clean or
  quarantined reaping outcomes.
- [2026-08-31 minimal privileged-kernel deep
  dive](../50-journal/2026-08-31-minimal-privileged-kernel-deep-dive.md) — records
  the primary literature, articles, design review trails, and evidence limits
  behind the proposal.
- [Kernel hardware and architecture support
  layer](../20-notes/kernel-hardware-and-architecture-support-layer.md) —
  proposes eleven semantic components, explicit authority and quiescence
  lifecycles, a cross-architecture comparison, and a phased verification plan.
- [2026-08-30 kernel hardware and architecture support deep
  dive](../50-journal/2026-08-30-kernel-hardware-and-architecture-support-deep-dive.md) —
  records the literature search, exact kernel-level scope, primary sources,
  method, and absence of implementation evidence.
- [BEAM, ERTS, and OTP principles for a new operating
  system](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md) —
  proposes a layered design with actor-friendly kernel mechanisms, required
  BEAM-compatible managed execution and process-local tracing collection, and
  user-space OTP recovery policy while strengthening security and resource
  control.
- [2026-08-28 BEAM, ERTS, and OTP deep
  dive](../50-journal/2026-08-28-beam-erts-and-otp-deep-dive.md) — records the
  pinned OTP 29.0.5 source audit, literature search, practitioner survey, and
  evidence limits.
- [AtomVM as an operating-system
  foundation](../20-notes/atomvm-as-an-operating-system-foundation.md) —
  assesses one possible compact execution nucleus and its native isolation
  limits.

## Unsettled threads

- Model capability derivation, call cancellation, scheduling-context donation,
  SMP domain freeze, and quiescence-gated reaping before choosing kernel data
  structures or optimizing fast paths.
- Define a checked initial authority manifest and prove that each supervisor's
  CPU, memory, fault path, and teardown reserve remains outside the child's
  reach.
- Validate the proposed architecture-support contracts with executable state
  models, one virtual target, and eventually a materially different second ISA.
- Define completion and failure budgets for cross-CPU mapping, code
  publication, interrupt delivery, CPU quiescence, and DMA revocation.
- Decide whether the first compatibility prototype should port a pinned ERTS
  or execute a declared BEAM/OTP profile in a new runtime; a principles-only
  runtime no longer satisfies the platform goal.
- Validate the proposed capability, quota, bounded-transport, and
  failure-domain semantics against a BEAM runtime without making each actor a
  kernel object.
- Measure reduction-style accounting against wall-clock latency, interrupt
  pre-emption, native work, and priority inversion.
- Demonstrate boot, driver-fault containment, crash-consistent persistence,
  authenticated distribution, atomic update/rollback, and retained diagnostics.
