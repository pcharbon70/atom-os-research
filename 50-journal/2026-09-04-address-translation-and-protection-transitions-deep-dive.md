---
title: "2026-09-04 address translation and protection transitions deep dive"
kind: journal
created: "2026-09-04"
tags:
  - architecture-support
  - literature-review
  - research-method
  - virtual-memory
aliases:
  - "Address-translation component research session"
---

# 2026-09-04 address translation and protection transitions deep dive

## Observations

This session expanded [address translation and protection
transitions](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions.md),
component 3 of the kernel hardware and architecture support layer, into nine
separately reviewable internal-service reports. The reports are ownership and
assurance boundaries inside one kernel component, not public daemons.

The central finding is that a page-table write, a TLB-maintenance instruction,
an interprocessor notification, an acknowledgement, closure of an old access
path, and permission to reclaim a resource are not interchangeable events.
The proposed design makes them typed stages of one accepted mapping operation:

- a durable address-space object binds authority, root interpretation,
  semantic mappings, context-tag leases, activation, and teardown;
- a total validator checks both destination and source authority, range and
  page geometry, physical provenance, aliases, final effective leaf meaning,
  and all resources needed after acceptance;
- an encoder is the sole constructor and decoder of raw architecture entries,
  but cannot decide policy or broaden authority;
- a transaction owns every transient and resource from the acceptance point
  through exactly-once terminal evidence;
- finite ASID/PCID-like fields are cache-tag leases held in a scope-keyed
  binding set, with per-target root/profile identity, namespace and lease
  generations, machine-specific sharing scope, rollover, and a flush-on-switch fallback;
- a monotonic planner compiles semantic hazards into immutable ISA-, revision-,
  feature-, virtualization-, and erratum-specific maintenance programs;
- a shootdown coordinator separates durable request ownership, notification,
  user-return closure, local maintenance, aggregate CPU-translation quiescence,
  and CPU-lifecycle exclusion;
- a reclamation gate joins independently required CPU translation/access,
  hardware-walker, software-reader, reference, code, IOMMU, and device-drain
  proofs before reuse; and
- safe user access uses capability-bound guards, nonwrapping ranges, bounded
  SMAP/PAN/SUM-like windows, exact fault recovery, explicit partial results,
  copy-once control snapshots, and no routine privileged alias of user-owned
  frames.

The research also corrected an overly strong interpretation of address-space
ownership. One protection-domain incarnation is the lifecycle and mutation
owner, but several execution contexts within that domain may share and
activate the address space. The sources do not support a one-thread/one-root
restriction.

All of these conclusions remain proposed architecture. The session did not
implement a page-table backend, execute a fence, send an IPI, boot hardware, or
prove a state machine.

## Environment

- Repository: `atom-os-research`
- Research date: 2026-09-04
- Host time zone: America/Toronto
- Activity: scientific-paper, specification, engineering-article, and kernel-
  documentation review; cross-source synthesis; archive editing
- Target kernel: no Atom implementation exists or was built
- Architecture scope: x86-64, Arm A-profile, and RISC-V supervisor translation
  were compared; none was executed
- Hardware, firmware, hypervisor, emulator, or IOMMU: none exercised
- BEAM runtime: none built or executed
- Prototype evidence: none produced
- Workspace handling: research changes were isolated on a dedicated worktree
  because the primary checkout contained unrelated user work

## Evidence

### Question and operational standard

The research asked:

> What internal services and proof boundaries let an authorized mapping change
> become architecturally complete across concurrent CPUs, and let the kernel
> reuse its dependent resources or access domain memory without ambient
> authority?

A recommendation was admitted only when it named the trust boundary, object
owner, authority, acceptance point, architecture/profile dependency, local and
remote completion evidence, failure result, resource lifetime, and a plausible
falsification method. Claims based on one ISA or implementation were retained
as profile-specific precedent rather than generalized silently.

### Search and review method

The existing parent note supplied nine proposed services and the initial
claims to challenge. Three parallel research passes examined:

1. address-space identity, mapping admission, and protected descriptor
   construction;
2. mapping transactions, finite context tags, and invalidation planning; and
3. cross-CPU completion, reclamation, and privileged user-memory access.

Searches prioritized current official Intel, Arm, RISC-V, Linux, and seL4
documentation plus primary systems/security papers. Historical operating-
system papers supplied design lineage; contemporary research supplied
scalability, formal-model, security, and optimization evidence. Articles and
maintainer material were used for implementation hazards and operational
practice. Search snippets and abstracts located sources but did not support
detailed claims on their own.

