---
title: "2026-09-02 kernel architecture components deep dive"
kind: journal
created: "2026-09-02"
tags:
  - architecture-support
  - literature-review
  - operating-systems
  - research-method
aliases:
  - "Kernel architecture component research session"
---

# 2026-09-02 kernel architecture components deep dive

## Observations

This session expanded every component in the [kernel hardware and architecture
support layer](../20-notes/kernel-hardware-and-architecture-support-layer.md)
into an independently useful implementation synthesis. The decomposition has
eleven components numbered 0 through 10, not ten components numbered 1 through
10.

The strongest common finding is that the architecture boundary should normalize
**semantic completion**, not hardware representation. Portability does not mean
making page tables, interrupt controllers, timers, CPU-start mechanisms, or
IOMMUs appear identical. It means that callers can rely on the same authority,
ownership, generation, context, failure, and completion rules while each
backend performs the architecture-specific protocol required to establish
them.

The research converged on these implementation choices:

- boot inputs are untrusted provider claims normalized once into a bounded,
  immutable `BootSnapshot` with provenance and contradiction handling;
- all direct privileged operations and inline assembly are confined to a small
  unsafe architecture-primitives capsule;
- entry and return use generated layout contracts, dedicated exceptional
  stacks, eager isolation of enabled context state, and fuzzed return
  validation;
- mapping changes are transactions around durable typed `Mapping` identities,
  centralized publication, generation-safe address-space tags, and explicit
  local/remote quiescence;
- compiler, ordinary memory, device, DMA, translation, and instruction-fetch
  ordering remain separate contracts;
- interrupts are flow-specific, generation-bound state machines whose hard
  path only acknowledges/masks and publishes a bounded event;
- raw time and deadline programming separates counter facts, conversion-
  snapshot generations, continuity eras, scheduler policy, and wall-clock time,
  using one canonical per-CPU channel and sticky token terminals across fire,
  cancellation, rebase, discontinuity, and channel failure;
- logical CPUs have a staged lifecycle with stable identity, exact start-
  transaction claims, immutable membership, explicit stop commit/abort,
  acknowledged request sets, and quarantine on incomplete removal;
- protected I/O keeps requester, endpoint, interrupt, and reset scopes
  independent, binds DMA leases to buffer-access and global frame epochs, and
  distinguishes enforced exclusion from trusted typestate; IOMMU address
  filtering alone is not sufficient containment, and reset execution remains
  distinct from manager-takeover authority;
- architecture faults use a preallocated two-plane design: tiny staging capture
  in hard entry, followed by operational copy or atomic terminal promotion and
  typed decoding/recovery policy outside entry; and
- the kernel-facing facade is statically composed from sealed generational
  objects and split-phase operation tokens, with a fake backend and optional
  profiles rather than one opaque HAL.

These remain architecture proposals. No component was implemented or benchmarked
in this session.

## Environment

- Repository: `atom-os-research`
- Research date: 2026-09-02
- Host time zone: America/Toronto
- Activity: literature search, official-specification review, synthesis, and
  archive editing
- Kernel target: none selected or built
- ISA target: x86-64, AArch64, and RISC-V compared at the contract level; none
  executed
- Firmware/boot target: UEFI, ACPI, Devicetree, Limine, PSCI, and SBI considered
  as explicit provider profiles; none executed
- BEAM runtime: none built or executed
- Hardware, hypervisor, or emulator: none used
- Markdown viewing: the parent architecture note was opened with MarkText in
  accordance with repository workflow
- Local changes: Markdown notes, source records, navigation, and journal only

## Evidence

### Method

The work began with the responsibilities, invariants, and cross-component
protocols in the existing architecture synthesis. Research was then divided
into four independent passes:

1. boot normalization, unsafe primitives, and entry/context;
2. translation, ordering/code publication, and interrupt events;
3. raw time, CPU lifecycle, and protected I/O/DMA; and
4. architecture faults and the typed facade.

