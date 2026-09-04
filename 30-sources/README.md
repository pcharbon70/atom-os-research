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

## Research provenance

The topic maps show which research stream a source supports. The dated
deep-dive journals are the authoritative session-level provenance records:
each has an exhaustive `## Source manifest` that separates source notes first
introduced in that session from pre-existing source notes reused by it. A
source may appear in several maps and several journal manifests without being
duplicated in this directory.

The table below is the exhaustive navigation list of current deep-dive
journals. A source note's `## Derived work` remains a selective route to
important outputs; it is not the provenance ledger and need not duplicate
every journal-manifest backlink.

| Research stream | Curated map | Exact deep-dive session manifests |
| --- | --- | --- |
| AtomVM foundation | [AtomVM foundation](../10-maps/atomvm-foundation.md) | [2026-08-28 AtomVM deep dive](../50-journal/2026-08-28-atomvm-deep-dive.md) |
| BEAM, ERTS, and OTP | [BEAM, ERTS, and OTP](../10-maps/beam-erts-and-otp.md) | [2026-08-28 BEAM, ERTS, and OTP deep dive](../50-journal/2026-08-28-beam-erts-and-otp-deep-dive.md) |
| Kernel hardware and architecture | [Kernel hardware and architecture support](../10-maps/kernel-hardware-and-architecture-support.md) | [2026-08-30 layer deep dive](../50-journal/2026-08-30-kernel-hardware-and-architecture-support-deep-dive.md); [2026-09-02 component deep dive](../50-journal/2026-09-02-kernel-architecture-components-deep-dive.md) |
| Minimal privileged kernel | [Minimal privileged kernel](../10-maps/minimal-privileged-kernel.md) | [2026-08-31 layer deep dive](../50-journal/2026-08-31-minimal-privileged-kernel-deep-dive.md); [2026-09-03 component deep dive](../50-journal/2026-09-03-minimal-privileged-kernel-components-deep-dive.md) |
| Managed actor runtime | [Managed actor runtime](../10-maps/managed-actor-runtime.md) | [2026-09-02 layer deep dive](../50-journal/2026-09-02-managed-actor-runtime-deep-dive.md); [2026-09-03 component deep dive](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md) |
| OTP-like system services | [OTP-like system services](../10-maps/otp-like-system-services.md) | [2026-09-03 system-services deep dive](../50-journal/2026-09-03-otp-like-system-services-deep-dive.md); [2026-09-04 component deep dive](../50-journal/2026-09-04-otp-like-system-services-components-deep-dive.md) |
| Authentication and authorization | [Authentication and authorization](../10-maps/authentication-and-authorization.md) | [2026-09-04 deep dive](../50-journal/2026-09-04-authentication-and-authorization-deep-dive.md); [2026-09-04 component deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md) |

### Sources introduced outside a deep-dive session

Twelve hardware-architecture foundation notes first entered the archive in Git
change `af7d686` before the dated kernel-layer deep-dive journal was written.
They are therefore honestly classified as reused by the 2026-08-30 deep dive,
not retroactively labeled as introduced by it:

- [A least-privilege memory protection model for modern hardware](achermann-et-al-2019-least-privilege-memory-protection.md)
- [Arm A-profile system architecture documentation](arm-2026-a-profile-system-architecture-documentation.md)
- [The Multikernel](baumann-et-al-2009-multikernel.md)
- [CleanQ](haecki-et-al-2019-cleanq.md)
- [Intel system-programming documentation](intel-2026-system-programming-documentation.md)
- [Comprehensive formal verification of an OS microkernel](klein-et-al-2014-comprehensive-sel4-verification.md)
- [Thunderclap](markettos-et-al-2019-thunderclap.md)
- [Arrakis](peter-et-al-2014-arrakis.md)
- [RISC-V privileged architecture](risc-v-international-2026-privileged-architecture.md)
- [x86-TSO](sewell-et-al-2010-x86-tso.md)
- [Relaxed virtual memory in Armv8-A](simner-et-al-2022-relaxed-virtual-memory.md)
- [LazyFP](stecklina-prescher-2018-lazyfp.md)

