---
title: "Page-table and protection encoder"
kind: note
created: "2026-09-04"
maturity: developing
tags:
  - architecture-support
  - memory-protection
  - page-tables
  - privilege
  - virtual-memory
aliases:
  - "Translation descriptor encoder"
  - "Protection-region encoder"
---

# Page-table and protection encoder

The page-table and protection encoder should be the sole completely mediated
boundary that can construct, install, inspect, or retire raw CPU translation
descriptors. It should accept typed semantic entry kinds under an immutable
backend profile, never caller-provided flag words, and return private encoded
plans plus exact publication, invalidation, and reclamation obligations.

“Sole boundary” does not mean one large function. It means every normal, boot,
fault, recovery, and diagnostic path either uses the same checked constructors
or is a narrowly enumerated primitive with an equivalent invariant. The
encoder owns representation; the mapping validator owns admissibility, the
transaction owns sequencing, and the architecture-primitives capsule owns the
few instructions or stores that require unsafe implementation.

This is an evidence-backed proposal. No Atom encoder, generated table, or
hardware test exists yet.

## Question, scope, and operational standard

The question is:

> How can semantic mappings become ISA-specific descriptors without allowing
> raw bit patterns, contextual type confusion, writable table aliases, or
> undocumented ordering to bypass the portable protection contract?

The encoder owns:

- exact entry and protection-region representations for one pinned profile;
- legal leaf, table-link, invalid, guard, and region descriptor construction;
- physical-address-field width and alignment checks;
- permission, privilege, globality, memory-type, and selected extension bits;
- table topology and typed translation-structure pages;
- hardware-owned accessed/dirty-bit update policy;
- descriptor decode and semantic comparison for verification;
- architecture-specific store/publication recipes; and
- a claim ledger linking each recipe to a manual section, feature, CPU revision,
  and erratum.

It does not decide whether the caller has authority, choose a frame, infer
alias safety, select a higher-level invalidation target set, or free table
memory.

A candidate implementation is adequate only if:

1. Raw descriptors can be created only from `LeafSpec`, `TableLinkSpec`,
   `InvalidSpec`, or a complete typed region plan; entry kind is never inferred
   accidentally from attenuated rights bits.
2. Every reserved, ignored, implementation-defined, physical-address, and
   extension bit has one named owner and deterministic value.
3. The final encoded result decodes to the same semantic kind, extent, level,
   privilege, rights, memory type, and globality as the normalized validated
   specification; rights-subset is an additional safety check, not permission
   for silent attenuation. Only declared hardware-owned A/D-like state is
   abstracted by normalization.
4. Translation-structure pages cannot be written through any ordinary alias
   while reachable by a hardware root.
5. Hardware updates to accessed/dirty or analogous state cannot be lost by an
   unsafe whole-entry store or destructive read-modify-write.
6. A descriptor is built privately where possible; the first live store is
   performed only by an accepted mapping transaction.
7. Every live change returns an explicit invalidation and ordering recipe;
   “write the PTE” is never the complete effect.
8. The same semantic test vectors pass on at least two materially different
   ISA encoders, while unrepresentable semantics are rejected rather than
   approximated.

## Evidence and claim boundary

| Evidence | Supported conclusion | Limit |
| --- | --- | --- |
| [Mach machine-independent VM](../../../30-sources/rashid-et-al-1987-machine-independent-virtual-memory.md) and [SVR4.2 HAT](../../../30-sources/balan-gollhardt-1992-scalable-virtual-memory-hat-layer.md) | Most VM semantics can remain machine independent while a small module owns MMU-dependent representation | Historical modules do not establish modern safety or complete mediation |
| [Nested Kernel](../../../30-sources/dautenhahn-et-al-2015-nested-kernel.md) | Protecting table pages and mediating every MMU update can isolate the translation reference monitor | Its same-ring x86 prototype is primarily uniprocessor and incomplete for DMA/SMI |
| [Secure memory management](../../../30-sources/achermann-et-al-2020-secure-memory-management.md) | Every translation engine and name-resolution path must be inside or mediated by the reference monitor | The preprint does not define this encoder API |
| [SecVisor retrospective](../../../30-sources/franklin-et-al-2008-secvisor-retrospective.md) | Unvalidated physical provenance and writable physical aliases defeat an apparently narrow mapping policy | Bounded old-x86 case study, not a proof of Atom |
| [seL4 RISC-V page-map defect](../../../30-sources/sel4-foundation-2020-risc-v-page-map-defect.md) | Rights masking can transform a supposed leaf into a table link when raw fields encode contextual type | One historical defect; typed constructors are the Atom deduction |
| [Asterinas verification report](../../../30-sources/asterinas-community-2025-practical-page-table-verification.md) | Page purpose, table mode, entry type, paging constants, cursors, and tree/flat refinement are useful proof units | Work remains on concurrency and verified-binary linkage |
| Current [Intel](../../../30-sources/intel-2026-system-programming-documentation.md), [Arm](../../../30-sources/arm-2026-a-profile-system-architecture-documentation.md), and [RISC-V](../../../30-sources/risc-v-international-2026-privileged-architecture.md) documents | Entry kinds, levels, rights, memory types, hardware-owned bits, invalidation, and ordering differ materially | Normative specifications do not prove an implementation or shared abstraction |

