---
title: "2026-08-29 hardware and architecture support deep dive"
kind: journal
created: "2026-08-29"
tags:
  - aarch64
  - hardware-architecture
  - literature-search
  - qemu
  - research-session
  - risc-v
  - source-audit
  - zig
aliases:
  - "Hardware architecture literature and specification audit"
---

# 2026-08-29 hardware and architecture support deep dive

## Observations

- “Hardware support” is too broad to be one module. The research repeatedly
  resolves into reset and firmware, privilege and traps, discovery, memory
  authority, interrupts, time, CPU lifecycle and ordering, cache/code
  publication, extended state, DMA, device resources, power, and security/debug
  evidence.
- The portable boundary is semantic rather than register-level. Firmware
  descriptions can become one immutable resource graph; device access can
  become typed resource bundles; CPU, mapping, interrupt, timer, DMA, and power
  operations can become explicit state machines. The instruction sequences that
  realize ordering, cache maintenance, TLB invalidation, and interrupt control
  remain architecture-specific.
- An emulator-only first step is valuable for deterministic bring-up but cannot
  validate all cache-coherence, DMA, firmware, reset, power, timing, or device
  failure claims. The documents therefore distinguish an emulator contract
  test from physical-hardware evidence.
- A single “simple” first profile would postpone the most important security
  interaction: a driver domain, interrupt route, queue, DMA buffers, and IOMMU
  context must be assigned and revoked together. The proposed R0/R1 split keeps
  console boot small while making protected DMA a planned second milestone.
- RISC-V is attractive for first bring-up because the selected supervisor
  interfaces are relatively regular and visible. Its modular extension and
  evolving platform ecosystem are costs, not automatic simplicity.
- AArch64 is a useful second architecture because its exception levels, weak
  memory model, GIC, cache maintenance, PSCI, and SMMU expose different hidden
  assumptions. x86-64 remains important, but its compatibility surface is not
  necessary for the first cross-ISA test.
- Hardware presence is not a security property. Thunderclap shows that an IOMMU
  may exist without enforcing least privilege; LazyFP shows that extended-state
  optimizations can leak across domains; firmware resiliency guidance separates
  protection, detection, and recovery.
- No local boot, hardware measurement, or fault-injection experiment was
  performed during this session. All proposed target choices remain a synthesis
  to be tested.

## Environment

Read-only host inspection on 2026-08-29 reported:

```text
Host kernel: Linux 6.8.0-51-generic x86_64
Python: 3.12.12
Git: 2.49.0
Branch: research/beam-otp-deep-dive
curl: 8.5.0
pdftotext: 24.02.0
```

The host `PATH` exposes an asdf Zig shim, but the repository has no
`.tool-versions` file and no Zig version was selected for the shell. The shim
reported these available candidates:

```text
No version is set for command zig
Consider adding one of the following versions in your config file ...
zig 0.16.0
zig 0.15.2
```

None of the required emulators was installed in the active environment:

```text
qemu-system-riscv64: not installed
qemu-system-aarch64: not installed
qemu-system-x86_64: not installed
```

No OpenSBI image, UEFI firmware image, cross compiler, JTAG probe, logic
analyzer, physical target, IOMMU-capable test device, power instrument, or
fault-injection harness was used. Those absences prevent this entry from
making boot, conformance, latency, or isolation claims.

## Evidence

### Research question and acceptance standard

The session asked:

> Which responsibilities belong in the hardware and architecture support
> layer of a Zig kernel informed by BEAM and OTP principles, how should they be
> decomposed, which architecture choices expose the right trade-offs, and what
> evidence would justify the first targets?

The standard for retaining a design claim was one of:

1. a normative architecture or platform specification defined the mechanism;
2. an official implementation document defined the emulator or firmware
   boundary;
3. a complete scientific paper supplied a model, implementation, experiment,
   or demonstrated failure; or
4. the synthesis explicitly labelled a project proposal or inference and
   supplied a falsification experiment.

Search-result snippets were used only to locate sources. Community summaries,
forum comments, vendor marketing, and unsourced architecture tutorials were
not used as proof. No benchmark result from a historical paper was projected
onto the proposed kernel.

### Specification search and revision choices

The official sources were checked at their canonical pages on 2026-08-29. The
source notes record metadata, claims, and limitations separately:

- [UEFI Specification 2.11](../30-sources/uefi-forum-2024-uefi-2-11.md),
  published December 2024, for boot and runtime services, memory-map handoff,
  configuration tables, and authenticated boot.
- [ACPI Specification 6.6](../30-sources/uefi-forum-2025-acpi-6-6.md),
  published May 2025, for discovery, topology, interrupts, timers, power, and
  platform configuration.
- [Devicetree Specification
  0.4](../30-sources/devicetree-org-2023-devicetree-0-4.md), released
  2023-06-28, for the flattened tree, node and property conventions, address
  translation, reservations, CPU description, and boot interface.
