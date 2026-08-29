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

- [Making reliable distributed systems in the presence of software errors](armstrong-2003-making-reliable-distributed-systems.md) —
  develops the original isolation, failure-detection, supervision, upgrade,
  and stable-storage argument.
- [A History of Erlang](armstrong-2007-history-of-erlang.md) — records the
  concurrency model's origin and candid lessons about isolation, foreign code,
  atoms, protocols, and distributed security.
- [AtomVM source tree at `0220c78e`](atomvm-project-2026-source-tree.md) — pins and audits the current
  runtime, platform seam, MCU entry points, native trust boundary, and build
  attempt.
- [AtomVM main documentation](atomvm-project-2026-main-documentation.md) —
  records the development documentation's process, memory, scheduling,
  execution, distribution, platform, and compatibility model.
- [Announcing AtomVM v0.7.0-alpha.0](atomvm-project-2026-v0-7-alpha0.md) — captures the official
  prerelease feature and stability boundary after the v0.6 line.
- [What's on your mind for AtomVM v0.7?](atomvm-community-2025-v0-7-priorities.md) — preserves a dated
  community view of performance, tooling, network, peripheral, power, and
  flash-layout priorities.
- [Functional Programming for the Internet of Things](branch-weinstock-2024-functional-programming-iot.md) — summarizes a
  2024 AtomVM/Elixir versus C++ LoRa–MQTT gateway comparison and its
  reproducibility limits.
- [Evaluating AtomVM for Fault-Tolerant ESP32-Based Systems](ferenczi-ruda-toth-2025-evaluating-atomvm.md) — records
  abstract-level evidence about redundant hardware and remote-node monitoring.
- [Measuring Erlang-Based Scalability and Fault Tolerance on the Edge](ferenczi-ruda-toth-2025-measuring-erlang-scalability.md) — records
  open-access process, supervision, mailbox, LoRa, memory, and power
  measurements on ESP32-S3.
- [Erlang/OTP 29.0.5 system documentation](erlang-otp-team-2026-otp-29-documentation.md) —
  records current process, signal, scheduler, memory, code-loading,
  supervision, release, distribution, and security contracts.
- [Erlang/OTP source tree at 5cf5f9725452](erlang-otp-team-2026-otp-29-source-tree.md) —
  pins and audits current ERTS internals, constants, code publication, native
  boundaries, and host-OS dependencies.
- [The Road to the JIT](gustavsson-2020-road-to-the-jit.md) — traces Erlang
  execution engines and the whole-system trade-offs behind BeamAsm.
- [A brief introduction to BEAM](hogberg-2020-brief-introduction-to-beam.md) —
  establishes the official distinction between BEAM instructions and ERTS
  runtime facilities.
- [Efficient memory management for concurrent programs that use message passing](sagonas-wilhelmsson-2006-efficient-memory-management.md) —
  compares local, communal, and hybrid heaps and evaluates incremental
  collection trade-offs.
- [The BEAM Book](stenman-2025-beam-book.md) — provides a detailed secondary
  guide to compiler and ERTS internals, used with current primary checks.
- [Scaling Reliably](trinder-et-al-2017-scaling-reliably.md) — evaluates VM and
  distributed-actor scaling and shows the costs of global topology,
  namespaces, and recovery data.
- [Characterizing the scalability of Erlang VM on many-core processors](zhang-2011-erlang-vm-many-core-scalability.md) —
  provides historical evidence about hidden runtime synchronization beneath a
  share-nothing programming model.
- [UEFI Specification 2.11](uefi-forum-2024-uefi-2-11.md) — defines the boot
  and runtime service boundary, memory-map handoff, configuration tables, and
  authenticated-boot mechanisms used by standards-based platform entry.
- [ACPI Specification 6.6](uefi-forum-2025-acpi-6-6.md) — defines table and
  namespace mechanisms for discovery, topology, interrupts, timers, power, and
  platform configuration.
- [Devicetree Specification 0.4](devicetree-org-2023-devicetree-0-4.md) —
  defines the flattened hardware-description and boot contract proposed for
  the first RISC-V profile.
- [RISC-V privileged and unprivileged architecture specifications](risc-v-international-2026-privileged-architecture.md) —
  records privilege, traps, translation, PMP, fences, counters, extension
  discovery, and RVWMO obligations.
- [RISC-V Supervisor Binary Interface Specification 3.0](risc-v-international-2025-sbi-3-0.md) —
  defines the provisional supervisor-to-firmware interface for timers, IPIs,
  hart lifecycle, reset, and related platform operations.
- [RISC-V Advanced Interrupt Architecture 1.0](risc-v-international-2023-advanced-interrupt-architecture.md) —
  defines APLIC, IMSIC, message-signaled interrupts, and per-hart interrupt
  state for the protected RV64 profile.
- [RISC-V IOMMU Architecture Specification 1.0.1](risc-v-international-2026-iommu-1-0-1.md) —
  defines device contexts, translation, invalidation, queues, fault reporting,
  and MSI remapping for DMA isolation.
- [Arm A-profile system architecture documentation](arm-2026-a-profile-system-architecture-documentation.md) —
  routes through the architecture, GIC, SMMUv3, PSCI, generic timer, and cache
  publication material needed by the second-ISA profile.
- [Intel 64 system programming and VT-d documentation](intel-2026-system-programming-documentation.md) —
  records the x86-64 privilege, paging, APIC, extended-state, virtualization,
  and DMA-remapping comparison surface.
- [QEMU Arm and RISC-V virt platform documentation](qemu-project-2026-virt-platform-documentation.md) —
  records the emulator machine, discovery, interrupt, IOMMU, and version-pinning
  boundaries for the proposed target sequence.
- [The Multikernel](baumann-et-al-2009-multikernel.md) — motivates explicit
  per-core state and message-mediated coordination across heterogeneous,
  non-uniform multicore hardware.
- [Comprehensive formal verification of an OS microkernel](klein-et-al-2014-comprehensive-sel4-verification.md) —
  demonstrates a small precisely specified isolation core and documents the
  assumptions outside the verified boundary.
- [A least-privilege memory protection model for modern hardware](achermann-et-al-2019-least-privilege-memory-protection.md) —
  models translation structures and memory mappings as delegated authority.
- [Arrakis: The operating system is the control plane](peter-et-al-2014-arrakis.md) —
  evaluates protected direct I/O and separation of control-plane policy from
  data-plane device access.
- [CleanQ](haecki-et-al-2019-cleanq.md) — formalizes queue operations as
  ownership transfer across software and hardware boundaries.
- [Thunderclap](markettos-et-al-2019-thunderclap.md) — demonstrates DMA attacks
  against systems where IOMMU protection is absent, bypassed, or too
  permissive.
- [Multiprogramming a 64 kB computer safely and efficiently](levy-et-al-2017-tock.md) —
  presents an MPU-oriented embedded isolation design and its constrained-system
  trade-offs.
- [Improving the reliability of commodity operating systems](swift-et-al-2003-nooks.md) —
  supplies historical evidence about isolating and recovering faulty drivers
  inside a shared-kernel architecture.
- [x86-TSO](sewell-et-al-2010-x86-tso.md) — gives a rigorous model for x86
  multiprocessor ordering and qualifies the notion of a simply “strong” ISA.
- [Modelling the ARMv8 architecture, operationally](flur-et-al-2016-armv8-concurrency.md) —
  provides formal and experimental evidence about weakly ordered Arm
  concurrency behavior.
- [Relaxed virtual memory in Armv8-A](simner-et-al-2022-relaxed-virtual-memory.md) —
  analyzes interactions among weak memory, page-table updates, translation,
  and invalidation.
- [LazyFP](stecklina-prescher-2018-lazyfp.md) — shows how lazy FPU and SIMD
  switching can leak architectural state across protection domains.
- [Platform Firmware Resiliency Guidelines](regenscheid-2018-platform-firmware-resiliency.md) —
  separates firmware protection, detection, and recovery requirements.
- [CHERI Instruction-Set Architecture, version 9](watson-et-al-2023-cheri-v9.md) —
  defines a capability-hardware design retained as an optional research profile
  rather than a baseline portability assumption.
- [Zig 0.16.0 language documentation](zig-project-2026-language-documentation.md) — records the
  official execution, allocation, C-interoperability, cross-target, and SIMD
  semantics used to qualify the project's Zig implementation decision.

## Maintaining this index

Index every direct source note with a concise description. Preserve exact
metadata where available, never invent unknown fields, and link derived work.
