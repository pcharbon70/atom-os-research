---
title: "Architecture fault and diagnostic components"
kind: map
created: "2026-09-05"
tags:
  - architecture-support
  - archive-navigation
  - directory-index
  - diagnostics
  - fault-containment
aliases:
  - "Architecture-fault component reports"
---

# Architecture fault and diagnostic components (`architecture-faults-and-diagnostics`)

## Purpose

This directory contains the detailed implementation research for the six
internal services proposed by [Architecture faults and
diagnostics](../architecture-faults-and-diagnostics.md), component 9 of the
kernel hardware and architecture support layer.

## What belongs here

Put subcomponent-level syntheses here when they develop one part of bounded raw
capture, versioned decoding, containment classification and terminal promotion,
crash-safe storage and custody, typed escalation, or recursive-fault termination in
enough detail to state its evidence, objects, state machine, failure behavior,
cross-ISA obligations, and falsification plan. Keep the integrated fault
transaction and caller-visible contract in the parent component note.

Across the reports, a `FaultCaptureIncarnation` means the nominal tuple
`(boot_crash_generation, cpu_identity, cpu_incarnation, capture_sequence)`.
Identifiers in diagnostic records are never authority, a timeout is never a
containment proof, and no sink success establishes that execution may resume.

The shared phase order is: component 2 publishes entry/nesting state; capture
seals each immutable raw attempt before its associated destructive
acknowledgement, except for an explicitly profiled clear-on-read source where
observation itself is the acknowledgement and that loss of a pre-ack software
publication is recorded; after the bounded acknowledge/retry program ends, capture
seals the immutable attempt set; the tiny generated
`CaptureDispositionClassifier` decides return, park, or terminal; terminal
promotion or operational copy establishes its evidence substrate; an aggregate
decision→core→optional-derived-closure→projection graph seals and registers
against that substrate; the richer `FaultDecoder` then creates append-only
policy-plane views in fresh bounded graphs. Terminal sink control may proceed
from the winning sealed promotion before its optional graph finishes. Later decoding can widen future policy but
cannot retroactively authorize the interrupted return.

State names are deliberately namespaced by object:

