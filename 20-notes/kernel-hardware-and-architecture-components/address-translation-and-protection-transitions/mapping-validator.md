---
title: "Mapping validator"
kind: note
created: "2026-09-04"
maturity: developing
tags:
  - architecture-support
  - capabilities
  - memory-protection
  - security
  - virtual-memory
aliases:
  - "Translation mapping validator"
---

# Mapping validator

The mapping validator should be a total, side-effect-free admission engine over
typed requests, followed by one short revalidation at transaction acceptance.
It should translate untrusted ranges, frame references, requested rights,
memory types, page sizes, and replacement intent into a fully reserved
`PreparedMappingPlan`, or reject before any architecturally visible mutation.

The validator is the only place where the portable translation component may
turn authority plus policy into an admissible semantic mapping. The encoder may
reject an unrepresentable backend plan during preparation, but it may not
invent policy, broaden rights, repair an alias silently, or infer authority
from a physical address.

This design is proposed. It has not been model checked, fuzzed, or run on an
Atom kernel.

## Question, scope, and operational standard

The question is:

> What must be proven and reserved before a mapping mutation can be accepted
> such that all remaining failures have explicit post-effect handling rather
> than becoming partial unauthorized state?

The validator owns:

- checked arithmetic and address-range normalization;
- address-space, mapping, and frame capability validation;
- access-ceiling enforcement and operation-class classification;
- overlap, replacement, page-size, alias, and memory-type rules;
- backend representability checks through a pure encoder query;
- quota, table-page, operation-record, and teardown-capacity admission; and
- binding the result to the exact object incarnations and generations that
  were examined.

It does not allocate a frame, choose virtual layout, decide paging or copy-on-
write policy, write a page table, flush a translation, publish executable code,
or decide what to do after a target CPU fails.

A candidate passes only if:

1. Every byte of the requested range is within the caller's address-space
   envelope and every backing byte is within current frame authority.
2. Empty, wrapping, noncanonical, misaligned, reserved, cross-boundary, and
   unrepresentable ranges are rejected deterministically.
3. Requested rights must fit the address-space, mapping, frame, and backend
   access ceiling exactly; the public API rejects implicit attenuation, empty
   leaves, and unsupported semantics.
4. The baseline never admits persistent W+X or an executable physical extent
   that remains writable through any CPU, DMA, device, or diagnostic alias.
5. Incompatible cacheability or device-memory aliases are rejected before
   mutation unless an explicit closed-world transition plan removes the old
   aliases first.
6. Replace, upgrade, reduction, and unmap name the old
   `MappingIncarnation` through an authorized `MappingRef`; split and join name
   every affected mapping and table-page incarnation. Overlap does not imply
   replace.
7. All resources needed after acceptance—including failure and quarantine
   records—are reserved before the first visible effect.
8. Acceptance revalidates every mutable fact used during preparation and
   either rejects unchanged or transfers all reserved resources to exactly one
   operation.

## Evidence and claim boundary

| Evidence | Supported conclusion | Limit |
| --- | --- | --- |
| [Protection of information](../../../30-sources/saltzer-schroeder-1975-protection-information.md) | Complete mediation, least privilege, economy of mechanism, and fail-safe defaults are durable design principles | Principles do not define modern PTEs or a concrete capability ABI |
| [Least-privilege memory protection](../../../30-sources/achermann-et-al-2019-least-privilege-memory-protection.md) | Translator-configuration authority and memory-access authority must both be represented | Atom's exact authority intersection remains proposed |
| [seL4 reference manual](../../../30-sources/sel4-foundation-2026-reference-manual.md) | VSpace/paging-structure/frame objects and mapping relations can be capability-mediated; a Page capability carries frame authority and mapping state when mapped | The manual does not establish Atom's distinct `Mapping` object/`MappingRef`, and seL4's proof does not transfer |
| [Asterinas page-table verification](../../../30-sources/asterinas-community-2025-practical-page-table-verification.md) | Alignment preconditions, page-purpose types, range cursors, and flat/tree refinement can be made verification targets | Work-in-progress proof does not cover this admission transaction |
| [Secure memory management](../../../30-sources/achermann-et-al-2020-secure-memory-management.md) | Typed translation objects and authority derivation can expose memory-management invariants across hardware and software layers | The framework does not instantiate Atom's validator or transaction protocol |
| [SecVisor retrospective](../../../30-sources/franklin-et-al-2008-secvisor-retrospective.md) | Physical-frame provenance and executable-page policy must be mediated across aliases, not inferred from one virtual mapping | The prototype's hypervisor threat model and platform differ from Atom |
| [seL4 RISC-V page-map defect](../../../30-sources/sel4-foundation-2020-risc-v-page-map-defect.md) | Attenuating permissions can change a would-be leaf into another descriptor interpretation, so final encoded semantics must be revalidated | One historical defect is evidence of the hazard, not a complete validation method |
| [ret2dir](../../../30-sources/kemerlis-et-al-2014-ret2dir.md) | A supervisor alias of a user-controlled frame can bypass virtual-address-based access defenses | Historical exploits require an additional corruption primitive and do not evaluate Atom |
| [Nested Kernel](../../../30-sources/dautenhahn-et-al-2015-nested-kernel.md) | Declaring and protecting page-table pages and mediating every MMU-control path can narrow the trusted admission boundary | The same-ring x86 prototype is primarily uniprocessor and does not cover all DMA or SMI paths |
| [CertiKOS](../../../30-sources/gu-et-al-2016-certikos.md) and [Serval](../../../30-sources/nelson-et-al-2019-serval.md) | Validator assurance should state its abstraction boundary and omitted hardware behavior, and executable ISA-level checks can expose implementation and compiler defects | Neither work verifies Atom's mapping policy, contemporary translation caches, or this proposed validator |
| Current [Intel](../../../30-sources/intel-2026-system-programming-documentation.md), [Arm](../../../30-sources/arm-2026-a-profile-system-architecture-documentation.md), and [RISC-V](../../../30-sources/risc-v-international-2026-privileged-architecture.md) manuals | Legal addresses, descriptor bits, page sizes, memory attributes, and transition restrictions depend on the pinned ISA profile | Manuals specify mechanisms, not a common validator or capability policy |

