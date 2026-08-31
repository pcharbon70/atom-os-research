---
title: "BEAM, ERTS, and OTP"
kind: map
created: "2026-08-28"
tags:
  - actor-model
  - beam
  - erts
  - fault-tolerance
  - operating-systems
  - otp
  - virtual-machines
aliases:
  - "BEAM and OTP"
  - "Erlang runtime architecture"
---

# BEAM, ERTS, and OTP

## Scope

This map separates three layers that are often compressed into the word
“BEAM” and asks what each contributes to a new operating-system design:

- **BEAM** is the register instruction machine and code format used to execute
  compiled Erlang-family code.
- **ERTS** is the Erlang Runtime System that implements processes, signals,
  mailboxes, scheduling, garbage collection, ports, timers, tables, code
  loading, and distribution around that machine.
- **OTP** supplies libraries, behaviours, supervision trees, applications,
  releases, and operational conventions on top of the runtime mechanisms.

The distinction prevents an implementation detail in current Erlang/OTP from
being mistaken for a kernel requirement. Running compiled BEAM code is now a
platform requirement, including automatic process-local tracing collection.
The BEAM instruction set remains a managed-runtime contract rather than the
kernel ABI, and the project is not committed to one existing VM implementation.

## Start here

- [BEAM, ERTS, and OTP principles for a new operating
  system](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md) —
  the current synthesis, required compiled-BEAM and process-local-GC contract,
  proposed layering, design rules, risks, and research program.
- [Which BEAM, ERTS, and OTP principles belong in a new
  kernel?](../40-inquiries/which-beam-erts-and-otp-principles-belong-in-the-kernel.md) —
  the open decision and its falsifiable evaluation criteria.
- [2026-08-28 BEAM, ERTS, and OTP deep
  dive](../50-journal/2026-08-28-beam-erts-and-otp-deep-dive.md) — source
  acquisition, exact revision, search coverage, commands, and limitations.

## Trails

### Current system semantics and implementation

- [Erlang/OTP 29.0.5 system
  documentation](../30-sources/erlang-otp-team-2026-otp-29-documentation.md) —
  current language, process, scheduler, memory, code-loading, supervision,
  release, distribution, and security contracts.
- [Erlang/OTP source tree at
  5cf5f9725452](../30-sources/erlang-otp-team-2026-otp-29-source-tree.md) —
  pinned audit of ERTS internals, runtime constants, code loading, native
  boundaries, and Unix host dependencies.
- [A brief introduction to
  BEAM](../30-sources/hogberg-2020-brief-introduction-to-beam.md) — the official
  engineering distinction between the instruction VM and ERTS.
- [The Road to the
  JIT](../30-sources/gustavsson-2020-road-to-the-jit.md) — implementation
  history and the trade-offs behind load-time BeamAsm translation.
- [The BEAM Book](../30-sources/stenman-2025-beam-book.md) — a detailed
  secondary guide to compiler and ERTS internals, checked against the pinned
  source where it affects this synthesis.

### Reliability model and its qualifications

- [Making reliable distributed systems in the presence of software
  errors](../30-sources/armstrong-2003-making-reliable-distributed-systems.md) —
  the process-isolation, failure-detection, upgrade, stable-storage, and
  supervision argument.
- [A History of Erlang](../30-sources/armstrong-2007-history-of-erlang.md) —
  origin and evolution of the concurrency model, including candid limits in
  isolation, foreign code, atoms, and distributed security.

### Memory and scalability

- [Efficient memory management for concurrent programs that use message
  passing](../30-sources/sagonas-wilhelmsson-2006-efficient-memory-management.md) —
  compares process-local, shared, and hybrid heap designs and evaluates
  incremental collection.
- [Characterizing the scalability of Erlang VM on many-core
  processors](../30-sources/zhang-2011-erlang-vm-many-core-scalability.md) —
  historical evidence that a share-nothing process abstraction can still hide
  runtime-wide lock and allocator contention.
- [Scaling Reliably](../30-sources/trinder-et-al-2017-scaling-reliably.md) —
  shows how global namespaces, full-mesh distribution, and global recovery
  state constrain scale, and how partitioned groups recover it.

### Concrete implementation cases

- [AtomVM foundation](atomvm-foundation.md) — a compact, embedded BEAM
  implementation already studied in this archive. It is now treated as one
  design case rather than the project’s prescribed foundation.
- [Tyn](https://github.com/tyn-os/kernel), [GRiSP
  Metal](https://www.grisp.org/software), and historical LING are implementation
  leads surveyed in the journal. Their claims remain contextual until pinned,
  audited, and reproduced locally.

### Kernel mechanism boundary

- [Kernel hardware and architecture
  support](kernel-hardware-and-architecture-support.md) refines the lowest
  layer of the proposed operating-system decomposition. It defines the
  privileged entry, context, translation, ordering, event, time, CPU, DMA, and
  fault contracts that a managed actor runtime would consume without turning
  BEAM or OTP policy into architecture code.

## Open questions

- [What contract should the kernel hardware and architecture layer
  provide?](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
- [Which BEAM, ERTS, and OTP principles belong in a new
  kernel?](../40-inquiries/which-beam-erts-and-otp-principles-belong-in-the-kernel.md)
- Can reduction-like accounting provide predictable scheduling once interrupts,
  drivers, garbage collection, and multicore contention are included?
- Which pinned BEAM/OTP profile defines initial compatibility, and can a new
  runtime match its allocation, root-liveness, process-local collection,
  message, exception, code-loading, and observability behavior?
- Should mailboxes be bounded kernel objects, credit-controlled channels, or a
  runtime abstraction over lower-level capability endpoints?
- What is the smallest protection boundary that contains a faulty native
  driver without discarding cheap process creation and communication?
- Can versioned service endpoints and atomic publication preserve OTP-style
  upgrades while providing signed images, rollback, durable state migration,
  and recovery after power loss?
- Which parts of the Erlang distribution model remain useful after replacing
  fully trusted nodes and global naming with authenticated capabilities and
  explicit failure domains?