The proposed Rust-like types, two-phase encoded plan, and decode assertion are
not source claims. They are measures intended to make the source-backed hazards
locally testable.

## Boundary with the unsafe architecture capsule

The encoder is the semantic owner, but it should not duplicate inline assembly
or raw control-register access. Component 1's [unsafe architecture-primitives
capsule](../unsafe-architecture-primitives-capsule.md) exposes only operations
such as aligned descriptor load/store, table-root install, and architecture
barriers whose preconditions are proven by typed tokens.

```text
validator
  -> encoder.represent(SemanticDelta, TranslationProfile)
  -> EncodedPrivatePlan<NonExecutableEffect>
     | ProvisionalCloseEncoding(payload + bounded finalization capacity)
     | ProvisionalPrivateExecutableEncoding(
           payload + expected suspension binding +
           bounded plan-and-guard finalization capacity)
     | ProvisionalPrivateExecutableRetirementEncoding(
           payload + exact published-version/retirement binding +
           bounded plan-and-guard finalization capacity)

accepted close transaction
  -> encoder.finalize_close(Frozen CloseObserverSnapshot)  // class L only

private code-publication enable path
  -> encoder.bind_execution_suspension(
         ProvisionalPrivateExecutableEncoding,
         Borrowed<Authorized<AddressSpaceExecutionSuspension<Held>>>)
  -> BoundPrivateExecutablePublication {
         plan: EncodedPrivatePlan<PrivateExecutable>,
         guard: MutationGuard<PrivateExecutable>,
         retained_suspension_borrow
     }

private code-retirement removal path
  -> encoder.bind_executable_retirement(
         ProvisionalPrivateExecutableRetirementEncoding,
         Borrowed<CodeRetirementOperation<ExecutorQuiescent>>,
         Borrowed<Authorized<ExecutableVersionExecutionQuiescent,
                             RemoveExecutableMappingsForExactVersion>>)
  -> BoundPrivateExecutableRetirement {
         plan: EncodedPrivatePlan<PrivateExecutableRetirement>,
         guard: MutationGuard<PrivateExecutableRetirement>,
         retained_operation_and_quiescence_borrows
     }

accepted transaction
  -> encoder.publish(
         EncodedPrivatePlan<EffectKind>,
         MutationGuard<EffectKind>,
         PublicationAuthorityFor<EffectKind>)
  -> architecture capsule operations
  -> PublishedDescriptorEvidence<EffectKind>
```

Neither the capsule nor a caller can synthesize a semantic mapping. The capsule
knows how to execute a primitive; the encoder knows why this particular
descriptor and recipe are valid.

Preparation reserves the eventual `operation_id`. For ordinary non-executable
effects the encoder seals the private plan to the complete proposed effect
before acceptance. Class `L` is different: its observer set does not exist
until the `Live` → `Closing` linearization, so preparation produces only a
committed provisional payload and preallocated finalization capacity. While the
close is non-dispatchable `Accepting`, it freezes `CloseObserverSnapshot`,
computes the final request and completion-requirements digests, and only then
seals the `PublicationBinding`/`EncodedPrivatePlan`.