The exact validation order, error algebra, physical-extent W^X rule, and
reservation scheme below are Atom proposals. They are deliberately more
restrictive than some hardware permits so the first profile has a small
security argument.

## Input types

There should be no public `map(virtual_address, physical_address, flags)`.
Preparation takes typed references and semantic attributes. Reusable
address-space authority is borrowed; linear frame, mapping, and output-grant
authority is consumed only as shown:

```text
MappingRequest =
    Add {
        space: Borrowed<Authorized<AddressSpaceRef, MapWithin>>,
        range: UserVirtualRange,
        frame: Authorized<FrameRef, Map>,
        frame_offset,
        rights: DataRights,
        memory_type: MemoryType,
        preferred_page_sizes,
        output_ref_grant: Authorized<MappingRefGrantTemplate>,
        expected_space_sequence
    }
  | Upgrade {
        mapping: Authorized<MappingRef, Protect>,
        new_effective_rights: DataRights
    }
  | Reduce {
        mapping: Authorized<MappingRef, Protect>,
        new_rights: DataRights,
        returned_ref_authority:
            Preserve |
            AttenuateTo {
                retained_operation_verbs,
                retained_access_ceiling
            }
    }
  | Replace {
        old_mapping: Authorized<MappingRef, Replace>,
        new_frame: Authorized<FrameRef, Map>,
        new_frame_offset,
        new_rights,
        new_memory_type,
        output_ref_grant: Authorized<MappingRefGrantTemplate>
    }
  | Unmap {
        mapping: Authorized<MappingRef, Unmap>
    }
  | Close {
        space: Authorized<AddressSpaceRef, Close>,
        expected_space_sequence
    }
```

Every `MappingRef` resolves one exact `MappingIncarnation = (mapping_id,
mapping_generation)` in one `AddressSpaceIncarnation`, independently
attenuated operation rights, an immutable `capability_access_ceiling`, and a
capability generation, plus exact `ReferenceLineageIncarnation`,
`ReferenceGateIncarnation`, and observed reference-admission epoch. Neither a range nor a bare generation selects a
mapping. Derivation may only remove operation verbs or lower the access
ceiling; revalidation compares the complete nominal identity and capability
generation carried by the authorized reference.

`MappingRefGrantTemplateIncarnation` is the nominal pair
`(grant_template_id, grant_template_generation)`; neither a generation nor an
address-space/range tuple alone identifies this linear one-shot authority.
`MappingRefGrantTemplate` is capability-kernel data bound to one address-space
incarnation, an `authorized_mapping_range`, that exact template incarnation,
one nominal reference lineage/gate pair, and the anchor epoch at which it was
published.
It names the maximum operation verbs and access ceiling that may be minted into
a returned reference; it is not supplied as an untrusted bit mask. For `Add`,
the proposed relation range must be contained in both the template's
`authorized_mapping_range` and the `MapWithin` range, while the requested
output verbs and ceiling must be subsets of both the template and the
`MapWithin` envelope's output-grant ceiling. For `Replace`, the proposed
relation range must remain within the template range and the output authority
must additionally be no wider than the presented old `MappingRef`'s verbs and
access ceiling. A caller
authorized only to add or replace a relation therefore does not implicitly
receive `Protect`, `Unmap`, inspection, or broader access authority on success.
The template is a linear one-shot input to this submission: rejection returns
it unchanged, while acceptance moves the validated verb/access intersection
into an effect-keyed `AdmittedOutputRefGrant` owned by the operation until its
terminal disposition.