- [RISC-V privileged and unprivileged architecture
  specifications](../30-sources/risc-v-international-2026-privileged-architecture.md),
  current documentation release 20260120, for privilege, traps, Sv39, PMP,
  counters, fences, extension discovery, and RVWMO.
- [RISC-V SBI 3.0](../30-sources/risc-v-international-2025-sbi-3-0.md), ratified
  in 2025, for the provisional supervisor-to-firmware boundary.
- [RISC-V AIA 1.0](../30-sources/risc-v-international-2023-advanced-interrupt-architecture.md),
  ratified in 2023 with the 20250312 clarification, for APLIC, IMSIC, MSI, and
  per-hart interrupt files.
- [RISC-V IOMMU
  1.0.1](../30-sources/risc-v-international-2026-iommu-1-0-1.md), revised
  2026-02-22, for device contexts, command and fault queues, invalidation, MSI
  translation, and DMA protection.
- [Arm A-profile system architecture
  documentation](../30-sources/arm-2026-a-profile-system-architecture-documentation.md)
  as a documentation set covering the current Arm Architecture Reference
  Manual, GIC, SMMUv3, PSCI, generic timer, and official code-cache publication
  guidance. Individual revisions must be pinned when A1 begins.
- [Intel 64 system programming and VT-d
  documentation](../30-sources/intel-2026-system-programming-documentation.md),
  using the Intel SDM page reporting version 092 on 2026-08-19 and VT-d revision
  5.0 from August 2024. This was a comparison surface, not a selected first
  implementation target.
- [QEMU Arm and RISC-V `virt`
  documentation](../30-sources/qemu-project-2026-virt-platform-documentation.md)
  as rendered for QEMU 11.1.50 development, for the machine interfaces,
  optional AIA and IOMMU devices, discovery choices, and warning that
  unversioned defaults are moving targets.

The key revision lesson is that an ISA label such as “RV64” or “Armv8” is
insufficient. An experiment must pin ISA extensions, platform profile, firmware,
emulator release/build and full machine configuration, controller models,
discovery input, virtual devices, and enabled core count. Arm `virt` offers
versioned machine types; current RISC-V `virt` instead requires pinning the
QEMU build and complete options and retaining the generated Devicetree.

A parallel reachability check of the 24 canonical source URLs returned HTTP
200 for 21. The two UEFI Forum pages returned 403 to command-line `curl`, and
the St Andrews repository timed out in that check; all three had been opened
through the research browser during reading. HTTP reachability is not evidence
that a source supports a claim, but this separates an access-tool limitation
from an unverified citation.

### Scientific-paper search

Queries combined microkernel, multikernel, capability, memory protection,
verified kernel, weak memory, virtual memory, TLB, cache coherence, interrupt,
IOMMU, DMA attack, driver isolation, user-level I/O, queue ownership, MPU,
extended state, SIMD, and architecture names. Complete publisher,
institutional-repository, author, or project copies were preferred.

The following primary works materially changed or qualified the synthesis:

- [The Multikernel](../30-sources/baumann-et-al-2009-multikernel.md) — hardware
  diversity and explicit inter-core protocols.
- [Comprehensive formal verification of an OS
  microkernel](../30-sources/klein-et-al-2014-comprehensive-sel4-verification.md)
  — small explicit kernel contracts, proof scope, and the boundary between a
  verified kernel and unverified platform assumptions.
- [A least-privilege memory protection model for modern
  hardware](../30-sources/achermann-et-al-2019-least-privilege-memory-protection.md)
  — translation structures as delegated authority.
- [Arrakis](../30-sources/peter-et-al-2014-arrakis.md) — protected direct I/O
  and the control-plane/data-plane split.
- [CleanQ](../30-sources/haecki-et-al-2019-cleanq.md) — ownership transfer as a
  common queue abstraction.
- [Thunderclap](../30-sources/markettos-et-al-2019-thunderclap.md) — practical
  DMA attacks and the inadequacy of permissive IOMMU configuration.
- [Tock](../30-sources/levy-et-al-2017-tock.md) — MPU-based process isolation,
  language safety, and constrained embedded trade-offs.
- [Nooks](../30-sources/swift-et-al-2003-nooks.md) — driver fault containment
  and recovery limits in a shared-kernel design.
- [x86-TSO](../30-sources/sewell-et-al-2010-x86-tso.md) — a rigorous x86 memory
  model rather than an informal “strong ordering” assumption.
- [Operational ARMv8
  concurrency](../30-sources/flur-et-al-2016-armv8-concurrency.md) — empirical
  and formal treatment of Arm concurrency behaviors.
- [Relaxed virtual memory in
  Armv8-A](../30-sources/simner-et-al-2022-relaxed-virtual-memory.md) — the
  interaction of weak ordering and address translation.
- [LazyFP](../30-sources/stecklina-prescher-2018-lazyfp.md) — confidentiality
  failures caused by lazy extended-state switching.