`PrivateExecutable` is also finalized later, for a different reason.
Preparation can bind the exact reserved suspension incarnation, address space,
and code-publication operation into a provisional payload, but
`AddressSpaceExecutionSuspension<Held>` does not exist until execution admission
has closed and every frozen executor has drained or been terminally excluded.
The private code-publication enable path supplies that exact borrowed guard to
`bind_execution_suspension`, which uses preallocated capacity to seal the same
final binding into both the executable plan and its one-shot mutation guard.
`PrivateExecutableRetirement` is a third, disjoint effect. Its provisional
payload binds the exact published-code incarnation, parent retirement
operation, RX mapping/alias/extent set, persistent code-generation state, and
expected odd mutation sequence. It can be finalized only after no-new-dispatch
has committed and the exact version's executor set has become quiescent. The
private retirement path supplies both the matching
`CodeRetirementOperation<ExecutorQuiescent>` borrow and the version/source/
dispatch-epoch-bound `ExecutableVersionExecutionQuiescent` authority; a public
non-executable reduction cannot select this effect kind.
If class `L` has won the address-space gate, the only alternative is a
`ClosingAddressSpace` binding: the encoder requires the exact snapshot-bound
delegation from that close plus its whole-address-space execution-quiescence
proof. This branch may remove a frozen publication's prospective RX mapping or
a published version's RX mapping, but it can never enable execute access or
act for another child operation.
Ordinary accepted transactions mint their matching mutation guards at
acceptance; the class-`L` guard is minted during its non-dispatchable
finalization. The private executable guard cannot be minted earlier because the
held suspension fields do not yet exist. Neither `AcceptedReady` for class `L`
nor a live executable descriptor store may precede its required finalization:

```text
PublicationPrerequisite<EffectKind> =
    PrivateExecutable => HeldExecutionSuspensionBinding {
        suspension: AddressSpaceExecutionSuspensionIncarnation,
        address_space: AddressSpaceIncarnation,
        publication_operation: CodePublicationOperationIncarnation,
        execution_admission_epoch,
        suspension_digest
    }
  | PrivateExecutableRetirement => ExecutableRetirementRemovalBinding {
        published_or_prospective_code_incarnation,
        address_space: AddressSpaceIncarnation,
        code_publication_generation_state_incarnation,
        code_publication_generation_state_digest,
        exact_rx_mapping_alias_and_extent_set_digest,
        mutation_owner:
            ParentRetirement {
                retirement_operation: CodeRetirementOperationIncarnation,
                execution_quiescence_source_incarnation,
                dispatch_epoch,
                no_new_dispatch_gate_incarnation,
                executable_version_execution_quiescent_proof_digest,
                accepted_odd_mutation_sequence
            } |
            ClosingAddressSpace {
                close_operation_id,
                frozen_child_code_operation_incarnation,
                close_observer_snapshot_digest,
                address_space_close_execution_quiescent_proof_digest,
                accepted_odd_mutation_sequence,
                close_mutation_delegation_digest
            }
    }
  | NonExecutableEffect => NoExecutionSuspensionRequired

PublicationAuthorityFor<EffectKind> =
    PrivateExecutable =>
        Borrowed<Authorized<AddressSpaceExecutionSuspension<Held>>>
  | PrivateExecutableRetirement =>
        ParentRetirement {
            operation:
                Borrowed<CodeRetirementOperation<ExecutorQuiescent>>,
            quiescence:
                Borrowed<Authorized<ExecutableVersionExecutionQuiescent,
                                    RemoveExecutableMappingsForExactVersion>>
        } |
        ClosingAddressSpace {
            delegation:
                Borrowed<Authorized<
                    AddressSpaceCloseExecutableMutationDelegation,
                    RemoveProspectiveRx | RemovePublishedRx>>,
            execution_quiescent:
                Borrowed<Authorized<AddressSpaceCloseExecutionQuiescent>>
        }
  | NonExecutableEffect => NoExecutionSuspensionRequired

PublicationBinding<EffectKind> {
    operation_id,
    effect_kind,
    request_digest,
    completion_requirements_digest,
    encoded_payload_digest,
    address_space: AddressSpaceIncarnation,
    old_mapping_incarnations,
    proposed_mapping_incarnations,
    frame_incarnations_and_authority_epochs,
    table_pages: Set<TablePageIncarnation>,
    profile_id,
    publication_prerequisite: PublicationPrerequisite<EffectKind>,
    gate_expectation:
        AcceptedOdd(mutation_sequence, operation_owner_id) |
        AcceptedStableEven(mutation_sequence, operation_owner_id)
}

EncodedPrivatePlan<EffectKind> {
    binding: PublicationBinding<EffectKind>,
    payload: {
        sealed_descriptor_templates,
        publication_recipe,
        decoder_expectations,
        invalidation_constraints
    }
}

MutationGuard<EffectKind> {
    binding: PublicationBinding<EffectKind>,
    guard_capability_generation
}

PublishedDescriptorEvidence<EffectKind> {
    binding: PublicationBinding<EffectKind>,
    publication_epoch,
    exact_descriptor_effect_digest
}
```