`DataRights` cannot express execute. Component 4 owns the public executable-
publication protocol and invokes a private, pre-reserved translation plan with
an unforgeable `Authorized<CodePublication>` witness.

Class `L` is authorized by the exact current `AddressSpaceRef<Close>` and never
by a `MapWithin` envelope. Its close capability and expected sequence are moved
into the prepared plan and revalidated before the irreversible `Live` →
`Closing` acceptance linearization.

Raw integers are parsed into `UserVirtualRange`, `FrameOffset`, `PageSizeSet`,
and bounded lengths before semantic validation. Each type constructor uses
checked arithmetic and rejects invalid values; unsafe casts do not occur in
the validator.

## Validation pipeline

The order is chosen so cheap structural rejection happens before costly global
queries, while no successful plan depends on an unchecked later assumption.

### 1. Shape and arithmetic

- Reject zero length unless a specific no-op query API permits it.
- Compute `end = base + length` with checked addition, then retain a half-open
  range `[base, end)`; never validate with a wrapping end address.
- For a nonempty half-open range, check canonicality or implemented virtual-
  address width for `base` and the last included byte `end - 1`, then check
  `[base, end)` containment. `end` itself may legally equal the first excluded
  address and is not dereferenced.
- Reject a range that crosses the configured user/kernel boundary, recursive
  table area, guard region, or backend-reserved hole.
- Check frame-offset plus length for overflow and against frame extent.
- Check base, offset, and length against the selected leaf granularity.

The preferred page-size list is a performance hint. The plan may select a
smaller supported size without weakening rights or crossing object boundaries,
but it must record the choice. It may not silently round the range outward.

### 2. Object identity and authority

Resolve every capability once into a borrowed, generation-checked kernel
object and retain the borrow in the preparation snapshot. `Add` requires an
address-space handle whose `MapWithin` envelope admits the complete range,
rights, and output-reference grant, plus a frame handle for the complete
canonical physical extent. `Upgrade` and `Reduce` require `Protect` on the
exact `MappingRef`; `Replace` requires its `Replace` verb plus the new frame
and output-grant authorities; and `Unmap` requires its `Unmap` verb. They do not
also depend on an ambient address-space mutation right. The protected
address-space record nevertheless supplies the immutable mapping ceiling and
lifecycle check. Then compute the access ceiling:

```text
access_ceiling =
    address_space_mapping_ceiling
  ∩ frame_access_ceiling
  ∩ mapping_maximum_rights          // for existing mappings
  ∩ mapping_ref.capability_access_ceiling // Protect or Replace
  ∩ profile_access_ceiling

require requested_rights ⊆ access_ceiling
effective_rights = requested_rights
```

The public API rejects `requested_rights` that exceed this ceiling rather than
silently narrowing them. If a future batch language permits attenuation, it
must opt in explicitly, state minimum acceptable rights, and return the actual
rights; it still cannot produce an empty leaf.

For `Protect`, both reductions and later expansions are evaluated under the
presented reference's ceiling even when the durable mapping object has a wider
maximum. For `Replace`, that ceiling also bounds the rights of the replacement,
in addition to the new frame and address-space ceilings. `Add` has no prior
`MappingRef`; its returned reference records an immutable ceiling no wider than
the authority snapshot admitted for the new mapping. Both operations mint
exactly the output verbs and access ceiling admitted by the validated
`MappingRefGrantTemplate`, never a default all-verbs reference.

The address space and frame must be `Live`; every acting handle and object
incarnation must be current; and the frame-authority epoch must admit CPU
translation over the full extent. The address-space lifecycle owner need not
equal the frame owner when an explicit delegated frame capability grants the
acting domain the requested extent and rights. A raw frame number obtained
from a device, log, or earlier lookup has no authority.

Shared-frame mapping requires explicit authority for each address space. The
validator never infers sharing from the existence of another mapping.

### 3. Rights lattice and transition class

Normalize requests into a small semantic lattice:

```text
NoDataRights < Read < ReadWrite
NoExecute < Execute            // private publication path only
User and Supervisor are separate domains, not another bit to OR
```

