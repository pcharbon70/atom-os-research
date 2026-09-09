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

The [active T7500 / Intel x86-64 decision](../20-notes/proof-of-concept-requirements/dell-precision-t7500-target-and-minimal-qemu-profile.md)
selects the first implementation backend without narrowing this inquiry's
longer-term portability standard. Start with single-CPU CLI bring-up; Intel
processor-family qualification and the T7500's installed configuration are
the immediate hardware research gaps. Second-ISA and DMA evidence remain later work.

## Operational question

A candidate contract is adequate when all of the following can be demonstrated:

| Criterion | Evidence required |
| --- | --- |
| Complete responsibility model | Every privileged transition is owned by one component and every cross-component dependency is named |
| Authority safety | Tests show raw identifiers/pointers cannot bypass frame, interrupt, CPU, timer, or DMA authority |
| User-access mediation | Fault-injected copy and probe tests demonstrate nonwrapping checked ranges, bounded architecture privilege windows, explicit partial completion, stable snapshots for control data, and no ambient supervisor alias to user-owned frames |
| Completion safety | No identity, page-table page, frame, executable image, or DMA buffer is reclaimed or rebound until its separately required CPU-translation, hardware-walker, software-reader, pin/borrow, code-execution, IOTLB, and device-access quiescence predicates hold |
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

- Use the [nine address-translation service
  reports](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/README.md)
  as the initial state-machine and message-schema inventory. Reconcile their
  object incarnations, mutation and context-tag generations, acceptance
  handoffs, frozen target sets, completion-slot generations, invalidation
  effects, quiescence predicates, and user-access snapshots before coding.
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
- Delay IPI or firmware request acceptance independently from target execution
  and acknowledgement; verify that transport success, timeout, and a stale CPU
  lifecycle snapshot cannot satisfy `CpuTranslationQuiescent`.
- Deliver acknowledgements after CPU-number, address-space, mapping, context-
  tag, and completion-slot reuse; only the exact incarnation-and-generation
  tuple may advance its original teardown ledger.
- Race software page-table walkers, pinned user pages, executable-code
  retirement, IOMMU invalidation, device-TLB timeout, and in-flight DMA against
  frame and table-page reuse.
- Inject partial user-copy faults, arithmetic wrap, remapping, concurrent
  mutation, and supervisor direct-map aliases; authorization must consume one
  immutable snapshot and no failed path may leave the user-access gate open.
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

The [2026-09-08 internal-service research](../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md)
adds 55 reports for the nine components that previously lacked a deeper
decomposition. Together with components 3 and 9, all eleven components now
have service-level research. This concerns the full system architecture,
not a delivery milestone or emulator profile.

The new synthesis separates provider termination from data custody; exception
entry from memory synchronization; posted-write receipt from device completion;
snapshot consistency from storage lifetime; CPU start from admission and stop
from reclamation; and cooperative DMA ownership from hardware enforcement.
The facade now follows the selected Zig language, with runtime validation of
copied generational handles instead of an assumed linear type system.

The decisive remaining work is compositional: publication versus CPU lifecycle,
restriction versus all CPU aliases, device revocation versus already-issued
traffic, and accepted-operation custody after caller failure. Each service
supplies concrete falsifiers, but none was executed in this session. These
sharper contracts do not resolve this inquiry or establish recovery liveness.

The current literature synthesis is developed in [Kernel hardware and
architecture support
layer](../20-notes/kernel-hardware-and-architecture-support-layer.md), with
source trails in the [topic
map](../10-maps/kernel-hardware-and-architecture-support.md).

The [2026-09-02 component implementation deep
dives](../10-maps/kernel-hardware-and-architecture-support.md#component-implementation-deep-dives)
now give each of the eleven components its own operational standard, proposed
object and state-machine design, cross-ISA implementation strategy, failure
analysis, verification plan, and staged implementation. Across the independent
passes, the recommendations converge on static backend composition, immutable
prepared work, sealed generational ownership, explicit acceptance and terminal
completion, acknowledged/missing target sets, and quarantine whenever
quiescence cannot be proven. This strengthens the provisional contract but does
not supply the executable or two-ISA evidence required to resolve the inquiry.

The [nine address-translation service deep
dives](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/README.md)
further refine component 3 into separately reviewable identity, admission,
representation, transaction, context-tag, invalidation, shootdown, reclamation,
and safe-access contracts. Their shared conclusion is that
`CpuTranslationQuiescent` is evidence over an incarnation-bound frozen CPU
target set—not a synonym for IPI submission, firmware success, timeout,
CPU-number absence, privileged helper-borrow closure, or DMA quiescence. A
restrictive mapping succeeds only when that proof is joined with
`CpuAccessQuiescent` as `RestrictionQuiescent`. Reclamation is a further join
over the independently required hardware-walker, software-reader, reference,
code, IOMMU, device-drain, and lifecycle predicates. Safe user access requires
checked nonwrapping ranges, bounded architecture-gated windows, explicit
partial-fault results, copy-once immutable control snapshots, and no ambient
privileged alias to user-owned frames.

These are sharper proposed invariants and test obligations, not implementation,
hardware-conformance, liveness, or two-ISA evidence. They therefore strengthen
the inquiry without changing its open status. The [address-translation
component research
journal](../50-journal/2026-09-04-address-translation-and-protection-transitions-deep-dive.md)
records the exact newly introduced and reused evidence, cross-service
conclusions, falsifiers, and bounded remaining gaps.

The [six architecture-fault service deep
dives](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/README.md)
now refine component 9 into bounded capture, deferred decoding, capture-time
classification/promotion, crash-safe sink, escalation, and recursive-fault
contracts. Their shared protocol corrects several tempting equivalences: each
raw attempt normally seals before its separately published destructive
acknowledgement, with an explicit observation-is-acknowledgement exception for
profiled clear-on-read sources; a
small generated raw-fact classifier decides the interrupted return while the
richer decoder remains deferred; the first fatal record is the first successful
software promotion, not provably the first physical error; and a sink's seal,
adapter acceptance, reset survival, durability, authenticity, confidentiality,
freshness, and custody receipt are independent claims.

The reports also qualify escalation as generation-lifetime retained at least
once until a named persistence transition succeeds, keep evidence identifiers
separate from action capabilities, and give recursive failure a restricted sink
context rather than blessing an incomplete outer record. Optional RISC-V RERI
v1.0 is now a first-class profile alongside base-without-RERI and platform/
firmware records. These are sharper proposed invariants, not proof of bounded
MMIO response, memory survivability, safe continuation, reset persistence, or
recovery liveness. The [architecture-fault component research
journal](../50-journal/2026-09-05-architecture-faults-and-diagnostics-components-deep-dive.md)
records the exact source provenance and unresolved platform experiments.

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