Each pass searched current official architecture or project documentation,
primary systems papers, and engineering articles or maintainer guidance. Search
results, abstracts, and snippets located candidate works but were not used as
evidence for detailed claims. Substantively used new works received individual
records in the [source index](../30-sources/README.md). Existing source notes
were reused when they already preserved adequate metadata, method, findings,
and limits.

The component recommendations were checked against the established upper
boundary in the [minimal privileged kernel](../20-notes/minimal-privileged-kernel-layer.md)
and against the required managed-runtime boundary in [BEAM, ERTS, and OTP
principles](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md).
This prevented the deep dives from moving capability policy, BEAM instructions,
process-local tracing collection, or OTP supervision into architecture code.

### Consistency and provenance review

After drafting, independent passes reviewed all component seams and all thirty
new source records. The consistency review found and the documents corrected:

- machine-wide required features versus incarnation-bound per-CPU evidence;
- address-space activation and executable-mapping races;
- paired per-CPU and per-context ownership for extended processor state;
- Arm-alias-safe executable publication ordering;
- single-owner executable publication with pre-mutation rejection,
  split-phase completion, cancellation drainage, and quarantine;
- staging-first fault capture, proof-gated terminal capture, narrow NMI/fatal
  contexts, and recyclable versus terminal records;
- interrupt source versus binding generations, aggregate kernel/backend object
  ownership, and kernel-owned rate policy;
- clock-era versus conversion-publication generations and exact deadline-token
  replacement during comparator rebase;
- late CPU-start claims and the stop commit/abort handshake; and
- strict DMA alias enforcement, buffer-access and frame-authority epochs,
  completion attestation, independent reset scope and authority, complete
  close/reacquire states, pre-effect queue rejection, and dependency-ordered
  revocation.

The provenance pass verified source identities, links, derived-work paths, and
duplicate coverage. It corrected Tock's `BUSY` callback exception, one USENIX
page range, mutable versus pinned specification URLs, Linux RAS publication/
confidentiality wording, and three RISC-V authorship records. These checks do
not substitute for target implementation or hardware qualification.

### Component documents

#### Bootstrap and execution

- [Normalized boot handoff and feature discovery](../20-notes/normalized-boot-handoff-and-feature-discovery.md)
- [Unsafe architecture-primitives capsule](../20-notes/unsafe-architecture-primitives-capsule.md)
- [Privileged entry, exit, and execution context](../20-notes/privileged-entry-exit-and-execution-context.md)

#### Memory, publication, and events

- [Address translation and protection transitions](../20-notes/address-translation-and-protection-transitions.md)
- [Ordering, coherence, and code publication](../20-notes/ordering-coherence-and-code-publication.md)
- [Interrupt event fabric](../20-notes/interrupt-event-fabric.md)

#### Time, CPUs, and I/O

- [Raw time and deadline programming](../20-notes/raw-time-and-deadline-programming.md)
- [Logical-CPU coordination and lifecycle](../20-notes/logical-cpu-coordination-and-lifecycle.md)
- [Protected I/O and DMA ownership](../20-notes/protected-io-and-dma-ownership.md)

#### Failure evidence and common interface

- [Architecture faults and diagnostics](../20-notes/architecture-faults-and-diagnostics.md)
- [Typed kernel-facing architecture facade](../20-notes/typed-kernel-facing-architecture-facade.md)

### Source families

The source trail includes:

- current Intel, Arm, and RISC-V architecture specifications;
- UEFI, ACPI, Devicetree, Limine, PSCI, SBI, interrupt-controller, and platform
  interface documentation;
- Linux entry, timekeeping, interrupt, CPU-hotplug, DMA, RAS, and low-level API
  engineering guidance;
- L4/seL4, CertiKOS, OSKit, Think, SVA, Tock, Multikernel, Dune, and Arrakis
  architecture evidence;
- work on translation validation, TLB shootdowns, virtual-memory models,
  instruction publication, weak memory, and kernel concurrency;
