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
- [Scheduler Activations](anderson-et-al-1992-scheduler-activations.md) —
  separates kernel processor allocation from fine-grained user-level thread
  scheduling and evaluates the costs and complexity of activation upcalls.
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
- [Timing Analysis of a Protected Operating System Kernel](blackham-et-al-2011-timing-analysis-protected-kernel.md) —
  applies binary-level worst-case execution-time analysis to a protected
  microkernel and exposes configuration and hardware assumptions behind bounds.
- [Tolerating Malicious Device Drivers in Linux](boyd-wickizer-zeldovich-2010-malicious-device-drivers.md) —
  evaluates IOMMU and PCIe confinement, controlled device access, and
  user-process execution against an adversarial driver rather than accidental
  faults alone.
- [Functional Programming for the Internet of Things](branch-weinstock-2024-functional-programming-iot.md) —
  summarizes a 2024 AtomVM/Elixir versus C++ LoRa–MQTT gateway comparison and
  its reproducibility limits.
- [Microreboot—A Technique for Cheap Recovery](candea-et-al-2004-microreboot.md) —
  evaluates fine-grained component restart and makes state placement,
  dependency, retry, and application-visible recovery costs explicit.
- [Unreliable Failure Detectors for Reliable Distributed Systems](chandra-toueg-1996-failure-detectors.md) —
  formalizes the distinction between crash fact and liveness suspicion under
  timing assumptions.
- [Hive: Fault Containment for Shared-Memory Multiprocessors](chapin-et-al-1995-hive.md) —
  studies fault containment regions and correlated shared-memory failure on
  multiprocessors.
- [CuriOS: Improving Reliability through Operating System Structure](david-et-al-2008-curios.md) —
  isolates services and client-associated state to support recovery with less
  cross-client disruption.
- [Kernel Design for Isolation and Assurance of Physical Memory](elkaduwe-et-al-2008-kernel-memory-isolation.md) —
  connects explicit kernel-object memory, capabilities, and retyping to
  isolation and tractable assurance.
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
- [Time Protection: The Missing OS Abstraction](ge-et-al-2019-time-protection.md) —
  distinguishes CPU-budget isolation from microarchitectural timing-channel
  protection and evaluates partitioning, flushing, and padding mechanisms.
- [CertiKOS](gu-et-al-2016-certikos.md) — develops layered observable
  specifications and contextual refinement for concurrent kernels while
  documenting important model exclusions.
- [The Road to the JIT](gustavsson-2020-road-to-the-jit.md) — traces Erlang
  execution engines and the whole-system trade-offs behind BeamAsm.
- [CleanQ](haecki-et-al-2019-cleanq.md) — formalizes device queues as explicit
  buffer-ownership transfer and evaluates a lightweight common interface.
- [seL4 Design Principles](heiser-2020-sel4-design-principles.md) — records a
  practitioner account of functional minimality, explicit authority, bounded
  kernel work, and proof-oriented interface design.
- [Construction of a Highly Dependable Operating System](herder-et-al-2006-dependable-operating-system.md) —
  describes the MINIX 3 restructuring of drivers and services as isolated,
  restartable user-space processes and its recovery limits.
- [A brief introduction to BEAM](hogberg-2020-brief-introduction-to-beam.md) —
  establishes the official distinction between BEAM instructions and ERTS
  runtime facilities.
- [Intel 64 and IA-32 system programming documentation](intel-2026-system-programming-documentation.md) —
  records current x86 privilege, entry, translation, interrupt, time,
  extended-state, and optional virtualization mechanisms.
- [Comprehensive formal verification of an OS microkernel](klein-et-al-2014-comprehensive-sel4-verification.md) —
  connects explicit capabilities and objects to a small verified TCB and makes
  hardware, boot, assembly, cache, device, DMA, and timing assumptions visible.
- [On Micro-Kernel Construction](liedtke-1995-microkernel-construction.md) —
  derives functionally minimal protected mechanisms and analyzes why careful
  IPC and architecture-specific critical paths matter.
- [Linux kernel low-level core API documentation](linux-kernel-community-2026-low-level-core-apis.md) —
  compares current entry, interrupt-flow, time, ordering, cache/TLB,
  logical-CPU lifecycle, and DMA contracts.
- [Scheduling-Context Capabilities: A Principled, Light-Weight Operating-System Mechanism for Managing Time](lyons-et-al-2018-scheduling-context-capabilities.md) —
  makes CPU budgets capability-mediated, supports passive-server donation, and
  evaluates temporal-isolation costs.
- [Thunderclap](markettos-et-al-2019-thunderclap.md) — demonstrates why IOMMU
  remapping alone does not secure shared DMA protocols, transition windows,
  revocation, or reset.
- [Capability Myths Demolished](miller-et-al-2003-capability-myths.md) —
  distinguishes object capabilities from access-control lookalikes and
  analyzes designation, delegation, confinement, and revocation by indirection.
- [seL4: From General Purpose to a Proof of Information Flow Enforcement](murray-et-al-2013-sel4-information-flow.md) —
  connects configured capability flows to a machine-checked information-flow
  result and states its hardware, DMA, and timing assumptions.
