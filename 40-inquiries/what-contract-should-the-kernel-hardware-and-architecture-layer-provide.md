---
title: "What contract should the kernel hardware and architecture layer provide?"
kind: inquiry
created: "2026-08-30"
status: open
tags:
  - architecture-support
  - capabilities
  - dma
  - interrupts
  - operating-systems
  - privilege
  - virtual-memory
aliases:
  - "Kernel hardware-contract inquiry"
---

# What contract should the kernel hardware and architecture layer provide?

## Why this matters

The kernel must convert architecture-specific privileged mechanisms into
stable contracts for the rest of the operating system. If the boundary is too
thin, ordering rules, stale-state hazards, and ambient authority leak into
every subsystem. If it is too broad, device, scheduler, and memory policy
become trapped inside an untestable HAL.

This question is explicitly about the kernel-level boundary. It does not ask
which board, CPU product, physical memory, peripheral, or firmware stack the
project should build or buy.

## Operational question

A candidate contract is adequate when all of the following can be demonstrated:

| Criterion | Evidence required |
| --- | --- |
| Complete responsibility model | Every privileged transition is owned by one component and every cross-component dependency is named |
| Authority safety | Tests show raw identifiers/pointers cannot bypass frame, interrupt, CPU, timer, or DMA authority |
| Completion safety | Mapping, code, CPU, interrupt, and DMA state cannot be reclaimed or rebound before required local/remote quiescence |
| Context isolation | All enabled integer, FP/SIMD/vector, debug, and control state is saved, scrubbed, or disabled across domains |
| Ordering correctness | Language/ISA litmus tests and device/DMA tests match pinned memory and I/O models |
| Bounded exceptional paths | Entry, interrupt, NMI-like, and fatal-fault paths have measured stack, time, nesting, lock, and allocation bounds |
| Portability | The unchanged mandatory contract passes on two materially different ISA backends |
| Honest feature variation | Optional or absent mechanisms are represented in profiles without silently weakening invariants |
| Recoverable failure semantics | Timeouts, partial CPU sets, storms, reset failures, and non-quiescent DMA produce explicit contained states |
| Useful performance | Measured latency and scalability satisfy budgets defined by later runtime and service experiments |

The inquiry remains open until at least the contract model and one backend have
experimental evidence. Literature synthesis alone cannot resolve it.

## Working hypotheses

1. A monolithic HAL is the wrong unit. Eleven semantic components—boot
   normalization, architecture primitives, entry/context, translation,
   ordering/publication, interrupt events, time, CPU lifecycle, protected I/O,
   fault handling, and a typed facade—will provide a smaller and safer port
   surface.
2. Typed generational handles and explicit completion epochs can unify stale-
   state protection across otherwise different mechanisms.
3. The baseline should use eager extended-state isolation, centralized mapping
   transactions, flow-specific interrupts, one-shot deadlines, and mediated
   I/O; later experiments may justify optimized alternatives.
4. CPU-local bounded operations can be synchronous, while cross-CPU,
   firmware-dependent, device, IOMMU, and revocation work should be split-phase.
5. A mandatory semantic baseline plus declared optional profiles will preserve
   portability better than either a lowest-common-denominator API or separate
   architecture-shaped kernels.
6. Existing firmware or a hypervisor may provide bootstrap mechanisms without
   becoming part of the kernel abstraction; that dependency must remain
   explicit in the target profile.
7. Required BEAM process-local tracing collection should remain entirely in a
   managed runtime domain. The hardware layer should provision and account for
   memory in batches so ordinary term allocation and collection require no
   per-object kernel or translation operation.

## Paths to explore

### Specify before implementing

- Define the object, authority, generation, context-safety, failure, and
  completion schema for every proposed operation.
- Write executable state machines for mapping/reclamation, interrupt rebinding,
  CPU lifecycle, DMA revocation, and code publication.
- Derive a lock/order graph across entry, CPU lifecycle, mapping, event, timer,
  DMA, and crash paths.