Executable finalization requires the borrowed guard's suspension, address
space, and publication operation to equal the provisional reservation binding;
it then adds the immutable execution-admission epoch and suspension digest. A
mismatch after code-publication acceptance performs no descriptor store and is
an operation invariant/quarantine outcome, not a late representation error.

`encoded_payload_digest` is
`H(version_tag || canonical_encode(EncodedPrivatePlan.payload))`. Its domain is
exactly the descriptor templates, publication recipe, decoder expectations,
and invalidation constraints shown above; it excludes `PublicationBinding` and
the digest field itself, so the definition is not recursive. Before any store,
`publish` recomputes and compares that payload digest, requires exact equality
of both sealed bindings, and revalidates the operation, address-space, mapping,
frame-authority, table-page, profile, and guard-generation facts. It also
checks the effect-specific `gate_expectation`: a plan requiring a stable
observer snapshot must see its operation-owned odd sequence, while an ungated
additive/expansion plan must see its operation-owned unchanged stable-even
sequence. Universal “oddness” is not a publication precondition.

The publication prerequisite is effect-indexed rather than optional. A
non-executable effect must carry `NoExecutionSuspensionRequired`. A
`PrivateExecutable` effect must instead supply the exact live borrowed
`AddressSpaceExecutionSuspension<Held>` named by its binding. Before the first
store that can make an executable leaf reachable, `publish` revalidates exact
equality of suspension incarnation, address-space incarnation,
code-publication-operation incarnation, execution-admission epoch, and
suspension digest, and proves that the lifecycle/scheduler guard is still held.
The borrow remains live through all executable-leaf stores and construction of
`PublishedDescriptorEvidence`; the encoder cannot accept a sentinel on this
path. An `Authorized<CodePublication>` token may authorize preparation, but it
cannot by itself authorize the first executable leaf store.

A `PrivateExecutableRetirement` effect can publish only an RX-to-NX/invalid
restriction for the exact bound version. Before the first such store,
`publish` requires the parent operation to be in its noncancellable
`ExecutorQuiescent` typestate and revalidates the quiescence authority's
published-code, source, dispatch epoch, no-new-dispatch gate, frozen executor
set, generation-state incarnation/digest, RX mapping/alias/extent set, proof
digest, and operation-owned odd mutation sequence against the sealed binding.
The borrows remain live through the restrictive stores and evidence creation.
Neither an inspectable proof digest nor a generic `NonExecutableEffect`
authority can remove a published executable relation.
On the `ClosingAddressSpace` branch, the same checks are made against the close
operation, frozen child code operation, snapshot digest, exact mapping set,
whole-address-space execution proof, close-owned odd sequence, and one-effect
delegation. The two authority variants are disjoint; a close cannot be
presented as a retirement operation and neither can be reduced to a bare
operation ID.

A plan, mutation guard, or suspension from another operation—even one
describing identical virtual addresses or descriptor bits—is rejected before a
store. Returned evidence carries the same effect-indexed binding, so no later
invalidation or terminal record can substitute evidence from a different
effect or claim that an executable store occurred under a different
suspension.

## Immutable translation profile

Encoding is parameterized by a sealed profile, not ambient feature tests:

```text
TranslationProfile {
    profile_id,
    isa_and_architecture_revision,
    cpu_models_and_errata,
    regime_or_stage,
    root_and_entry_format,
    level_count,
    translation_granule,
    virtual_and_physical_widths,
    page_sizes_by_level,
    context_tag_scope_and_width,
    permission_vocabulary,
    memory_type_vocabulary,
    accessed_dirty_policy,
    global_mapping_policy,
    optional_extensions,
    invalidation_capabilities,
    ordering_recipes
}
```

Changing a control that alters descriptor interpretation—granule, level count,
physical size, MAIR/PAT-like vocabulary, translation mode, privilege regime,
or relevant extension—is an address-space reincarnation or a separately
modeled invalidate-and-rebind transition. It is not a mutable field read on
each encode call.

## Typed semantic inputs

Use disjoint types even if the hardware reuses bit layouts:

```text
TableLinkSpec<Profile, Level> {
    child: OwnedTablePage<Profile, Level + 1>,
    table_permissions,
    nonleaf_attributes
}

LeafSpec<Profile, Level> {
    frame: BorrowedFrameExtent,
    rights: EffectiveRights,
    privilege: UserData | KernelInternal | PrivateExecutable,
    memory_type: EffectiveMemoryType,
    globality,
    accessed_dirty_policy
}

InvalidSpec<Profile, Level> {
    invalid_kind: Empty | Guard | TransactionBreak,
    software_cookie: Option<ValidatedSoftwareBits>
}
```