Each substantively new work received an evidence-focused source note. Existing
source notes were reused when they already recorded adequate bibliographic
identity, findings, limitations, and relevance. The passes were reconciled
against the parent component, neighboring CPU/interrupt/code/DMA components,
the open hardware-contract inquiry, and the repository's distinction between
reported evidence and unverified proposal.

### Component reports

The [local component index](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/README.md)
is the exhaustive inventory:

1. [Address-space object](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/address-space-object.md)
2. [Mapping validator](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/mapping-validator.md)
3. [Page-table and protection encoder](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/page-table-and-protection-encoder.md)
4. [Mapping transaction](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/mapping-transaction.md)
5. [Translation-context allocator](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/translation-context-allocator.md)
6. [Translation invalidation planner](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/invalidation-planner.md)
7. [Shootdown coordinator](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/shootdown-coordinator.md)
8. [Reclamation gate](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/reclamation-gate.md)
9. [Safe user-access helpers](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions/safe-user-access-helpers.md)

### Cross-service reconciliation

The independent passes exposed and resolved these boundary questions in the
written proposals:

- object identity, capability generation, nominal mapping incarnation, mutation
  sequence, context-tag incarnation (including namespace and lease
  generations), scope-specific target binding, CPU incarnation, request-slot
  generation, reference- and execution-admission epochs, translation-catch-up
  state incarnation, code-publication state incarnation/generation, and
  terminal-publication epoch are separately typed; exact
  request, operation, plan, target-slot, and incarnation tuples prevent
  acknowledgement replay;
- root address plus numeric ASID/PCID is hardware representation, not durable
  security identity;
- final descriptor meaning is decoded from the `EffectiveLeaf` only after all
  authority ceilings and profile checks (and any explicitly requested future
  attenuation); the baseline rejects implicit attenuation and empty leaves, so
  changed bits cannot accidentally become a table link;
- additive changes are not portably “no invalidation,” because negative-
  translation caching rules differ by profile;
- target selection and invalidation instruction scope are orthogonal;
- queue overflow can conservatively widen an invalidation but cannot drop work;
  bounded coalescing retains an exact covered-operation set, dominance proof,
  and late-evidence validation record;
- CPU, executable, IOMMU/DMA, device, and diagnostic alias writers serialize
  through one canonical-physical-extent/backing-lineage reservation ledger;
  `PendingAdd` and `RetiringOldAccess` remain conflicts until the relevant
  completion predicates actually close;
- returned mapping references use a generation-checked output-grant template,
  so add or replace authority cannot silently mint protect, unmap, inspection,
  or broader access rights;
- under enforced-exclusive DMA ownership, an installed IOVA relation remains
  dormant/no-access while CPU ownership is live; only the transfer operation
  activates device rights after CPU restriction quiescence;
- entering CPU publication and `UserAccessGuard` borrow publication each form a
  two-sided handshake with mutation-sequence observation. Activation also
  binds the execution-admission epoch and persistent translation/code-
  publication states, closing the active-set snapshot, late executable-
  eligibility, and post-snapshot privileged-borrow races;
- notification, IPI submission, and standardized SBI RFENCE success are
  transport evidence, not proof that a target executed its local program;
- early acknowledgement can at most prove `CpuUserReturnClosed` under strict
  return gates; it does not prove helper-borrow drain, CPU translation
  quiescence, or table-page safety;
- restrictive success is `RestrictionQuiescent`, the conjunction of
  `CpuTranslationQuiescent` and `CpuAccessQuiescent`;
- CPU translation completion does not discharge hardware-table-walker,
  software-reader, reference, device, DMA, or executable-code obligations;
- address-space close is its own checked lifecycle product: success means the
  exact incarnation reached `Dead` after mappings, roots, activations, helper
  borrows, context bindings, both persistent catch-up states and their owned
  program/pin resources, code, DMA, and references all discharged or moved to
  named retirement/quarantine owners;
- RCU and hazard pointers can manage instrumented software readers but do not
  flush uninstrumented hardware agents; and
- pinning user pages stabilizes backing lifetime, not mutable contents, so
  privileged decisions consume one kernel-owned control snapshot.

### Cross-service hardening found during consistency audit

The final protocol pass tightened several claims that were individually
plausible but unsafe when composed:

