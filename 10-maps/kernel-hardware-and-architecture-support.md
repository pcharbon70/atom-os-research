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

This is full-system architecture research. Its service boundaries and
cross-ISA comparisons are not constrained by a proof-of-concept milestone,
emulator profile or selected physical machine. Target-specific implementation
decisions remain separate from the architectural claims examined here.

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
- [Research session: component implementation deep
  dives](../50-journal/2026-09-02-kernel-architecture-components-deep-dive.md)
  records the expanded source search, shared review questions, resulting
  implementation recommendations, and the continuing lack of prototype
  evidence.
- [Address-translation service deep
  dives](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/README.md)
  develop component 3 as nine separately reviewable contracts while preserving
  one integrated protection-transition lifecycle.
- [Research session: address-translation and protection-transition deep
  dive](../50-journal/2026-09-04-address-translation-and-protection-transitions-deep-dive.md)
  records the expanded primary-source search, exact source manifest,
  cross-service synthesis, and remaining proof and platform gaps.
- [Architecture-fault service deep
  dives](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/README.md)
  develop component 9 as six separately reviewable contracts while preserving
  one capture, decision, custody, and terminal-fallback transaction.
- [Research session: architecture-fault service deep
  dive](../50-journal/2026-09-05-architecture-faults-and-diagnostics-components-deep-dive.md)
  records the primary-source search, exact source manifest, cross-service
  reconciliation, and remaining platform/proof gaps.

## Internal-service research across the remaining components

The [2026-09-08 research session](../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md)
adds 55 internal-service reports. These complement the existing component-3
and component-9 decompositions, giving all eleven components deeper coverage.
The parent protocols retain authority over the integrated lifecycles; writing
the reports does not verify their proposed contracts.

- [0. Normalized boot handoff and feature discovery](../20-notes/kernel-hardware-and-architecture-components/normalized-boot-handoff-and-feature-discovery/README.md) — Separate provider lifetime, parsing, physical-resource reconciliation, discovery, and final publication. These six boundaries prevent a successful provider transaction from being mistaken for validated kernel facts.
- [1. Unsafe architecture-primitives capsule](../20-notes/kernel-hardware-and-architecture-components/unsafe-architecture-primitives-capsule/README.md) — Separate the contract inventory, privileged state, memory effects, device/wait effects and binary boundary. These are private mechanism services, never a second capability or policy layer.
- [2. Privileged entry, exit and execution context](../20-notes/kernel-hardware-and-architecture-components/privileged-entry-exit-and-execution-context/README.md) — Separate early admission, semantic frames, return authority, context ownership, nested failure and transition security. All six share the parent entry state; none duplicates component 9's capture or disposition owner.
- [4. Ordering, coherence and code publication](../20-notes/kernel-hardware-and-architecture-components/ordering-coherence-and-code-publication/README.md) — Seven distinct services separate ordinary synchronization, device completion, maintenance planning, sealing, publication, membership catch-up and retirement. Visibility, execution eligibility and reclamation are deliberately not one notion of completion.
- [5. Interrupt event fabric](../20-notes/kernel-hardware-and-architecture-components/interrupt-event-fabric/README.md) — Six services separate source identity, electrical/controller flow, bounded evidence, binding lifetime, accounting and polling handoff. Kernel IPI transport remains owned by component 7 and consumes this fabric rather than duplicating a second request protocol.
- [6. Raw time and deadline programming](../20-notes/kernel-hardware-and-architecture-components/raw-time-and-deadline-programming/README.md) — Six services distinguish source quality, arithmetic, snapshot lifetime, continuity, hardware programming and terminal outcomes. Diagnostic sampling and delay bounds are part of source qualification; timer queues, civil time and scheduling policy remain above this component.
- [7. Logical-CPU coordination and lifecycle](../20-notes/kernel-hardware-and-architecture-components/logical-cpu-coordination-and-lifecycle/README.md) — Separate CPU identity, admission, bounded remote work, removal, policy eligibility and uncertain recovery. The six services share one lifecycle authority; none independently declares a CPU safely stopped.
- [8. Protected I/O and DMA ownership](../20-notes/kernel-hardware-and-architecture-components/protected-io-and-dma-ownership/README.md) — Separate device identity, memory authority, transfer, maintenance, revocation, reset and fault custody. These seven services refine one protected-I/O lifecycle rather than inventing independent buffer or device owners.
- [10. Typed kernel-facing architecture facade](../20-notes/kernel-hardware-and-architecture-components/typed-kernel-facing-architecture-facade/README.md) — Separate object identity, admission, asynchronous custody, backend profiles, completion composition and conformance. These six services expose existing component authority rather than introducing a second hardware-management layer.

The most important joins remain open: code publication against CPU admission
and removal; CPU access closure against every alias; DMA revocation against
device and translation-cache completion; and asynchronous custody after caller
failure. The reports distinguish these proof obligations from source findings.

## Component implementation deep dives

The layer is decomposed into eleven components numbered 0 through 10. Each
deep dive recommends an implementation while preserving the same capability-
microkernel and managed-runtime boundary.