`EffectiveRights` is constructed only after every capability and policy
intersection. The encoder rejects an empty data leaf, illegal right combination,
or entry kind unsupported at that level. A private executable leaf additionally
requires a code-publication token to prepare and cannot be constructed through
the public mapping API. Making that prepared leaf live additionally requires the
exact effect-bound `AddressSpaceExecutionSuspension<Held>` borrow; the earlier
code-publication token is not a store authority.

Software-reserved bits are allocated centrally. The profile identifies which
bits remain ignored by hardware in every supported revision; unknown future or
extension bits stay zero. Storing arbitrary pointers or capability identifiers
inside unused fields is forbidden unless a pinned profile and decoder own the
entire lifecycle.

## Represent, allocate, publish, and retire

### Pure representability

`represent` performs no table store. It checks:

- address-width fit after alignment and any encryption/tag transformation;
- legal entry kind at the requested level;
- exact page/block size and physical alignment;
- permission and privilege encodability without broadening;
- memory-type and shareability encodability;
- global/non-global semantics and invalidation implications;
- accessed/dirty mode and concurrent-update policy;
- optional extension and errata requirements; and
- whether replacement requires break-before-make or a wider operation.

It returns an `EntryTemplate` whose variable address field and fixed fields are
separately typed, plus a decoder expectation. Templates are ordinary data and
grant no right to publish. Only their sealed, digest-bound
`EncodedPrivatePlan` form can pair with the accepted operation's matching
`MutationGuard` at the publication boundary.

### Table topology allocation

Missing intermediate tables are allocated from reservations owned by the
prepared plan. A `TablePage<Profile, Level>` records physical identity,
generation, parent count, live-child count, and state:

```text
FreeFrame -> Initializing -> PrivateTable -> Linked -> Unlinking
          -> Retired<ReclamationGate> -> Reclaimable<TablePage> -> Retypable
```

`FreeFrame` is not merely a frame whose current mapping list looks empty. The
`FreeFrame -> Initializing` input combines an exact
`Authorized<FrameRef, RetypeAsPageTable>` with either a fresh-never-exposed
allocation proof or a linear reclamation-gate proof for that frame incarnation
and canonical physical extent/backing lineage. Under the shared global extent
reservation, the transition atomically closes new CPU, DMA/device, temporary,
and diagnostic writer admission; revalidates that all former writer aliases
are absent and their required CPU-access/translation, device/DMA, and reference
quiescence is complete; and only then advances the physical-purpose epoch. An
existing writer is first moved to `RetiringOldAccess` and drained by its owning
typed transition—the encoder cannot make it disappear during retype. After the
proof is revalidated, the encoder zeroes through a kernel-private window and
initializes legal invalid entries. A table page is not shareable between
independently owned address-space roots in the baseline.

The reverse transition consumes a linear `Reclaimable<TablePage>` token emitted
only by the reclamation gate after it independently validates
`CpuTranslationQuiescent`, `HardwareWalkerQuiescent(table)`,
`SoftwareReaderQuiescent`, `ReferenceQuiescent`, and every profile/provenance-
selected obligation. The encoder then zeroes/retypes the page and creates a new
frame incarnation. Hardware-walker evidence is only one gate input; neither it
nor a reference count proves the other predicates.

### Publication

The accepted transaction supplies the mutually bound, effect-indexed
`MutationGuard` and `PublicationAuthorityFor` described above. Publication
revalidates every binding field and then chooses the sealed recipe by semantic
change class. In particular, the invalid-to-private-executable case cannot reach
the architecture capsule until the exact held execution-suspension borrow has
passed that revalidation:

