---
title: "Hardware and architecture support"
kind: map
created: "2026-08-29"
tags:
  - aarch64
  - dma
  - hardware-architecture
  - interrupts
  - iommu
  - kernel-development
  - memory-protection
  - multicore
  - risc-v
  - zig
aliases:
  - "Kernel hardware layer"
  - "Architecture support map"
---

# Hardware and architecture support

## Scope

This map follows the mechanisms between reset and the architecture-neutral
kernel: firmware handoff, privilege state, hardware discovery, memory
protection, traps, interrupts, timers, CPU lifecycle, memory ordering, cache
maintenance, FPU/SIMD/vector ownership, DMA isolation, driver resources, power,
security roots, debug, and retained failure evidence.

The layer is not one catch-all HAL. It is a dependency-ordered collection of
small components with typed authority and explicit lifecycle transitions. The
map connects the architecture specifications to OS research and then to the
project's proposed Zig interfaces and target profiles.

## Start here

- [Hardware and architecture support for the Zig
  kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md) —
  the comprehensive synthesis, component model, architecture comparison,
  target sequence, interaction rules, and verification matrix.
- [Which hardware contract should the kernel
  adopt?](../40-inquiries/which-hardware-contract-should-the-kernel-adopt.md) —
  the falsifiable target and contract decision, including RV64 R0/R1 and
  AArch64 A1 acceptance paths.
- [2026-08-29 hardware and architecture support deep
  dive](../50-journal/2026-08-29-hardware-and-architecture-support-deep-dive.md) —
  records the search scope, revision choices, host limitations, and the line
  between literature-backed design and unperformed experiments.
- [BEAM, ERTS, and OTP principles for a new operating
  system](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md) —
  places this layer below the protected domains, managed actor runtime, and
  OTP-inspired service policy that consume it.

## Trails

### Entry, firmware, and discovery

- [UEFI 2.11](../30-sources/uefi-forum-2024-uefi-2-11.md) defines the boot
  services, memory-map handoff, configuration tables, runtime services, and
  authenticated-boot vocabulary relevant to an x86-64 or standards-based Arm
  entry path.
- [ACPI 6.6](../30-sources/uefi-forum-2025-acpi-6-6.md) supplies a rich but
  complex table and namespace model for topology, interrupts, timers, power,
  and platform devices.
- [Devicetree 0.4](../30-sources/devicetree-org-2023-devicetree-0-4.md) supplies
  the simpler hierarchical hardware-description contract used by the proposed
  RISC-V bootstrap.
- [Platform Firmware Resiliency
  Guidelines](../30-sources/regenscheid-2018-platform-firmware-resiliency.md)
  frames protection, detection, and recovery as separate firmware properties;
  successful verification at boot does not remove the need for recovery.

The architectural result is a one-way parsing boundary: validate the selected
firmware format early, preserve the original blob as evidence, and publish an
immutable typed resource graph. Higher layers should not traverse raw ACPI or
Devicetree namespaces.

### RISC-V bootstrap and protected profile

- [RISC-V privileged and unprivileged architecture
  specifications](../30-sources/risc-v-international-2026-privileged-architecture.md)
  define privilege, traps, page translation, fences, counters, PMP, extension
  discovery, and RVWMO.
- [SBI 3.0](../30-sources/risc-v-international-2025-sbi-3-0.md) defines the
  supervisor-to-firmware operations used for the provisional boot, timer, IPI,
  hart lifecycle, reset, and debug boundary.
- [AIA 1.0](../30-sources/risc-v-international-2023-advanced-interrupt-architecture.md)
  introduces APLIC and per-hart IMSIC state, making interrupt files, affinity,
  MSI routing, and virtualization explicit.
- [RISC-V IOMMU
  1.0.1](../30-sources/risc-v-international-2026-iommu-1-0-1.md) defines device
  translation contexts, invalidation, fault reporting, MSI translation, and
  the synchronization obligations needed for protected device assignment.
- [QEMU `virt` platform
  documentation](../30-sources/qemu-project-2026-virt-platform-documentation.md)
  identifies the emulator features and reproducibility inputs to pin for the
  R0 and R1 experiments.

This trail supports two intentionally different profiles: a small PLIC/Sv39
proof of ownership and a second AIA/IOMMU profile that makes message-signaled
interrupts and hostile DMA part of the design rather than later extensions.

### AArch64 portability and x86-64 comparison

- [Arm A-profile system architecture
  documentation](../30-sources/arm-2026-a-profile-system-architecture-documentation.md)
  routes through the Arm architecture, GIC, SMMUv3, PSCI, generic timer, and
  cache-maintenance rules needed by the A1 port.