| Object | Publication states | Meaning |
| --- | --- | --- |
| Raw attempt | `Empty → Writing → Sealed` | One CPU-local source snapshot is normally immutable before its following destructive acknowledgement; an explicitly profiled clear-on-read observation is the acknowledgement and records that no pre-ack publication exists |
| Source-result/acknowledgement set | `Empty → Writing → Sealed` | Storage-independent logical digest plus generation-tagged physical publication identity bind every terminal per-source result |
| Entry snapshot | `Empty → Writing → Sealed → Reclaimable → Clearing → Empty(next generation)` | Component-2-owned bounded frame/incarnation/epoch/mutation facts; exact borrows and a complete dependency set prevent reuse until every accepted semantic copy is rehomed, while a full-extent receipt plus current reclaim authority handles a fenced `Writing` cut |
| Raw staging slot (one native-atomic lifecycle/generation/owner word) | `Free → WritingRaw → AttemptsOpen → RawSetSealed → CopyingOperational/HeldForContainment`; containment arbitrates `HeldForContainment → ContainmentCommitting → ContainmentAccepted` against `HeldForContainment/ContainmentCommitting → HeldForTerminal`; next-boot reclaim uses `→ Reclaimable → Clearing → Free(next generation)` | The final bounded set is immutable only after acknowledgement/retry seals every attempt; a protected same-word outcome gate prevents containment/terminal split brain, and terminal or interrupted generations require full-extent custody, current reclaim authority, borrow drain, and never-accepted or complete-rehome proof |
| Restricted operational evidence slot | descriptor-tagged `Empty → Writing → Sealed → Exporting → Exported → Clearing → Empty(next generation)` | Ring-to-queue export first seals a source commitment under an ordinary borrow, then closes/drains readers and uses the exact tagged `Exporting` tuple as an exclusive exporter-read lease; no ordinary reader accepts `Exporting` |
| Operational evidence transfer controller | `Empty → CommitmentWriting → SourceCommitted`; success continues through destination/receipt/rehome to `Committed → Released → Clearing → Empty(next)`, while preaccept rejection uses `Cancelling → Clearing → Empty(next)` | One predeclared descriptor owns all staging-to-ring, ring-to-queue, and staging-to-loss extents; per-member reuse gates and frontier-first exposure prevent old recovery from reading a reused generation, while exact forward-versus-cancel predicates and full-group crash custody close every partial cut |
| Operational queue receipt | descriptor-tagged `(Empty → Writing → Sealed → Clearing → Empty(next generation), generation)` | The exporter validates the source against its preclosed logical commitment under exclusive authority and binds historical source values to the live queue; later decoders never dereference the old ring |
| Sticky operational-loss summary | descriptor/owner-tagged `Empty/Pending → Updating → Pending`; acknowledged or interrupted cleanup uses `→ Reclaimable/Clearing → Empty(next)` as applicable | The immutable update descriptor carries the complete prior summary; closeable exact-generation holders serialize writers, acknowledgements, transfer copies, and cleanup, while a persistent cleanup descriptor/frontier makes every interrupted clear resumable |
| Compact operational-loss transfer | descriptor-tagged `Empty → Writing → Sealed → Reclaimable → Clearing → Empty(next generation)` | Async-only immutable logical core-evidence custody when raw bytes cannot be retained; its explicit digest domain, dedicated complete custody receipt, registered current reclaim, dependency/borrow drains, and retained cleanup descriptor gate rearm. It is non-decodable and never authorizes local resume |
| Fault-record publication graph | `Empty → ReservationWriting → Reserved → decision/core/derived/projection writing+seal phases → Sealed → Rehoming/Abandoned/Reclaimable → Clearing → Empty(next generation)` | A sealed reservation header binds owner/capture/role/seed and companion slot before child writes; no child is independently acceptable; the root and a bidirectionally matching live dependency entry jointly publish one physical graph, while exact unused or abandoned reservations are proven, cleared, and rekeyed |
| Evidence graph dependency set | one atomic `Open → Closing → Drained` word with reservation and accepted bitmaps, plus per-entry `Empty/Claiming/Reserved/ReadyToAccept/Live/Rehomed/Revoked` | Acceptance is the accepted-bit CAS only after any required continuation hold is `Complete`; closing enumerates both bitmaps and every entry before substrate clear |
| Continuation-custody hold | `Empty → PlanWriting → Prepared → Acquiring → Complete`, then return-arm or park transfer, `Releasing → Released → Clearing → Empty(next generation)` | Preallocated holder bits make every partial acquisition/release recoverable; accepted return/park cannot lose graph/evidence custody, and a return fault retains the armed hold |
| Return-armed record, completion proof, and reuse gate | descriptor-tagged arm `Empty → Writing → Armed → Finalizing → Consumed/Reclaimable → Clearing → Empty(next)`; one-way-bound proof `Empty → Writing → Sealed → Claimed → Consumed → Clearing → Empty(next)`; gate `Free → ArmReserved → FinalizerCompleting → PairRearmed → StateViewFolded → Clearing → Free(next)` | The gate is reserved before arm claim and remains nonfree while proof and arm publish next-`Empty` and component 2 folds the old state view; gate next-`Free` is the final reuse exposure, so a new arm cannot race paired cleanup or an old locator |
| Decoder run plan/control/outcome | descriptor-tagged plan `Empty → Writing → Prepared → Clearing → Empty(next)`; native run word `Idle → Running → OutcomeWriting → OutcomeSealed → Releasing → Released → Idle(next)`; outcome `Empty → Writing → Sealed → Clearing → Empty(next)` | A `Writing` plan may cancel but `Prepared` must finish its bounded run; success alone may set the graph accepted bit. Before teardown, input swaps to an immutable cleanup descriptor whose old/next tuple makes sidecar-clear, run-Idle, and final-input cuts exactly resumable |
| Local-resume token | `Free → Writing → Available → Consumed/Revoked → Clearing → Free(next generation)` | One-shot protected return authority bound to an initial graph seed, exact CPU/context, sealed ring-root graph and live dependency entry; async return has no token |
| Requirement evidence slot | descriptor/owner-tagged accepted `Free → Writing → Sealed → Held → Reclaimable → Clearing → Free(next)`; rejected `Sealed → Abandoned → Reclaimable → Clearing → Free(next)` | The shared staging gate plus `Held` CAS is acceptance; the reclaim CAS atomically replaces build tags with a closed accepted-held or never-held cleanup descriptor, retaining the corresponding proof/custody or full-extent receipt/reclaim and frontier through final exposure |
| Completion constructor gate/tokens | per-requirement gate `Idle → ClaimingTokens → BuildingCompletion → CompletionSealed → ConsumingTokens → Released → RearmingTokens → ReleasingTokens → Clearing → Idle(next)`; tokens `Available → Claimed → Consumed → Clearing → RearmedHeld(next) → Empty(next)` carry the gate's descriptor tag | One descriptor binds the complete token set and slot; non-writer-eligible `RearmedHeld` plus frontier-first exposure serializes reuse without letting a new writer race the old gate |
| Park handoff, shared release-mode gate, and parked-release proof | handoff `Empty → Writing → Sealed → Parked` or `Writing/Sealed → Aborting → Aborted`, then `Reclaimable → Clearing → Empty(next)`; its atomic mode gate arbitrates resume/terminal/durable sidecars; proof `Empty → Writing → Available → Claimed → Consumed → Clearing → Empty(next)` | The named custodian accepts parking; the one shared gate makes resume-record and nonresume-proof construction contend on the same word. Aborted source/destination/handoff rearms remain pool-reserved behind one descriptor-tagged group barrier until every member reaches its exact next state |
| Acknowledgement | `NotStarted → InProgress → Completed/Failed` | A separately published result for source clear/invalidate/recheck |
| Terminal promotion | descriptor/owner-tagged `Free → Writing → Sealed → Reclaimable → Clearing → Free(next generation)` | The first CAS installs the exact capture/input/copy plan before bytes; one system-wide observation wins, while a `Writing` cut requires complete custody, current reclaim, fenced descriptor owner, no accepted context/dependency, and exact borrow drain |
| Recursive record | descriptor-tagged `Empty → Writing → Sealed → Reclaimable → Clearing → Empty(next generation)` | One independently provisioned terminal explanation; sealed source reuse requires the source-specific receipt and current reclaim authority, while incomplete/no-write proof-slot cuts reserve the target generation before paired clear |
| Fatal-preclassification proof | descriptor-tagged `Empty → Writing → Available → Claimed → Consumed → Reclaimable → Clearing → RearmedHeld(next) → Empty(next generation)` | One pinned depth-two authority for the exact recursive slot; paired cleanup holds the proof non-writer-eligible, publishes the source next state, then exposes proof `Empty` last, with an explicit old/next-generation resume predicate for every cut |
| Normal capsule bank descriptor | `Invalid → Open`, then a separate superblock becomes `Committed` | `Open` makes a validated section-zero prefix discoverable even if final publication never occurs |
| Crash-capsule section | `Empty → Writing → Committed`, optionally `Torn` only on a safely returned short-copy error | A sink-local copy; `Committed` is not automatically reset-persistent or authentic |
| Crash bank/recursive retention word | `Unused → WritingProtected → Protected/Retained → Reclaimable → Revoking → Clearing → Cleared → Unused(next generation)` | A native compact descriptor-index CAS claims only fully initialized `Unused`; `Cleared` is not writer-eligible, and next borrow/dependency controls plus identity descriptor precede next `Unused` publication |
| Custody receipt and crash-reclaim authority | receipt `Empty → Writing → Sealed → Rehoming/Reclaimable → Clearing → Empty(next)`; reclaim `Empty → Writing → Available → Claimed → Consumed → Clearing → Empty(next)` | A boot-sealed injective source-to-registration-cell manifest permits only one reclaim publication per source generation; each reclaim owns an authoritative receipt-holder bit, and both remain generation-held until the target's final next-state publication |
| Per-CPU recursive capsule slot | `Empty → Writing → Committed`; its separate retention word governs authorized reuse | CPU-incarnation-bound storage independent of normal banks, other CPUs, and the interrupted outer section; content state alone never makes it writable |
| Escalation event slot | admission-descriptor/owner-tagged `(Empty → Writing → Sealed → Clearing → Empty(next generation), generation)` plus append-only headed custody transitions | The first claim installs the full event/genesis plan; fenced incomplete admission and its explicit cleanup-resume predicate require no committed head, full-group custody/reclaim, exact old/next generations, quiescence, and borrow drain |
| Escalation append authority | `Unbound → GenesisAppending → Open`; ordinary successors use `Open → Appending → Open/EffectFenced`, effects use `EffectFenced → AppendingOutcome → Open`, and `Recovering` handles fenced takeover | A native compact descriptor-index CAS plus prevalidated phase descriptors distinguishes predecessor-free genesis from ordinary/effect appends and prohibits replay after an indeterminate outcome |
| Persistent graph-binding hold | descriptor-tagged `Empty → PlanWriting → Prepared → Acquiring → Complete → Transferring/Releasing → Released → Clearing → Empty(next generation)` | Its claim atomically installs a prevalidated event/binding/graph/token plan; `PlanWriting` cancellation uses full-extent custody and exact no-binding/no-holder proof, while completed destination custody overlaps before source release and remains live through quiescence |
| Escalation custody | `RecordedVolatile` or `RecordedDurable(domain)` onward | Delivery/custody strength qualified by the exact surviving memory or persistence domain |