`NoDataRights` and `NoExecute` are lattice bottoms used while intersecting
authority; their conjunction is not a valid leaf. Semantic mapping absence is a
separate `Absent` value produced only by the `Unmap`/invalid-entry path.

After the ceiling check, construct a fresh `EffectiveLeaf` from the exact
requested semantic rights and ask the encoder to decode its proposed
representation back into those semantics. Empty data rights produce
`EmptyEffectiveLeaf` rather than an entry. In particular, clearing
read/write/execute bits must never cause an ISA to reinterpret the word as a
valid nonleaf table link or another descriptor kind. This final reconstruction
is mandatory even when an earlier requested leaf was representable.

Classify each change by comparing old and new semantic mappings:

| Class | Examples | Required downstream proof |
| --- | --- | --- |
| Additive | invalid → read-only data | publication and any negative-cache invalidation needed for `Usable` |
| Upgrade | read → read/write | `Usable`; stale denial is not a policy bypass but still affects caller semantics |
| Restrictive | read/write → read; mapped → `Absent` through `Unmap` | `RestrictionPublished`, then CPU-translation and privileged-access-borrow closure as `RestrictionQuiescent` |
| Replacement | frame A → frame B at one range | break old mapping, establish `RestrictionQuiescent`, publish new mapping, establish `Usable` |
| Attribute change | normal memory → device or cacheability change | close old CPU access with `RestrictionQuiescent`, close conflicting aliases, run the cache protocol, and establish new usability |
| Table topology | split/join or remove intermediate table | `CpuTranslationQuiescent` plus distinct hardware-walker and software-reader proofs before the table-page reclamation gate may retype memory |

If a request contains both upgrade and reduction dimensions, choose the
stronger replacement/break path. The validator never treats an opaque flags
word as a monotonic upgrade.

### 4. Ledger and alias invariants

Under a range intent or mutation snapshot, query:

- overlapping virtual mappings and guard/reserved ranges;
- every CPU, IOMMU, DMA, device, and diagnostic alias whose normalized
  canonical physical extent overlaps the requested bytes, plus its authority
  epoch and backing lineage;
- effective write and execute rights across those aliases;
- memory type, cacheability, shareability, encryption, and device attributes;
- pins, code-publication state, DMA ownership, and teardown state; and
- huge-page ancestors or descendants that a smaller change must split.

Baseline rules:

- `Add` requires an entirely unmapped range. `Replace` must name exactly the
  existing generation it will supersede.
- No executable physical byte may remain writable through any CPU, IOMMU/DMA,
  device, or diagnostic alias, even when overlapping extents are represented
  by different frame objects or address spaces. The code-publication lifecycle
  is the only baseline transition between those states.
- A code image in `Sealing` carries the seal operation's exclusive extent
  reservations, advanced/revoked frame-write epochs, and operation-owned
  `RetiringOldAccess`/write-admission deny state. From `Sealed` through
  `Published` and retirement it carries a persistent `SealedWriteDeny` ledger
  entry for the exact extents/backing lineages and epochs. Any proposed CPU,
  IOMMU/DMA, device, or diagnostic write alias conflicts even before an RX alias
  becomes live; a stale `FrameRef` cannot bypass either phase.
- User-owned frames have no ambient supervisor direct-map alias in the secure
  profile. An explicitly borrowed temporary alias is tracked separately.
- Normal, noncacheable, device, and write-combining interpretations may not
  conflict across live aliases. An architecture-specific exception must be an
  explicit profile rule with a transition plan.
- `PendingAdd` and `RetiringOldAccess` entries in the global alias ledger retain
  their proposed or old effective W^X and memory-type hazards. Logical detach
  cannot make a conflicting alias admissible while a stale translation, helper
  borrow, cache interpretation, or device path may still use the old meaning.
- Component-local DMA states `PendingInstall` and `PendingDeviceAccess` project
  to `PendingAdd` with intended device rights, memory type, extent/lineage, and
  enforcement profile. Alias admission always tests this normalized state
  under the shared reservation.
- Live frame objects may not overlap physically unless they are explicit
  derived views of one canonical backing object and participate in the same
  global alias index. A frame admitted for page-table, kernel-object, secret,
  or device-control purpose cannot be reinterpreted as ordinary user data
  until its prior generation is fully reclaimed and retyped.

The CPU validator reads DMA and code ledgers but does not claim to complete
their teardown. Reading those ledgers is not sufficient for concurrent
admission: CPU mapping, component-4 code publication, IOMMU/DMA mapping, and
device or diagnostic alias creation all serialize through the same canonical-
physical-extent/backing-lineage reservation protocol. A cross-component
transaction obtains the other components' teardown proofs before the frame
becomes reusable.

