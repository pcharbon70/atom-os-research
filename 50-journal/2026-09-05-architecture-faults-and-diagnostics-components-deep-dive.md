---
title: "2026-09-05 architecture faults and diagnostics components deep dive"
kind: journal
created: "2026-09-05"
tags:
  - architecture-support
  - diagnostics
  - fault-containment
  - literature-review
  - research-method
aliases:
  - "Architecture-fault component research session"
---

# 2026-09-05 architecture faults and diagnostics components deep dive

## Observations

This session expanded [architecture faults and
diagnostics](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics.md),
component 9 of the kernel hardware and architecture support layer, into six
separately reviewable internal-service reports. These are ownership and
assurance boundaries inside the architecture-fault component, not public
daemons and not ordinary OTP supervisors.

The main result is a staged fault transaction whose evidence and authority
claims do not collapse into one “handled” Boolean:

1. component 2 establishes architecture entry, stack, frame, and nesting state;
2. a generated bounded routine normally copies and seals raw attempt(s) before
   a separately published destructive acknowledgement, while explicitly
   profiled clear-on-read sources record observation itself as acknowledgement;
3. a tiny generated capture-time classifier uses only raw/profile facts,
   acknowledgement state, and entry-safe snapshots to select return, park, or
   terminal disposition;
4. terminal promotion preserves the first successfully promoted software
   observation, while hardware overwrite flags retain uncertainty about the
   first physical error;
5. the deferred policy-plane decoder appends provenance-carrying normalized
   views without changing the original entry decision;
6. a mandatory reserved-memory first record precedes optional firmware,
   device, capture-environment, or forensic adapters;
7. escalation separates retained from durable custody, evidence identifiers
   from action capabilities, and at-least-once delivery from exactly-once
   effects; and
8. one independently provisioned recursive record can explain an interrupted
   outer transaction before an architecture/profile-specific terminal leaf.

The cross-report audit removed several unsafe shortcuts: `NoneKnown` is not
proof that no external effect occurred; a rich decoded view cannot sit on the
hard-entry return dependency; an interrupted outer writer cannot be assumed to
return and mark torn bytes safe; a checksum is neither authenticity nor
freshness; a fixed operation count cannot bound a wedged MMIO access; and
software nesting state cannot protect the hardware entry window before the
first depth store.

All results remain proposed architecture. No Atom kernel, decoder, classifier,
sink, recovery service, emulator campaign, hardware error, reset-survival test,
or model check was executed.

## Environment

- Repository: `atom-os-research`
- Research date: 2026-09-05
- Host time zone: America/Toronto
- Activity: scientific-paper, ratified-specification, official architecture,
  kernel-documentation, source-code, and engineering-practice review;
  cross-source synthesis; archive editing
- Target kernel: no Atom implementation exists or was built
- Architecture scope: x86-64, Arm A-profile, and RISC-V privilege/RAS profiles
  were compared; none was executed
- Firmware and interchange scope: UEFI CPER and ACPI APEI/BERT/ERST/EINJ were
  reviewed; no firmware was called
- Hardware, hypervisor, emulator, IOMMU, reset controller, or persistent medium:
  none exercised
- BEAM runtime: none built or executed
- Prototype evidence: none produced
- Workspace handling: research changes were isolated on a dedicated worktree
  because the primary checkout contained unrelated user work

## Evidence

### Question and operational standard

The research asked:

> What internal services let component 9 preserve the strongest defensible
> architecture-fault evidence and containment result when entry, decoding,
> persistence, policy, or the fault mechanism itself can fail?

A recommendation was admitted only when it named its trust and privilege
boundary, owner, exact input/output object, bounded or explicitly unbounded
dependency, architecture/profile variation, failure result, authority source,
custody/persistence domain, information-loss behavior, and a plausible
falsification method. Producer labels such as corrected, recoverable,
restartable, or containable were treated as evidence inputs rather than recovery
authority.