### Bootstrap and execution

- [0. Normalized boot handoff and feature
  discovery](../20-notes/kernel-hardware-and-architecture-components/normalized-boot-handoff-and-feature-discovery.md) —
  treats boot inputs as untrusted claims and seals validated, bounded,
  provenance-carrying facts into an immutable snapshot.
- [1. Unsafe architecture-primitives
  capsule](../20-notes/kernel-hardware-and-architecture-components/unsafe-architecture-primitives-capsule.md) — confines
  privileged instructions, inline assembly, and raw architecture
  representations behind reviewed safety contracts.
- [2. Privileged entry, exit, and execution
  context](../20-notes/kernel-hardware-and-architecture-components/privileged-entry-exit-and-execution-context.md) —
  develops generated frame layouts, dedicated exceptional stacks, eager state
  isolation, and hostile return-frame validation.

### Translation, publication, and events

- [3. Address translation and protection
  transitions](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions.md) —
  composes typed address-space identity and mapping admission with
  architecture-specific encoding, generation-safe context tags, monotonic
  invalidation planning, acknowledged shootdown, joined reclamation evidence,
  and bounded user access.
- [4. Ordering, coherence, and code
  publication](../20-notes/kernel-hardware-and-architecture-components/ordering-coherence-and-code-publication.md) — keeps
  compiler, memory, device, DMA, translation, and instruction-fetch ordering
  distinct and gives executable code an explicit lifecycle.
- [5. Interrupt event fabric](../20-notes/kernel-hardware-and-architecture-components/interrupt-event-fabric.md) — models
  each interrupt source with flow-specific, generation-bound delivery,
  completion, rebinding, overflow, and quarantine states.

### Time, CPUs, and protected I/O

- [6. Raw time and deadline
  programming](../20-notes/kernel-hardware-and-architecture-components/raw-time-and-deadline-programming.md) — separates
  monotonic continuity eras and conversion snapshots from one-shot hardware
  deadlines, timer queues, scheduling policy, and civil time; fired records
  remain sticky across event-sink pressure.
- [7. Logical-CPU coordination and
  lifecycle](../20-notes/kernel-hardware-and-architecture-components/logical-cpu-coordination-and-lifecycle.md) — develops
  stable CPU identity, exact start-transaction claims, immutable membership,
  an explicit stop commit/abort handshake, acknowledged request sets, and
  quarantine after incomplete removal.
- [8. Protected I/O and DMA
  ownership](../20-notes/kernel-hardware-and-architecture-components/protected-io-and-dma-ownership.md) — keeps requester,
  endpoint, interrupt, and reset scopes independent while composing
  frame-epoch-bound buffers, mappings, queues, completion attestation, and
  quiescence into an enforced revocable protocol.

### Failure evidence and common interface

- [9. Architecture faults and
  diagnostics](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics.md) — proposes a
  preallocated staging/terminal capture plane plus a distinct generated
  capture-time disposition gate and append-only policy-plane decoder, with
  synchronous return proof-gated, containment split-phase, and crash custody
  failure-domain qualified.
- [10. Typed kernel-facing architecture
  facade](../20-notes/kernel-hardware-and-architecture-components/typed-kernel-facing-architecture-facade.md) — exposes the
  components through sealed generational objects, context requirements,
  split-phase tokens, explicit feature profiles, and conformance tests.

## Component 3 service deep dives

The [local research
index](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/README.md)
is the exhaustive inventory. The nine reports separate internal ownership
without changing the parent component's caller-visible contract.

### Identity, admission, and representation

- [1. Address-space object](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/address-space-object.md) —
  binds authority, roots, ledgers, generations, activation, and teardown to one
  durable address-space incarnation.
- [2. Mapping validator](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/mapping-validator.md) —
  performs total checked admission and reserves all post-accept resources
  before visible mutation.
- [3. Page-table and protection encoder](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/page-table-and-protection-encoder.md) —
  confines raw ISA representation and publication recipes behind typed
  semantic constructors and complete mediation.

### Transaction, tag, and invalidation planning

- [4. Mapping transaction](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/mapping-transaction.md) —
  owns the interval from accepted intent through publication, invalidation,
  terminal evidence, and retained-resource transfer.
- [5. Translation-context allocator](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/translation-context-allocator.md) —
  manages finite ASID/PCID-like values as incarnation- and generation-bound
  leases with explicit rollover and fallback.
- [6. Translation invalidation planner](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/invalidation-planner.md) —
  lowers semantic hazards to immutable backend plans and permits only
  correctness-preserving strengthening.

### Completion, reclamation, and privileged access

- [7. Shootdown coordinator](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/shootdown-coordinator.md) —
  closes the activation/snapshot race, executes bounded target work, and
  distinguishes transport, local execution, CPU-translation quiescence,
  lifecycle exclusion, and incomplete completion.
- [8. Reclamation gate](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/reclamation-gate.md) —
  joins CPU translation/access, hardware-walker, software-reader, reference,
  code, IOMMU, and device-drain predicates before reuse.