## Index

### Subdirectories

- None yet.

### Documents

- [A least-privilege memory protection model for modern hardware](achermann-et-al-2019-least-privilege-memory-protection.md) —
  separates authority to configure address translation from authority to
  access the translated memory across CPUs and devices.
- [A scalability benchmark suite for Erlang/OTP](aronis-et-al-2012-scalability-benchmark-suite-erlang-otp.md) —
  defines multidimensional Erlang scalability measurement across resources and
  workloads instead of relying on one throughput point.
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
- [Work-Stealing, Locality-Aware Actor Scheduling](barghi-karsten-2018-locality-aware-actor-scheduling.md) —
  compares actor work-stealing policies on NUMA machines and shows both the
  gains and tail-latency risks of locality and affinity mechanisms.
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
- [Formally verified system initialisation](boyton-et-al-2013-verified-system-initialisation.md) —
  proves a model-level connection from a declarative capDL configuration to
  the state reached by an automatic seL4 system initialiser while preserving
  its implementation boundary.
- [Functional Programming for the Internet of Things](branch-weinstock-2024-functional-programming-iot.md) —
  summarizes a 2024 AtomVM/Elixir versus C++ LoRa–MQTT gateway comparison and
  its reproducibility limits.
- [Microreboot—A Technique for Cheap Recovery](candea-et-al-2004-microreboot.md) —
  evaluates fine-grained component restart and makes state placement,
  dependency, retry, and application-visible recovery costs explicit.
- [Dynamic instrumentation of production systems](cantrill-et-al-2004-dtrace.md) —
  develops DTrace's typed dynamic probes, safe execution, per-consumer state,
  aggregation, and disabled-probe discipline while exposing its larger trust
  and timing surface.
- [Unreliable Failure Detectors for Reliable Distributed Systems](chandra-toueg-1996-failure-detectors.md) —
  formalizes the distinction between crash fact and liveness suspicion under
  timing assumptions.
- [Finding Race Conditions in Erlang with QuickCheck and PULSE](claessen-et-al-2009-quickcheck-pulse.md) —
  combines property generation, controlled scheduling, shrinking, and trace
  visualization to reproduce Erlang concurrency faults.
- [Orca: GC and Type System Co-Design for Actor Languages](clebsch-et-al-2017-orca.md) —
  demonstrates concurrent actor collection and zero-copy sharing under Pony’s
  stronger reference-capability assumptions.
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
  records the process, signal, scheduler, memory, code-loading, supervision,
  release, distribution, and security baseline aligned with the pinned 29.0.5
  source audit.
- [Erlang/OTP 29.0.6 managed-runtime documentation](erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md) —
  records the current compatibility, actor, signal, scheduler, collection,
  code, timer, table, tracing, port, and native-extension behavior.
- [Erlang/OTP source tree at 5cf5f9725452](erlang-otp-team-2026-otp-29-source-tree.md) —
  pins and audits OTP 29.0.5/ERTS 17.0.5 internals, constants, code
  publication, native boundaries, and host-OS dependencies.
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
- [A few notes on message passing](hogberg-2021-message-passing.md) — explains
  per-sender signal order, message copying, signal/message queue separation,
  and the cost and optimization limits of selective receive.
- [Intel 64 and IA-32 system programming documentation](intel-2026-system-programming-documentation.md) —
  records current x86 privilege, entry, translation, interrupt, time,
  extended-state, and optional virtualization mechanisms.
- [Comprehensive formal verification of an OS microkernel](klein-et-al-2014-comprehensive-sel4-verification.md) —
  connects explicit capabilities and objects to a small verified TCB and makes
  hardware, boot, assembly, cache, device, DMA, and timing assumptions visible.
