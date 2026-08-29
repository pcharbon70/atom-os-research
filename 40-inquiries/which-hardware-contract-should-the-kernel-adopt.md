---
title: "Which hardware contract should the kernel adopt?"
kind: inquiry
created: "2026-08-29"
status: open
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
  - "Initial kernel hardware profile"
  - "Kernel architecture contract"
---

# Which hardware contract should the kernel adopt?

## Why this matters

The first target is not merely a board choice. It selects the privilege model,
page-table and invalidation rules, interrupt topology, firmware boundary,
device-description format, timer source, memory-order hazards, DMA threat
model, and the failures that the first kernel can observe. A target that is too
simple may let accidental assumptions harden into the interface; one that is
too broad can consume the project in firmware and driver compatibility before
its capability, actor, and recovery principles are testable.

The hardware layer also determines whether the proposed system boundaries are
real. A driver domain is not isolated if its device can DMA through all of
memory. A pre-emptible actor system is not predictable if interrupt routing,
timer cancellation, extended-state ownership, and cross-core invalidation are
implicit. A versioned native-code loader is not correct until instruction-cache
publication is specified for every participating core.

Zig is already the fixed implementation language for new kernel and native
system code. This inquiry chooses the contracts and target profiles that the
Zig implementation must satisfy; it does not reopen the language decision.

## Operational question

Choose the smallest explicit set of architectural contracts and target
profiles that can demonstrate all of the following without embedding one
machine's register layout in the rest of the kernel:

1. **Reproducible entry:** a pinned firmware or direct-boot route reaches Zig
   with a recorded privilege level, memory map, discovery blob, boot CPU,
   secondary-CPU protocol, and firmware ownership boundary.
2. **Protected execution:** the kernel creates, revokes, and audits address
   spaces or constrained protection domains with guard regions, non-executable
   data, immutable kernel mappings, and architecture-correct invalidation.
3. **Bounded events:** interrupts, inter-processor interrupts, and timers have
   explicit acknowledgement, masking, affinity, cancellation, generation, and
   overload behavior.
4. **Multicore correctness:** CPU startup, publication, teardown, atomic
   operations, memory barriers, page-table changes, and executable-code changes
   survive weak ordering and concurrent failure.
5. **Contained I/O:** device resources are granted as typed bundles; DMA is
   denied or isolated by default; queue ownership and driver restart are
   testable state machines.
6. **Recoverable lifecycle:** device, CPU, and system power transitions either
   complete or leave diagnosable state; reset and watchdog paths preserve a
   minimal crash record.
7. **Portability:** the same architecture-neutral contracts boot on two
   materially different ISAs, with architecture-specific code confined to the
   mechanism packages named in the synthesis.
8. **Evidence quality:** tests identify the simulator or board, firmware and
   specification revisions, enabled ISA features, core count, cache-coherence
   assumptions, IOMMU configuration, fault injection, and observed result.

The inquiry is resolved only when a bootstrap profile, a protected I/O profile,
and a second-ISA profile have executed the acceptance tests. A document or
successful console boot alone does not resolve it.

## Working hypotheses

### H1: use two RISC-V profiles instead of one overloaded first target

Start with RV64 QEMU `virt` in supervisor mode above pinned OpenSBI, using
Devicetree, Sv39, SBI timer and hart services, PLIC, UART, and simple virtio.
Then enable a second profile with AIA, message-signaled interrupts, and the
RISC-V IOMMU.

This makes the first bring-up small while ensuring that interrupt remapping,
device assignment, DMA revocation, and stale-event rejection are designed
before physical-hardware convenience can make them optional.

Falsifier: QEMU's exposed interfaces may omit or inaccurately model a failure
needed for the kernel contract, or the two profiles may diverge enough to
produce two implementations rather than a staged subset. Compare the relevant
QEMU behavior with the architecture specifications and at least one physical
implementation before calling a mechanism validated.

### H2: AArch64 `virt` should be the second ISA

AArch64 supplies a mature, materially different weakly ordered architecture,
exception-level model, GIC interrupt hierarchy, generic timer, and SMMU family.
Porting the same contracts to QEMU `virt` should expose hidden RISC-V
assumptions without beginning with x86 legacy enumeration and interrupt modes.

Falsifier: if the project chooses a physical x86-64 deployment constraint, or
if an AArch64 profile cannot exercise protected DMA and MSI semantics in the
available emulator, the order may change. Portability still requires a
different ISA before the interfaces are considered stable.

### H3: normalized resources should cross the firmware boundary

Firmware parsers should produce a validated, immutable resource graph. The
rest of the kernel should consume typed CPU, memory, interrupt, timer, bus,
IOMMU, reset, and reserved-region records rather than Devicetree paths, ACPI
handles, or raw tables.

Falsifier: a required runtime firmware operation may inherently use a
firmware-native identifier. Such identifiers may survive inside a typed token,
but parsing and namespace traversal should not leak into drivers or policy.

### H4: one interface surface can support MMU and constrained profiles, but
not pretend they are equally capable

Both page-table systems and MPU/PMP-style systems can expose memory-object,
authority, map, revoke, and synchronize operations. Feature types must state
whether arbitrary sparse address spaces, per-domain aliases, execute-only
mapping, independent DMA translation, and efficient revocation actually exist.

Falsifier: if the shared surface forces the constrained implementation to lie,
or forces the MMU implementation through an unusably weak abstraction, split
the profiles while retaining common authority and lifecycle vocabulary.

### H5: interrupt, DMA, and driver lifecycles must be one transactional design

Device assignment should bind an MMIO grant, an IOMMU domain, queues, interrupt
routes, ownership generation, and cleanup authority. Revocation should mask
and drain interrupts, stop DMA, detach translations, reject stale completions,
and only then reclaim buffers.

