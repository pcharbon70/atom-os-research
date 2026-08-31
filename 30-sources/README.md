---
title: "Sources"
kind: map
created: "2026-08-28"
tags:
  - archive-navigation
  - directory-index
aliases:
  - "Sources index"
---

# Sources (`30-sources`)

## Purpose

Source notes preserve bibliographic provenance and evidence-focused reading
notes separately from the archive's synthesis.

## What belongs here

Create one note for each substantively used paper, book, specification,
official documentation set, codebase revision, talk, dataset, or other primary
work. Incidental mentions can remain citations in the document using them.

## Index

### Subdirectories

- None yet.

### Documents

- [A least-privilege memory protection model for modern hardware](achermann-et-al-2019-least-privilege-memory-protection.md) —
  separates authority to configure address translation from authority to
  access the translated memory across CPUs and devices.
- [Arm A-profile system architecture documentation](arm-2026-a-profile-system-architecture-documentation.md) —
  records current AArch64 exception, translation, ordering, cache, timer, and
  feature-state semantics relevant to a kernel backend.
- [Making reliable distributed systems in the presence of software errors](armstrong-2003-making-reliable-distributed-systems.md) —
  develops the original isolation, failure-detection, supervision, upgrade,
  and stable-storage argument.
- [A History of Erlang](armstrong-2007-history-of-erlang.md) — records the
  concurrency model's origin and candid lessons about isolation, foreign code,
  atoms, protocols, and distributed security.