- [capDL: A language for describing capability-based systems](kuz-et-al-2010-capdl.md) —
  makes kernel objects and capability distributions explicit data so an
  installed authority graph can be connected to isolation and information-flow
  reasoning.
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
- [Read-copy update](mckenney-slingwine-1998-read-copy-update.md) — separates
  removal from reclamation and uses observed execution quiescence to defer
  reuse until pre-existing software readers have completed.
- [Hazard pointers](michael-2004-hazard-pointers.md) — provides bounded explicit
  reference publication for safe lock-free node reclamation while leaving CPU,
  translation, interrupt, and device quiescence outside its scope.
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
- [Lockless ring buffer design](rostedt-2009-lockless-ring-buffer-design.md) —
  specifies Linux tracing's per-CPU page ring, nested-writer commit order,
  reader exchange, and explicit overwrite versus producer/consumer modes.
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
- [The Many-to-One Parallel Signal Sending Optimization](winblad-2021-parallel-signal-sending.md) —
  explains adaptive sender-striped ingress and bounds its extreme
  many-to-one microbenchmark result.
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
- [Proof-carrying code](necula-1997-proof-carrying-code.md) — develops
  producer-supplied safety proofs checked by a small consumer and exposes the
  proof-policy and toolchain obligations behind that trust reduction.
- [Simple, fast, and practical concurrent queue algorithms](michael-scott-1996-concurrent-queue-algorithms.md) —
  supplies linearizable blocking and non-blocking queue algorithms while
  leaving actor-level ordering, reclamation, wakeup, and overload unspecified.
- [Scheduling multithreaded computations by work stealing](blumofe-leiserson-1999-work-stealing.md) —
  proves work-stealing bounds for fully strict computations and makes clear why
  those bounds do not transfer directly to long-lived communicating actors.
- [Hashed and hierarchical timing wheels: Data structures for the efficient implementation of a timer facility](varghese-lauck-1987-timing-wheels.md) —
  develops efficient bounded-range and extended timer structures while
  exposing granularity, cascade, bucket-burst, and cancellation trade-offs.
- [HiPErJiT](kallas-sagonas-2018-hiperjit.md) — evaluates a profile-driven
  tracing JIT for Erlang and records warmup, compilation, code-size, and
  workload-dependence limits relevant to an interpreter-first runtime.
- [Resource containers](banga-et-al-1999-resource-containers.md) — separates
  resource principals from execution threads and supports causal attribution
  across asynchronous server work.
- [A contention adapting approach to concurrent ordered sets](sagonas-winblad-2018-contention-adapting-ordered-sets.md) —
  adapts ordered-set structure to measured contention and supplies one
  workload-sensitive candidate for ETS-like tables.
- [Systematic testing for detecting concurrency errors in Erlang programs](christakis-et-al-2013-concuerror.md) —
  explores Erlang process schedules to reproduce concurrency errors while
  documenting the supported-runtime boundary of systematic exploration.
- [Efficient and deterministic record and replay for actor languages](aumayr-et-al-2018-actor-record-replay.md) —
  records actor-level nondeterministic ordering rather than every instruction
  and motivates a separate deterministic runtime test profile.
- [Orleans](bernstein-et-al-2014-orleans.md) — develops distributed virtual
  actors with platform-managed activation and stable logical identity, a useful
  service-layer contrast to incarnation-specific BEAM PIDs.
- [Crash-only software](candea-fox-2003-crash-only-software.md) — argues for
  externally coordinated component restart and state separation while making
  retry safety and durable-state assumptions explicit.
- [A NUMA-aware runtime environment for the actor model](francesquini-et-al-2013-numa-aware-actor-runtime.md) —
  evaluates topology-aware actor placement and hierarchical work stealing and
  bounds its conclusions to the measured VM, machines, and workloads.
- [PARTISAN](meiklejohn-et-al-2019-partisan.md) — evaluates replaceable
  distributed-actor topologies, parallel channels, and channel affinity instead
  of treating one full mesh as actor semantics.