- class-`L` finalization is deferred until acceptance, atomically closes
  mapping, activation, helper-borrow, reference, and code-publication
  admission, and freezes every already-accepted participant;
- context-tag target history is cumulative, interrupted root installation has
  an explicit `LoadingRoot` state and full slot/guard incarnation, and tag
  reuse waits for the reclamation gate rather than a flush bitmap alone;
- every target carries its complete nominal root/tag or temporary-alias
  observer-binding set, and target, program, slot, and requirement maps must
  have exactly matching keys and digests;
- the address-space writer token remains held through one atomic terminal,
  ownership, observer-gate, and reclamation-reservation transfer; cancellation
  compensation is subordinate to that same owner;
- authority-bearing results—including mapping-reference grants, returned input
  references, address-space sealing, and teardown-recovery facets—live in
  stable one-shot extraction slots, so repeated polling cannot duplicate a
  capability;
- existing-relation effects distinguish a caller-supplied `MappingRef` from
  authority delegated by address-space close or code seal; delegated effects
  complete into their parent and never fabricate a caller return slot;
- stable-even translation publication installs an actual immutable catch-up
  state owning executable maintenance programs and binding/root pins, not only
  a plan digest; history remains pinned or is replaced by a conservative
  dominating program until every lagging CPU is covered;
- deadline expiry reports progress only; an authorized recovery decision may
  quarantine, while late evidence advances a separate generation-bound
  recovery record without rewriting the immutable terminal;
- code sealing preserves a persistent write-admission deny and joins every CPU,
  DMA/device, diagnostic, temporary-alias, and frame-authority writer proof
  before hashing the exact page-granular extent; and
- executable publication joins sealed-image authority, an address-space range
  capability, and a scheduler-issued complete target-set witness under the
  same close-serialization gate. Its final RX leaf can become live only while
  an exact generation-bound execution suspension has drained the whole target
  address space; that suspension remains held through every CPU's fetch
  synchronization and is released atomically with `PublishedCode`. Runtime
  dispatch-table absence is therefore never mistaken for hardware
  unreachability.
- executable publication also maintains a persistent nominal generation state
  containing the typed fetch-reachable version/extent set, actual per-profile
  catch-up programs, pin dispositions, and per-CPU observations. Late CPU
  eligibility/migration must catch up before execution, retirement transfers
  pins exactly once through a `RetiringBy` state, and address-space close
  freezes and disposes the whole registry.

### Failure and liveness boundary

Timeout means that proof is missing. It can trigger suspicion, diagnostic
capture, retry, or an authorized CPU/device isolation action, but cannot prove
that the timed-out agent will never use stale state. Deadline expiry therefore
returns progress without changing ownership. Only a separate recovery-policy
decision that completion cannot be established publishes a named incomplete
result with its dependent objects transferred to the recorded quarantine. A
later incarnation-matched proof can advance that teardown ledger without
rewriting the exactly-once terminal result.

Safety is required without fairness: no execution may reuse an object while a
required proof is absent. Eventual completion additionally assumes that a live
target eventually receives work, exits longer masked regions, runs a bounded
handler, and that CPU/device lifecycle eventually yields an explicit terminal
outcome. Those assumptions must appear in the executable model rather than be
hidden in an informal “IPI always works” premise.

### Evidence boundary

This was a literature and architecture session. It did not:

- implement or type-check any proposed object or API;
- model-check the activation/shootdown/reclamation product state;
- test compiler ordering, architecture page-table litmus cases, or generated
  assembly;
- validate a CPU revision, erratum, firmware RFENCE adapter, hypervisor, IOMMU,
  or device completion contract;
- measure map, unmap, TLB, IPI, rollover, copy, or reclamation latency;
- force ASID/PCID wrap, CPU hotplug, queue overflow, partial user-copy faults,
  or late acknowledgements on a prototype;
- demonstrate hardware-walker quiescence before page-table retype; or
- run compiled BEAM code or process-local tracing collection over the proposed
  memory system.

Official specifications can serve as a reproducible normative basis only when
their exact editions and profiles are pinned. The reused Arm A-profile source
note currently resolves a mutable `latest` URL, so this session treats its Arm
claims as provisional architecture guidance rather than as a pinned normative
baseline. Paper measurements apply only to the reported systems and hardware.
Linux and other mature implementations supply valuable precedent, not proof
that Atom's synthesis is correct. The reports deliberately retain unresolved
questions and developing maturity.