### Search and review method

The existing parent note supplied six proposed services and the claims to
challenge. Three parallel research passes examined:

1. entry-safe raw capture, architecture record access, recursive failure, and
   stack/terminal behavior;
2. versioned decoding, evidence provenance, containment classification,
   promotion, and memory-error recovery; and
3. crash storage, reset/power survival, confidentiality/freshness, escalation,
   delivery semantics, and recovery-service failure.

Searches prioritized current official Intel, Arm, RISC-V, UEFI, ACPI, Linux,
and seL4 material plus primary systems, reliability, security, and distributed-
systems papers. Historical papers were retained when they supplied direct
mechanism or experimental evidence and were labeled as historical. Search
snippets and abstracts located candidates but did not support detailed claims
on their own.

Each substantively new work received an evidence-focused source note. Existing
source notes were reused when they already preserved adequate identity,
findings, relevance, and limits. A final consistency audit checked phase
ordering, immutable-state claims, recursive control flow, source fidelity,
cross-ISA terminology, and every local link.

### Component reports

The [local component
index](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/README.md)
is the exhaustive inventory:

1. [Bounded capture routine](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/bounded-capture-routine.md)
2. [Fault decoder](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/fault-decoder.md)
3. [Containment classifier and promotion](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/containment-classifier-and-promotion.md)
4. [Crash-safe sink](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/crash-safe-sink.md)
5. [Escalation channel](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/escalation-channel.md)
6. [Double-fault guard](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/double-fault-guard.md)

### Cross-service reconciliation

- `RawStagingSlot` attempts, acknowledgement state, terminal promotion,
  recursive record, crash-capsule sections, and escalation custody have
  distinct state machines; “sealed,” “committed,” and “durable” are not
  synonyms.
- Every raw attempt is immutable after publication. Clear-on-read sources are
  an explicit exception where observation itself acknowledges the source and
  therefore cannot support narrow recovery.
- Optional RISC-V RERI v1.0 is modeled separately from the mandatory privileged
  ISA. Its exact `v`/`rdip` outcomes distinguish coherent invalidation, a new
  record after invalidation, and possible overwrite during collection.
- The canonical `ArchitectureFaultRecord` has an immutable raw/decision core
  and append-only decoded projections. Every policy, escalation, and custody
  record binds the exact version it consumed.
- Source validity, capture availability, structural parse status, agreement,
  evidence loss, producer trust, correction, poison, context integrity,
  epistemic scope, enforced scope, and disposition remain independent axes.
- `AsynchronousNonDisruptive` and `LocalResumePostcondition` are incomparable
  return proofs. Loss of either premise moves to park/containment or terminal;
  it does not transform one proof into the other.
- The terminal winner record is immutable; collision accounting lives outside
  its payload/checksum. A losing CPU retains its own sealed raw staging record.
- Normal `CrashContext` follows a sealed outer promotion. A separately sealed
  recursive record creates only `RecursiveCrashContext`, which may preserve a
  suspect outer prefix but cannot certify it or invoke rich adapters.
- A reusable crash capsule requires a target-specific alternating-bank and
  atomic generation/commit protocol. Without proven persistence ordering, the
  truthful result is local seal or adapter acceptance—not cross-reset or
  power-loss durability.
- Escalation is generation-lifetime retained at least once while its memory
  domain survives. A named durable guarantee begins only after a profile-
  specific persistence transition succeeds; delivery liveness separately
  assumes receiver progress.
- Receiver failure after an actuator may have run enters reconciliation. It
  never blindly reoffers the action or reclaims an indeterminate obligation
  unless a broader authorized ledger durably assumes both the obligation and
  quarantine.
- The recursive guard's finite software state starts only after architecture
  delivery. Each ISA profile must name the hardware-protected early-entry
  window or explicitly admit that the window is unprotected.