- [Special delivery: Programming with mailbox types](fowler-et-al-2023-mailbox-types.md) —
  develops static mailbox protocols that prevent classes of actor mismatch and
  deadlock, supporting an optional typed profile rather than a BEAM baseline.
- [On the scalability of the Erlang Term Storage](klaftenegger-et-al-2013-ets-scalability.md) —
  measures ETS contention and concurrency options and motivates explicit,
  workload-sensitive shared-table implementations.
- [Implementing remote procedure calls](birrell-nelson-1984-remote-procedure-calls.md) —
  develops request identifiers, retransmission, acknowledgements, and duplicate
  suppression while preserving the ambiguity of failures after remote effects.
- [A high performance Erlang system](johansson-et-al-2000-high-performance-erlang.md) —
  integrates native Erlang compilation with runtime stacks, roots, garbage
  collection, exceptions, and services, exposing conventions a safe-point-aware
  execution engine must preserve.
- [The Chubby lock service for loosely-coupled distributed systems](burrows-2006-chubby.md) —
  develops a coarse-grained coordination
  service with sessions, leases, cache invalidation, and sequencer values while
  preserving quorum and non-Byzantine limits.
- [SWIM](das-et-al-2002-swim.md) — separates scalable probing from
  dissemination and uses suspicion and incarnations for weakly consistent
  membership without turning observations into authoritative truth.
- [NixOS: A Purely Functional Linux Distribution](dolstra-et-al-2008-nixos.md) —
  applies immutable,
  derivation/input-identified dependency closures and atomic profile selection to
  system configuration while exposing mutable activation limits.
- [Erlang/OTP 29.0.6 system-services documentation](erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md) —
  records current behaviour, supervision, application, release, distribution,
  registry, configuration, and Logger semantics and limits.
- [Erlang/OTP 24 Highlights](larsson-2021-erlang-otp-24-highlights.md) — explains
  the process-alias reply path and the deadlock-avoidance motivation for
  significant children and supervisor automatic shutdown.
- [Erlang/OTP 28 Highlights](huang-2025-erlang-otp-28-highlights.md) — uses
  Logger mailbox overload to motivate receiver-authorized priority messages
  while leaving admission, fairness, and resource bounds unspecified.
- [Sagas](garcia-molina-salem-1987-sagas.md) — decomposes long-lived
  transactions into committed subtransactions and application-defined
  compensations without promising global rollback.
- [Implementing linearizability at large scale and low latency](lee-et-al-2015-rifl.md) —
  develops RIFL's durable request-result and
  retry-rendezvous conditions for a restricted exactly-once RPC profile.
- [ARIES](mohan-et-al-1992-aries.md) — develops analysis, repeat-history redo,
  logical undo, compensation log records, and fuzzy checkpoints over
  write-ahead logging.
- [Practical dynamic software updating for C](neamtiu-et-al-2006-practical-dynamic-software-updating.md) —
  evaluates
  Ginseng safe update points, type transformation, and state migration while
  exposing its single-program assumptions.
- [In search of an understandable consensus algorithm](ongaro-ousterhout-2014-raft.md) —
  decomposes crash-fault consensus
  into leader election, log replication, safety, and membership change with
  majority-availability assumptions.
- [Survivable key compromise in software update systems](samuel-et-al-2010-tuf.md) —
  develops role-separated update metadata,
  threshold trust, freshness, and repository consistency under partial key
  compromise.
- [Secure audit logs to support computer forensics](schneier-kelsey-1999-secure-audit-logs.md) —
  develops
  forward-integrity protections for logs written by a machine that may later
  be compromised while retaining availability and deletion limits.
- [Dapper](sigelman-et-al-2010-dapper.md) — describes low-overhead distributed
  context propagation, sampling, collection, and analysis and why traces are
  not a complete audit history.
- [The SPIFFE Workload API](spiffe-project-2026-workload-api.md) — specifies
  local delivery and rotation of workload identities, keys, and trust bundles
  while leaving authorization and platform attestation to other policy.