- [Intel 64 system programming and VT-d
  documentation](../30-sources/intel-2026-system-programming-documentation.md)
  records the mature but broad x86-64 privilege, APIC, paging, extended-state,
  virtualization, and DMA-remapping surface.
- [QEMU `virt` platform
  documentation](../30-sources/qemu-project-2026-virt-platform-documentation.md)
  also defines the Arm `virt` and SBSA-reference machine boundaries.

AArch64 is the proposed second ISA because it tests a different exception,
interrupt, cache, and weak-ordering model without making x86 compatibility
machinery part of the first portability milestone. x86-64 remains strategically
important and is not rejected as a future target.

### Kernel structure and authority

- [The Multikernel](../30-sources/baumann-et-al-2009-multikernel.md) motivates
  explicit per-core state and message-mediated coordination when modern
  hardware behaves more like a distributed system than one uniform machine.
- [Comprehensive seL4
  verification](../30-sources/klein-et-al-2014-comprehensive-sel4-verification.md)
  demonstrates the payoff and boundary conditions of a small, precisely
  specified authority and isolation core.
- [Least-privilege memory protection for modern
  hardware](../30-sources/achermann-et-al-2019-least-privilege-memory-protection.md)
  treats translation structures as authority rather than an unstructured map
  of page tables.
- [CHERI ISAv9](../30-sources/watson-et-al-2023-cheri-v9.md) provides a concrete
  capability-hardware direction but remains an optional research profile, not
  a portability assumption.
- [Tock](../30-sources/levy-et-al-2017-tock.md) shows a constrained MPU-oriented
  design with language and kernel isolation; it motivates a truthful
  constrained profile rather than pretending an MPU is a full MMU.

Together these works support a minimal mechanism kernel with explicit
authority, while leaving actor scheduling policy, supervision, device policy,
and application recovery above the hardware layer.

### Ordering, translation, and architectural state

- [x86-TSO](../30-sources/sewell-et-al-2010-x86-tso.md) gives a rigorous model
  for an architecture often—but incorrectly—treated as simply sequential.
- [Operational ARMv8
  concurrency](../30-sources/flur-et-al-2016-armv8-concurrency.md) exposes the
  behaviors a weakly ordered AArch64 implementation must handle.
- [Relaxed virtual memory in
  Armv8-A](../30-sources/simner-et-al-2022-relaxed-virtual-memory.md) shows why
  translation-table updates, TLB invalidation, and ordinary memory ordering
  form an interacting protocol.
- [LazyFP](../30-sources/stecklina-prescher-2018-lazyfp.md) demonstrates that
  deferred FPU/SIMD state switching can become a cross-domain confidentiality
  bug.

This trail leads to two rules: design portable synchronization against the
weakest selected model, and represent address-space, code-publication, and
extended-state transitions as named protocols rather than scattered fences.

### Devices, queues, and failure containment

- [Arrakis](../30-sources/peter-et-al-2014-arrakis.md) shows how virtualized
  hardware can allow protected direct I/O while separating control-plane
  policy from data-plane operations.
- [CleanQ](../30-sources/haecki-et-al-2019-cleanq.md) models queues in terms of
  ownership transfer, a useful basis for actor messages, virtio descriptors,
  DMA buffers, and revocation.
- [Thunderclap](../30-sources/markettos-et-al-2019-thunderclap.md) demonstrates
  that peripheral DMA can defeat OS isolation when IOMMUs are absent,
  bypassed, or permissively configured.
- [Nooks](../30-sources/swift-et-al-2003-nooks.md) supplies historical evidence
  that driver fault isolation can improve reliability even when recovery is
  imperfect and shared-kernel assumptions remain.

The combined design implication is a transactional resource bundle: MMIO,
interrupt route, IOMMU context, queues, buffers, reset control, owner
generation, and cleanup authority move together. A driver restart is not
complete until stale events and DMA are impossible or the device is
quarantined.

## Open questions

- [Which hardware contract should the kernel
  adopt?](../40-inquiries/which-hardware-contract-should-the-kernel-adopt.md)
- Which exact QEMU release/build, `virt` options, CPU model, OpenSBI release,
  ISA extensions, Devicetree hash, and virtual devices should be frozen for R0
  and R1?
- Can QEMU exercise the required IOMMU, MSI, reset, and ordering failures, and
  which claims require physical hardware or a second simulator?
- Which first physical board has sufficient public documentation, debug and
  reset access, protected DMA, reproducible firmware, availability, and a
  credible upstream lifecycle?
- What latency and throughput budgets should constrain interrupt handling,
  TLB shootdown, timer delivery, queue transfer, driver restart, and CPU
  offline?
- Should a constrained MPU/PMP profile share the same runtime and service
  model, or is it a separate product profile with fewer isolation guarantees?
- When, if ever, should CHERI capabilities or virtualization extensions become
  a required target rather than optional evidence?