The search also found no primary paper that specifies the complete finite
ASID/PCID allocator protocol proposed here across sharing scopes, concurrent
installation, rollover, CPU hotplug, failure quarantine, and eventual reuse.
The allocator report therefore labels its Linux and ISA evidence as precedent
and leaves the combined protocol as an explicit model-checking obligation.

### Unresolved source-pinning item

- Record the exact Arm Architecture Reference Manual issue, stable artifact or
  URL, architecture profile, and supporting sections for every Arm ASID, TLBI,
  break-before-make, PAN, and barrier claim; then re-audit the affected reports.
  Do not freeze an Atom Arm profile against the mutable `latest` reference.

## Source manifest

### Newly introduced sources

- [Machine-independent virtual memory management](../30-sources/rashid-et-al-1987-machine-independent-virtual-memory.md) — semantic VM objects and a machine-dependent translation boundary.
- [A scalable virtual-memory HAT layer](../30-sources/balan-gollhardt-1992-scalable-virtual-memory-hat-layer.md) — context activation, mapping, and processor-accounting precedent.
- [TLB consistency: a software approach](../30-sources/black-et-al-1989-tlb-consistency.md) — queued remote invalidation, bounded address lists, acknowledgements, and overflow strengthening.
- [Ephemeral mapping management](../30-sources/elmeleegy-et-al-2005-ephemeral-mapping-management.md) — explicit ownership and lifetime for bounded temporary kernel mappings.
- [SecVisor retrospective](../30-sources/franklin-et-al-2008-secvisor-retrospective.md) — physical executable-page provenance and cross-alias mediation.
- [RadixVM](../30-sources/clements-et-al-2013-radixvm.md) — range concurrency, per-core table tradeoffs, target tracking, and delayed reference release.
- [ret2dir](../30-sources/kemerlis-et-al-2014-ret2dir.md) — privileged direct-map aliases as a user/supervisor isolation bypass.
- [Nested Kernel](../30-sources/dautenhahn-et-al-2015-nested-kernel.md) — complete mediation of page-table and isolation machinery within privileged software.
- [HATRIC](../30-sources/yan-et-al-2017-hatric.md) — hardware translation coherence and dependency-tracking alternative.
- [Reducing liveness to safety](../30-sources/padon-et-al-2018-reducing-liveness-to-safety.md) — TLB shootdown safety/liveness modeling, fairness, and atomic-region sensitivity.
- [seL4 RISC-V page-map defect](../30-sources/sel4-foundation-2020-risc-v-page-map-defect.md) — evidence that rights attenuation can change final descriptor interpretation.
- [Don't shoot down TLB shootdowns](../30-sources/amit-et-al-2020-dont-shoot-down-tlb-shootdowns.md) — conditional batching, deferral, early acknowledgement, and required return/uaccess gates.
- [Secure memory management](../30-sources/achermann-et-al-2020-secure-memory-management.md) — typed, authority-aware memory-management model, executable specification, and scoped prototype evaluation.
- [Midas](../30-sources/bhattacharyya-et-al-2022-midas.md) — page-table-mediated double-fetch prevention and measured overhead.
- [SafeFetch](../30-sources/duta-et-al-2024-safefetch.md) — compiler-instrumented, byte-granular replay of first-fetched user data on later overlapping fetches.
- [Practical page-table verification](../30-sources/asterinas-community-2025-practical-page-table-verification.md) — typed page purposes, representability, cursor invariants, and flat/tree refinement.
- [Linux arm64 ASID context management](../30-sources/linux-kernel-community-2026-arm64-asid-context-management.md) — current generation/bitmap/reserved-active tag-allocation precedent.
- [Linux virtual-memory implementation contracts](../30-sources/linux-kernel-community-2026-virtual-memory-implementation-contracts.md) — current teardown, table-walker, user-copy, pinning, and secondary-MMU lifecycle rules.

### Reused sources

- [Protection of information in computer systems](../30-sources/saltzer-schroeder-1975-protection-information.md) — complete mediation, least privilege, fail-safe defaults, and economy of mechanism.
- [Read-copy update](../30-sources/mckenney-slingwine-1998-read-copy-update.md) — software-reader grace-period precedent and its scope.
- [Hazard pointers](../30-sources/michael-2004-hazard-pointers.md) — explicit lock-free software-reference publication and reclamation.
- [Unreliable failure detectors](../30-sources/chandra-toueg-1996-failure-detectors.md) — distinction between timing suspicion and terminal exclusion.
- [From L3 to seL4](../30-sources/elphinstone-heiser-2013-l4-lessons.md) — minimal capability-mediated address-space mechanisms and policy separation.
- [Translation validation for a verified OS kernel](../30-sources/sewell-et-al-2013-translation-validation.md) — generated-code checking across the verified-kernel compiler gap.
- [CertiKOS](../30-sources/gu-et-al-2016-certikos.md) — contextual refinement and multicore layer-specification precedent.
- [Optimizing TLB shootdown](../30-sources/amit-2017-optimizing-tlb-shootdown.md) — page/context thresholds, target tracking, and workload-specific cost evidence.
- [Least-privilege memory protection](../30-sources/achermann-et-al-2019-least-privilege-memory-protection.md) — separate translator-configuration and translated-memory authority.
- [Arm instruction-fetch semantics](../30-sources/simner-et-al-2020-arm-instruction-fetch.md) — executable publication/retirement obligations beyond data translation.
- [Relaxed virtual memory](../30-sources/simner-et-al-2022-relaxed-virtual-memory.md) — formal page-table mutation, invalidation, barrier, and walker interactions.
- [Scalable page-table and TLB management](../30-sources/gao-et-al-2024-scalable-page-table-tlb.md) — NUMA replication, sharer tracking, and shootdown scalability.
- [Intel VT-d architecture](../30-sources/intel-2024-vt-d-architecture.md) — device-translation invalidation and completion mechanisms.
- [Arm SMMUv3 architecture](../30-sources/arm-2025-smmuv3-architecture.md) — device translation, command completion, and protected-I/O lifecycle mechanisms.
- [RISC-V supervisor binary interface](../30-sources/risc-v-international-2025-supervisor-binary-interface.md) — remote-fence transport and fallible firmware boundary.
- [Intel system-programming documentation](../30-sources/intel-2026-system-programming-documentation.md) — x86 paging, PCID, invalidation, SMAP, and ordering rules.
- [Arm A-profile documentation](../30-sources/arm-2026-a-profile-system-architecture-documentation.md) — Arm translation regimes, ASIDs, TLBI, break-before-make, PAN, and barriers.
- [RISC-V privileged architecture](../30-sources/risc-v-international-2026-privileged-architecture.md) — `satp`, ASIDs, `SFENCE.VMA`, PTE interpretation, SUM, and optional translation features.
- [RISC-V IOMMU architecture](../30-sources/risc-v-international-2026-iommu-architecture.md) — device translation caches, invalidation, and completion.
- [Linux low-level core APIs](../30-sources/linux-kernel-community-2026-low-level-core-apis.md) — portable cache/TLB effect and low-level lifecycle precedent.
- [seL4 reference manual](../30-sources/sel4-foundation-2026-reference-manual.md) — typed capability-mediated roots, tables, frames, and mappings.
- [Serval](../30-sources/nelson-et-al-2019-serval.md) — symbolic verification of page-table representation and systems invariants.

## Threads

- Establish a machine-readable profile that pins architecture edition, CPU
  revision, translation regime, enabled extensions, virtualization layer,
  firmware adapter, and relevant errata.
- Decide whether hardware-walker completion can be established directly on the
  first two target machines or requires a conservative protected table-page
  epoch.
- Determine whether the baseline can exclude user-owned frames from all
  routine supervisor aliases on every bootstrap, debug, and crash path.
- Reconcile the nine reports into one executable state machine before allowing
  range-concurrent mutations or deferred acknowledgements.

## Follow-ups

- Implement a deliberately slow flat reference mapper and plan-dominance
  oracle before an optimized backend.
- Model CPU activation, mutation, bounded mailboxes, hotplug, timeout, and
  reclamation together under weak memory and explicit fairness assumptions.
- Port architecture virtual-memory litmus tests and add Atom-specific
  generation/late-acknowledgement cases.
- Test one x86-64 and one materially different Arm or RISC-V backend on real
  hardware, including documented errata and firmware behavior.
- Add exhaustive fault injection for partial user copy, unmap races, queue
  overflow, ASID/PCID rollover, walker delay, DMA delay, and code retirement.
- Measure tail latency, IPI amplification, retained/quarantined bytes, access-
  window duration, and BEAM arena-growth behavior before admitting
  optimizations.