### 5. Backend representability

Pass a normalized, authority-free semantic leaf description to the encoder's
pure `represent` query. It returns either:

```text
Represented {
    selected_page_size,
    leaf_template,
    topology_changes,
    publication_recipe,
    invalidation_constraints,
    hardware_owned_bit_policy
}
```

or a typed reason such as `UnsupportedPageSize`, `UnrepresentableRights`,
`PhysicalWidthExceeded`, `MemoryTypeUnavailable`, `RequiresBreakBeforeMake`,
or `ProfileErratum`. The validator does not approximate execute-only as read-
execute, device memory as ordinary noncacheable memory, or unsupported range
invalidation as no invalidation.

### 6. Work and resource admission

Before success, compute a conservative bound for:

- new table pages and split/join metadata;
- ledger records and mapping identities;
- target-set and invalidation-plan storage;
- per-CPU queue slots or the safe coalescing fallback;
- completion, diagnostic, cancellation, and quarantine records;
- frame/table pins held until reclamation; and
- generation-bound reservations for every affected canonical physical extent
  and backing lineage in the global alias ledger; and
- bounded kernel CPU time charged to the requester.

Reserve those resources atomically against object quota and the system's
teardown reserve. A restrictive close path may draw from a separately protected
reserve so an attacker cannot prevent revocation by consuming ordinary quota.

## Prepared plan and acceptance revalidation

Successful preparation returns an immutable object:

```text
AddressSpaceAuthoritySnapshot<OperationKind> =
    Add => MapWithinAuthority {
        address_space: AddressSpaceIncarnation,
        capability_generation,
        verb: MapWithin,
        full_map_envelope: {
            authorized_virtual_range,
            authorized_frame_constraints,
            rights_ceiling,
            output_ref_grant_ceiling
        }
    }
  | Close => CloseAuthority {
        address_space: AddressSpaceIncarnation,
        capability_generation,
        verb: Close
    }
  | Upgrade | Reduce | Replace | Unmap => NoAddressSpaceAuthority

PreparedMappingPlan {
    plan_id,
    operation_kind,
    request_commitment:
        SealedRequestDigest(request_digest) |
        DeferredCloseRequest(provisional_request_domain_digest,
                             snapshot_slot_id,
                             bounded_capacity_commitment),
    address_space: AddressSpaceIncarnation,
    expected_mutation_sequence,
    authority_snapshot: {
        address_space_authority:
            AddressSpaceAuthoritySnapshot<operation_kind>,
        mapping_ref_authority?: {
            address_space: AddressSpaceIncarnation,
            mapping: MappingIncarnation,
            capability_generation,
            verbs,
            capability_access_ceiling,
            reference_lineage: ReferenceLineageIncarnation,
            reference_gate: ReferenceGateIncarnation,
            observed_reference_admission_epoch
        },
        frame_authority?: {
            frame_identity_and_incarnation,
            authorized_byte_extent_and_offset,
            capability_generation,
            rights,
            frame_authority_epoch
        },
        output_ref_template_authority?: {
            template: MappingRefGrantTemplateIncarnation,
            address_space: AddressSpaceIncarnation,
            reference_lineage: ReferenceLineageIncarnation,
            reference_gate: ReferenceGateIncarnation,
            observed_reference_admission_epoch,
            authorized_mapping_range,
            verbs,
            access_ceiling
        }
    },
    linear_close_authority:
        NotApplicable |
        PreparedOwned(Authorized<AddressSpaceRef, Close>),
    affected_mapping_incarnations,
    frame_incarnations_and_authority_epochs,
    semantic_delta,
    encoding_plan:
        Sealed(EncodedPrivatePlan) |
        DeferredCloseEncoding(provisional_payload_digest,
                              reserved_encoding_capacity),
    requires_stable_observer_snapshot,
    alias_snapshot,
    alias_extent_reservations,
    completion_requirements: CompletionRequirements,
    resource_reservations,
    reservation_expiry_admission_sequence
}
```

For every effect except class `L`, `request_digest` is
`H(request_domain_version || canonical_encode(normalized_request,
authority_snapshot, completion_requirements_and_refinement))`. The normalized
request contains the operation/effect kind, address-space incarnation and
expected sequence, exact virtual range, frame offset/extent and old/new frame
and mapping incarnations, requested and admitted rights, memory type, selected
page-size semantics, and alias-ledger intent. The authority member is the
complete joined snapshot above, including the exact admitted output-template
incarnation and range when present. `Add` carries the complete
`MapWithinAuthority`; class `L` instead carries `CloseAuthority` and has no
fabricated mapping envelope. The final member is the complete checked
`CompletionRequirements` plus its refinement digest. The domain excludes
`EncodedPrivatePlan`, `PublicationBinding`, and `request_digest` itself, so it
is nonrecursive; `PublicationBinding` later couples this semantic digest to the
encoder's separate payload digest. The address-space member is total and
operation-indexed; each remaining optional authority member is present exactly
when its effect kind consumes or borrows that authority.