- Publication acceptance and physical reuse are now modeled as separate
  transactions. Aggregate record graphs require a live dependency entry and
  accepted bit; continuation, decoder, park, escalation, and completion work
  install prevalidated compact descriptors before their first mutable byte;
  every registered holder is released from an authoritative bitmap/frontier.
- Containment and terminal fallback arbitrate on one generation-tagged raw-
  staging word. `ContainmentCommitting` can reach terminal only after the exact
  requirement becomes `Abandoned`; requirement `Held` instead forces
  `ContainmentAccepted`, preventing two accepted dispositions for one capture.
- Reset never silently frees interrupted evidence. Incomplete or crash-retained
  raw staging, snapshots, requirements, recursive pairs, promotion, park,
  decoder, transfer, loss, and escalation groups require their exact complete-
  extent custody, current reclaim, fencing, and no-authority/complete-rehome
  predicate. Already accepted operations instead use only their closed normal
  recovery arm; reset is never authority to select either branch.
- Multi-owner containment completion uses one per-requirement constructor gate
  whose immutable descriptor binds the complete token set and destination
  slot. Claimed tokens carry that descriptor tag, making partial construction
  recoverable without allowing concurrent builders to strand disjoint subsets.
- Staging-to-ring, ring-to-queue, and staging-to-loss use one descriptor-tagged
  operational-transfer family. Ring export commits the source while it is
  ordinarily readable, then closes/drains readers and grants one exclusive
  exporter lease; disjoint forward, never-accepted cancellation, incomplete-
  commitment, and cancellation-resume arms cover every fixed-pool cut.
- A valid prepared decoder plan is durable run ownership, not cancellation
  authority. Recovery must start and finish its bounded success/failure run;
  only a descriptor-tagged `Writing` plan or input can use full-extent
  cancellation.
- Return finalization now has its own bounded proof publication, constructed
  one-way after the return arm seals. Disjoint proved-return and proved-no-
  return cleanup retain complete crash custody, fence the old context, and
  rehome accepted sources before any continuation-hold bit releases. A
  per-arm reuse gate remains held while proof/arm reach next `Empty` and the
  old state view folds; gate next-`Free` is the reuse exposure.
- Parked resume, terminal, and durable release builders contend on one shared
  atomic mode gate. A disposition switch cancels an exact `Prepared` scheduler
  record before constructing the nonresume proof, so an empty-record
  observation cannot race a new resume authority or leak a finite slot.
- Reclaim authorization now has one boot-sealed injective source-generation to
  registration-cell manifest. A reclaim builder owns one descriptor-assigned
  receipt-holder bit, only the registered reclaim may linearize source reuse,
  and receipt/reclaim evidence remains held through the source's final next-
  generation publication.
- Paired and multi-object rearm paths do not expose descriptor-free storage
  before their surviving recovery authority is safe: recursive proof/source
  pairs publish the destination member last; return arms use their separate
  reuse gate; transfer and normal parked cleanup use frontier-first exposure
  bitmaps; completion tokens use `RearmedHeld`; and aborted park, decoder,
  terminal-promotion, and escalation groups retain a descriptor/barrier gate
  until every old member is beyond recovery access.
- The sticky operational-loss summary is itself descriptor/owner tagged.
  Its update descriptor carries the complete prior summary rather than only a
  digest; exact-generation holder bits serialize updates, acknowledgements,
  transfer copies, and clearing. Interrupted `Updating` requires full-extent
  custody, unique reclaim, and proof that no accepted loss transfer used that
  generation; the compact loss copy has a distinct digest domain, custody
  receipt, reclaim target, and cleanup lifecycle.
- Reclaim authority is scoped explicitly. Protected same-boot internal rehome
  is a narrow closed variant; reset, crash retention, durable obligation
  transfer, or external custody requires the exact registered source target,
  authenticated complete receipt, and generation-current reclaim. A receipt
  cannot be paired with the internal arm to bypass retention policy.

### Evidence boundary and falsifiers

