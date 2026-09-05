---
title: "Translation invalidation planner"
kind: note
created: "2026-09-04"
maturity: developing
tags:
  - architecture-support
  - multicore
  - tlb
  - virtual-memory
aliases:
  - "TLB invalidation planner"
---

# Translation invalidation planner

The invalidation planner should be a pure, deterministic compiler from a
semantic mapping effect and a frozen machine profile to an immutable
maintenance plan. It should decide which cached state may be stale, which CPU
incarnations may hold it, which local architecture operations dominate that
hazard, which per-target completion class is required, and which orthogonal
aggregate predicates the caller must obtain. It should not send interrupts,
edit page tables, or infer that a target has executed anything.

The central safety rule is monotonicity: optimization may replace a plan only
with one proved to dominate it for the same architecture profile. Queue
pressure, range size, missing feature knowledge, and errata may widen an
address operation into a context or system operation; they may never weaken
the semantic obligation.

This is proposed Atom architecture. Its common plan algebra and backend
refinement proofs do not yet exist.

## Question, scope, and operational standard

The question is:

> Given an already accepted translation change, what is the least maintenance
> plan that is known to close every stale-translation path on this exact
> machine, without confusing target selection with instruction scope or
> request delivery with completion?

The planner owns:

- semantic classification of the old-to-new mapping transition;
- architecture-, revision-, virtualization-, and erratum-specific lowering;
- address, range, context, stage, global, and sharing-domain scope;
- a conservative may-hold target set derived from frozen activation/helper
  evidence and allocator-owned snapshots for every affected context binding,
  whether or not the operation retires the tag;
- local ordering, invalidation, synchronization, and instruction-fetch steps;
- legal coalescing and dominance proofs; and
- an explainable record of why each obligation appears in the plan.

It does not own descriptor publication, remote execution, CPU-offline proof,
or resource reclamation. A candidate planner is adequate only if:

1. Every plan is derived from decoded old and proposed semantics, not from an
   untrusted request's claim that a change is “just an unmap” or “local.”
2. Leaf, nonleaf, root, memory-type, page-size, globality, execute, and
   accessed/dirty changes are distinguished before lowering.
3. Every target is a CPU identity plus incarnation; a recycled CPU number
   cannot satisfy a previous plan.
4. The selected local sequence is sufficient for the exact ISA profile,
   translation stage, sharing domain, and known errata.
5. Any coalesced plan dominates each input plan and preserves each operation's
   completion and reclamation identity.
6. Unknown features, ambiguous ancestry, arithmetic overflow, or exhausted
   plan capacity cause pre-accept rejection or conservative strengthening.
7. A performance threshold can change cost but cannot change correctness.
8. A reference planner and each optimized backend agree on millions of
   generated transitions, including deliberately tiny tag and queue spaces.

## Evidence and limits