The class-`L` `CloseAuthority` member is only an equality snapshot. The actual
linear `Authorized<AddressSpaceRef, Close>` is held in
`linear_close_authority=PreparedOwned` and moves intact through every
pre-acceptance rejection. At the irreversible `Live -> Closing`
linearization, the transaction consumes that exact facet and records a
generation-bound consumption proof; neither the snapshot nor its digest can
stand in for the capability. `Add` borrows `MapWithin` only while the validator
checks and mints its internal prepared admission intent, then releases the
borrow before `mapping_prepare` returns. Commit revalidates its capability
generation and object envelope; the prepared intent cannot mint broader
authority.

Class `L` cannot truthfully seal that digest during preparation because its
only observer snapshot is still `DeferredUntilAcceptance`. Preparation instead
commits to the normalized pre-snapshot domain, provisional encoder payload, and
bounded slots/capacity. Inside non-dispatchable `Accepting`, after `Live` →
`Closing` and the fenced observer scan, the validator replaces the deferred
field with `Frozen`, recomputes the complete final request and requirements
digests, and asks the encoder to seal the final `PublicationBinding`. No
descriptor store or `AcceptedReady` publication may precede that conversion.

The validator invokes the sealed `CompletionRequirements` constructor; callers
cannot choose its per-target class, proof flags, result variants, or table
obligations. The constructor derives them from the normalized semantic delta,
checks the effect-specific refinements, and binds its refinement digest into
the sealed request digest or class-`L` provisional commitment as appropriate;
the latter is rebound into the final digest after snapshot freeze. Any
contradictory or unrepresentable combination is a pre-effect rejection.

Preparation grants no future authority. At acceptance, while holding the
address-space mutation gate or equivalent range intents and the reserved
canonical-physical-extent/backing-lineage entries in a documented global order,
recheck every value that can change: object state and incarnation,
capability generations, the effect-indexed address-space verb and either the
complete `MapWithin` range/frame/rights/output-template envelope or the exact
`Close` authority, attenuation ceilings, each reference/template's nominal
lineage and registered gate, `ReferenceAdmissionAnchor == Open`, unchanged
admission epoch, each template's authorized mapping
range, frame identity/incarnation and authorized extent/offset, frame epochs,
mapping incarnations, overlapping ranges, frame
aliases, code/DMA state, profile identity, quota reservation, and expected
mutation sequence. The alias reservations are committed atomically into the
global ledger or returned before rejection; two address spaces cannot both
validate then publish conflicting W^X or memory-type aliases.

If any fact changed, acceptance returns `Rejected(StalePreparation,
returned_resources)` without a page-table effect. Otherwise it moves all
borrows, pins, capacity, each effect-keyed one-shot
`AdmittedOutputRefGrant`, and the exact encoded plan into a
`TranslationOperation`. This move is the last point at which a mapping error
may be returned. Later architecture or target failure becomes `Incomplete` or
`Quarantined`. If the architecture-fault component completes an actual
containing-machine halt, control takes the separate nonreturning
`machine_halt(ArchitectureFaultRecord) -> !` path and no later mapping terminal
is constructed. None is a rollback-shaped `MappingError`.

Minting later revalidates the operation-owned admitted lineage, gate, and epoch
under the still-held lifecycle/writer token, and the returned `MappingRef` must
carry those exact fields. Its terminal identity check includes them. The mint
atomically transfers the already-registered template pin/obligation to the new
reference rather than registering a second lineage. Reference mint and terminal
publication are ordered before token release, so close either observes the
registered lineage or wins afterward and denies the mint.

## Error algebra

Errors should be machine-readable and avoid leaking mappings outside the
caller's inspection authority:

