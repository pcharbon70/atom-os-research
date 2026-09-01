---
title: "Kernel hardware and architecture support"
kind: map
created: "2026-08-30"
tags:
  - architecture-support
  - archive-navigation
  - operating-systems
  - privilege
aliases:
  - "Kernel architecture support map"
---

# Kernel hardware and architecture support

## Scope

This map covers the kernel-level layer that turns privilege, execution state,
translation, ordering, interrupts, counters, logical CPUs, protected I/O, and
architecture faults into stable operating-system contracts.

It deliberately excludes board design, physical-component selection, SoC
bring-up, device-protocol surveys, clock-tree engineering, and firmware
implementation. Platform or firmware mechanisms appear only where a kernel
backend must declare them as dependencies.

## Start here

- [Kernel hardware and architecture support
  layer](../20-notes/kernel-hardware-and-architecture-support-layer.md) is the
  comprehensive synthesis, proposed component decomposition, tradeoff analysis,
  cross-architecture comparison, and test plan.
- [What contract should the kernel hardware and architecture layer
  provide?](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
  turns the synthesis into falsifiable criteria and open experiments.
- [Research session: kernel hardware and architecture support deep
  dive](../50-journal/2026-08-30-kernel-hardware-and-architecture-support-deep-dive.md)
  records search scope, method, and the limit of this literature-only evidence.

## Trails

### Where the kernel boundary belongs

- [From L3 to seL4](../30-sources/elphinstone-heiser-2013-l4-lessons.md)
  traces minimal mechanisms, capability authority, asynchronous interrupt
  notification, user drivers, portability, and reduced assembly across L4
  generations.
- [Exokernel](../30-sources/engler-et-al-1995-exokernel.md) sharpens the
  distinction between protection and management and supplies revocation
  vocabulary.
- [Flux OSKit](../30-sources/ford-et-al-1997-flux-oskit.md) explains why module
  boundaries require semantic interfaces and explicit dependency glue.
- [The Multikernel](../30-sources/baumann-et-al-2009-multikernel.md) motivates
  explicit cross-CPU coordination and replicated local state on heterogeneous
  machines.

### Assurance and its assumptions

- [CertiKOS](../30-sources/gu-et-al-2016-certikos.md) supplies observable layer
  specifications, per-CPU/shared-state structure, and contextual refinement;
  its exclusions help identify proof obligations this project must not hide.
- [Comprehensive seL4
  verification](../30-sources/klein-et-al-2014-comprehensive-sel4-verification.md)
  connects explicit capabilities and kernel objects to a small TCB while
  documenting assumptions around hardware, assembly, boot, caches, devices,
  DMA, and timing.

### Translation, ordering, context, and executable code

- [A least-privilege memory protection
  model](../30-sources/achermann-et-al-2019-least-privilege-memory-protection.md)
  separates translation authority from access authority across modern address
  spaces.
- [Relaxed virtual memory in
  Armv8-A](../30-sources/simner-et-al-2022-relaxed-virtual-memory.md) treats page
  table mutation, invalidation, barriers, and remote observation as a protocol.
- [Arm instruction-fetch
  semantics](../30-sources/simner-et-al-2020-arm-instruction-fetch.md) grounds
  executable-code publication in cache and cross-core state transitions.
- [x86-TSO](../30-sources/sewell-et-al-2010-x86-tso.md) and [simplified Armv8
  concurrency](../30-sources/pulte-et-al-2018-simplifying-arm-concurrency.md)
  give rigorous but differently relaxed ordinary-memory models.
- [LazyFP](../30-sources/stecklina-prescher-2018-lazyfp.md) demonstrates that
  extended processor state is security context, not merely switch overhead.

### Interrupts, time, CPUs, and practical contract precedent

- [Linux low-level core API
  documentation](../30-sources/linux-kernel-community-2026-low-level-core-apis.md)
  is the practical trail through entry state, interrupt flow, time primitives,
  barriers, cache/TLB effects, CPU lifecycle, and DMA address/lifetime rules.

### Protected delegation and I/O

- [Dune](../30-sources/belay-et-al-2012-dune.md) demonstrates controlled access
  to selected privileged CPU facilities behind hardware protection.
- [Arrakis](../30-sources/peter-et-al-2014-arrakis.md) separates a kernel control
  plane from delegated application I/O data paths and measures workload-
  specific gains.
- [CleanQ](../30-sources/haecki-et-al-2019-cleanq.md) gives device queues a
  formally specified ownership-transfer interpretation.
- [Thunderclap](../30-sources/markettos-et-al-2019-thunderclap.md) shows why an
  IOMMU alone does not secure driver/device shared-memory protocols or
  transition windows.

### Normative architecture mechanisms

- [Intel 64 and IA-32 system programming
  documentation](../30-sources/intel-2026-system-programming-documentation.md)
  is the current x86-64 privilege, translation, interrupt, context, timer, and
  optional virtualization reference.
- [Arm A-profile system architecture
  documentation](../30-sources/arm-2026-a-profile-system-architecture-documentation.md)
  is the current AArch64 exception, translation, memory-order, cache,
  timekeeping, and context reference.
- [RISC-V privileged
  architecture](../30-sources/risc-v-international-2026-privileged-architecture.md)
  is the current ratified supervisor/privilege, translation, ordering, trap,
  and extension-state reference.

### Connection to the larger operating-system model

- [Minimal privileged kernel](minimal-privileged-kernel.md) is the immediate
  upper layer. It authorizes and accounts for these mechanisms through typed
  capabilities, domains, IPC, CPU budgets, faults, and safe teardown.
- [BEAM, ERTS, and OTP principles for a new operating
  system](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md)
  places this mechanism layer beneath protected domains, a managed actor
  runtime with required BEAM-compatible process-local tracing collection,
  OTP-like services, and applications.
- [BEAM, ERTS, and OTP map](beam-erts-and-otp.md) explains which runtime
  semantics the kernel should enable without embedding the full hosted runtime
  in its trust boundary.

## Open questions

The central [kernel hardware-contract
inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
tracks minimum profiles, completion semantics, cross-CPU coordination, event
delivery, direct I/O delegation, and the two-ISA portability test.

Additional gaps include architecture-version and errata pinning for a concrete
backend, a formal method that spans language/CPU/translation/DMA ordering, and
experimental latency budgets derived from the managed runtime rather than
assumed in advance.

The upper-layer [minimal privileged-kernel contract
inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
tracks how these completion primitives become authorized domain and recovery
semantics.