Falsifier: hardware may not provide a reliable quiescence signal. The design
must then reset or permanently quarantine the device and its memory rather than
claim that revocation completed.

### H6: the portable contract should target the weakest chosen ordering model

Architecture-neutral synchronization should be expressed through ownership,
atomics, acquire/release publication, explicit invalidation protocols, and
device-memory accessors. Architecture backends implement the required fences;
ordinary code must not depend on x86-TSO behavior.

Falsifier: measurements may justify a stronger architecture-specific fast path,
but it must refine a tested portable path and keep identical observable
semantics.

## Paths to explore

### Contract-first prototypes

1. Define typed Zig interfaces for boot handoff, CPU-local state, address-space
   identifiers, interrupt routes, timer tokens, DMA domains, device-resource
   bundles, cache ranges, and reset reasons without importing register layouts.
2. Implement a deterministic fake backend whose state machines reject illegal
   ordering: double acknowledgement, use after revoke, stale generations,
   unbalanced mapping pins, DMA after detach, and CPU offline with live routes.
3. Generate positive and negative traces for every cross-component transaction
   in the [hardware synthesis](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md).

### Profile R0: RV64 bootstrap

- Pin the RISC-V ISA extensions, OpenSBI release, QEMU release/build, `virt`
  options, CPU model, Devicetree input and hash, UART, PLIC, virtio device, CPU
  count, and boot command. RISC-V `virt` has no Arm-style versioned machine
  alias, so the complete configuration is the reproducibility boundary.
- Prove reset-to-Zig entry, early exception recording, immutable discovery,
  physical allocation, Sv39 kernel and user mappings, user-mode entry, timer
  pre-emption, one interrupt, and clean shutdown or reset.
- Inject malformed discovery data, unmapped accesses, execute faults, spurious
  interrupts, timer cancellation races, and unsupported extension use.

### Profile R1: RV64 protection and SMP

- Add multiple harts, AIA, MSI, the RISC-V IOMMU, a device-domain assignment,
  cross-core TLB invalidation, code publication, CPU offline, and driver reset.
- Stress all litmus-sensitive publication paths under RVWMO and test stale
  interrupts and DMA after revocation.
- Measure interrupt and timer latency distributions, shootdown cost, queue
  contention, driver restart time, and quarantined-resource growth.

### Profile A1: AArch64 portability

- Pin a QEMU release and versioned Arm `virt-N.N` machine type, the implemented
  Arm architecture and CPU model, boot firmware or direct-entry contract, GIC
  version, timer, SMMU exposure, and discovery form.
- Re-run the same semantic tests with Arm barriers, cache maintenance, ASIDs,
  TLBI, exception levels, GIC routing, and PSCI lifecycle operations.
- Treat a source-level port that changes higher-layer semantics as a contract
  failure, not merely normal platform work.

### Physical target selection

Score candidate boards only after R0 and the contract tests exist. Required
evidence includes public documentation, reproducible boot and recovery,
debug access, RAM, coherent DMA behavior, IOMMU availability, interrupt model,
reset controls, storage, networking, price and availability, and a path to
observe or inject failures. Do not select a board solely because Linux already
boots on it.

### Focused adversarial experiments

- Corrupt or duplicate firmware resource descriptions.
- Race mapping replacement with remote-core execution and DMA.
- Flood level-triggered, edge-triggered, MSI, timer, and IPI paths.
- Restart a driver with queued requests, an asserted interrupt, and an active
  DMA transaction.
- Exercise nested FPU/SIMD use and verify that secrets do not cross domains.
- Publish generated native code while other CPUs enter and leave the domain.
- Simulate suspend, partial resume, watchdog reset, and crash-record recovery.
- Attempt DMA outside the assigned memory and verify that the fault is charged
  to the device domain without corrupting the kernel.

## Findings

The current evidence is synthesized in [Hardware and architecture support for
the Zig kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md)
and routed through the [hardware and architecture support
map](../10-maps/hardware-and-architecture-support.md).

- Architecture manuals expose different mechanisms, but the recurring kernel
  responsibilities are stable: boot ownership, privilege transitions,
  discovery, memory authority, interrupts, time, CPU lifecycle, ordering,
  cache publication, extended state, DMA, device resources, power, and retained
  failure evidence.
- seL4 and least-privilege memory research support a small explicit authority
  core; Barrelfish supports treating hardware state and cross-core coordination
  as distributed state rather than assuming uniform shared-memory behavior.
- Arrakis shows why protected direct access can reduce mediation, while CleanQ
  supplies an ownership-oriented vocabulary for queues. Thunderclap shows why
  an IOMMU that is present but broadly configured does not establish DMA
  isolation.
- Tock and Nooks provide distinct containment lessons for constrained systems
  and fault-prone drivers, but neither by itself supplies the hostile-device
  boundary required here.
- The x86-TSO, Arm concurrency, and relaxed virtual-memory work shows that
  ordinary shared-memory synchronization and translation-table maintenance
  cannot be collapsed into one intuitive “barrier.”
- LazyFP makes extended architectural state a confidentiality and ownership
  concern, not just a context-switch optimization.
- No emulator trace, physical-board boot, interrupt-latency measurement,
  IOMMU-fault test, or cross-ISA port has yet been produced in this archive.
  Consequently, the target sequence is a design recommendation, not verified
  implementation evidence.

## Outcome

Open. The working decision is to implement the contracts against RV64 QEMU
`virt` in two stages—R0 bootstrap and R1 protected SMP—and then validate them on
AArch64 QEMU `virt`. The exact QEMU, OpenSBI, ISA-extension, GIC/SMMU, and
physical-board revisions remain to be pinned by implementation work. The
inquiry remains open until the profile acceptance tests and failure injections
are reproducible.