- [Arrakis](peter-et-al-2014-arrakis.md) — separates a kernel control plane from
  delegated application I/O data paths and reports workload-specific latency
  and throughput gains.
- [For a Microkernel, a Big Lock Is Fine](peters-et-al-2015-big-lock-microkernel.md) —
  compares coarse, fine-grained, and transactional kernel synchronization and
  argues for measuring contention before accepting assurance complexity.
- [Simplifying Arm concurrency](pulte-et-al-2018-simplifying-arm-concurrency.md) —
  gives rigorous multicopy-atomic axiomatic and operational models for the
  relaxed Armv8 memory model.
- [The RISC-V privileged architecture](risc-v-international-2026-privileged-architecture.md) —
  records current ratified RISC-V privilege, trap, translation, ordering,
  instruction-fetch, counter, and extension-state semantics.
- [Design and Verification of Secure Systems](rushby-1981-design-verification-secure-systems.md) —
  develops a separation-kernel abstract machine and a verification argument
  for configured information-flow boundaries.
- [Efficient memory management for concurrent programs that use message passing](sagonas-wilhelmsson-2006-efficient-memory-management.md) —
  compares local, communal, and hybrid heaps and evaluates incremental
  collection trade-offs.
- [The Protection of Information in Computer Systems](saltzer-schroeder-1975-protection-information.md) —
  develops reference-monitor and least-privilege principles used to review the
  kernel's authority boundary.
- [seL4 Reference Manual, version 16.0.0](sel4-foundation-2026-reference-manual.md) —
  documents current capability spaces, explicit object memory, IPC,
  scheduling-context, fault, interrupt, virtual-memory, and boot mechanisms.
- [x86-TSO](sewell-et-al-2010-x86-tso.md) — supplies a rigorous usable model for
  x86 multiprocessor memory behavior and clearly bounds what that model does
  not cover.
- [Vulnerabilities in Synchronous IPC Designs](shapiro-2003-synchronous-ipc-vulnerabilities.md) —
  analyzes dependency, priority, resource-retention, and denial-of-service
  hazards in synchronous invocation designs.
- [EROS: A Fast Capability System](shapiro-et-al-1999-eros.md) — demonstrates a
  pure capability object system, fast invocation, and transparent persistence,
  with trade-offs for driver and recovery boundaries.
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
- [Improving the Reliability of Commodity Operating Systems](swift-et-al-2003-nooks.md) —
  evaluates wrapper-mediated isolation, typed resource tracking, and recovery
  for legacy in-kernel extensions while exposing its partial protection.
- [Recovering Device Drivers](swift-et-al-2004-recovering-device-drivers.md) —
  evaluates shadow drivers, request tracking, restart, and the indeterminate
  state left by device operations interrupted by failure.
- [Scaling Reliably](trinder-et-al-2017-scaling-reliably.md) — evaluates VM and
  distributed-actor scaling and shows the costs of global topology,
  namespaces, and recovery data.
- [Capsicum: Practical Capabilities for UNIX](watson-et-al-2010-capsicum.md) —
  demonstrates capability mode, rights-limited descriptors, and incremental
  application compartmentalization in a Unix kernel.
- [Characterizing the scalability of Erlang VM on many-core processors](zhang-2011-erlang-vm-many-core-scalability.md) —
  provides historical evidence about hidden runtime synchronization beneath a
  share-nothing programming model.
- [Concurrency in the Linux kernel](alglave-et-al-2018-linux-kernel-concurrency.md) —
  develops and tests the Linux Kernel Memory Model and supports keeping
  executable litmus tests beside architecture-ordering protocols.
- [Optimizing the TLB shootdown algorithm with page access tracking](amit-2017-optimizing-tlb-shootdown.md) —
  evaluates selective invalidation using observed page access and bounds the
  optimization behind a conservative acknowledged-shootdown baseline.
- [Arm CoreLink GICv3 and GICv4 software overview](arm-2019-gicv3-v4-software-overview.md) —
  documents flow-specific interrupt acknowledgement, priority, routing, EOI,
  deactivation, affinity, and virtualization behavior.
- [Caches and self-modifying code: Working with threads](bramley-2025-arm-self-modifying-code-threads.md) —
  gives current Arm engineering guidance for cross-thread instruction
  publication and motivates immutable code versions as the safe baseline.
- [Secure Virtual Architecture](criswell-et-al-2007-secure-virtual-architecture.md) —
  evaluates a typed low-level execution and privileged-operation interface for
  a minimally changed commodity kernel.
- [Devicetree specification, release 0.4](devicetree-org-2023-devicetree-specification-0-4.md) —
  defines the flattened device-tree handoff format, cells, nodes, properties,
  reservations, and version rules consumed by a bounded boot adapter.
- [Think](fassino-et-al-2002-think.md) — demonstrates strongly typed kernel
  components and explicit bindings, including separate hardware-abstraction
  components, without requiring one fixed kernel architecture.
- [Scalable and effective page-table and TLB management on NUMA systems](gao-et-al-2024-scalable-page-table-tlb.md) —
  evaluates page-table placement and shootdown approaches while supporting a
  stable mapping contract above replaceable optimization policy.