- [CHERI ISAv9](../30-sources/watson-et-al-2023-cheri-v9.md) — a concrete but
  optional capability-hardware direction.

The session also read official Arm engineering articles on instruction-cache
maintenance for self-modifying code and cross-thread code publication. Those
articles are recorded within the Arm documentation-set source note because
they clarify the normative architecture operations rather than constitute an
independent research result.

### Cross-source synthesis method

For each responsibility, the synthesis records:

1. the hardware state owned by the component;
2. the smallest architecture-neutral contract that preserves authority and
   lifecycle semantics;
3. the architecture-specific operations that must remain behind the contract;
4. choices and their benefits, costs, and failure modes;
5. dependencies and transactions with other components;
6. interactions with protected domains and the managed actor runtime; and
7. an experiment that can falsify the proposed design.

The resulting dependency order is:

```text
boot evidence -> discovery graph -> early memory and trap substrate
              -> interrupt/time/CPU lifecycle
              -> address spaces and cross-core invalidation
              -> IOMMU and device resource bundles
              -> isolated drivers and protected runtime domains
```

Power, reset, watchdog, debug, and retained-error paths cut across the chain
and therefore cannot be deferred to an unrelated late platform module.

### Decisions versus evidence

The literature and specifications support the component boundaries and expose
failure modes. They do not scientifically prove that RV64 is universally the
best first ISA. The proposed sequence—R0 on RV64 QEMU `virt`, R1 with AIA and
IOMMU, then A1 on AArch64 QEMU `virt`—is a project judgment based on staged
complexity and the value of an early weak-order/cross-ISA test.

The exact physical target remains deliberately undecided. Availability,
documentation quality, debug and reset access, protected DMA, reproducible
firmware, and observable failure behavior must be scored when implementation
is ready; product popularity alone is insufficient evidence.

### Archive artifacts produced

- [Hardware and architecture support for the Zig
  kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md)
  preserves the durable model and detailed design trade-offs.
- [Which hardware contract should the kernel
  adopt?](../40-inquiries/which-hardware-contract-should-the-kernel-adopt.md)
  keeps the unverified choices and acceptance tests open.
- [Hardware and architecture
  support](../10-maps/hardware-and-architecture-support.md) supplies a curated
  route through the specifications, papers, synthesis, and open work.
- Twenty-four evidence-focused source notes preserve the official
  specifications, architecture documentation, emulator boundary, OS research,
  concurrency models, I/O and isolation studies, firmware guidance, and
  extended-state security result used substantively.

## Threads

- The proposed resource graph needs a schema with stable identifiers,
  provenance, reserved-region handling, dependency edges, and an explicit
  policy for contradictory firmware descriptions.
- Address-space and IOMMU invalidation should share a generation and completion
  vocabulary without sharing page-table formats or silently coupling CPU and
  device translation.
- Interrupt events delivered to actor-facing services need bounded coalescing
  and backpressure; mapping each hardware edge to an actor message would make
  an interrupt flood an unbounded mailbox attack.
- CPU-local scheduling and accounting must treat interrupt and deferred work as
  charged execution, or reduction-like actor fairness will ignore time spent on
  behalf of a domain.
- FPU/SIMD/vector ownership should be per protected domain or kernel execution
  context, not per cheap managed actor, unless workload measurements falsify
  that granularity.
- Driver recovery needs a formal “quiesced, reset, rebound, or quarantined”
  outcome; a timeout is evidence of uncertainty, not permission to reuse DMA
  memory.
- The constrained MPU/PMP profile may need different actor placement and
  upgrade guarantees. Its interface must advertise missing capabilities
  instead of simulating them unsafely.

## Follow-ups

1. Pin a Zig toolchain, QEMU release/build, OpenSBI release, RISC-V extensions,
   CPU model, complete `virt` options, and generated Devicetree for R0.
2. Write the architecture-neutral types and deterministic fake backend before
   controller code; generate illegal-transition tests from the synthesis.
3. Produce a reset-to-Zig boot journal with exact build commands, binaries,
   hashes, firmware, QEMU command line, Devicetree, console transcript, and
   failure cases.
4. Implement and test Sv39 mapping, ASID lifecycle, TLB invalidation, user-mode
   entry, timer pre-emption, PLIC acknowledgement, and reset.
5. Add R1 only after R0 contracts pass: SMP, AIA, MSI, IOMMU, isolated virtio,
   stale-event rejection, DMA fault charging, and driver restart.
6. Port the same semantic tests to AArch64 `virt`, then compare source changes
   above the architecture packages. Any higher-layer semantic fork should
   reopen the abstraction.
7. Define latency, throughput, memory, and recovery budgets before optimizing;
   preserve distributions and failure outcomes rather than only averages.
8. Select a physical board through the documented gate and reproduce at least
   one cache, DMA, reset, and firmware behavior that an emulator cannot
   establish.