| Evidence | Supported conclusion | Limit |
| --- | --- | --- |
| [Intel system-programming documentation](../../../30-sources/intel-2026-system-programming-documentation.md) | x86 exposes address-, context-, non-global-, and global-sensitive invalidation mechanisms, and paging-structure caches can matter in addition to leaf TLB entries | Exact availability and virtualization behavior are profile dependent |
| [Arm A-profile documentation](../../../30-sources/arm-2026-a-profile-system-architecture-documentation.md) | Arm TLBI scope, translation regime/stage, shareability, barriers, and break-before-make are one ordered protocol | Architecture documents do not validate a particular CPU revision or firmware path |
| [Relaxed virtual memory](../../../30-sources/simner-et-al-2022-relaxed-virtual-memory.md) | Page-table writes, walks, barriers, and invalidations have observable relaxed interactions that informal sequential reasoning misses | The model covers a bounded Arm feature set, not all production cores |
| [RISC-V privileged architecture](../../../30-sources/risc-v-international-2026-privileged-architecture.md) | `SFENCE.VMA` is local; operand and global-mapping rules affect scope; invalid PTEs may be cached without Svvptc | Remote execution and platform coherence are separate contracts |
| [RISC-V supervisor binary interface](../../../30-sources/risc-v-international-2025-supervisor-binary-interface.md) | RFENCE standardizes remote-fence requests, but `SBI_SUCCESS` reports successful transmission to targeted harts rather than target execution | A platform may specify stronger completion separately; the standard return alone does not |
| [TLB consistency](../../../30-sources/black-et-al-1989-tlb-consistency.md) | Address lists can be accumulated and safely upgraded to a full flush on overflow, with explicit remote participation | The measured multiprocessors and software interfaces are historical |
| [Ephemeral mapping management](../../../30-sources/elmeleegy-et-al-2005-ephemeral-mapping-management.md) | CPU-private and shared temporary mappings have different remote-invalidation scope and lifetime costs | Historical FreeBSD mechanisms do not establish Atom's alias policy or modern ISA ordering |
| [Optimizing TLB shootdown](../../../30-sources/amit-2017-optimizing-tlb-shootdown.md) | Page-versus-context thresholds and target pruning can reduce cost when the correctness invariant is preserved | Results are workload- and x86/Linux-specific |
| [Don't shoot down TLB shootdowns](../../../30-sources/amit-et-al-2020-dont-shoot-down-tlb-shootdowns.md) | Deferral and batching require return-to-user and privileged-access gates; they are not transparent substitutions | Early acknowledgement does not establish table-reclamation safety |
| [HATRIC](../../../30-sources/yan-et-al-2017-hatric.md) | Hardware translation coherence can replace some software shootdown work and exposes the value of precise dependency tracking | It is a simulated proposal, not a generally available platform guarantee |
| [RadixVM](../../../30-sources/clements-et-al-2013-radixvm.md) | Range-indexed metadata and precise per-range CPU tracking can reduce unrelated shootdown work | Its per-core-table research design and x86 evaluation do not establish a portable target-set proof |

These sources establish architecture-specific obligations and optimization
constraints. The common effect lattice, plan schema, and proof interface below
are cross-source synthesis.

## Immutable input and output

The planner consumes a kernel-generated snapshot:

```text
InvalidationIntent {
    operation_id,
    address_space: AddressSpaceIncarnation,
    accepted_mutation_sequence,
    affected_mapping_incarnations: Set<MappingIncarnation>,
    decoded_old_semantics,
    decoded_new_semantics,
    modified_levels_and_global_ancestry,
    virtual_ranges_and_granules,
    frozen_observer_translation_bindings:
        BoundedMap<(CpuIdentity, CpuIncarnation),
                   BoundedSet<ObserverTranslationBinding,
                              MAX_OBSERVER_BINDINGS_PER_TARGET>>,
    frozen_active_and_entering_cpus,
    observer_borrow_scan_epoch_and_obligations,
    access_drain_snapshot:
        Option<FrozenBorrowEpochAndObligations>,
    affected_binding_observer_snapshots:
        BoundedMap<TargetTranslationBinding,
                   BindingObserverSnapshot {
                       cumulative_may_hold_cpus,
                       installing_loading_installed_restoring_cpus,
                       frozen_slot_states_and_install_attempt_identities,
                       required_install_load_exclusions,
                       binding_matched_entering_cpus
                   }>,
    context_tag_retirement_snapshots:
        BoundedMap<ContextTagRetirementObligation,
                   RetirementTargetSnapshot {
                       cumulative_may_hold_cpus,
                       installing_loading_installed_restoring_cpus,
                       frozen_slot_states_and_install_attempt_identities,
                       required_install_load_exclusions,
                       binding_matched_entering_cpus
                   }>,
    close_observer_snapshot: Option<CloseObserverSnapshot>,
    requires_stable_observer_snapshot,
    software_walker_obligations,
    table_or_frame_reclamation_requested,
    completion_requirements: CompletionRequirements,
    machine_profile_id
}
```

The `ContextTagRetirementObligation` map key is authoritative for obligation
ID, exact binding, and retirement epoch; `RetirementTargetSnapshot` does not
repeat those fields. Its constructor derives the target/install-state value
under allocator serialization and binds it to that complete key.

The result is immutable and content-addressed:

```text
InvalidationPlan {
    plan_id,
    plan_digest,
    intent_digest,
    requirements_id,
    completion_requirements_digest,
    profile_digest,
    target_set: Set<(CpuIdentity, CpuIncarnation)>,
    per_target_observer_bindings:
        Map<(CpuIdentity, CpuIncarnation),
            BoundedSet<ObserverTranslationBinding,
                       MAX_OBSERVER_BINDINGS_PER_TARGET>>,
    observer_gate_requirement,
    per_target_local_program:
        Map<(CpuIdentity, CpuIncarnation), LocalProgram>,
    publication_preconditions,
    per_target_required_class:
        Option<CpuUserReturnClosed | LocalMaintenanceComplete>,
    access_borrow_drain_requirement,
    hardware_walker_obligations:
        BoundedMap<TablePageIncarnation, HardwareWalkerObligation>,
    software_quiescence_requirements,
    legal_strengthenings,
    diagnostic_derivation
}

HardwareWalkerObligation {
    table: TablePageIncarnation,
    walker_obligation_digest,
    required_detachment_evidence,
    required_target_local_programs:
        Map<(CpuIdentity, CpuIncarnation),
            TableSpecificLocalProgramRequirement>,
    profile_walker_completion_rule,
    required_additional_walker_evidence:
        Option<WalkerRetirementEvidenceRequirement>,
    canonical_program_coverage_and_dominance_digest,
    aggregate_derivation_id
}

WalkerRetirementEvidenceRequirement {
    authorized_producer,
    event_kind,
    table_and_operation_binding,
    generation_or_sequence_binding,
    required_order_before_and_after_event,
    evidence_format_and_validation_rule
}
```

`plan_digest` is a canonical domain-separated digest over the complete plan
except that digest field itself: `plan_id`, the immutable intent and profile
digests, `requirements_id`, `completion_requirements_digest`, every target and
observer binding, every local program, all publication/access preconditions,
all hardware-walker and software-quiescence obligations, legal
strengthenings, and their canonical ordering. It therefore cannot be copied
onto a plan with a different target, program, profile, or terminal-product
requirement.

Each `walker_obligation_digest` is likewise a canonical domain-separated
digest over its owning `plan_id`, `requirements_id`, the operation and address-
space incarnations committed by `intent_digest`, the authoritative
`TablePageIncarnation` map key, detachment evidence requirement, exact target-
program map, frozen-profile walker-completion rule, optional additional
evidence requirement, coverage/dominance certificate, and aggregate
derivation identity. The digest field itself is excluded. Constructors reject
a repeated `table` that differs from the map key or any digest that does not
recompute from this full tuple.

The walker-obligation map keys equal
`CompletionRequirements.hardware_walker_obligations` exactly, and each value's
`table` equals its key. This checked bijection admits exactly one canonical rich
obligation for every required table: no table can be omitted, duplicated, or
added merely while retaining the correct completion-requirements digest. For
each walker obligation, the required-target map keys are an exact subset of the
plan target set. Every table-specific program must equal or be dominated by the canonical
`per_target_local_program[target_cpu]` under the identical frozen profile and
observer-binding set. The checked key coverage and dominance certificate are
committed into `canonical_program_coverage_and_dominance_digest`, which in turn
is part of `walker_obligation_digest`; a second unlinked program source cannot
mint walker completion. The pure planner does not allocate completion slots.
Coordinator construction joins each CPU key to the accepted operation's exact
reserved slot generation, and the eventual target-set digest must cover those
joined tuples.

The planner has two pure phases. During preparation it derives
`observer_gate_requirement` from the semantic effect, promised completion,
and machine profile, before a mutable target set is consulted. At acceptance,
that flag controls the odd/even gate; only then does the planner bind the
frozen target identities and privileged-access borrow epoch/set into the final
immutable plan, before the first live descriptor edit. If CPU membership or
borrow demand changes later, the gate prevents a new old-generation use and
requires catch-up/retry; the planner is not silently rerun against moving sets.
The plan's `requirements_id` and canonical completion-requirements digest must
equal the intent-bound `CompletionRequirements` and the accepted operation's
terminal product; `plan_digest` commits to that exact linkage. The observer-
binding-map and local-program map key sets must each equal `target_set`, and
every observer-binding value is a nonempty bounded set. Each local program is
compiled for exactly its key's CPU incarnation, complete observer-binding set,
and frozen profile; validation rejects a missing, additional, or cross-target
program. `TargetRoot` members carry the
exact context-tag incarnation, binding scope, root fingerprint, retirement
epoch, and profile; `TemporaryAlias` members instead carry their alias-slot,
operation, reservation, private kernel-context, and profile identities. A tag
from another CPU namespace cannot be substituted merely because its numeric
value matches, and a temporary-alias-only target does not acquire a fictional
address-space tag. Binding resolution precedes publication of `Entering`, so
every frozen activation already contributes a `TargetRoot` member.

Within each `BindingObserverSnapshot` and `RetirementTargetSnapshot`, the
`frozen_slot_states_and_install_attempt_identities` map is authoritative. Each
value is a nonterminal `Installing`, `LoadingRoot`, `Installed`, or
`RestoringSafeContext` slot and includes the allocator-slot generation, install
generation, install-guard incarnation, and owner; `NoBinding` entries are
omitted. The
`installing_loading_installed_restoring_cpus` field is a checked projection of
exactly its keys, not an independently supplied set. The
`required_install_load_exclusions` map covers every frozen slot
exactly once and binds the identical CPU incarnation, target binding,
allocator-slot generation, install generation, guard/owner incarnation, and
frozen state to the state-appropriate discharge. No summary
member may lack a slot obligation, and no frozen slot may disappear from the
summary or exclusion map.

`None` means that this plan has no per-CPU coordinator work and its terminal
product requires no target-set proof; the transaction bypasses shootdown and
cannot manufacture `TargetSetCompleted`. The checked invariant is
`per_target_required_class == None => target_set`, observer-binding map,
local-program map, and completion-slot map are all empty. Conversely,
`require_cpu_translation_quiescence => per_target_required_class ==
Some(LocalMaintenanceComplete)`, including when the exact target set is empty.
For that empty set the coordinator immediately emits the uniquely bound,
vacuous zero-target `TargetSetCompleted<LocalMaintenanceComplete>` and
`CpuTranslationQuiescent`; it is not represented by `None`. `Some(C)` is
lowered into a `ShootdownOperation` whose per-target field is the concrete
class `C`; neither requests nor aggregate results ever carry `None`.

If a profile needs an event beyond table detachment plus the target-local
programs, that requirement is a typed, digest-bound part of the obligation; an
opaque timeout or unbound platform event cannot fill it. A profile with no
validated evidence producer and format for its required event is unsupported
for table-page reclamation, and the detached table remains quarantined.

## Semantic decision procedure

Start from the effect classes defined by the [mapping
transaction](mapping-transaction.md):

| Effect | Minimum semantic question | Portable baseline |
| --- | --- | --- |
| `A` invalid → valid | Can the profile cache a negative result or stale ancestor? | Establish usability; invalidate where the profile cannot prove negative caching absent |
| `P+` permission expansion | Can stale denial be exposed to the caller? | Establish usability for the public synchronous API |
| `R` restriction/unmap | Which CPUs or privileged helper borrows could still exercise old authority? | Publish restriction, invalidate every may-hold CPU, block new helper borrows, drain the frozen old borrow set, and await `RestrictionQuiescent` |
| `X` valid replacement | Could old/new frame, type, size, globality, or descriptor kind coexist? | Break-before-make when required; invalidate after break before make |
| `T` table unlink | Could a hardware or software walker still reach the table page? | Invalidate the required ancestry/scope, then request distinct `HardwareWalkerQuiescent` and `SoftwareReaderQuiescent` proofs |
| `M` A/D sample or clear | Could cached metadata race the observation? | Use a distinct architecture-specific observation program and confidence result |
| `E` executable publish/retire | Could data, instruction, prediction, or code references be stale? | Compose with the executable-code lifecycle; do not reduce to data-TLB completion |
| `L` address-space close | Which activations, helper borrows, context leases, mappings/roots, accepted operations/grants, code, DMA, and references retain the dying incarnation? | After irreversible close admission, consume the frozen close snapshot; compile subordinate restriction/table work, drain activation/borrow observers, retire every exact tag snapshot, and require the checked `AddressSpaceClosed` product or quarantine |

A transition with several dimensions takes the union. For example, replacing a
writable data frame with executable code is `X + E`, not a permission edit.
Removing the last leaf and its now-empty intermediate table is `R + T`.

`observer_gate_requirement` is mandatory for `R`, `X`, `T`, `L`, applicable `E`
retirement, and any `A` or `P+` whose synchronous `Usable` result requires
active-target-scoped maintenance. It may be `None` only when the profile proves
that no joining CPU can retain state that violates the promised `Usable`
result. The baseline type algebra has no published-may-fault result.

For every restrictive class, the intent also carries the accepted borrow epoch
and explicit pre-existing `UserAccessGuard` obligations. The planner requests
their drain but does not fabricate it from TLB maintenance: the mapping
transaction combines the coordinator's CPU-translation result with access-
borrow evidence to form `RestrictionQuiescent`.

Every plan that performs CPU translation maintenance or claims `Usable`,
`CpuTranslationQuiescent`, or `RestrictionQuiescent` freezes the allocator's
observer snapshot for every affected `TargetTranslationBinding`. Its target set
includes `cumulative_may_hold_cpus ∪ Installing ∪ LoadingRoot ∪ Installed ∪
RestoringSafeContext ∪ binding-matched Entering`, even when a CPU is no longer
active. Active/entering records and helper borrows are additional target
sources, not substitutes for this historical set. An implementation may prune
a member before snapshot only by atomically removing it from every applicable
allocator/activation/borrow source under already-validated exact-binding
invalidation or terminal CPU-lifecycle evidence. Once frozen, the source union
is the target set and cannot be pruned. Otherwise an inactive CPU could retain a stale tagged
translation while a frame or table is reused.

For every frozen nonterminal install state, the local plan also requires a
generation-matched `InstallLoadExclusion`: forced pre-load abort or
`InstallWithdrawnSafe` for `Installing`, safe-context restoration for any state
where a root may have loaded, or terminal lifecycle exclusion. Its exact-
binding invalidation is ordered after that proof, unless the validated
lifecycle stop/reset/fence itself destroys or forever excludes all retained
state. An acknowledgement emitted
before an interrupted old installer is prevented from loading cannot enter
`TargetSetCompleted`.

Class `L` is provisional during preparation: only snapshot capacity and the
deferred requirement are known. The planner may finalize it only inside
non-dispatchable `Accepting`, after `Live` → `Closing` and the fenced capture
replaces that field with the exact sealed `CloseObserverSnapshot`. In addition
to the general binding-observer rule, class `L` freezes a retirement snapshot
for every lease and binds its retirement epoch. For every effect, the key set of
`frozen_observer_translation_bindings` must cover the union of activation,
helper, affected-binding, and applicable tag-retirement target sources. There
is no post-freeze pruning or unrecorded omitted-member proof.

### Additive is profile dependent

There is no portable “adding a mapping never needs invalidation” rule. A
documented Arm profile may treat selected translation faults as noncached,
while RISC-V permits invalid PTEs to be cached unless a feature such as Svvptc
changes the contract. Atom therefore records negative-cache behavior in the
machine profile and returns synchronous `Usable` only after the required
maintenance.

### Target set is not invalidation scope

The target set answers *where* a local program must run. The instruction scope
answers *what cached state* each execution covers. A single context-wide local
flush on CPU 3 does not replace address flushes on CPUs 1 and 2, and an
all-CPU broadcast instruction does not justify omitting software targets unless
the profile proves that its broadcast and completion domain includes them.

Target pruning means proof-backed removal from the underlying may-hold source
sets before the acceptance snapshot, under their lifecycle serialization. It is
allowed only from a sound invariant maintained by activation/deactivation and
the allocator. “The task last ran elsewhere,” scheduler affinity, or an idle-
state guess is not such proof; the planner never drops a member of a frozen
source union.

## Plan dominance and coalescing

Within one fixed profile, define a partial order over local programs. A typical
translation scope grows approximately as:

```text
address < address-range < one-context < all-non-global < all-including-global
```

This is not one universal ISA ordering. Stage, global ancestry, shareability,
and executable maintenance add dimensions, so the backend must prove its own
`dominates(stronger, weaker, profile)` relation.

Coalescing is legal when:

- all input ranges and arithmetic are represented exactly;
- the replacement target set is a superset of all target sets;
- every ordering and completion requirement is retained;
- context-tag and address-space incarnations cannot be confused;
- table-walker and code/DMA requirements remain attached to their resources;
- every original operation can obtain its own terminal evidence; and
- the strengthened program is valid on the profile.

A bounded per-CPU range vector may upgrade on overflow to one context flush.
If a global or nonleaf hazard prevents that context operation from dominating,
it upgrades again to the profile's safe broader sequence. It never drops the
oldest item or returns success with an incomplete vector.

## Architecture lowering

### x86-64

The profile records PCID, INVPCID, global-page policy, page sizes, root-pairing,
virtualization, and relevant errata. The backend chooses among mechanisms such
as `INVLPG`, INVPCID's individual-address, single-context, all-context
non-global, and all-context including-global types, or a profile-approved CR3
sequence. The plan explicitly accounts for paging-structure caches and global
ancestry; it does not equate one leaf address with every upper-level change.

Publication ordering, invalidation execution, and acknowledgement are distinct
events in the trace. The proof also covers a CPU that can speculatively consult
stale translation state before architectural use.

### Arm A-profile

The profile fixes exception level, translation regime and stage, ASID/VMID
width, granule, shareability, CnP promises, and CPU revision. A local program
spells out descriptor store, required `DSB`, the chosen TLBI address/ASID/all
and leaf/all-level variant, post-TLBI `DSB`, and `ISB` where required. A valid-
to-valid change that falls under break-before-make becomes two publication
phases with completion between them.

Errata are executable profile data, not prose. If a core revision requires an
extra or wider TLBI/barrier sequence, the compiled plan contains it and its
derivation names the erratum. An unknown revision fails profile construction
or selects the conservative reviewed fallback.

### RISC-V

The backend lowers to the appropriate `SFENCE.VMA` operand combination. An
address-plus-ASID fence can target one nonglobal mapping; an all-address ASID
fence can cover one context; global ancestry and certain nonleaf edits require
all-ASID scope. An over-fence is permitted, but an ASID-scoped fence must not
claim to remove global entries.

`SFENCE.VMA` affects the local hart. Svinval or Svvptc may change available
sequences only when present in the frozen profile. In the standardized SBI
RFENCE interface, `SBI_SUCCESS` establishes successful request transmission to
the targeted harts, not their execution of the local fence. The coordinator
therefore either uses an IPI only to invoke an Atom target handler that executes
and acknowledges the local fence, or consumes a separately specified platform
completion emitted causally after execution of that exact RFENCE and bound to
the request and hart incarnation. An unrelated later OS acknowledgement cannot
repair the missing causal link, and an adapter cannot reinterpret the SBI
return.

## Completion classes and orthogonal walker obligations

The planner requests a typed result rather than a Boolean `flushed`:

| Completion | Establishes | Does not establish |
| --- | --- | --- |
| `RequestAccepted` | Coordinator took durable ownership | Notification, delivery, execution, or semantic completion |
| `CpuUserReturnClosed(cpu)` | Named CPU incarnation cannot return to affected user execution without its pending-generation gate | Local maintenance or privileged helper-borrow drain |
| `LocalMaintenanceComplete(cpu, plan)` | Named CPU incarnation ran the required immutable local architecture sequence | Aggregate target completion, helper-borrow, software-reader, DMA, or code quiescence |
| `TargetSetCompleted(operation, per_target_required_class, target_set)` | Every frozen target produced the planner-selected per-target class or valid lifecycle-exclusion evidence | Translation quiescence for a user-return-only class; access, walker, software-reader, DMA, code, reference, or reclamation quiescence |
| `CpuTranslationQuiescent(operation, target_set)` | Every frozen may-hold CPU target completed the required local plan or was terminally excluded; no cached translation or in-flight leaf walk can later install/use the old mapping | Privileged helper borrows, detached table-page walkers, software readers, DMA, code, or reference quiescence |
| `HardwareWalkerQuiescent(table)` | Under a named profile rule, the detached table, complete exact-target local evidence, and any required additional walker event together prove no hardware walker can still interpret that table page | CPU-translation, software-reader, ordinary-frame/tag, DMA, code, or reference quiescence |

The plan names the weakest sufficient **per-target** coordinator class for its
operation; aggregation first yields the correspondingly indexed
`TargetSetCompleted`. A caller may request a dominating class within that frozen local
class lattice, but no component can cast a weaker token into a stronger one.
Hardware-walker quiescence is not a stronger point in that lattice: it is an
orthogonal, table-bound aggregate obligation. The planner supplies the profile
rule and derivation identifier; the shootdown coordinator consumes exact
detachment, all required target-local evidence, and any
`required_additional_walker_evidence`, and may then construct
`HardwareWalkerQuiescent(table)`. `CpuAccessQuiescent`,
`RestrictionQuiescent`, `SoftwareReaderQuiescent`, and `Reclaimable` are
composed outside the planner's per-CPU maintenance result and are never inferred
from it.

## Failure and conservative fallback

- **Unknown profile or erratum:** reject before acceptance; if discovered
  afterward, retain the operation and resources in quarantine.
- **Range overflow or unsupported granule:** reject the prepared operation,
  never truncate.
- **Plan allocation failure:** use pre-reserved emergency capacity or reject
  before acceptance; an accepted teardown cannot abandon its obligation.
- **Queue capacity exceeded:** strengthen into a bounded context/system plan.
- **Target becomes unavailable:** preserve its incarnation in the coordinator
  obligation until CPU lifecycle supplies terminal exclusion.
- **Backend instruction fault or hypervisor refusal:** record a typed platform
  failure and quarantine; do not report a mapping error as if no effect began.
- **Planner/backend disagreement:** fail closed at profile activation and make
  the machine ineligible for that security profile.

## Verification and experiments

### Reference model

Build a deliberately slow specification over a flat set of possible cached
translations. For every old/new semantic pair and target history, execute the
planned abstract invalidation and assert that no forbidden old interpretation
remains. Prove or exhaustively check backend dominance and coalescing laws.

### Generated differential tests

Generate page-size changes, leaf/nonleaf swaps, global ancestry, tag rollover,
negative entries, memory-type changes, disjoint and overlapping ranges,
range-overflow fallback, and CPU entry/exit races. Compare the optimized plan
with the reference plan and a table decoder.

### Architecture litmus and hardware tests

- Port the relevant Arm relaxed-VM litmus cases and add Atom's activation
  handshake.
- On RISC-V, probe ASID length and Svvptc/Svinval, then test invalid-to-valid,
  global ancestry, and remote-hart paths.
- On x86, test PCID/global combinations, page-size replacement, paging-
  structure cache cases, and virtualized execution.
- Inject queue overflow, delayed IPIs, CPU hotplug, duplicate delivery, and
  stale acknowledgements.

Performance measurements report per-page/context crossover points, IPI count,
remote stall time, coalescing ratio, and tail latency by machine profile. They
tune thresholds only after safety equivalence is established.

## Staged implementation

1. Implement one correctness-first plan per ISA using broad invalidation and a
   full frozen target set.
2. Add the reference planner, trace replay, generated transition corpus, and
   profile/erratum registry.
3. Add address/range precision with machine-measured thresholds and verified
   dominance.
4. Add safe target pruning from the address-space activation invariant.
5. Evaluate deferred or hardware-coherent profiles as separate, explicitly
   weaker/stronger contracts rather than silent fast paths.

## Alternatives and tradeoffs

- **Always flush everything** is an auditable bootstrap but can turn frequent
  mapping changes into global tail-latency events.
- **Always flush individual pages** avoids broad collateral eviction but can be
  slower and may be insufficient for topology/global changes.
- **Lazy/deferred completion** can reduce IPIs, but moves enforcement into
  every user-return and privileged user-access path.
- **Hardware translation coherence** is architecturally attractive; until a
  shipping profile exposes precise, verified completion semantics, it remains
  a different backend rather than an assumption in the software protocol.

## Unresolved questions

- What is the smallest machine-profile schema that still captures relevant
  architecture revisions, hypervisor behavior, and errata?
- Can one mechanically checked dominance algebra cover x86, Arm, and RISC-V,
  or should only the semantic input/output be common?
- Which targets can be pruned without making scheduler state part of the
  trusted translation core?
- How should stage-1 and stage-2 plans compose under confidential or nested
  virtualization?
- Which additive-operation result should an asynchronous pager receive when
  immediate usability is unnecessary?
- How will real hardware expose a test oracle strong enough to catch rare
  stale-walker behavior?

## Connections

- [Address translation and protection transitions](../address-translation-and-protection-transitions.md)
- [Mapping transaction](mapping-transaction.md)
- [Translation-context allocator](translation-context-allocator.md)
- [Shootdown coordinator](shootdown-coordinator.md)
- [Reclamation gate](reclamation-gate.md)
- [Ordering, coherence, and code publication](../ordering-coherence-and-code-publication.md)
- [Interrupt event fabric](../interrupt-event-fabric.md)
- [Privileged entry, exit, and execution context](../privileged-entry-exit-and-execution-context.md)

## Sources

- [Intel system-programming documentation](../../../30-sources/intel-2026-system-programming-documentation.md)
- [Arm A-profile documentation](../../../30-sources/arm-2026-a-profile-system-architecture-documentation.md)
- [Relaxed virtual memory](../../../30-sources/simner-et-al-2022-relaxed-virtual-memory.md)
- [RISC-V privileged architecture](../../../30-sources/risc-v-international-2026-privileged-architecture.md)
- [RISC-V supervisor binary interface](../../../30-sources/risc-v-international-2025-supervisor-binary-interface.md)
- [TLB consistency](../../../30-sources/black-et-al-1989-tlb-consistency.md)
- [Ephemeral mapping management](../../../30-sources/elmeleegy-et-al-2005-ephemeral-mapping-management.md)
- [Optimizing TLB shootdown](../../../30-sources/amit-2017-optimizing-tlb-shootdown.md)
- [Don't shoot down TLB shootdowns](../../../30-sources/amit-et-al-2020-dont-shoot-down-tlb-shootdowns.md)
- [HATRIC](../../../30-sources/yan-et-al-2017-hatric.md)
- [RadixVM](../../../30-sources/clements-et-al-2013-radixvm.md)