| Change | Encoder action | Returned obligation |
| --- | --- | --- |
| Invalid → non-executable leaf | publish initialized descendants, then leaf | backend-specific visibility and possible negative-cache invalidation |
| Invalid/NX → private executable leaf | revalidate the exact held suspension, publish initialized descendants, then the executable leaf while retaining the borrow | backend-specific visibility, instruction-fetch synchronization, and continued suspension until component 4 publishes the version |
| Permission upgrade | atomic legal leaf update | usability maintenance required by profile |
| Non-executable permission reduction/unmap | publish restrictive/invalid entry | `RestrictionPublished`, then external `RestrictionQuiescent` |
| Executable RX → NX/invalid | revalidate either the exact retirement-operation typestate plus exact-version quiescence authority or the disjoint class-`L` child-bound close delegation plus whole-space quiescence proof, then publish the restriction | `RestrictionPublished`, followed by translation/fetch completion and external `RestrictionQuiescent` returned only to the owning code-retirement or address-space-close operation |
| Frame, size, type, or entry-kind replacement | publish break, invalidate to completion, then publish make | old `RestrictionQuiescent` plus new `Usable`; transient fault may be legal |
| Remove nonleaf | publish parent break after children detached | table-retirement obligation set: CPU translation, hardware walker, software reader, and reference quiescence before the gate emits `Reclaimable<TablePage>` |
| Clear A/D metadata | architecture-specific atomic clear | observation fence/invalidation needed to make later sampling meaningful |

The encoder emits a trace of descriptor address, old/new decoded semantics,
store primitive, ordering steps, and claim identifiers. It redacts physical
addresses for callers without diagnostic authority while retaining protected
fault evidence.

## Architecture-specific encodings

### x86-64

The backend owns `P`, `R/W`, `U/S`, `XD`, global, PAT/cache-control, page-size,
physical-address, protection-key, accessed, dirty, and software fields under
the chosen paging mode. It validates reserved bits against physical width and
selected extensions.

Important constraints include:

- a non-present entry and a present table link/leaf have different legal
  fields;
- leaf size is determined by level plus the page-size bit, so changing size is
  an entry-kind/topology replacement;
- the effective privilege and write/execute result depends on all walk levels,
  not only the leaf;
- hardware may set accessed/dirty state, so concurrent software updates need an
  atomic masking strategy that preserves owned bits; and
- PAT and other physical-range memory-type rules cannot be derived from one
  leaf in isolation—the validator supplies the admitted effective type.

`INVLPG`, `INVPCID`, and control-register transitions are not emitted as raw
call-site choices. The encoder supplies change constraints to the invalidation
planner, which chooses a supported scope.

### AArch64

The backend distinguishes invalid, table, block, and page descriptors by both
level and low-bit pattern. It owns output address, access permissions, user/
privileged execute-never, access flag, dirty/write-management features,
AttrIndx, shareability, globality, and selected tagged or protected-memory
extensions.

Important constraints include:

- MAIR and translation-control state are part of the profile interpreting an
  AttrIndx; an index alone is not a semantic memory type;
- valid-to-valid changes to output address, size, memory type, or other fields
  may require break-before-make;
- descendant initialization and descriptor publication need the documented
  store/barrier/TLBI/completion sequence for the selected regime; and
- table and leaf permissions can interact across levels, so decode checks walk
  the complete path.

The backend records the exact architecture revision and CPU errata. A recipe
that is sound for the base architecture can require extra TLBI/barrier work on
a particular core revision.

### RISC-V supervisor translation

The backend distinguishes invalid entries, valid nonleaf table pointers
(`V=1` and `R=W=X=0`), and legal leaf permission combinations. It owns `V`,
`R/W/X`, `U`, `G`, `A`, `D`, physical-page number, RSW, and selected PBMT/NAPOT
or other extension fields. `V=0` is invalid regardless of `R/W/X`.

Important constraints include:

- `W=1, R=0` and other reserved combinations are rejected for the selected
  revision;
- a valid entry whose rights become `R=W=X=0` is a nonleaf rather than a leaf—
  this exact semantic type confusion caused the documented seL4 defect;
- superpage PPN fields must meet level-specific alignment;
- nonleaf/global ancestry affects the legal invalidation scope; and
- A/D behavior depends on the profile's hardware-update or fault-based scheme.

Unsupported `satp` modes or extensions are not “best effort.” The profile
constructor probes or obtains trusted boot facts, then rejects an unsupported
configuration before an address space is sealed.

### RISC-V PMP region protection

Finite ordered-region hardware does not use page-table entry kinds. Its
encoder consumes a complete `RegionPlan`, because one entry's meaning can
depend on priority, the previous bound, alignment encoding, granularity, and
lock state. For RISC-V PMP, the lowest-numbered matching entry wins, TOR uses a
predecessor as a lower bound, NAPOT imposes power-of-two alignment, and locked
entries constrain later mutation.

A single-region convenience call must still compile and validate the entire
ordered plan. If the region capacity or atomic transition cannot preserve the
requested isolation, the backend reports an unsupported profile rather than
pretending it has page-table atomicity.