The proposed architecture is falsified or must widen its guarantee if a target
cannot provide fixed reserved storage; a raw read or sink access can wedge
without an independent terminal mechanism; destructive acknowledgement occurs
before any defensible observation can be preserved; recursive delivery reuses
and overwrites the only stack/record; a decoder silently resolves conflicts;
unknown evidence satisfies a positive return premise; the first-fatal winner
can be overwritten; a record survives one reset class but is described as
power-loss durable; a diagnostic identifier authorizes an action; receiver
replacement loses an accepted obligation; or an indeterminate action becomes
reclaimable without transferred quarantine.

The next evidence must come from a concrete platform profile: generated binary
inspection and stack bounds, formal state exploration, weak-memory tests,
faults at every entry/copy/acknowledgement/promotion/custody transition,
concurrent fatal sources, full queues, recovery-service replacement, stale
generations, DMA contamination, firmware busy/failure, watchdog/reset classes,
torn persistence, replay, planted-secret leakage, and at least two materially
different ISA implementations.

## Source manifest

### Newly introduced sources

- [Arm Reliability, Availability, and Serviceability specification](../30-sources/arm-2019-ras-specification.md) — supplies normative Arm error-record validity, overwrite, ordering, and clearing rules.
- [Scrash](../30-sources/broadwell-et-al-2003-scrash.md) — demonstrates crash-report secret exposure, explicit cleaning, and remaining indirect leakage.
- [GCM and GMAC](../30-sources/dworkin-2007-gcm-gmac.md) — separates authenticated encryption from protocol-level replay protection and key/nonce availability.
- [FATE and DESTINI](../30-sources/gunawi-et-al-2011-fate-destini.md) — supports compound-failure schedules and specification-driven recovery testing.
- [Ramoops](../30-sources/iordache-2021-ramoops.md) — records reserved-RAM placement, mapping, overwrite, ECC, and restart-survival constraints.
- [Machine-check handling on Linux](../30-sources/kleen-2004-machine-check-handling-linux.md) — supports fixed raw collection and deferred interpretation in constrained machine-check context.
- [Recovery domains](../30-sources/lenharth-et-al-2009-recovery-domains.md) — bounds narrow rollback by shared state, request scope, and output commit.
- [A realistic evaluation of memory hardware errors](../30-sources/li-et-al-2010-realistic-memory-error-evaluation.md) — supplies trace-driven correlated-error injection and external-oracle requirements.
- [Linux entry/exit handling](../30-sources/linux-kernel-community-2026-entry-exit-handling.md) — records current non-instrumentable, nesting-aware NMI-like entry discipline.
- [Linux hwpoison design](../30-sources/kleen-2009-hwpoison.md) — supplies historical split-phase memory-poison recovery precedent and its unsupported-page boundary.
- [Linux pstore/blk](../30-sources/linux-kernel-community-2026-pstore-crash-backends.md) — defines panic-time preallocation, polling, lock, DMA, overwrite, and adapter-result constraints.
- [Machine-check recovery on Itanium](../30-sources/luck-2003-machine-check-recovery-itanium.md) — supplies narrow recovery cases and their process/kernel boundary limits.
- [Revisiting memory errors in production data centers](../30-sources/meza-et-al-2015-revisiting-memory-errors.md) — provides long-running recurrence and page-offlining evidence without proving individual-event recovery.
- [Memoir](../30-sources/parno-et-al-2011-memoir.md) — shows why a valid authenticated old state still needs protected continuity to resist rollback.
- [RISC-V RERI v1.0](../30-sources/risc-v-international-2024-ras-error-record-interface.md) — supplies the optional ratified RISC-V record, containability, overwrite detection, injection controls, and implementation-defined reset-retention rules.
- [Evaluating Linux kernel crash dumping mechanisms](../30-sources/vazquez-cao-2006-evaluating-linux-crash-dumping.md) — supplies crash-path failure modes and a multidimensional dump-reliability test method.