- [Kdump](goyal-et-al-2005-kdump.md) — prepares reserved memory, processor
  metadata, and an independent capture kernel before failure so bulk crash
  evidence need not depend on the failed kernel's ordinary services.
- [Spectre attacks](kocher-et-al-2019-spectre.md) — demonstrates speculative
  execution attacks that make entry and return mitigation a pinned machine
  profile rather than an assumed property of privilege checks.
- [The Limine boot protocol](limine-project-2026-limine-boot-protocol.md) —
  provides a current versioned loader protocol case and evidence for a narrow
  adapter into an owned normalized boot snapshot.
- [Linux reliability, availability, and serviceability documentation](linux-kernel-community-2026-ras-documentation.md) —
  distinguishes hardware-error origin, correction, severity, reporting, and
  containment while retaining raw source-specific evidence.
- [Meltdown](lipp-et-al-2018-meltdown.md) — demonstrates transient user access
  to privileged mappings on affected processors and motivates explicit
  entry/return mitigation and mapping profiles.
- [Serval](nelson-et-al-2019-serval.md) — evaluates scalable symbolic execution
  for systems code and supports making the unsafe primitive capsule a small,
  modelled, binary-checked unit.
- [BootStomp](redini-et-al-2017-bootstomp.md) — finds exploitable early-boot
  parsing flaws and supports treating privileged handoff parsing as hostile-
  input processing with strict bounds.
- [The RISC-V advanced interrupt architecture](risc-v-international-2023-advanced-interrupt-architecture.md) —
  documents IMSIC/APLIC interrupt identity, routing, priority, delivery, and
  completion mechanisms for a declared RISC-V event profile.
- [RISC-V platform-level interrupt controller specification](risc-v-international-2023-platform-level-interrupt-controller.md) —
  defines priority, enable, threshold, non-idempotent claim, and context-bound
  completion semantics for the legacy RISC-V PLIC flow.
- [RISC-V supervisor binary interface specification](risc-v-international-2025-supervisor-binary-interface.md) —
  defines firmware-mediated timer, IPI, remote-fence, and hart-lifecycle calls
  whose dependency and completion assumptions a backend must declare.
- [The RISC-V unprivileged architecture](risc-v-international-2026-unprivileged-architecture.md) —
  supplies normative ordinary-memory, I/O-ordering, instruction-fetch, atomic,
  and fence semantics below the architecture facade.
- [Translation validation for a verified OS kernel](sewell-et-al-2013-translation-validation.md) —
  validates generated kernel binary against source-level assumptions and shows
  why assembly and privileged-register code need more than source inspection.
- [Design of Tock kernel hardware interface layers](tock-project-2026-hil-design.md) —
  gives maintainer rules for typed split-phase interfaces, acceptance,
  completion, error, callback, virtualization, and buffer ownership.
- [Unified Extensible Firmware Interface specification, version 2.11](uefi-forum-2024-uefi-2-11.md) —
  defines boot-service lifetime, memory-map, system-table, image, and exit
  semantics needed by a UEFI handoff adapter.
- [Advanced Configuration and Power Interface specification, version 6.6](uefi-forum-2025-acpi-6-6.md) —
  defines static platform-description and error-record tables while exposing
  the complexity and trust cost of early AML evaluation.
- [When poll is better than interrupt](yang-et-al-2012-when-poll-is-better-than-interrupt.md) —
  evaluates adaptive polling for high-rate devices and motivates a funded,
  capability-controlled polling lease rather than an automatic interrupt
  fast-path policy.
- [Arm Power State Coordination Interface, version 1.3](arm-2024-power-state-coordination-interface.md) —
  defines firmware-mediated CPU start, suspend, and off operations that must
  remain fallible steps inside a richer logical-CPU lifecycle transaction.
- [Arm SMMUv3 architecture specification](arm-2025-smmuv3-architecture.md) —
  defines stream/requester attachment, translation, command queues, faults,
  invalidation, and completion needed by the Arm protected-DMA backend.
- [Intel VT-d architecture specification](intel-2024-vt-d-architecture.md) —
  defines requester remapping, queued invalidation, interrupt remapping, faults,
  and completion rules needed by the x86-64 protected-I/O backend.
- [Timecounters](kamp-2002-timecounters.md) — develops an efficient SMP
  timecounter model using counter masks and generation-published conversion
  state while keeping raw counting separate from time policy.
- [RISC-V IOMMU architecture specification](risc-v-international-2026-iommu-architecture.md) —
  defines device contexts, translation, fault records, invalidation, and
  `IOFENCE.C` completion for a RISC-V DMA-domain backend.
- [Efficient design of high-resolution timekeeping in real-time operating systems](terraneo-cattaneo-2026-high-resolution-timekeeping.md) —
  evaluates high-resolution timekeeping with a globally qualified counter and
  CPU-local deadlines while exposing scheduler- and hardware-specific limits.

## Maintaining this index

Index every direct source note with a concise description. Preserve exact
metadata where available, never invent unknown fields, and link derived work.