## Index

### Subdirectories

- None yet.

### Documents

- [Bounded capture routine](bounded-capture-routine.md) — specifies destructive-read ordering, fixed per-CPU storage, sealed publication, loss accounting, and a statically bounded hard-entry path.
- [Fault decoder](fault-decoder.md) — derives traceable versioned facts from immutable raw blocks while retaining unknown fields, conflicting evidence, and decoder provenance.
- [Containment classifier and promotion](containment-classifier-and-promotion.md) — compiles pinned platform rules into conservative dispositions and separates local return, split-phase containment, and terminal promotion.
- [Crash-safe sink](crash-safe-sink.md) — defines a mandatory reserved-memory capsule plus optional persistent and independent bulk-capture adapters with explicit durability and confidentiality claims.
- [Escalation channel](escalation-channel.md) — transfers evidence and requested action scope to higher policy, which must join separate capabilities, without blocking hard entry or confusing notification with completion.
- [Double-fault guard](double-fault-guard.md) — provides independent stack, code, state, and terminal storage for one recursive capture attempt followed by a finite halt/reset path.

## Maintaining this index

Inventory every direct report and keep the six-service decomposition aligned
with the parent component. Whenever a report is added, renamed, moved,
archived, or superseded, update this index, the parent component index, the
kernel architecture map, the open inquiry, and the relevant deep-dive journal.