- State which architecture manuals and memory-model versions justify each
  primitive.

### Falsify the component boundary

- Attempt one minimal backend and record every operation that needs a hidden
  policy decision or cross-component bypass.
- Attempt a second, materially different ISA backend and identify accidental
  assumptions in the first interface.
- Compare static backend selection with any runtime-dispatched critical path by
  generated-code inspection and measurement.
- Test whether MMU page tables, MPU/PMP protection, and IOMMU mappings can share
  lifecycle vocabulary without claiming identical revocation.

### Stress failure and concurrency

- Inject nested traps at every entry transition and fuzz every user return.
- Force ASID generation rollover, delayed shootdowns, CPU failure, and task
  migration during mapping and code publication.
- Exercise edge/level interrupt storms, receiver overflow, affinity changes,
  and stale completion tokens.
- Delay DMA completions across revoke, reset, domain reuse, and driver restart.
- Corrupt ordinary crash dependencies and evaluate the preallocated fault path.

### Connect to the managed-runtime design

- Run compiled BEAM allocation/reclamation workloads long enough to establish
  a bounded steady state under process-local tracing collection. Confirm that
  a process-exit-only arena is neither required nor reported as compatible.
- Measure the page-refill frequency, per-process heap/collector overhead,
  collection pause distributions, allocator contention, and tail latency of
  unrelated processes without moving tracing into privileged code.
- Determine event semantics needed by OTP-like supervision: counted,
  coalescing, at-least-once, loss-reporting, or bounded lossless.
- Measure the cost of kernel-domain scheduling plus runtime actor scheduling.
- Test atomic code replacement over the proposed executable publication and
  retirement protocol.
- Determine which hardware-layer failures can become ordinary supervised
  exits and which require domain, CPU, device, or machine recovery.

## Findings

The current literature synthesis is developed in [Kernel hardware and
architecture support
layer](../20-notes/kernel-hardware-and-architecture-support-layer.md), with
source trails in the [topic
map](../10-maps/kernel-hardware-and-architecture-support.md).

Evidence currently supports these constraints:

- L4 history and OSKit support a small architecture-specific surface with
  semantic components, rather than forcing identical low-level code.
- Exokernel work supports separating enforceable protection from replaceable
  management policy.
- CertiKOS and seL4 verification work support explicit abstract state and also
  show why assumptions about boot, assembly, devices, DMA, TLBs, and timing
  must be recorded rather than inferred from a proof headline.
- architecture memory, virtual-memory, and instruction-fetch work shows that
  ordinary memory ordering does not by itself establish TLB, executable-code,
  or remote-core completion;
- Linux's current low-level documentation provides practical evidence for
  separate entry, interrupt-flow, time, cache/TLB, CPU-lifecycle, and DMA
  contracts; and
- CleanQ and Thunderclap show that protected I/O needs an ownership/lifetime
  protocol in addition to address remapping.

The immediate consumer is now developed in [Minimal privileged kernel
layer](../20-notes/minimal-privileged-kernel-layer.md). Its capability and
failure-boundary design makes several lower-layer completions non-optional:
cross-core domain stop, completed TLB invalidation, interrupt-source drainage,
IOTLB/DMA quiescence, and safe zero-before-reuse. The corresponding [minimal
kernel inquiry](what-contract-should-the-minimal-privileged-kernel-provide.md)
keeps those cross-layer obligations testable.

No source proves that the proposed eleven-component boundary is minimal, that it
will meet performance goals, or that one contract can support this project's
eventual targets. Those are experimental questions.

## Outcome

Open. The current provisional answer is the architecture in [Kernel hardware
and architecture support
layer](../20-notes/kernel-hardware-and-architecture-support-layer.md). Resolve
only after the operational criteria have been tested on at least two
materially different ISA backends, or replace the criteria explicitly if
prototype evidence shows they are inappropriate.

The compact [topic map](../10-maps/kernel-hardware-and-architecture-support.md)
keeps this workbench connected to its evidence trails.