- [9. Safe user-access helpers](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/safe-user-access-helpers.md) —
  combines checked ranges, bounded architecture access windows, explicit
  partial faults, copy-once control snapshots, and the absence of ambient
  privileged aliases.

## Component 9 service deep dives

The [local research
index](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/README.md)
is the exhaustive inventory. The six reports separate entry-safe capture and
decision from deferred interpretation, failure-domain-qualified custody, and
recursive terminal handling.

### Capture, interpretation, and disposition

- [1. Bounded capture routine](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/bounded-capture-routine.md) —
  generates fixed architecture-profiled raw-read and acknowledgement programs,
  seals each attempt before its associated destructive acknowledgement except for explicitly
  profiled observation-is-acknowledgement sources such as clear-on-read MMIO,
  and records loss without claiming the first physical error.
- [2. Fault decoder](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/fault-decoder.md) —
  creates deterministic append-only views whose facts retain validity,
  availability, conflict, loss, producer trust, and raw provenance.
- [3. Containment classifier and promotion](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/containment-classifier-and-promotion.md) —
  applies a tiny total raw-fact rule table in capture context, separates two
  incomparable return proofs from park/terminal outcomes, and publishes one
  immutable first-fatal software observation.

### Custody, escalation, and recursive termination

- [4. Crash-safe sink](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/crash-safe-sink.md) —
  commits a reserved-memory first record before optional adapters and keeps
  acceptance, durability, reset survival, authenticity, confidentiality,
  freshness, and custody as independent claims.
- [5. Escalation channel](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/escalation-channel.md) —
  qualifies at-least-once semantics by failure domain, separates evidence from
  action capabilities, and gates retry/reclamation on recovery epochs and
  durable receipts.
- [6. Double-fault guard](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/double-fault-guard.md) —
  uses a separately provisioned recursive record/context and an ISA-profiled
  finite halt/reset path, including the hardware-protected early-entry window.

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
- [TLB consistency](../30-sources/black-et-al-1989-tlb-consistency.md),
  [shootdown liveness](../30-sources/padon-et-al-2018-reducing-liveness-to-safety.md),
  and [conditional shootdown
  deferral](../30-sources/amit-et-al-2020-dont-shoot-down-tlb-shootdowns.md)
  ground target-set, acknowledgement, bounded-handler, safety, and liveness
  obligations.
- [Linux virtual-memory implementation
  contracts](../30-sources/linux-kernel-community-2026-virtual-memory-implementation-contracts.md)
  expose the distinct translation, software-walker, pin, and secondary-MMU
  lifetime constraints hidden by a simple “flush the TLB” abstraction.
- [Midas](../30-sources/bhattacharyya-et-al-2022-midas.md),
  [SafeFetch](../30-sources/duta-et-al-2024-safefetch.md), and
  [ret2dir](../30-sources/kemerlis-et-al-2014-ret2dir.md) establish the double-
  fetch and privileged-alias hazards that shape safe domain access.

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

### Fault evidence, containment, and custody

- [Evaluating Linux kernel crash dumping
  mechanisms](../30-sources/vazquez-cao-2006-evaluating-linux-crash-dumping.md)
  supplies a failure-injection method spanning corrupt stacks, entry context,
  DMA, device state, and dump completeness.
- [Recovery domains](../30-sources/lenharth-et-al-2009-recovery-domains.md) and
  [recovering device drivers](../30-sources/swift-et-al-2004-recovering-device-drivers.md)
  bound narrow rollback by shared state, commit points, device reconstruction,
  and indeterminate effects.
- [Ramoops](../30-sources/iordache-2021-ramoops.md) and [pstore/blk](../30-sources/linux-kernel-community-2026-pstore-crash-backends.md)
  document practical reserved-RAM and panic-time storage constraints without
  proving survival across every reset class or power-loss durability.
- [Scrash](../30-sources/broadwell-et-al-2003-scrash.md), [NIST authenticated
  encryption guidance](../30-sources/dworkin-2007-gcm-gmac.md), and
  [Memoir](../30-sources/parno-et-al-2011-memoir.md) separate dump minimization,
  confidentiality/integrity, and anti-replay state continuity.
- [Life beyond distributed
  transactions](../30-sources/helland-2007-life-beyond-distributed-transactions.md)
  motivates stable identities, deduplication, idempotence, and explicit retry
  windows for recovery escalation.

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
- [Arm RAS](../30-sources/arm-2019-ras-specification.md) and the ratified
  optional [RISC-V RERI v1.0](../30-sources/risc-v-international-2024-ras-error-record-interface.md)
  expose materially different record, overwrite, validity, and acknowledgement
  protocols that the capture profile must preserve.
- [UEFI 2.11](../30-sources/uefi-forum-2024-uefi-2-11.md) and [ACPI
  6.6](../30-sources/uefi-forum-2025-acpi-6-6.md) define CPER and APEI
  interchange/persistence mechanisms without making firmware a bounded or
  authenticated first-record dependency.

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