### Reused sources

- [Intel system-programming documentation](../30-sources/intel-2026-system-programming-documentation.md) — supplies x86 MCA, NMI, IST, double-fault, and processor-shutdown semantics.
- [Arm A-profile system architecture documentation](../30-sources/arm-2026-a-profile-system-architecture-documentation.md) — supplies current exception routing, stack selection, SError, and optional feature-profile context.
- [RISC-V privileged architecture](../30-sources/risc-v-international-2026-privileged-architecture.md) — supplies early trap, scratch, double-trap, RNMI, and critical-error semantics.
- [Linux RAS documentation](../30-sources/linux-kernel-community-2026-ras-documentation.md) — supplies current raw-plus-normalized reporting and confidentiality precedent.
- [Linux low-level core APIs](../30-sources/linux-kernel-community-2026-low-level-core-apis.md) — supplies entry, ordering, CPU-lifecycle, interrupt, and DMA contract context used by the parent synthesis.
- [Linux lockless ring-buffer design](../30-sources/rostedt-2009-lockless-ring-buffer-design.md) — supplies reserve/commit and nested per-CPU writer precedent while exposing non-persistence limits.
- [Kdump](../30-sources/goyal-et-al-2005-kdump.md) — supplies the preloaded independent capture-environment mechanism and DMA/common-mode limits.
- [UEFI 2.11](../30-sources/uefi-forum-2024-uefi-2-11.md) — supplies CPER, hardware-error variable, runtime reentry, capacity, and variable-commit semantics.
- [ACPI 6.6](../30-sources/uefi-forum-2025-acpi-6-6.md) — supplies APEI source, boot-record, serialization, busy/failure, and injection interfaces.
- [seL4 reference manual](../30-sources/sel4-foundation-2026-reference-manual.md) — supports capability-authorized fault delivery and one-shot reply/return separation.
- [Unreliable failure detectors](../30-sources/chandra-toueg-1996-failure-detectors.md) — formalizes why timeout and missing progress are suspicion rather than terminal proof.
- [Gray failure](../30-sources/huang-et-al-2017-gray-failure.md) — supplies differential-observability limits for health and recovery decisions.
- [Life beyond distributed transactions](../30-sources/helland-2007-life-beyond-distributed-transactions.md) — supplies the duplicate-after-commit window, durable history, and idempotence basis for escalation retry.
- [Recovering device drivers](../30-sources/swift-et-al-2004-recovering-device-drivers.md) — supplies device-specific reconstruction and indeterminate external-effect precedent.
- [Crash-only software](../30-sources/candea-fox-2003-crash-only-software.md) — supports independently restartable recovery services and external authoritative state.
- [Comprehensive seL4 verification](../30-sources/klein-et-al-2014-comprehensive-sel4-verification.md) — bounds what functional kernel verification does and does not prove under hardware failure.
- [CertiKOS](../30-sources/gu-et-al-2016-certikos.md) — supports explicit layered abstract state while preserving hardware, boot, and device assumptions.

## Threads

- Convert the six proposals into one executable product-state model with exact
  object ownership and separate safety/liveness assumptions.
- Pin the first processor, board, firmware, virtualization, reset, memory, and
  error-injection profile before admitting any nonterminal machine-error rule.
- Decide whether the first prototype supports only reserved-memory evidence or
  also a prepared capture environment and one optional persistent adapter.

## Follow-ups

- Generate and inspect the first entry-to-raw-seal binary and prove its stack,
  call, memory, register-access, and acknowledgement bounds.
- Test every RERI `v`/`rdip` outcome or the equivalent selected x86/Arm record
  protocol without treating software injection as real-silicon propagation.
- Measure retention and torn-write behavior for each reset/power class and
  document the exact persistence domain.
- Exercise recovery-service failure before and after actuator invocation and
  verify that reconciliation, quarantine, deduplication, and receipt-gated
  reclamation remain safe.