| Family | Examples | Information returned |
| --- | --- | --- |
| Authority | `NoSpaceRight`, `NoFrameRight`, `RightsExceedCeiling`, `StaleCapability` | Generic denial unless caller may inspect object identity |
| Range | `Overflow`, `NonCanonical`, `ReservedRange`, `Misaligned` | Rejected field and public profile constraint |
| Conflict | `Overlap`, `StaleMapping`, `WxAlias`, `MemoryTypeAlias` | Conflict class; object identity only with inspection right |
| Backend | `UnsupportedPageSize`, `EmptyEffectiveLeaf`, `UnrepresentableAttribute`, `ProfileErratum` | Stable feature/profile reason |
| Capacity | `QuotaExceeded`, `TableReserveUnavailable`, `CompletionReserveUnavailable` | Charged class and retryability |
| Lifecycle | `SpaceClosing`, `FrameRetiring`, `CodeTransitionActive`, `DmaTransitionActive` | Current public state and optional completion handle |

No `UnknownFlagIgnored` success exists. Unknown enum values, reserved bits, or
future semantics are rejected until the profile defines them.

## Concurrency and denial-of-service bounds

Expensive global scans must not run while holding a page-table writer lock.
Maintain bounded ledger indices by virtual range, canonical physical extent,
and backing lineage so partial-overlap alias queries have charged complexity.
Preparation can run optimistically over versioned snapshots; acceptance
performs the short authoritative check.

Set explicit limits on batch entries, page-table levels traversed, aliases per
frame, huge-page splits, target CPUs, diagnostic detail, and retries. A caller
that repeatedly submits stale plans consumes its own CPU budget. Conflicting
writers receive a typed stale/conflict result; they do not spin unboundedly in
the kernel.

## Cross-ISA validation

| Concern | x86-64 | AArch64 | RISC-V supervisor |
| --- | --- | --- | --- |
| Address legality | implemented linear width and canonical form | configured translation size and tagged-address policy | selected `satp` mode and canonical virtual-address rule |
| Leaf sizes | 4 KiB and supported large-page levels | translation-granule-specific block/page levels | Sv mode leaf levels and supported page sizes |
| Rights | U/S, R/W, XD and optional protection features | AP, UXN/PXN, privilege regime | R/W/X/U with illegal encodings rejected |
| Memory type | PAT/MTRR interaction under pinned profile | MAIR index, shareability, device/normal rules | PMA plus PBMT when Svpbmt is selected; PMP is validated separately as a physical-access and page-walk constraint |
| Mutation constraints | paging-structure cache and invalidation rules | break-before-make and TLBI/barrier rules where applicable | PTE update plus `SFENCE.VMA` and extension-specific rules |

The portable request describes a semantic need. The backend may reject a
profile it cannot represent, but must not expose raw bits or silently select a
weaker access or memory type.

## Security and failure cases

### Revocation during preparation

Capability and frame-authority epochs are snapshots, not promises. Revocation
between preparation and acceptance makes the plan stale. Revocation after
acceptance becomes an ordered participant in the accepted operation and
cannot free its objects until that operation is terminal.

### Huge-page partial change

A one-page reduction inside a huge leaf requires an explicitly reserved split
plan. If the table pages or completion work cannot be reserved, reject before
breaking the huge mapping. Never broaden the requested range merely to avoid a
split.

### Information disclosure through errors

An unauthorized caller should not learn whether a secret mapping occupies a
range. Error redaction is decided by `InspectMappings`, not by which internal
check ran first. Diagnostics retain the full reason in a protected record.

### Speculative and alias bypass

Range checks and PTE rights establish architectural conditions. Backend code
must additionally apply required speculation barriers between validation and
use, while the no-ambient-user-frame-alias rule prevents a privileged synonym
from bypassing user/supervisor access controls. This still does not claim
complete microarchitectural noninterference.

## Verification strategy

### Reference function

Write an executable pure validator over finite maps and a small capability
lattice. Prove or exhaustively check:

- success implies every effective right is within all authority ceilings;
- success implies effective rights equal the explicitly requested rights and
  are nonempty;
- success preserves virtual nonoverlap and physical-extent W^X/memory-type
  invariants over canonical physical extents, including device-writable
  aliases;
- any change to a bound incarnation, generation, epoch, profile, or alias
  makes acceptance fail unchanged;
- the operation class is at least as strong as every changed semantic
  dimension requires; and
- every accepted plan owns enough resources to reach completion or a fully
  recorded quarantine.

Differentially test the production validator against the reference function.

### Property and adversarial tests

- Generate bases and lengths around zero, maximum integers, canonical gaps,
  object boundaries, half-open ranges ending exactly at a boundary, and every
  supported alignment.
- Fuzz unknown rights, memory types, page sizes, reserved attributes, and
  serialized capability values.
- Fuzz requested rights above and below every ceiling and require explicit
  `RightsExceedCeiling` or `EmptyEffectiveLeaf`, never implicit attenuation.
- Race frame revocation, mapping replacement, domain close, code publication,
  DMA mapping, and address-space recreation between prepare and accept.