- [Large-scale cluster management at Google with Borg](verma-et-al-2015-borg.md) —
  reports desired-state reconciliation,
  controller/agent separation, resource policy, and operational introspection
  at datacenter scale.
- [SEDA](welsh-et-al-2001-seda.md) — evaluates explicit stages, finite queues,
  admission control, and adaptive resource controllers while documenting queue
  and isolation trade-offs.
- [Overload control for scaling WeChat microservices](zhou-et-al-2018-dagor.md) —
  evaluates queue-delay detection,
  early rejection, and propagated admission state across a service call graph.
- [Computer security technology planning study](anderson-1972-computer-security-technology-planning-study.md) —
  develops the reference-monitor and security-kernel requirements of complete
  mediation, tamper resistance, and analyzability while exposing assurance
  assumptions outside the mechanism.
- [Protection](lampson-1971-protection.md) — models subjects, objects, domains,
  rights, and access matrices and separates protection mechanism from policy.
- [The confused deputy](hardy-1988-confused-deputy.md) — shows how ambient
  authority lets an authorized program misuse its privilege for a less-
  privileged caller and motivates designation coupled to authority.
- [Protection in operating systems](harrison-et-al-1976-protection-in-operating-systems.md) —
  proves general safety undecidable for an unrestricted access-control model,
  motivating a deliberately constrained authority algebra.
- [The KeyKOS architecture](hardy-1990-keykos-architecture.md) — describes a
  pure capability system whose protected keys combine object designation and
  authority without a global privileged identity.
- [Digital identity guidelines: Authentication and authenticator management](temoshok-et-al-2025-authentication-and-authenticator-management.md) —
  records current NIST authentication assurance, phishing-resistance,
  authenticator lifecycle, binding, recovery, and notification requirements.
- [Web Authentication: An API for accessing public key credentials — Level 3](w3c-2026-webauthn-level-3.md) —
  specifies the current W3C public-key credential ceremony, relying-party and
  origin bindings, user presence/verification signals, and authenticator data.
- [Client to Authenticator Protocol 2.2](fido-alliance-2025-ctap-2-2.md) —
  specifies authenticator transport, PIN/user-verification, credential
  management, and authenticator behavior below a FIDO client.
- [A formal analysis of the FIDO2 protocols](guan-et-al-2022-formal-analysis-fido2.md) —
  analyzes WebAuthn and CTAP composition and exposes parallel-session and
  state-sharing risks that subsystem-only arguments can miss.
- [Operating System Framed](bravo-lillo-et-al-2012-operating-system-framed.md) —
  empirically evaluates OS-framed credential prompts and shows that strong
  visual security treatments do not eliminate spoofing.