This evidence supports the RISC-V PMP backend only. A future generic MPU or
other ordered-region backend needs its own pinned specification, semantic
model, capacity rules, and transition proof; this report does not infer those
properties from PMP.

## Hardware-owned state

Accessed, dirty, young, and analogous bits require a declared ownership model:

1. `HardwareManaged`: hardware may set named bits atomically; software updates
   preserve them unless explicitly sampling/clearing.
2. `FaultManaged`: entries begin without access/dirty permission and faults
   drive a separate metadata transaction.
3. `Hybrid`: selected features let hardware update while software periodically
   samples under an architecture-specific observation protocol.

Clearing a bit is not an ordinary mapping update. Without the required
invalidation or ordering, a later clear bit may fail to prove no subsequent
access occurred. The transaction classifies metadata observation separately
and returns `AccessObservation(epoch, confidence_scope)`, never a permission-
transition completion token.

Whole-entry compare-and-swap must mask and merge hardware-owned bits under the
pinned manual's rules. If the hardware can modify a field in a way the atomic
primitive cannot preserve, the backend uses locks/fault management or rejects
that feature combination.

## Complete mediation audit

At build time, maintain an allowlist of symbols that can:

- write memory typed as a translation structure;
- install or change a translation root;
- change translation-control or attribute registers;
- execute local invalidation instructions;
- request remote invalidation; or
- retype table memory.

Boot assembly receives a minimal provisional-root builder. Before general
allocation or untrusted input, the kernel imports those roots by decoding them
into the first ledger, verifies protected ranges, and transfers them to normal
encoder ownership. Recovery may freeze or install a prevalidated emergency
root but cannot edit arbitrary live entries. Diagnostic code receives read-
only decoded views unless a fatal machine-reset path explicitly supersedes the
normal contract.

Generated-code inspection and linker/visibility rules should fail a build when
another component acquires these primitives. This is defense in depth; the
runtime page protections on table pages remain necessary.

## Error and failure semantics

### Preparation errors

`Unrepresentable`, `IllegalEntryKind`, `AddressWidthExceeded`, `Misaligned`,
`UnsupportedMemoryType`, `ReservedBitConflict`, `ProfileMismatch`, and
`ErratumUnsupported` are pre-effect errors. They return the immutable request
and reservations unchanged.

### Post-publication failures

After the first live store, the encoder cannot return a representation error.
A machine check, failed readback, unexpected descriptor, or primitive fault
produces a protected `ArchitectureFaultRecord` and moves the encompassing
transaction toward forward completion, `Incomplete`, quarantine, or fatal
containment. Rewriting the old bits is not an invisible rollback.

### Decode mismatch

In verification or high-assurance profiles, read back and decode a descriptor
after the required visibility point. A mismatch freezes the address space,
captures the raw word and profile identity, and prevents activation. It is not
safe to continue by trusting either the ledger or the unexplained hardware
state alone.

## Verification strategy

### Encoder/decoder properties

For every profile and legal level, generate semantic specifications and check:

```text
decode(encode(spec)) == normalize(spec)
decode(encode(spec)).rights == normalize(spec).rights
decode(encode(spec)).rights ⊆ spec.rights       // independent safety check
encode(spec).reserved_bits == profile.required_reserved_values
```

Generate illegal combinations at every bit boundary and require typed
rejection. Include rights attenuation to empty, leaf/nonleaf ambiguity,
maximum physical addresses, misaligned superpages, unknown extensions, and
every memory type.

### Tree-to-ledger refinement

Construct random legal ledgers, compile complete trees, decode every reachable
path, and compare effective rights including ancestor restrictions. Then inject
partial topology, orphan table pages, alias writes, hardware A/D updates, and
stale generations. Only transients owned by one accepted operation may differ
from the flat ledger.

### Concurrency and hardware tests

- Race hardware A/D updates against permission changes and sampling.
- Remove a nonleaf while CPUs fault and walk its descendants.
- Attempt writes through every direct, temporary, DMA, and stale alias of a
  live table page.
- Run ISA-specific virtual-memory litmus tests for invalid-to-valid, reduction,
  break-before-make, leaf/nonleaf replacement, and table-page reuse.
- Inspect emitted assembly and run on real target revisions, not only emulators;
  record errata and virtualization environment.
- Differentially compare a simple model encoder and optimized production
  encoder over the same vectors.

### Assurance boundary