- Build aliases through every available API and verify the central frame index
  catches partial physical overlap, CPU/device W^X, memory-type, and
  privileged-direct-map conflicts even across distinct frame-object IDs.
- Force every allocation/reservation failure and verify no architectural or
  ledger state changed.
- Decode each accepted backend plan and compare its semantic rights to the
  normalized request.

### Measurements

Measure validation latency by batch size, alias count, page-size mix, conflict
rate, and CPU count; acceptance critical-section time; reserved bytes per
operation; false conflicts under optimistic snapshots; and denial-of-service
behavior under malicious stale-plan submission. Tail latency matters more than
one uncontended mean.

## Staged implementation

1. Implement pure checked-range and authority-lattice functions with a model
   backend and one page size.
2. Add the mapping and frame indices, W^X and memory-type alias checks, typed
   error algebra, and exhaustive property tests.
3. Add resource estimation/reservation and prepare/accept revalidation with
   fault injection at every reservation.
4. Add one real ISA representability adapter and decode-based differential
   tests, then port the same semantic suite to a second ISA.
5. Add mixed page sizes, split/join, batch validation, code/DMA interactions,
   and measured optimistic concurrency only after the baseline invariants hold.

## Alternatives and trade-offs

### Validate only in the encoder

This mixes authority and policy with raw bit construction, makes cross-ISA
comparison difficult, and risks architecture-specific privilege broadening.
The encoder should report representability, not decide authorization.

### Validate once, then queue indefinitely

Long-lived plans become authority tokens even after revocation or mapping
change. Revalidation at acceptance keeps preparation speculative and bounded.

### Let callers supply PTE flag words

Unknown, reserved, global, supervisor, memory-type, and hardware-owned bits can
escape semantic review. Only normalized enums cross the portable boundary.

### Permit W+X for trusted services

“Trusted” is not a stable property after memory corruption. The baseline uses
the private staged code-publication transition; a future exception needs a
separate profile and security claim.

## Unresolved questions

- Which rights lattice best expresses read-only, write-only device, execute-
  only, tagged, encrypted, and capability-memory profiles without false
  portability?
- Should virtual-range envelopes be capabilities in their own right or
  immutable attenuation fields on an address-space mapping right?
- How large may a frame's alias set become, and which party pays for index
  storage and lookup work?
- What scalable reservation/index implementation can preserve the mandatory
  canonical-physical-extent alias serialization across CPU, code, and DMA
  admission without one global bottleneck?
- Which topology changes can be prepared entirely privately on each initial
  backend?
- What error details are safe for a caller without mapping-inspection rights?

## Connections

- [Parent translation component](../address-translation-and-protection-transitions.md)
- [Address-space object](address-space-object.md)
- [Page-table and protection encoder](page-table-and-protection-encoder.md)
- [Mapping transaction](mapping-transaction.md)
- [Reclamation gate](reclamation-gate.md)
- [Safe user-access helpers](safe-user-access-helpers.md)
- [Ordering, coherence, and code publication](../ordering-coherence-and-code-publication.md)
- [Protected I/O and DMA ownership](../protected-io-and-dma-ownership.md)

## Sources

- [Protection of information in computer systems](../../../30-sources/saltzer-schroeder-1975-protection-information.md)
- [Least-privilege memory protection](../../../30-sources/achermann-et-al-2019-least-privilege-memory-protection.md)
- [seL4 reference manual](../../../30-sources/sel4-foundation-2026-reference-manual.md)
- [Asterinas page-table verification report](../../../30-sources/asterinas-community-2025-practical-page-table-verification.md)
- [Secure memory management](../../../30-sources/achermann-et-al-2020-secure-memory-management.md)
- [SecVisor retrospective](../../../30-sources/franklin-et-al-2008-secvisor-retrospective.md)
- [seL4 RISC-V page-map defect](../../../30-sources/sel4-foundation-2020-risc-v-page-map-defect.md)
- [ret2dir](../../../30-sources/kemerlis-et-al-2014-ret2dir.md)
- [Nested Kernel](../../../30-sources/dautenhahn-et-al-2015-nested-kernel.md)
- [CertiKOS](../../../30-sources/gu-et-al-2016-certikos.md)
- [Serval](../../../30-sources/nelson-et-al-2019-serval.md)
- [Intel system-programming documentation](../../../30-sources/intel-2026-system-programming-documentation.md)
- [Arm A-profile system architecture documentation](../../../30-sources/arm-2026-a-profile-system-architecture-documentation.md)
- [RISC-V privileged architecture](../../../30-sources/risc-v-international-2026-privileged-architecture.md)