- CleanQ, Thunderclap, least-privilege memory protection, direct-I/O
  protection, and recoverable-driver research; and
- Kdump and failure-detection work for preserving evidence without converting
  suspicion into a false containment claim.

Articles and maintainer documents were used to expose implementation pitfalls
and current practice. They did not override a normative architecture manual or
a primary experiment.

### Cross-pass review questions

Every component was challenged with the same questions:

- Which caller or capability may start this transition?
- Which object owns every mutable piece of state?
- What can run in boot, thread, hard-entry, NMI-like, or crash context?
- At what exact point can submission no longer be rejected without mutation?
- What evidence establishes local, remote-CPU, device, firmware, or IOMMU
  completion?
- What happens to ownership after rejection, timeout, cancellation, partial
  completion, or generation change?
- Which operation can allocate, block, recurse, or wait for another CPU?
- How is a stale interrupt, IPI, timer, DMA completion, or firmware response
  rejected after object replacement?
- What raw architecture fact is retained when normalization is incomplete or a
  decoder changes?
- Can the same mandatory contract be implemented honestly on two materially
  different ISAs?
- Which feature absence must reject the configuration rather than degrade a
  security claim?
- Does any proposed mechanism accidentally move BEAM runtime or OTP policy into
  privileged code?

This review produced a common vocabulary of sealed objects, scoped
generations, immutable prepared work, acceptance tokens, exactly-once terminal
results, completion epochs, acknowledged/missing target sets, and quarantine.

### Evidence boundary

This was a literature and design session. It did not:

- build or boot a kernel;
- execute firmware, a boot protocol, or an architecture backend;
- inspect generated assembly from a proposed implementation;
- run memory-model or virtual-memory litmus tests;
- measure entry, mapping, publication, interrupt, timer, IPI, CPU-lifecycle,
  DMA, fault-capture, or facade cost;
- inject a CPU, memory, device, IOMMU, or firmware fault;
- verify an executable state machine or proof; or
- demonstrate compiled BEAM execution or process-local tracing collection over
  the proposed layer.

Therefore:

- architecture and interface specifications are normative only for their
  pinned versions and optional profiles;
- research-paper measurements apply to their evaluated implementations and
  hardware;
- mature-kernel and project guidance supplies precedent, not proof of
  minimality;
- type-safe interfaces reduce misuse but do not prove hardware protocol
  completion;
- a successful return from firmware or a fault handler is not containment
  evidence by itself; and
- the recommended state machines and “best implementation” choices are
  cross-source proposals awaiting prototype evidence.

## Threads

- [Kernel hardware and architecture support map](../10-maps/kernel-hardware-and-architecture-support.md)
  now routes through the individual component implementations and their source
  families.
- [Kernel hardware-contract inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
  remains open and carries the falsification criteria.
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
  owns the upper-layer capability, invocation, temporal-authority, teardown,
  and recovery obligations that consume these completions.

## Follow-ups

1. Turn the common object/transition vocabulary into executable state-machine
   models before selecting data structures.
2. Implement a deterministic fake backend that can inject every rejection,
   delay, duplicate, stale generation, partial target set, cancellation, and
   terminal failure described by the notes.
3. Select the first virtual ISA/platform profile only after defining its pinned
   firmware, architecture, interrupt, timer, and DMA assumptions.
4. Implement the smallest single-CPU vertical slice: boot snapshot, primitive
   capsule, entry/return, protection, one-shot deadline, bounded event, crash
   record, and typed facade.
5. Inspect generated code and measure local paths before adding SMP.
6. Add cross-CPU mapping, code publication, and lifecycle completion, then
   protected I/O and DMA, with quarantine as the default incomplete state.
7. Port the mandatory semantic suite to a second materially different ISA and
   revise any contract that accidentally encoded the first backend.
8. Run a compiled-BEAM allocation, process-local tracing-GC, scheduling, code
   loading, and supervision workload above the minimal kernel to derive real
   latency and resource budgets.