Translation validation can check generated machine code against a low-level
contract, as the existing [translation-validation source](../../../30-sources/sewell-et-al-2013-translation-validation.md)
motivates, but it does not supply correct hardware semantics. The claim ledger
must connect source types, compiler output, architecture model/manual, and
tested CPU profile without calling any one layer a complete proof.

## Measurements

Measure pure encoding time, table-page allocation/zeroing, topology creation,
live-store critical sections, readback/decode checks, A/D handling, page-size
splits, table memory per mapping, and added cost of protected table access.
Report distributions for cold and hot tables and mutation-heavy workloads.
Nested Kernel's historical low overhead and Asterinas's proof size are context,
not performance budgets.

## Staged implementation

1. Define one immutable profile and pure model encoder/decoder for one page
   size; exhaustively test the small semantic state space.
2. Add typed table pages, remove ordinary writable aliases, and compile a
   single-CPU tree from a flat ledger.
3. Add live publication through accepted transactions, hardware-owned-bit
   policy, readback tracing, and local invalidation tests.
4. Add large pages, topology replacement, table-page reclamation, and
   adversarial concurrency.
5. Implement a materially different second ISA using the same semantic vector
   suite and compare rejection surfaces explicitly.
6. Only after correctness, consider code generation from machine descriptions,
   specialized fast paths, or a region-protection backend.

## Alternatives and trade-offs

### Public raw-PTE helpers

They are easy to port existing kernel code to, but make complete mediation,
type, reserved-bit, and authority audits nearly impossible. They are rejected.

### One universal packed descriptor type

It hides contextual leaf/table and level differences until runtime and invites
the class of defect seen in seL4's RISC-V mapping path. Separate semantic types
are intentionally repetitive.

### Generated encoders

Generation from a trusted machine description could reduce handwritten bit
errors and produce decoders/tests together. It also adds a generator and
specification language to the assurance chain. Begin with small reviewed
encoders, then compare generated candidates through the same vectors.

### Permanently writable self-map of page tables

It makes traversal convenient but creates a broad mutation capability and
expands the blast radius of corruption. A narrowly scoped encoder window or
protected kernel-only mapping is the baseline.

## Unresolved questions

- Which exact x86-64 and AArch64 or RISC-V profile should be implemented first,
  including CPU revisions and errata?
- Should decoder/readback checks run on every transition, only debug builds,
  or a sampled high-assurance profile?
- Can a single table-page ownership protocol cover split kernel/user roots,
  nested translation, and IOMMU structures without erasing their different
  completion rules?
- Which A/D policy best supports an unprivileged pager without exposing raw
  architecture bits?
- How should encryption, tagging, protection keys, and capability-memory
  extensions enter the semantic rights vocabulary?
- Can the unsafe symbol allowlist be enforced at link time across boot and
  recovery assembly?

## Connections

- [Parent translation component](../address-translation-and-protection-transitions.md)
- [Mapping validator](mapping-validator.md)
- [Mapping transaction](mapping-transaction.md)
- [Invalidation planner](invalidation-planner.md)
- [Reclamation gate](reclamation-gate.md)
- [Unsafe architecture-primitives capsule](../unsafe-architecture-primitives-capsule.md)
- [Ordering, coherence, and code publication](../ordering-coherence-and-code-publication.md)

## Sources

- [Machine-independent virtual memory management](../../../30-sources/rashid-et-al-1987-machine-independent-virtual-memory.md)
- [SVR4.2 HAT layer](../../../30-sources/balan-gollhardt-1992-scalable-virtual-memory-hat-layer.md)
- [Nested Kernel](../../../30-sources/dautenhahn-et-al-2015-nested-kernel.md)
- [Secure memory management on modern hardware](../../../30-sources/achermann-et-al-2020-secure-memory-management.md)
- [SecVisor retrospective](../../../30-sources/franklin-et-al-2008-secvisor-retrospective.md)
- [seL4 RISC-V page-map defect](../../../30-sources/sel4-foundation-2020-risc-v-page-map-defect.md)
- [Asterinas page-table verification report](../../../30-sources/asterinas-community-2025-practical-page-table-verification.md)
- [Translation validation for a verified OS kernel](../../../30-sources/sewell-et-al-2013-translation-validation.md)
- [Intel system-programming documentation](../../../30-sources/intel-2026-system-programming-documentation.md)
- [Arm A-profile system architecture documentation](../../../30-sources/arm-2026-a-profile-system-architecture-documentation.md)
- [RISC-V privileged architecture](../../../30-sources/risc-v-international-2026-privileged-architecture.md)