- [What's on your mind for AtomVM v0.7?](atomvm-community-2025-v0-7-priorities.md) —
  preserves a dated community view of performance, tooling, network,
  peripheral, power, and flash-layout priorities.
- [AtomVM main documentation](atomvm-project-2026-main-documentation.md) —
  records the development documentation's process, memory, scheduling,
  execution, distribution, platform, and compatibility model.
- [AtomVM source tree at `0220c78e`](atomvm-project-2026-source-tree.md) — pins
  and audits the current runtime, platform seam, MCU entry points, native trust
  boundary, and build attempt.
- [Announcing AtomVM v0.7.0-alpha.0](atomvm-project-2026-v0-7-alpha0.md) —
  captures the official prerelease feature and stability boundary after the
  v0.6 line.
- [The Multikernel](baumann-et-al-2009-multikernel.md) — motivates explicit
  cross-core messages, replicated local state, and hardware-neutral structure
  for heterogeneous multicore systems.
- [Dune](belay-et-al-2012-dune.md) — demonstrates controlled user-level access
  to selected privileged CPU features behind second-level protection.
- [Functional Programming for the Internet of Things](branch-weinstock-2024-functional-programming-iot.md) —
  summarizes a 2024 AtomVM/Elixir versus C++ LoRa–MQTT gateway comparison and
  its reproducibility limits.
- [From L3 to seL4](elphinstone-heiser-2013-l4-lessons.md) — reviews durable
  microkernel lessons about minimal mechanism, capabilities, asynchronous
  interrupts, address spaces, portability, and assembly boundaries.
- [Exokernel](engler-et-al-1995-exokernel.md) — distinguishes enforceable
  resource protection from application-level management and analyzes secure
  binding and revocation.
- [Erlang/OTP 29.0.5 system documentation](erlang-otp-team-2026-otp-29-documentation.md) —
  records current process, signal, scheduler, memory, code-loading,
  supervision, release, distribution, and security contracts.
- [Erlang/OTP source tree at 5cf5f9725452](erlang-otp-team-2026-otp-29-source-tree.md) —
  pins and audits current ERTS internals, constants, code publication, native
  boundaries, and host-OS dependencies.
- [Evaluating AtomVM for Fault-Tolerant ESP32-Based Systems](ferenczi-ruda-toth-2025-evaluating-atomvm.md) —
  records abstract-level evidence about redundant hardware and remote-node
  monitoring.
- [Measuring Erlang-Based Scalability and Fault Tolerance on the Edge](ferenczi-ruda-toth-2025-measuring-erlang-scalability.md) —
  records open-access process, supervision, mailbox, LoRa, memory, and power
  measurements on ESP32-S3.
- [The Flux OSKit](ford-et-al-1997-flux-oskit.md) — provides evidence about
  semantic component interfaces, dependency glue, architecture exposure, and
  component granularity in kernel construction.
- [CertiKOS](gu-et-al-2016-certikos.md) — develops layered observable
  specifications and contextual refinement for concurrent kernels while
  documenting important model exclusions.
- [The Road to the JIT](gustavsson-2020-road-to-the-jit.md) — traces Erlang
  execution engines and the whole-system trade-offs behind BeamAsm.
- [CleanQ](haecki-et-al-2019-cleanq.md) — formalizes device queues as explicit
  buffer-ownership transfer and evaluates a lightweight common interface.
- [A brief introduction to BEAM](hogberg-2020-brief-introduction-to-beam.md) —
  establishes the official distinction between BEAM instructions and ERTS
  runtime facilities.
- [Intel 64 and IA-32 system programming documentation](intel-2026-system-programming-documentation.md) —
  records current x86 privilege, entry, translation, interrupt, time,
  extended-state, and optional virtualization mechanisms.
- [Comprehensive formal verification of an OS microkernel](klein-et-al-2014-comprehensive-sel4-verification.md) —
  connects explicit capabilities and objects to a small verified TCB and makes
  hardware, boot, assembly, cache, device, DMA, and timing assumptions visible.
- [Linux kernel low-level core API documentation](linux-kernel-community-2026-low-level-core-apis.md) —
  compares current entry, interrupt-flow, time, ordering, cache/TLB,
  logical-CPU lifecycle, and DMA contracts.
- [Thunderclap](markettos-et-al-2019-thunderclap.md) — demonstrates why IOMMU
  remapping alone does not secure shared DMA protocols, transition windows,
  revocation, or reset.
- [Arrakis](peter-et-al-2014-arrakis.md) — separates a kernel control plane from
  delegated application I/O data paths and reports workload-specific latency
  and throughput gains.
- [Simplifying Arm concurrency](pulte-et-al-2018-simplifying-arm-concurrency.md) —
  gives rigorous multicopy-atomic axiomatic and operational models for the
  relaxed Armv8 memory model.
- [The RISC-V privileged architecture](risc-v-international-2026-privileged-architecture.md) —
  records current ratified RISC-V privilege, trap, translation, ordering,
  instruction-fetch, counter, and extension-state semantics.
- [Efficient memory management for concurrent programs that use message passing](sagonas-wilhelmsson-2006-efficient-memory-management.md) —
  compares local, communal, and hybrid heaps and evaluates incremental
  collection trade-offs.
- [x86-TSO](sewell-et-al-2010-x86-tso.md) — supplies a rigorous usable model for
  x86 multiprocessor memory behavior and clearly bounds what that model does
  not cover.
- [Arm instruction-fetch semantics](simner-et-al-2020-arm-instruction-fetch.md) —
  models cache, barrier, and cross-core obligations for executable-code
  publication on Armv8-A.
- [Relaxed virtual memory in Armv8-A](simner-et-al-2022-relaxed-virtual-memory.md) —
  models page-table mutation, TLB invalidation, barriers, and remote observation
  as a virtual-memory protocol.
- [LazyFP](stecklina-prescher-2018-lazyfp.md) — demonstrates speculative leakage
  from lazy floating-point context switching and motivates explicit ownership
  of all enabled extended state.
- [The BEAM Book](stenman-2025-beam-book.md) — provides a detailed secondary
  guide to compiler and ERTS internals, used with current primary checks.
- [Scaling Reliably](trinder-et-al-2017-scaling-reliably.md) — evaluates VM and
  distributed-actor scaling and shows the costs of global topology,
  namespaces, and recovery data.
- [Characterizing the scalability of Erlang VM on many-core processors](zhang-2011-erlang-vm-many-core-scalability.md) —
  provides historical evidence about hidden runtime synchronization beneath a
  share-nothing programming model.

## Maintaining this index

Index every direct source note with a concise description. Preserve exact
metadata where available, never invent unknown fields, and link derived work.