- [A Nitpicker's guide to a minimal-complexity secure GUI](feske-helmuth-2005-nitpicker.md) —
  develops a small secure-GUI service with protected input, focus, display,
  and trusted labeling boundaries.
- [The abusability of passkeys](daffalla-et-al-2025-passkey-abusability.md) —
  studies passkey enrollment, sharing, synchronization, and recovery abuse and
  broadens evaluation beyond the assertion protocol.
- [Zero trust architecture](rose-et-al-2020-zero-trust-architecture.md) —
  separates policy decision, administration, and enforcement and rejects
  network location as an implicit trust signal.
- [Remote ATtestation procedureS architecture](birkholz-et-al-2023-rats-architecture.md) —
  defines attester, verifier, relying-party, endorsement, reference-value, and
  appraisal-policy roles while keeping attestation distinct from authorization.
- [The Entity Attestation Token](lundblade-et-al-2025-entity-attestation-token.md) —
  specifies a claims container for attestation results and evidence without
  making those claims a resource-permission decision.
- [TPM 2.0 Library Specification, version 185](trusted-computing-group-2026-tpm-2-0-library.md) —
  provides the current full hardware profile for protected keys, measured
  state, authorization sessions, sealing, and platform attestation.
- [Hardware requirements for a Device Identifier Composition Engine](trusted-computing-group-2024-dice-hardware-requirements.md) —
  provides a constrained-device hardware root and compound identity profile
  for measured, layered key derivation.
- [Macaroons: Cookies with contextual caveats for decentralized authorization in the cloud](birgisson-et-al-2014-macaroons.md) —
  develops monotonic caveat-based attenuation and third-party discharge
  patterns while retaining important bearer, revocation, and verifier-key
  limitations.
- [Zanzibar: Google's consistent, global authorization system](pang-et-al-2019-zanzibar.md) —
  develops relationship-based authorization with causal consistency tokens and
  exposes the distributed new-enemy problem.
- [Cedar: A new language for expressive, fast, safe, and analyzable authorization](cutler-et-al-2024-cedar.md) —
  develops a typed policy language over principals, actions, resources,
  context, roles, groups, and relationships with explicit forbid semantics.
- [Verification-guided development of Cedar authorization](disselkoen-et-al-2024-verification-guided-cedar.md) —
  combines mechanized policy properties with differential randomized testing
  of production authorization implementations.
- [Best current practice for OAuth 2.0 security](lodderstedt-et-al-2025-oauth-security-bcp.md) —
  consolidates current OAuth attack mitigations, deprecates unsafe grants, and
  requires precise redirect, audience, PKCE, and sender-constraint profiles.
- [OAuth 2.0 Demonstrating Proof of Possession](fett-et-al-2023-dpop.md) —
  sender-constrains application-layer tokens while documenting replay,
  endpoint, and request-body limits that stronger Atom profiles must address.
- [Verified security for the Morello capability-enhanced prototype Arm architecture](bauereiss-et-al-2022-verified-morello-security.md) —
  proves selected architectural security properties for a formal Morello
  model and carefully bounds what hardware-capability evidence can transfer.
- [Exponential backoff and jitter](brooker-2015-exponential-backoff-jitter.md) —
  explains how capped randomized retry schedules reduce synchronized
  contention while preserving their workload-specific limitations.
- [The Erlang start phase](burcsi-et-al-2010-erlang-start-phase.md) — analyzes
  dependency-aware parallel startup and records the benchmark and compatibility
  limits of the proposed Erlang wrapper.
- [FSCQ](chen-et-al-2015-fscq.md) — connects crash specifications,
  write-ahead logging, recovery, and machine-checked filesystem behavior while
  preserving the proof's storage-model boundary.
- [etcd API guarantees](etcd-project-2026-api-guarantees.md) — records
  revisioned updates, consistency classes, ordered watches, compaction, and
  explicit resynchronization behavior.
- [xDS REST and gRPC protocol](envoy-project-2026-xds-protocol.md) — records
  versioned configuration delivery, ACK/NACK semantics, reconnection, and the
  distinction between validation and actual activation.
- [Leases](gray-cheriton-1989-leases.md) — derives time-bounded cache validity
  tradeoffs and exposes the timing assumptions that constrain lease safety.
- [Vault secrets, leases, and security model](hashicorp-2026-vault-secrets-and-leases.md) —
  records dynamic credential lifetime, renewal, revocation lineage, key
  rotation, and product threat-model limits.
- [sDDF design](heiser-et-al-2026-sddf-design.md) — specifies isolated driver
  and virtualizer components, bounded ownership queues, selective shared
  memory, and IOMMU-backed DMA containment.
- [Gray failure](huang-et-al-2017-gray-failure.md) — characterizes partial and
  perspective-dependent failures that evade binary health detection in
  cloud-scale systems.
- [QUIC](iyengar-thomson-2021-quic.md) — specifies secure multiplexed
  transport, connection and stream flow control, path migration, and 0-RTT
  replay limits without claiming application commit.
- [A global name service for a highly decentralized system](lampson-1986-global-name-service.md) —
  distinguishes stable names from changing locations and analyzes caching,
  hierarchy, and failure in decentralized naming.
- [TOSCA 2.0](oasis-2025-tosca-2.md) — defines a current typed service-model
  representation and orchestration vocabulary while leaving implementation
  and rollback behavior non-prescriptive.
- [OpenTelemetry specification 1.60](opentelemetry-project-2026-specification-1-60.md) —
  records the current traces, metrics, logs, context, sampling, limits, and
  exporter contract as interoperability evidence.
- [End-to-end arguments in system design](saltzer-et-al-1984-end-to-end-arguments.md) —
  explains why lower-layer delivery and checks cannot replace correctness
  checks at the application's actual boundary.
- [Omega](schwarzkopf-et-al-2013-omega.md) — evaluates shared-state,
  optimistic, version-checked scheduling by specialized cluster controllers.
- [Anvil](sun-et-al-2024-anvil.md) — verifies eventually stable reconciliation
  for generated controllers and makes liveness assumptions and wrapper trust
  explicit.
- [Android Protected Confirmation](android-project-2026-protected-confirmation.md) —
  documents a TEE-backed trusted user-confirmation path whose token is
  cryptographically authenticated and bound to the displayed message.
- [Recommendation for key management: Part 1 – General](barker-2020-key-management.md) —
  defines cryptographic-key lifecycle states, protection requirements,
  compromise handling, destruction, accountability, and metadata.
- [RATS Conceptual Message Wrapper](birkholz-et-al-2026-rats-conceptual-message-wrapper.md) —
  defines typed wrappers for attestation evidence, appraisal policy,
  endorsements, reference values, and attestation results.
- [Argon2 memory-hard function for password hashing](biryukov-et-al-2021-argon2.md) —
  specifies the Argon2 password-hashing construction, parameter choices, and
  memory-hardness tradeoffs for a confined compatibility verifier.
- [Secrets, lies, and account recovery](bonneau-et-al-2015-secrets-lies-account-recovery.md) —
  empirically studies account-recovery mechanisms and exposes recovery as a
  distinct, frequently weaker authentication system.
- [OAuth 2.0 mutual-TLS client authentication and certificate-bound access tokens](campbell-et-al-2020-oauth-mutual-tls.md) —
  specifies mutual-TLS client authentication and proof-of-possession binding
  for externally federated OAuth tokens.
- [Efficient data structures for tamper-evident logging](crosby-wallach-2009-tamper-evident-logging.md) —
  develops authenticated append-only data structures and efficient proofs for
  tamper-evident audit histories.
- [The Web SSO standard OpenID Connect](fett-et-al-2017-openid-connect-security.md) —
  gives a formal security analysis of OpenID Connect and identifies protocol-
  composition and deployment conditions needed for its guarantees.
- [FIDO Metadata Service](fido-alliance-2026-metadata-service.md) —
  specifies signed authenticator metadata, certification and status records,
  and relying-party processing for credential inventory and risk decisions.
- [Guide to attribute based access control definition and considerations](hu-et-al-2014-attribute-based-access-control.md) —
  defines ABAC actors, attributes, policies, environmental inputs, and the
  governance concerns behind authoritative attribute services.
- [Security Event Token](hunt-et-al-2018-security-event-token.md) —
  specifies an interoperable signed security-event envelope plus event and
  ordering semantics, while leaving delivery reliability to profiles.
- [OAuth 2.0 token exchange](jones-et-al-2020-oauth-token-exchange.md) —
  specifies explicit subject-token, actor-token, audience, resource, and scope
  semantics for bounded external delegation and impersonation.
- [Signed syslog messages](kelsey-et-al-2010-signed-syslog-messages.md) —
  specifies cryptographic signatures, certificate blocks, replay protection,
  and loss detection for syslog event streams.
- [Guide to computer security log management](kent-souppaya-2006-log-management.md) —
  treats log generation, transport, storage, analysis, retention, and incident
  response as an operational lifecycle with capacity and availability limits.
- [Certificate Transparency version 2.0](laurie-et-al-2021-certificate-transparency-v2.md) —
  specifies Merkle-tree commitments and consistency and inclusion proofs for
  independently witnessed append-only logs.
- [OAuth 2.0 token revocation](lodderstedt-et-al-2013-oauth-token-revocation.md) —
  specifies a revocation endpoint while making propagation delay, validation
  behavior, and short-lived-token limitations explicit.
- [A firmware update architecture for Internet of Things](moran-et-al-2021-firmware-update-architecture.md) —
  separates update authorship, distribution, manifest processing, installation,
  trust anchors, and anti-rollback responsibilities.
- [A manifest information model for firmware updates in IoT devices](moran-et-al-2022-firmware-manifest-information-model.md) —
  defines typed firmware applicability, dependency, storage, sequencing,
  cryptographic, and installation metadata.
- [eXtensible Access Control Markup Language version 3.0 plus Errata 01](oasis-2017-xacml-3-0.md) —
  specifies policy decision, administration, information, and enforcement
  roles plus obligations, combining algorithms, and indeterminate outcomes.
- [PKCS #11 Cryptographic Token Interface Usage Guide version 3.2](oasis-2025-pkcs11-usage-guide-3-2.md) —
  records practical token, session, login, object, concurrency, and recovery
  behavior that constrains a safe cryptographic-service wrapper.
- [PKCS #11 Specification version 3.2](oasis-2026-pkcs11-3-2.md) —
  defines cryptographic-token objects, mechanisms, sessions, authentication,
  operation state, and error contracts.
- [Platform firmware resiliency guidelines](regenscheid-2018-platform-firmware-resiliency.md) —
  defines protection, detection, and recovery roots for resisting unauthorized
  firmware changes and restoring known-good platform state.
- [OAuth 2.0 token introspection](richer-2015-oauth-token-introspection.md) —
  specifies authenticated active-state queries for externally issued tokens
  and clarifies the freshness-versus-availability tradeoff.
- [The NIST model for role-based access control](sandhu-et-al-2000-nist-rbac-model.md) —
  unifies flat, hierarchical, constrained, and symmetric RBAC and formalizes
  sessions and separation-of-duty constraints.
- [JSON Web Token best current practices](sheffer-et-al-2020-jwt-best-practices.md) —
  catalogues algorithm, key, issuer, audience, substitution, replay, and cross-
  JWT confusion hazards for any confined token parser.
- [SPIFFE Federation](spiffe-project-2026-federation.md) —
  documents explicit trust-domain bundle exchange and name authentication while
  leaving local workload authorization to relying parties.
- [The X.509 SPIFFE Verifiable Identity Document](spiffe-project-2026-x509-svid.md) —
  defines exact SPIFFE URI identity, leaf/signing-certificate, key-usage,
  path-validation, and bundle constraints for X.509-SVIDs.
- [in-toto: Providing farm-to-table guarantees for bits and bytes](torres-arias-et-al-2019-in-toto.md) —
  binds software-supply-chain steps, actors, materials, products, and layout
  policy into verifiable provenance metadata.
- [The Update Framework Specification version 1.0.36](tuf-project-2026-specification-1-0-36.md) —
  defines role-separated signed metadata, thresholds, delegation, expiration,
  consistent snapshots, and rollback and freeze resistance.
- [Uptane Standard for Design and Implementation version 2.1.0](uptane-community-2023-standard-2-1-0.md) —
  extends role-separated update metadata with vehicle-specific inventory,
  assignment, installation reporting, and compromise-resilient recovery.
- [User interaction design for secure systems](yee-2002-user-interaction-design-secure-systems.md) —
  derives trusted-path and authorization-interface principles from the limits
  of user attention, distinguishability, and untrusted application surfaces.

## Maintaining this index

Index every direct source note with a concise description. Preserve exact
metadata where available, never invent unknown fields, and link derived work.
Do not duplicate or move a source note to represent reuse: classify it in each
deep-dive journal manifest and route it through every conceptually relevant
map instead.
