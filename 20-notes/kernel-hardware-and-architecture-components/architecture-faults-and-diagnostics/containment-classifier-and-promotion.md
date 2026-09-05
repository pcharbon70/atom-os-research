---
title: "Architecture-fault containment classifier and terminal promotion"
kind: note
created: "2026-09-05"
maturity: developing
tags:
  - architecture-support
  - fault-containment
  - hardware-errors
  - ras
  - recovery
aliases:
  - "Containment classifier and promotion"
---

# Architecture-fault containment classifier and terminal promotion

The capture-time classifier should be a generated total decision function over
sealed raw/profile facts, separately published acknowledgement state, an exact
entry-safe execution/object snapshot, and a pinned recovery profile. It is not
the rich policy-plane decoder. Its output is one of four noninterchangeable
products:

1. `AsynchronousNonDisruptive` for a report proven unrelated to the interrupted
   return state;
2. a sealed `LocalResumePostcondition` for a completed bounded CPU-local repair;
3. a `ContainmentRequirement` that parks/diverts execution while other owners
   coordinate a split-phase quarantine; or
4. `TerminalDisposition`, which promotes the already sealed record and forbids
   ordinary return.

Hardware labels such as corrected, recoverable, restartable, action-required,
or containable are premises. None is an output capability. Before the final
decision seals, any missing fact, evidence loss, rule/profile mismatch, or
failed admission can only widen the planned scope or select terminal. A later
containment failure never rewrites that decision; it appends a fallback outcome
and keeps/widens the enforced scope toward terminal.

This is an unverified Atom proposal. The initial implementation should contain
very few nonterminal rules.

## Question, scope, and operational standard

The question is:

> Given imperfect architecture evidence, what is the strongest recovery claim
> the kernel can justify without confusing a producer's label, attempted
> action, or timeout with completed containment?

The service owns:

- a total, bounded, profile-pinned rule table and its validation proof;
- independent fault axes and an uncertainty-monotone disposition lattice;
- local repair execution and construction of unforgeable local postconditions;
- generation-bound containment requirements and the initial park/divert action;
- system first-fatal promotion from sealed staging; and
- immutable classification and promotion decision records.

It does not perform VM teardown, TLB shootdown, DMA/device quiescence, CPU
offline, domain restart, crash persistence, or OTP supervision. Those owners
return their own completion evidence through the escalation/recovery plane.

A classifier passes only if:

1. its rule set is total over all valid, invalid, unknown, conflicting, and
   incomplete raw/profile/acknowledgement inputs admitted by capture;
2. rule overlap is rejected or accompanied by a checked dominance relation;
3. the terminal/unknown rule is the final default;
4. weakening evidence cannot produce a narrower scope or more permissive
   disposition;
5. synchronous return consumes a source/profile-specific local postcondition
   constructed only after all required local actions complete;
6. remote or policy work produces a requirement, never a counterfeit local
   token;
7. the requirement names every known CPU, mapping, frame, domain, requester,
   device, cache/persistence, and external-effect obligation;
8. deadline expiry changes suspicion/progress metadata but never creates
   containment completion;
9. terminal promotion preserves the first successfully promoted record and
   never overwrites it; and
10. an action capability is supplied independently of evidence identifiers.

## Evidence and limits

| Evidence | Supported conclusion | Limit |
| --- | --- | --- |
| [Intel system-programming documentation](../../../30-sources/intel-2026-system-programming-documentation.md) | Processor-context corruption, restart-IP validity, precision, overflow, address/misc validity, and machine-check class must be evaluated separately | Recovery matrices are processor/profile specific |
| [Arm RAS specification](../../../30-sources/arm-2019-ras-specification.md) | Corrected, deferred, poison, uncorrected type, overflow, and validity remain independent; “recoverable” still needs software action | Does not define a selected SoC's complete topology or errata |
| [RISC-V RERI](../../../30-sources/risc-v-international-2024-ras-error-record-interface.md) | `containable` means may be containable and explicitly leaves recovery determination to the handler | RERI is optional and may provide sparse information |
| [Linux hwpoison](../../../30-sources/kleen-2009-hwpoison.md) | Page poisoning, mapping discovery, process notification/termination, and future exclusion are split-phase VM work; not all page types can be recovered | Linux policy and signals are not an Atom proof |
| [Itanium machine-check recovery](../../../30-sources/luck-2003-machine-check-recovery-itanium.md) | Narrow continuation requires object-specific reconstruction and can require sacrificing a process; kernel/shared state forces wider failure | Historical architecture and implementation |
| [Recovery domains](../../../30-sources/lenharth-et-al-2009-recovery-domains.md) | Request-local rollback is possible only when shared state and committed output remain inside the recovery boundary | Evaluated injected software faults, not arbitrary hardware corruption |
| [Recovering device drivers](../../../30-sources/swift-et-al-2004-recovering-device-drivers.md) | Device recovery has class-specific reconstruction and indeterminate external-effect cases | Does not cover malicious hardware or every device |
| [seL4 reference manual](../../../30-sources/sel4-foundation-2026-reference-manual.md) | Structured faults may suspend a thread and delegate policy while one-shot reply authority controls exact resumption | Thread fault IPC is not machine-failure containment |
| [Unreliable failure detectors](../../../30-sources/chandra-toueg-1996-failure-detectors.md) and [gray failure](../../../30-sources/huang-et-al-2017-gray-failure.md) | Missing progress and differential observability produce suspicion, not proof of failure or isolation | Distributed-system models are analogies for local CPU/device liveness |
| [Production memory errors](../../../30-sources/meza-et-al-2015-revisiting-memory-errors.md) and [realistic error evaluation](../../../30-sources/li-et-al-2010-realistic-memory-error-evaluation.md) | Persistent page retirement can help, while realistic errors include correlated and nontransient patterns | Fleet statistics and injection do not prove an individual recovery |

The sources justify conservative, scope-aware, split-phase recovery. The token
types, information lattice, rule compiler, and terminal-promotion protocol are
Atom synthesis.

## Classification input

```text
EntrySnapshot {
    capture: FaultCaptureIncarnation,
    schema_and_layout_id,
    entry_context_class,
    return_frame_integrity_fields,
    cpu_identity_and_incarnation,
    thread_and_domain_incarnation,
    address_space_incarnation,
    mapping_and_frame_incarnations,
    interrupt_binding_generation,
    dma_and_device_epochs,
    request_or_operation_id,
    privilege_and_mutation_phase,
    locks_or_transactions_known_held,
    external_effect_status,
    captured_field_bitmap,
    loss_and_unknown_bitmap
}

EntrySnapshotPublication {
    lifecycle_word: Atomic<(
        Empty | Writing | Sealed | Reclaimable | Clearing,
        snapshot_slot_generation,
        compact_snapshot_operation_descriptor_index_and_generation_or_none,
        compact_snapshot_owner_tag_or_none,
        cleanup_frontier:
            None | DependenciesClosing | DependenciesDrained |
            BorrowClosing | BorrowDrained | ReclaimCommitted |
            ClearAuthorized | BodyVerifiedEmpty
    )>,
    snapshot_semantic_id: Hash(canonical_encoding({
        capture,
        schema_and_layout_id,
        canonical_entry_snapshot_digest
    })),
    snapshot_publication_id: Hash(canonical_encoding({
        intended_state: Sealed,
        snapshot_storage_owner_and_generation,
        entry_snapshot_owner_descriptor_digest,
        snapshot_semantic_id,
        payload_length_and_bounds,
        canonical_entry_snapshot_digest
    })),
    snapshot_storage_owner_and_generation,
    entry_snapshot_owner_descriptor_digest,
    capture: FaultCaptureIncarnation,
    payload_length_and_bounds,
    canonical_entry_snapshot_digest,
    snapshot: EntrySnapshot,
    borrow_word: Atomic<(
        Open | Revoking | Drained,
        snapshot_borrow_generation,
        live_classifier_graph_requirement_and_recovery_reader_count:
            BoundedBorrowCount<MAX_ENTRY_SNAPSHOT_BORROWS>
    )>,
    evidence_dependency_set_ref_and_generation
}

EntrySnapshotOwnerDescriptor {
    descriptor_index_and_generation,
    snapshot_slot_and_generation,
    capture: FaultCaptureIncarnation,
    cpu_identity_and_incarnation,
    fixed_extent_layout_and_bounds,
    protected_component_2_writer_authority_and_generation,
    canonical_descriptor_digest
}

EntrySnapshotCleanupDescriptor {
    descriptor_index_and_generation,
    snapshot_slot_old_and_next_generation,
    cleanup_variant:
      WritingCrash {
          original_owner_descriptor_ref_generation_and_digest,
          complete_entry_snapshot_attempt_receipt_ref_and_id,
          matching_current_crash_reclaim_ref_and_id
      }
    | SealedSameBoot {
          internal_rehome_receipt_and_digest,
          protected_component_2_release_authority_and_generation
      }
    | SealedAfterCrash {
          complete_entry_snapshot_attempt_receipt_ref_and_id,
          all_accepted_copy_custody_receipt_manifest,
          matching_current_crash_reclaim_ref_and_id
      },
    exact_dependency_borrow_close_drain_and_clear_rekey_plan,
    protected_cleanup_owner_identity_and_generation,
    canonical_descriptor_digest
}

EntrySnapshotBorrowToken {
    snapshot_publication_ref_id_and_slot_generation,
    snapshot_borrow_generation,
    holder_identity_and_generation,
    use_class: Classifier | GraphBuilder | RequirementBuilder | RecoveryCopier,
    token_id_and_kernel_authority
}

EntrySnapshotInternalRehomeReceipt {
    source_snapshot_publication_ref_id_slot_generation_and_semantic_id,
    exact_source_body_digest_and_capture,
    destination_graph_requirement_or_terminal_publication_ref_id_and_generation,
    exact_destination_snapshot_copy_and_semantic_digest,
    complete_dependency_set_closing_and_drained_result,
    no_live_pointer_to_source_snapshot,
    protected_component_2_issuer_authority_and_generation,
    canonical_receipt_digest
}

EntrySnapshotReclaimPredicate =
    WritingCrashRecovery {
        snapshot_slot_generation_and_compact_owner_tag,
        capture_and_observed_lifecycle_state: Writing,
        exact_old_writer_fence_evidence,
        no_accepted_dependency_or_snapshot_semantic_use,
        complete_attempt_receipt_ref_and_id:
            CustodyReceiptPublication::IncompleteCrashAttempt(
                EntrySnapshotAttempt),
        matching_current_crash_reclaim_ref_and_id,
        exact_borrow_epoch_observed_zero_or_drained,
        prevalidated_cleanup_descriptor_and_owner,
        protected_crash_cleanup_authority_and_generation
    }
  | SealedSameBootRehome {
        source_snapshot_publication_ref_id_slot_generation_and_owner_tag,
        capture_semantic_id_and_exact_body_digest,
        internal_rehome_receipt: EntrySnapshotInternalRehomeReceipt,
        exact_borrow_epoch_drained,
        prevalidated_cleanup_descriptor_and_owner,
        protected_component_2_release_authority_and_generation
    }
  | SealedCrashRecovery {
        source_snapshot_publication_ref_id_slot_generation_and_owner_tag,
        capture_semantic_id_and_exact_body_digest,
        exact_old_writer_fence_evidence,
        complete_attempt_receipt_ref_and_id:
            CustodyReceiptPublication::IncompleteCrashAttempt(
                EntrySnapshotAttempt),
        complete_dependency_set_drained,
        all_accepted_semantic_copies_and_custody_receipts,
        no_live_pointer_to_source_snapshot,
        matching_current_crash_reclaim_ref_and_id,
        exact_borrow_epoch_drained,
        prevalidated_cleanup_descriptor_and_owner,
        protected_crash_cleanup_authority_and_generation
    }

EntrySnapshotCleanupResumePredicate {
    original_snapshot_slot_generation_cleanup_descriptor_owner_and_variant,
    observed_lifecycle_state:
        Reclaimable | Clearing | EmptyNextGeneration,
    original_variant_authority:
      WritingCrash(receipt_and_current_or_consumed_reclaim)
    | SealedSameBoot(internal_rehome_receipt_and_release_authority)
    | SealedAfterCrash(receipt_copy_manifest_and_current_or_consumed_reclaim),
    exact_dependency_borrow_old_and_next_generations_and_atomic_cleanup_frontier,
    protected_cleanup_resume_authority_and_generation
}

ClassificationInput {
    capture: FaultCaptureIncarnation,
    sealed_raw_evidence_ref_and_digest,
    sealed_ordered_source_results: BoundedArray<{
        source_id,
        source_owner_and_route_generations,
        program_and_profile_hashes,
        source_attempt_set_ref_and_digest,
        validity_capture_completion_overwrite_and_loss,
        acknowledgement_state_result_and_digest
    }, MAX_SOURCES>,
    capture_profile_id_and_hash,
    entry_snapshot_publication_ref_and_id,
    classifier_profile_id,
    classifier_rule_table_hash
}
```

Component 2 and the capture allocator bind the capture incarnation before raw
reads. Component 2 validates an immutable `EntrySnapshotOwnerDescriptor` and
claims an exact preallocated snapshot storage generation while atomically
installing its compact descriptor tag,
privately builds the fixed-capacity entry snapshot under `Writing`, computes a
canonical digest over its incarnation, layout, bounds, values, validity, and
loss fields, derives the storage-independent `snapshot_semantic_id`, then
release-publishes `Sealed` with a storage-generation-bound publication ID. The
classifier acquire-loads and accepts only that exact publication state,
generation, capture, semantic ID, bounds, and digest; a torn or reused frame
forces terminal classification. Custody copies preserve the semantic ID/body
digest but receive new physical publication IDs. Every classifier, graph,
requirement, or recovery reader first installs a bounded exact-generation
borrow, rechecks `Sealed`, the publication identity, owner/slot generation, and
borrow `Open`, and then copies; no accepted graph retains a raw pointer. Each
accepted destination is registered in the snapshot's bounded evidence
dependency set before its acceptance linearization.

A source snapshot may leave `Writing` or `Sealed` only through an exact
`EntrySnapshotReclaimPredicate`. For `Writing`, a fenced owner must prove no
accepted dependency and preserve the entire fixed snapshot extent—including
partial and apparently untouched bytes—in a sealed
`IncompleteCrashAttempt(EntrySnapshotAttempt)` receipt. For `Sealed`, recovery
must additionally close and drain the complete dependency set and prove every
accepted semantic copy independently owned; one copied decision or core does
not suffice. An ordinary same-boot release uses a protected internal snapshot-
rehome receipt and component-2 release authority after the accepted destination
owns the complete semantic copy. A fenced/next-boot release instead uses the
complete fixed-extent crash receipt and a separate generation-current
`CrashReclaim`; every incomplete `Writing` arm requires this latter form.
These are closed correlated variants: a `WritingCrashRecovery` can never pair
with same-boot authority, and `SealedSameBootRehome` can never substitute an
undefined external receipt or omit its exact internal copy/dependency proof.
Each arm first prevalidates its corresponding immutable
`EntrySnapshotCleanupDescriptor`. Only then may the owner atomically replace
the old owner/build tags with that cleanup descriptor and protected cleanup
owner while CASing the exact source state/generation to `Reclaimable` at
frontier `ReclaimCommitted`. The closed variant permanently distinguishes
`WritingCrash`, `SealedSameBoot`, and `SealedAfterCrash` and retains the exact
receipt/reclaim or internal-rehome authority through exposure. The owner then
closes borrow admission, drains `(Revoking, b, 0) → (Drained, b, 0)`, and enters
`Clearing`, advancing the atomic frontier before each mutation. Verified clear covers the full payload, owner/control metadata,
dependency set, and borrow metadata; it initializes the next zero-borrow epoch
and empty dependency set, advances checked-nonwrapping generations, and
publishes descriptor-/owner-free `(Empty, next_generation, None, None, None)`
last. A cut resumes only through `EntrySnapshotCleanupResumePredicate`, which
recovers the exact variant authority and next step from the atomic cleanup tags
rather than from bytes being erased; missing custody, an ambiguous dependency/borrow, or exhaustion retires
the slot. The complete snapshot lifecycle and borrow tuples must each fit a
target-supported native atomic operation; the per-CPU pool uses fixed disjoint
shards if the configured field widths do not fit. The snapshot
contains only entry-safe, previously maintained identifiers and epochs. The
classifier never follows arbitrary object pointers in hard entry. Missing or
stale snapshot fields are explicit unknowns and cannot satisfy a positive rule
premise. Rich CPER/vendor parsing and cross-record correlation are
absent from this path; the later `FaultDecoder` may inform future policy but
cannot alter this immutable decision.

Every generated source premise names the exact source ID, program/profile
hashes, attempt-set digest, and acknowledgement result it consumes. An
acknowledgement for one MCA bank, RAS node, RERI record, route generation, or
other source cannot satisfy another source's return rule. Aggregate
completion/loss summaries are derived diagnostics and never replace this
per-source binding.

`external_effect_status` is `NoExternalEffectByConstruction`,
`NotCommittedByFencedTransaction`, `NoneObserved`, `Committed`, `Indeterminate`,
or `Unknown`. Narrow request rollback may use only the first two and only under
the exact pinned construction/transaction proof. Absence of an observed effect
is not proof of absence. The remaining states are non-permissive unless a
separate idempotence/deduplication contract covers the exact effect.

## Independent axes and information ordering

The rule language consumes separate facts:

- source/detector/consumer/reporter identity and independently recorded
  producer trust/provenance;
- synchronous, asynchronous, polled, NMI-like, or firmware delivery;
- exact instruction, restartable instruction, bounded window, component, or
  unknown precision;
- hardware correction status, deferred status, poison presence, poison
  propagation, and poison consumption as separate axes;
- processor context intact/suspect/lost, kernel shared-state phase, and
  external-effect state;
- affected thread, request, address space, domain, CPU, frame/extent,
  requester/device, interconnect, or machine scope, plus separate epistemic
  scope uncertainty;
- source-field validity, capture availability, structural parse status,
  cross-source agreement/conflict, overflow/overwrite/missing evidence, and
  producer trust as separate axes; and
- persistence and repeated-event history.

Define the containment scope order approximately as:

```text
Thread/Request
    <= AddressSpace/Domain
    <= CPU or MemoryExtent or Device/RequesterSet
    <= CoupledSubsystem
    <= Machine
```

Some scopes are incomparable: a CPU and a DMA requester may both be required.
The result is therefore a set of obligations, not a single enum. Evidence
weakening adds obligations or replaces a narrow member with a conservative
superset; it never removes an obligation. `scope = Unknown` is epistemic state,
not a location above `Machine`; its enforced fallback is machine scope unless a
pinned rule independently proves a smaller safe bound.

The disposition relation is a partial order:

```text
AsynchronousNonDisruptive   LocalResumePostcondition
              \             /
          ParkForCoordinatedContainment
                       |
                   Terminal
```

The two return-authorizing products are incomparable proofs: one proves the
report did not disrupt return state, while the other proves a bounded local
repair. Both require fewer interventions than park/containment, which in turn
is below terminal. A newly unknown prerequisite can only remove a return proof
or widen the enforced action; it cannot transform one return proof into the
other.

## Generated rule form

```text
ClassifierRule {
    rule_id,
    profile_id,
    required_facts,
    forbidden_facts,
    exact_entry_classes,
    execution_phase_predicate,
    local_action_program: Option<BoundedLocalAction>,
    output_template,
    dominance_rank,
    fallback_rule_id,
    test_vector_set_hash
}
```

Build-time tooling expands each field's valid/invalid/unknown/conflicting
states, proves that every admitted tuple matches at least one rule, reports
overlap, and accepts overlap only when the stronger rule dominates on every
output obligation. Runtime uses a fixed decision DAG or verified first-match
table with a constant maximum step count. The rule hash is retained in the
classification record.

The default rule is not “no match.” It records epistemic scope `Unknown`,
enforces machine scope, emits terminal disposition, and preserves the exact
missing/contradictory premises.

## Output products

The generated table first produces a `ClassificationPlan`. A bounded local
admission phase then establishes any prerequisite destination and initial fence
before the final product seals. A containment plan must reserve one dedicated
requirement slot and then establish and verify its profile-defined minimum
park/access fence before spending the evidence-copy interval. Only after that
fence prevents every possible accessor from consuming or propagating the fault
does admission start the reserved slot's bounded evidence copy. The slot stays
`Writing` while the candidate decision body and semantic record-core seed are
assembled; admission adds those non-publication bodies/digests to the same
envelope, computes the whole-envelope
digest, and publishes the slot `Sealed` once. If
reservation, initial fencing, or evidence copy fails, the one decision that is
ultimately sealed is terminal; in particular, a fencing failure goes terminal
immediately. There is no previously sealed decision to “widen.” After the
candidate decision and core seed are assembled, an authorized requirement custodian must
validate and accept that exact sealed publication as `Held` before staging can
be released. A nested failure before that ownership transition leaves staging
held and takes the recursive terminal path.
An asynchronous-nondisruptive report may use the separately sealed compact
loss-transfer path when the full ring cannot take its raw bytes. Local repair
is stricter: its one-shot token is not consumable without a complete restricted
ring custody root, so ring admission failure revokes the unused token and
selects the terminal product. No safety rule depends on a deferred decoder
queue reservation.

The effective product is sealed exactly once as:

```text
CaptureDispositionDecisionBody {
    decision_id,
    capture,
    input_digest,
    rule_id_and_hash,
    planned_product_digest,
    admission_outcome,
    effective_product:
      AsynchronousNonDisruptiveProduct {
          body: AsynchronousNonDisruptive
      }
    | LocalResumeProduct {
          body: LocalResumePostcondition,
          accepted_token_identity_owner_generation_and_publication_id,
          accepted_token_body_digest
      }
    | ContainmentProduct {
          requirement_id,
          requirement_body_and_canonical_digest
      }
    | TerminalProduct {
          body: TerminalDispositionProduct
      },
    effective_product_digest
}

CaptureDispositionDecisionPublication {
    state: Empty | Writing | Sealed,
    decision_publication_id: Hash(canonical_encoding({
        intended_state: Sealed,
        decision_owner_and_generation,
        decision_id,
        acceptance_root,
        canonical_decision_digest
    })),
    decision_owner_and_generation,
    decision_id,
    acceptance_root:
        DirectDecision
      | HeldRequirementWitness(requirement_held_witness),
    canonical_decision_digest,
    body: CaptureDispositionDecisionBody
}

ContinuationCustodyHoldPublication {
    hold_word: Atomic<(
        Empty | PlanWriting | Prepared | Acquiring | Complete |
        Transferring | Transferred | Releasing | Released | Clearing,
        hold_slot_generation,
        compact_plan_descriptor_index_and_generation,
        compact_owner_tag,
        operation_frontier:
            None | AcquireGraph | AcquireEvidenceRoot | AcquireRequirement |
            AcquisitionComplete | TransferPreparingDestination |
            TransferDestinationComplete | TransferCommitted |
            TransferAbortSelected | TransferAbortComplete |
            ReleaseGraph | ReleaseEvidenceRoot | ReleaseRequirement |
            ReleaseComplete,
        acquired_token_bitmap
    )>,
    hold_id_and_protected_kernel_authority,
    capture,
    disposition: AsynchronousReturn | LocalResume | ContainmentPark,
    component_2_entry_state_view_generation,
    graph_publication_ref_id_and_generation,
    dependency_set_entry_identity_generation_and_preaccept_state,
    exact_readable_evidence_root_identity_generation_and_state,
    token_plan: {
        graph_borrow_generation_preallocated_token_id_and_holder_bit,
        evidence_root_borrow_generation_preallocated_token_id_and_holder_bit,
        containment_requirement_borrow_generation_preallocated_token_id_and_holder_bit_or_none
    },
    park_transfer_plan_or_none: {
        park_handoff_slot_and_generation,
        destination_hold_slot_and_generation,
        compact_park_abort_owner_tag_and_protected_authority_generation
    },
    acquired_token_manifest,
    canonical_hold_plan_and_manifest_digest
}

ContinuationCustodyPlanDescriptor {
    descriptor_index_and_generation,
    intended_hold_slot_and_generation,
    capture_and_disposition,
    component_2_entry_state_view_generation,
    graph_dependency_and_exact_evidence_root_binding,
    complete_token_to_source_holder_bit_plan,
    park_transfer_plan_or_none,
    canonical_descriptor_digest,
    protected_plan_authority_and_generation
}

ContinuationHoldCancellationPredicate {
    hold_ref_generation_and_compact_plan_descriptor,
    observed_hold_state_frontier_and_acquired_bitmap,
    publisher_fence_evidence,
    exact_source_holder_words_and_planned_bit_observations,
    graph_dependency_reservation_and_accepted_bit_observations,
    graph_entry_state_and_generation,
    cancellation_authority_and_generation
}

ParkedSchedulerResumeRecordPublication {
    lifecycle_word: Atomic<(
        Empty | Writing | Prepared | Available | Claimed | Consumed | Clearing,
        resume_record_generation,
        compact_resume_build_descriptor_index_and_generation_or_none,
        compact_scheduler_builder_owner_tag_or_none
    )>,
    publication_id: Hash(canonical_encoding({
        intended_initial_state: Prepared,
        resume_record_generation,
        resume_build_descriptor_digest,
        compact_scheduler_builder_owner_tag,
        parked_context_identity_and_generation,
        coordinated_completion_publication_ref_id_and_digest,
        sanitized_resume_frame_and_context_digest,
        scheduler_owner_and_generation,
        canonical_body_digest
    })),
    parked_context_identity_and_generation,
    source_destination_hold_identity_and_generation,
    coordinated_completion_publication_ref_id_and_digest,
    sanitized_resume_frame_and_context_copy,
    scheduler_owner_and_generation,
    resume_build_descriptor_digest,
    canonical_body_digest
}

ParkedSchedulerResumeBuildDescriptor {
    descriptor_index_and_generation,
    resume_record_slot_and_generation,
    parked_context_identity_and_generation,
    source_destination_hold_identity_and_generation,
    coordinated_completion_publication_ref_id_and_digest,
    parked_release_mode_gate_generation_and_expected_state,
    sanitized_resume_frame_source_and_expected_digest,
    scheduler_builder_identity_and_generation,
    canonical_descriptor_digest
}

ParkHandoffPublication {
    lifecycle_word: Atomic<(
        Empty | Writing | Sealed | Parked | Aborting | Aborted |
        Reclaimable | Clearing,
        handoff_generation,
        compact_handoff_or_abort_owner_tag
    )>,
    publication_id: Hash(canonical_encoding({
        intended_state: Sealed,
        handoff_generation,
        capture_and_requirement_id,
        accepted_graph_dependency_and_held_witness_digest,
        parked_context_identity_and_generation,
        fence_and_custodian_identity_generation,
        source_and_destination_hold_refs_ids_generations_and_token_bitmaps,
        release_mode_plan_digest,
        canonical_body_digest
    })),
    capture_and_requirement_id,
    accepted_graph_dependency_and_held_witness_digest,
    parked_context_identity_and_generation,
    fence_and_custodian_identity_generation,
    source_and_destination_hold_refs_ids_generations_and_token_bitmaps,
    transfer_frontier_and_protected_acceptance_authority,
    release_mode_word: Atomic<(
        Undecided | ResumeRecordWriting | ResumePrepared |
        SwitchingToTerminal | SwitchingToDurable | ProofWriting |
        ProofAvailable | ProofClaimed | Released | Clearing,
        release_mode_generation,
        selected_release_variant_or_none: None | Resume | Terminal | Durable,
        compact_resume_or_proof_descriptor_tag_or_none,
        compact_release_mode_owner_tag_or_none,
        release_or_cleanup_frontier: {
            step: ModeUnselected | SidecarClaimPending | SidecarOwned |
                  ProofClaimed | HoldReleasing | HoldReleased |
                  SuccessorPublished | MembersClearing | MembersRearmed |
                  HandoffClearing | Complete,
            exposure_authorized_member_bitmap
        }
    )>,
    preallocated_resume_record_and_release_proof_slots_and_generations,
    preallocated_abort_group_cleanup_barrier_slot_and_generation,
    source_destination_handoff_pool_reservation_bits,
    release_mode_plan_digest,
    protected_abort_authority_and_generation,
    canonical_body_digest
}

ParkAbortGroupCleanupBarrierPublication {
    control_word: Atomic<(
        Empty | Claimed | MembersReleasing | MembersClearing |
        MembersRearmed | Released | Clearing,
        barrier_generation,
        compact_cleanup_descriptor_index_and_generation_or_none,
        compact_cleanup_owner_tag_or_none,
        member_frontier_and_completion_bitmap
    )>,
    exact_handoff_source_hold_destination_hold_refs_and_old_generations,
    exact_next_member_generations_and_pool_reservation_bits,
    source_obligation_rehome_receipt_and_reclaim_refs,
    canonical_cleanup_plan_digest
}

ParkAbortGroupCleanupDescriptor {
    descriptor_index_and_generation,
    barrier_slot_and_generation,
    handoff_source_hold_destination_hold_refs_and_old_generations,
    destination_variant: NeverClaimed | ClaimedAndReleased,
    source_obligation_rehome_plan_and_exact_receipt_reclaim_targets,
    exact_next_member_generations_and_pool_reservation_bits,
    protected_cleanup_authority_and_generation,
    canonical_descriptor_digest
}

ParkedContinuationReleaseProofPublication {
    lifecycle_word: Atomic<(
        Empty | Writing | Available | Claimed | Consumed | Clearing,
        release_proof_generation,
        compact_release_proof_build_descriptor_index_and_generation_or_none,
        compact_release_proof_builder_owner_tag_or_none
    )>,
    target_park_handoff_publication_ref_id_and_generation,
    target_destination_hold_ref_id_generation_and_token_bitmap,
    publication_id: Hash(canonical_encoding({
        intended_state: Available,
        release_proof_generation,
        release_proof_build_descriptor_digest,
        compact_release_proof_builder_owner_tag,
        target_park_handoff_publication_ref_id_and_generation,
        target_destination_hold_ref_id_generation_and_token_bitmap,
        canonical_body_digest,
        protected_one_shot_release_authority_and_generation
    })),
    body: ParkedContinuationReleaseProof,
    release_proof_build_descriptor_digest,
    canonical_body_digest,
    protected_one_shot_release_authority_and_generation
}

ParkedReleaseProofBuildDescriptor {
    descriptor_index_and_generation,
    release_proof_slot_and_generation,
    target_park_handoff_publication_ref_id_and_generation,
    target_destination_hold_ref_id_generation_and_token_bitmap,
    closed_release_variant_and_exact_destination_binding_digest,
    parked_release_mode_gate_generation_selected_variant_and_expected_state,
    protected_release_proof_builder_identity_and_generation,
    canonical_descriptor_digest
}

ParkSidecarWritingRecoveryPredicate {
    cancellation_case:
      InitialSchedulerResumeRecord {
          sidecar_kind: SchedulerResumeRecord,
          slot_generation_owner_and_resume_build_descriptor,
          exact_release_mode_gate:
              ResumeRecordWriting(Resume, resume_descriptor, scheduler_owner),
          companion_release_proof_slot_observed_descriptor_free_empty,
          postcancel_release_mode: Undecided
      }
    | ResumeCustodyTransferProof {
          sidecar_kind: ResumeCustodyTransferReleaseProof,
          slot_generation_owner_and_release_proof_build_descriptor,
          exact_release_mode_gate:
              ProofWriting(Resume, release_proof_descriptor, proof_owner),
          companion_resume_record_observed_exact_valid_prepared_and_matching_handoff,
          postcancel_release_mode: ResumePrepared
      },
    exact_old_builder_fence_evidence,
    target_handoff_observed_parked_and_destination_hold_complete,
    no_available_or_claimed_sidecar_publication,
    no_hold_release_frontier_or_parked_reclaim_transition,
    complete_fixed_extent_sidecar_receipt_and_current_crash_reclaim_if_next_boot,
    protected_sidecar_recovery_authority_and_generation
}

ParkHandoffAbortPredicate {
    handoff_ref_generation_observed_state_and_abort_owner:
        Writing | Sealed | Aborting,
    exact_source_hold_ref_generation_state_frontier_and_bitmap,
    destination_hold_observation:
      DestinationNeverClaimed {
          exact_descriptor_free_empty_hold_slot_and_generation,
          immutable_destination_hold_plan_from_source_hold,
          all_destination_holder_bits_absent,
          destination_hold_pool_reservation_bit_retained
      }
    | DestinationClaimed {
          hold_ref_generation_descriptor_owner_and_state:
              PlanWriting | Prepared | Acquiring | Complete |
              Releasing | Released,
          exact_acquisition_or_release_frontier_and_bitmap,
          destination_hold_pool_reservation_bit_retained
      },
    no_parked_acceptance_witness,
    protected_abort_authority_and_generation
}

ParkHandoffAbortGroupCleanupPredicate =
    InitialCleanup {
        handoff_ref_generation_abort_owner_and_observed_state: Aborted,
        source_hold_ref_generation_descriptor_owner_state_frontier_and_bitmap:
            Complete,
        destination_observation:
            NeverClaimedReservedEmpty | ClaimedReleased,
        preallocated_barrier_observed_descriptor_free_empty,
        complete_group_extent_receipt_ref_and_id,
        matching_current_crash_reclaim_ref_and_id,
        complete_independent_rehome_of_accepted_requirement_graph_and_source_obligation,
        exact_member_pool_reservation_bits_still_installed,
        protected_group_cleanup_authority_and_generation
    }
  | CleanupResume {
        original_handoff_source_destination_and_barrier_generations,
        cleanup_phase:
          MembersAdmissionBlocked {
              barrier_descriptor_owner_state_frontier_and_completion_bitmap:
                  Claimed | MembersReleasing | MembersClearing |
                  MembersRearmed,
              source_hold_observation:
                  Complete | Releasing | Released | Clearing |
                  EmptyNextGeneration,
              destination_observation:
                  NeverClaimedReservedEmpty | Released | Clearing |
                  EmptyNextGeneration,
              handoff_observation:
                  Reclaimable | Clearing | EmptyNextGeneration,
              exact_member_pool_reservation_bits_still_installed
          }
        | MembersAdmissionReleased {
              barrier_descriptor_owner_state_and_frontier:
                  Released | Clearing | EmptyNextGeneration,
              exact_atomic_member_pool_reservation_word_observed_released,
              old_member_slots_no_longer_read_or_constrained
          },
        original_group_receipt_reclaim_and_rehome_refs,
        exact_old_and_next_member_generations_and_pool_reservation_bits,
        protected_group_cleanup_authority_and_generation
    }

ParkedContinuationReleaseProof =
    ResumeCustodyTransfer {
        park_handoff_publication_ref_id_and_generation_observed_parked,
        destination_hold_ref_id_generation_and_token_bitmap,
        parked_context_identity_and_generation,
        coordinated_completion_publication_ref_id_generation_and_digest,
        completion_acceptance_witness,
        scheduler_resume_record_publication_ref_id_generation_and_digest,
        scheduler_resume_record_observed_state: Prepared,
        canonical_release_proof_digest
    }
  | TerminalCustodyTransfer {
        park_handoff_publication_ref_id_and_generation_observed_parked,
        destination_hold_ref_id_generation_and_token_bitmap,
        parked_context_identity_and_generation,
        terminal_destination:
            TerminalPromotionDestination {
                terminal_promotion_publication_ref_id_generation_and_digest,
                observed_lifecycle_state: Sealed
            }
          | RecursiveTerminalDestination {
                recursive_fault_record_publication_ref_id_generation_and_digest,
                observed_publication_state: Sealed
            },
        terminal_context_owner_and_nonreturning_disposition,
        scheduler_resume_record_disposition:
            ProvedEmpty(resume_slot_and_generation)
          | CancelPrepared {
                resume_record_publication_ref_id_generation_and_digest,
                resume_build_descriptor_and_scheduler_owner_tags
            },
        canonical_release_proof_digest
    }
  | DurableObligationTransfer {
        park_handoff_publication_ref_id_and_generation_observed_parked,
        destination_hold_ref_id_generation_and_token_bitmap,
        parked_context_identity_and_generation,
        durable_obligation_transfer_receipt_ref_id_generation_and_digest,
        exact_continuing_quarantine_and_parked_context_acceptance_scope,
        scheduler_resume_record_disposition:
            ProvedEmpty(resume_slot_and_generation)
          | CancelPrepared {
                resume_record_publication_ref_id_generation_and_digest,
                resume_build_descriptor_and_scheduler_owner_tags
            },
        canonical_release_proof_digest
    }

PreparedResumeCancellationPredicate {
    resume_record_ref_id_generation_descriptor_owner_and_state: Prepared,
    target_park_handoff_publication_ref_id_and_generation_observed_parked,
    prevalidated_terminal_or_durable_release_proof_build_descriptor_and_destination,
    exact_terminal_or_durable_destination_acceptance,
    release_mode_gate_observed_exact:
        SwitchingToTerminal | SwitchingToDurable,
    no_resume_custody_transfer_proof_publication_or_claim,
    no_available_claimed_or_consumed_scheduler_resume_authority,
    protected_cancel_authority_and_generation
}

ParkReleaseModePairRecoveryPredicate {
    handoff_cleanup_phase:
      ParkedActive {
          handoff_ref_id_generation_and_observed_state: Parked,
          exact_release_mode_generation_variant_descriptor_owner_frontier_and_state:
              ResumeRecordWriting | ResumePrepared | SwitchingToTerminal |
              SwitchingToDurable | ProofWriting | ProofAvailable |
              ProofClaimed
      }
    | ReleaseCommitted {
          handoff_ref_id_generation_and_observed_state: Reclaimable,
          exact_release_mode_generation_variant_descriptor_owner_frontier_and_state:
              ProofClaimed | Released | Clearing,
          each_proof_and_destination_hold_observation:
            UnexposedMember {
                matching_member_exposure_bit_observed_clear,
                proof_state_if_proof_member:
                    Consumed | Clearing | EmptyNextGeneration,
                destination_hold_state_if_hold_member:
                    Released | Clearing | EmptyNextGeneration
            }
          | ExposedMember {
                matching_member_exposure_bit_observed_set,
                member_observed_old_clearing_or_at_least_exact_next_generation,
                no_member_body_read_or_mutation
            },
          exact_variant_successor_publication_gate
      }
    | HandoffClearing {
          handoff_ref_id_generation_and_observed_state: Clearing,
          exact_release_mode_generation_variant_descriptor_owner_frontier_and_state:
              Released | Clearing | UndecidedNextGeneration,
          exact_sidecar_hold_and_successor_cleanup_frontier
      },
    member_observation:
      BeforeMemberExposure {
          selected_sidecar_observation:
            PreclaimEmpty {
                sidecar_slot_and_same_generation_observed_descriptor_free_empty
            }
          | ClaimedOrPublished {
                sidecar_slot_generation_descriptor_owner_and_state:
                    Writing | Prepared | Available | Claimed | Consumed
            }
          | SidecarClearing {
                sidecar_slot_generation_descriptor_owner_state_and_clear_verification:
                    Clearing
            },
          exact_resume_record_and_release_proof_companion_observations,
          exact_destination_hold_state_frontier_and_authoritative_bits
      }
    | AfterMemberExposureAuthorized {
          exact_release_mode_frontier_and_exposure_authorized_member_bitmap,
          exact_remaining_unexposed_member_states_and_frontiers,
          each_exposed_member_observed_old_clearing_or_at_least_exact_next_generation,
          no_exposed_next_generation_body_is_read_or_mutated
      },
    deterministic_next_step:
        ClaimSelectedSidecar | FinishSelectedSidecar |
        FinishPreparedCancellation | ClaimOrFinishProof |
        CompleteProofClaim | CompleteRelease | CompleteCleanup,
    complete_sidecar_extent_receipt_and_current_or_consumed_reclaim_if_required,
    protected_pair_recovery_authority_and_generation
}
```

The decision ID is a preallocated generation-scoped identifier rather than a
hash of fields that refer back to it. The body is built privately after
admission under `Writing`; its canonical digest covers every body field with no
self-reference. `effective_product` is a closed, self-describing union: a
reader never interprets `effective_product_digest` through an out-of-band
lookup. The digest is recomputed from the canonical variant tag and complete
variant body. The asynchronous variant carries its proofs, the local-resume
variant carries the accepted token's immutable identity/publication manifest,
the containment variant carries the complete semantic requirement body and
digest, and the terminal variant carries its explicit scope and reason. Every
operational, requirement, terminal, graph-rehome, and crash-capsule copy
preserves this union byte-for-byte and validates that its tag agrees with the
decision rule, acceptance root, entry action, and any escalation
`disposition_class`. `decision_publication_id` then joins intended `Sealed` state,
owner/generation, decision ID, acceptance root, and body digest with its own
field omitted. A non-containment decision child is release-published `Sealed`
only after its custody prerequisite, but becomes accepted only when its
enclosing aggregate decision→core→projection graph root is `Sealed`, its
product-required reservation-bound continuation hold (if any) is `Complete`, the accepted-bit CAS wins,
and the matching entry reaches `Live`. A containment decision is never
accepted merely because a standalone decision object looks sealed: its
`acceptance_root` must embed the protected acceptance witness proving the
exact requirement slot/generation reached validated lifecycle state `Held`, and
its body digest must equal the candidate digest committed inside that envelope;
its graph then follows the same Complete-hold/accepted-bit/`Live` gate.
Together with the immutable raw-block set, ordered per-source result and
acknowledgement set, and entry-snapshot reference/digest, the decision forms the `ArchitectureFaultRecordCore`
described by the [fault decoder](fault-decoder.md). Later decoded projections
reference this decision; they never replace it.

No nonterminal decision is exposed before component 2 owns a publisher-only
preaccept `ContinuationCustodyHoldPublication`. Admission preallocates its
exact slot/generation and token/holder-bit plan, first seals the immutable
`ContinuationCustodyPlanDescriptor`, and binds its compact descriptor identity
in both the graph reservation and hold claim. Component 2 CASes `Empty →
PlanWriting` with that descriptor before changing hold-plan audit bytes,
validates the copied plan against the descriptor, and release-publishes
`Prepared` before the graph can reach `ReadyToAccept`. Thus a cut in plan
construction has a named owner, a complete protected recovery plan, and no
anonymous source borrow.

After the graph root is `Sealed` and its dependency entry is
`ReadyToAccept`, but **before** the accepted-bit CAS, component 2 changes the
hold to `Acquiring`. Before each graph, evidence-root, and (for containment)
held-requirement borrow CAS, it publishes the corresponding acquisition
frontier. The preallocated token ID selects one bit in that source's
generation-bound `BoundedBorrowCount`; the source CAS atomically installs the
holder bit and increments its checked count. Component 2 then records the bit
in the hold word and immediately rechecks graph `Sealed`, entry
`ReadyToAccept`, dependency-set `Open` with reservation bit set and accepted
bit clear, and the root's variant-specific readable state. A cut between the
source CAS and hold-bit update is not ambiguous: fenced recovery compares the
published frontier with the source word's exact token bit, then either records
the acquisition or performs the one idempotent release. The complete hold word
and each source borrow word must fit a target-supported atomic operation.

Only a fully validated `Complete` hold with every required token bit installed
permits the atomic accepted-bit CAS and subsequent `ReadyToAccept → Live`;
that CAS is the nonterminal decision's acceptance. If closing wins, no accepted
disposition exists: recovery changes the named hold to `Releasing`, releases
exactly the installed token bits, publishes `Released`, and follows sealed-
but-unaccepted graph abandonment/terminal fallback. If acceptance wins, a cut
before `Live` preserves both the accepted bit and complete hold, so recovery
must finish `ReadyToAccept → Live`; later closing cannot invalidate the
accepted return or park.

The return leaf stops all graph/evidence dereferences and transfers the hold to
the exact `ReturnArmed` record **before** the architecture return instruction.
While the hold remains exact `Complete`, it first validates the arm descriptor,
claims the arm `Empty → Writing`, and seals and validates the armed record as
the destination. For local resume, only that sealed arm permits the exact
one-shot token `Available → Consumed` CAS; async has no token. Only after the
arm is sealed and any token is consumed does it CAS the hold `Complete → Transferring`,
publish `TransferPreparingDestination`, bind the already sealed arm, publish
`TransferCommitted`, and change the hold to `Transferred`; any cut retains
depth one and the authoritative operation frontier. Thus no exposed
`Transferring` hold can coexist with a descriptor-free empty arm. A cut before
the arm claim has changed no destination and may retry the same prevalidated
claim; a cut in arm `Writing|Armed` is owned by the return-arm recovery
protocol.
It cannot release tokens after `IRET`, `ERET`, or `xRET`, because a successful
instruction has already left the handler. A return-instruction fault re-enters
through the pinned depth-one `ReturnArmed` route and terminalizes without
releasing the hold. After a successful return, the next protected entry or
context-switch finalizer distinguishes the reached target privilege/context
from the return-leaf PC, validates the per-context return cookie, and only then
publishes return completion, releases the exact hold token bits, and resets
entry depth. Specifically it CASes `Transferred → Releasing`, publishes the
closed `ReleaseGraph`, `ReleaseEvidenceRoot`, and optional
`ReleaseRequirement` frontier before clearing each corresponding authoritative
source bit, then publishes `ReleaseComplete` and `Released`. Until that proof,
the hold remains live and the context cannot be
reused. Local resume never consumes its one-shot token before the arm is
sealed.
`ParkCommitting` first claims the exact preallocated
`ParkHandoffPublication` `Empty → Writing` using the handoff and
destination-hold generations already bound in the source hold's immutable
park-transfer plan; this occurs before any destination acquisition. It then
changes the source hold to `Transferring`, and the preallocated destination
hold installs and rechecks replacement graph/root/requirement token bits.
Before either can be released, component 2 copies into the claimed handoff the exact
accepted graph/requirement/witness, parked context, fence, custodian, both hold
manifests and transfer frontier, validates its digest, and publishes `Sealed`.
The named custodian's exact `Sealed → Parked` CAS is the stable handoff
acceptance. Only then does the source hold publish `TransferCommitted` and
`Transferred`; the source enters `Releasing`, uses the same closed per-token
release frontiers, verifies all source bits clear, and publishes `Released`.
Only after that exact `Released` state validates may component 2 reset entry
depth and leave the park leaf. Until then a nested entry remains depth two and
is interpreted through the retained `ParkCommitCut`; at/after `Parked` the
custodian and destination hold already own the parked continuation, while
component 2 owns only completion of the source-release transaction. A cut in
either transfer or release is resolved from
the handoff lifecycle, two hold words, source holder bits, and `ParkCommitCut`;
before `Parked` the source remains owner, while at/after `Parked` the custodian
and destination hold are authoritative. Ambiguity keeps the execution parked/
terminal rather than guessing completion. A graph ID or post-hoc borrow cannot bridge
either handoff.

Failure before `Parked` has a CAS-arbitrated terminal abort rather than an
orphan destination borrow. The source plan's protected abort authority can
change the exact handoff `(Writing|Sealed, generation) → (Aborting,
generation, abort_owner)` while the source hold remains exact `Complete` or
`Transferring`.
For a sealed handoff, that single-word CAS races the custodian's `Sealed →
Parked`, so exactly one outcome wins; a `Writing` handoff was never eligible for
custodian acceptance. After `Aborting` wins, the abort owner publishes
`TransferAbortSelected` and evaluates the closed
`ParkHandoffAbortPredicate`. `DestinationNeverClaimed` requires the exact
preallocated hold slot still descriptor-free `Empty` and every planned source
bit absent; it skips destination release and records that empty observation in
the abort frontier. `DestinationClaimed` instead resumes or drives the
descriptor-tagged hold through its closed `Releasing` frontiers, clears every
installed destination holder bit, and verifies `Released`. Abort context does
not advance that hold to `Clearing`: both its pool reservation bit and the
never-claimed variant's reservation bit remain installed for group cleanup. It
then restores the still-authoritative source hold atomically to
`Complete/TransferAbortComplete` without changing its installed source bits and
publishes the handoff `Aborted`. No entry-depth reset or return is permitted:
the already accepted containment obligation remains, and component 2 enters a
nonreturning terminal/manual-custody leaf. A cut resumes from the handoff word,
the two exact hold words, and authoritative source bitmaps; it never guesses
whether parking occurred.

An `Aborted` handoff, its released-or-never-claimed reserved destination hold,
and its retained source hold are not reused in that crash generation.
Next-boot cleanup is one explicitly blocked multi-object transaction, not three
independent rearms. It requires a complete fixed-extent
`IncompleteCrashAttempt(ParkHandoffAbortGroup/InitialCleanup)` custody receipt,
a generation-current `CrashReclaim`, and complete independent rehome of the
accepted requirement/graph/source-hold obligation. The cleanup owner validates
the preallocated `ParkAbortGroupCleanupDescriptor`, atomically claims its
barrier, and verifies all three original pool reservation bits before CASing
handoff `Aborted → Reclaimable`. From then on only the `CleanupResume` arm is
admissible; the barrier's descriptor, member frontier/bitmap, receipt, reclaim,
and old/next generations survive every cut.

Under barrier `MembersReleasing`, recovery drives the retained source hold
through its exact release frontier to `Released`; the claimed destination is
already `Released`, while `NeverClaimedReservedEmpty` is never fabricated into
a hold. Under `MembersClearing`, it clear/rekeys and verifies a claimed
destination hold first, then the source hold, then the handoff, publishing each
exact next-generation `Empty` only while its pool reservation bit remains set.
The never-claimed destination remains its observed old-generation `Empty` and
retains only its reservation bit. Each completed member sets its authoritative
barrier bitmap before the next begins. When the required bitmap is complete,
the barrier publishes `MembersRearmed`, atomically releases the complete
three-bit pool reservation set in one admission word, and publishes `Released`.
Only that one CAS makes the member slots eligible for new allocation. It then
clear/rekeys the barrier and publishes its next descriptor-free `Empty`; this
is the abort group's final source publication, after which the sink may clear
the still-held reclaim and receipt reference. A cut after any member reaches
next `Empty` cannot race reuse while the barrier is blocked; a cut after the
barrier release needs no old member body. Without the exact predicate, barrier,
receipt, reclaim, rehome, or reservation tuple, the whole group is retired.

The hold pool has an exact bounded rearm. A preaccept attempt that lost closing
may rearm its `Released` hold only after the graph accepted bit is proved clear,
the dependency entry is `Revoked`, every source holder bit is absent, and the
sealed-but-unaccepted abandonment proof names that exact hold. An accepted
source hold may rearm only after a proved successful-return finalizer or
completed park transfer releases every planned source bit. In either case, the
exclusive owner CASes `Released → Clearing`, clears/rekeys and verifies the
plan, token manifest, owner and frontier, advances the hold generation with
checked nonwrap, and publishes next `Empty` last. A cut in `Releasing` or
`Clearing` resumes idempotently and exposes no new hold. Generation exhaustion
retires the slot. If the return instruction faults or return success remains
ambiguous, the `ReturnArmed`/hold pair is terminal evidence and remains
nonreusable for the crash generation; cleanup never releases it merely to
restore pool capacity. Its only later path is the double-fault guard's closed
next-boot `ReturnArmRecoveryPredicate`: complete full-group custody and current
reclaim authority, an exact successful-finalizer proof or a disjoint fenced
no-return proof, complete accepted-source rehome, and descriptor-tagged
clear/rekey. It never resumes the retired context.

Required-but-never-complete holds use the same bounded path. After fencing the
publisher and proving the graph accepted bit clear, recovery evaluates the
closed `ContinuationHoldCancellationPredicate` against the immutable plan
descriptor, exact hold word/frontier/bitmap, every authoritative source holder
word, and dependency entry. It may CAS `PlanWriting|Prepared|Acquiring|Complete
→ Releasing`; for a cut between a source-bit CAS and hold-bit update, the
published frontier plus planned bit selects the one idempotent record-or-release
action. It then releases exactly the installed set and reaches `Released`
before normal rearm. A missing descriptor, accepted graph, ambiguous frontier,
or unexplained source bit holds the slot. This rule also cleans a partially
acquired pre-`Parked` destination hold after the handoff abort wins; no direct
incomplete-state-to-`Empty` edge exists.

The destination hold transferred to a stable parked custodian has its own
finite lifetime; it is not silently discarded at `Parked`. It may be replaced
only by the same overlap-then-release custody protocol. Final release requires
a protected `ParkedContinuationReleaseProofPublication` binding that exact
hold and parked-context generation through one closed
`ResumeCustodyTransfer`, `TerminalCustodyTransfer`, or
`DurableObligationTransfer` body. The custodian claims exact proof `Available
→ Claimed`, publishes hold `Releasing`, clears each authoritative holder bit
once, and reaches `Released`. A cut resumes from the claimed proof and release
frontier; after all bits are clear it publishes proof `Consumed` and handoff
`Parked → Reclaimable`, then release mode `ProofClaimed → Released`. Missing
proof keeps the context parked and the destination hold live. The proof,
handoff, and hold each use verified `Clearing → Empty(next generation)` rearm;
the release-mode word reaches `Clearing` only after their required successor
publication gate, and returns to next-generation `Undecided` before the
handoff itself becomes reusable. From the handoff reclaim CAS onward, recovery
uses the `ReleaseCommitted` or `HandoffClearing` arm of
`ParkReleaseModePairRecoveryPredicate`; the predicate therefore never requires
an already reclaimed handoff to still appear `Parked`, and each arm restricts
the admissible gate, proof, hold, successor, and sidecar states for that exact
cleanup frontier. During verified member cleanup, the release-mode owner
clear/rekeys one sidecar or destination hold while its old pool reservation
remains installed. It then advances the atomic cleanup frontier and sets that
member's exposure-authorized bit **before** publishing the member's next
`Empty`. A cut before the `Empty` CAS finishes it from old `Clearing`; a cut
afterward may observe a new generation and never reads or mutates it. Once an
exposure bit is set, the old transaction no longer requires the member body.
After the complete exposure bitmap, successor gate, and next-generation mode
word validate, handoff next-`Empty` is the final publication; no old recovery
predicate is needed or permitted beyond that point.

The handoff initializes one shared native-atomic `release_mode_word` as
`Undecided` before publishing `Parked`; both sidecars must win this word before
their independent slot claims. To prepare resume, the scheduler validates an
immutable `ParkedSchedulerResumeBuildDescriptor` binding the parked context,
completion, holds, sanitized frame, slot, and this gate generation, then CASes
exact `(Undecided, g, None, None, None, (ModeUnselected, zero_bitmap)) →
(ResumeRecordWriting, g, Resume,
resume_descriptor, scheduler_owner, (SidecarClaimPending, zero_bitmap))`.
Only that state permits its resume-record
`Empty → Writing` claim. The sidecar/hold pool also requires that no older
handoff reservation names the slot, or that the older gate's exact exposure
bit is already set; descriptor-free `Empty` alone is not admission authority.
The completed body must reproduce the descriptor
before `Prepared`, after which the scheduler publishes gate `ResumePrepared`.

A direct terminal or durable proof builder instead wins exact
`Undecided → ProofWriting` with its variant, proof descriptor, and owner before
checking the descriptor-free `Empty` resume-record slot; the scheduler can no
longer race `Empty → Writing`. A change away from an already prepared resume
must CAS the same word `ResumePrepared → SwitchingToTerminal` or
`SwitchingToDurable`; this races the resume proof's
`ResumePrepared → ProofWriting(Resume)` selection, so exactly one wins. The
nonresume winner applies `PreparedResumeCancellationPredicate`, CASes the exact
tagged record `Prepared → Clearing`, verifies clear/rekey and publishes
`(Empty, next_generation, None, None)` last, then advances the same gate to
`ProofWriting` for its selected variant. Its proof body binds the resulting
exact empty generation. If the record is `Writing`, fenced recovery first
finishes it to the descriptor-bound `Prepared` state; `Available`, `Claimed`,
`Consumed`, mismatch, or an existing resume-proof selection makes the switch
ineligible and keeps the hold live.

Only exact gate `ProofWriting` permits the release-proof slot
`Empty → Writing` claim. Its completed body must reproduce the gate variant and
descriptor before both proof `Available` and gate `ProofAvailable` publish.
Proof claim and gate `ProofAvailable → ProofClaimed` are idempotently completed
as one descriptor-bound pair before any hold bit releases. Thus `ProvedEmpty`
cannot go stale, the three release variants are exclusive, and changing
disposition cannot strand a `Prepared` record or latent resume authority.

Every cut between that shared gate and either sidecar is covered by
`ParkReleaseModePairRecoveryPredicate`. If mode is `ResumeRecordWriting` or
`ProofWriting` while the selected slot is still same-generation descriptor-
free `Empty`, fenced recovery performs the descriptor-bound slot claim; it
does not roll the mode back from an observation of the empty body. If mode is
`SwitchingToTerminal|SwitchingToDurable`, the exact record state
`Prepared|Clearing|Empty(next)` and published cleanup frontier determine
whether to claim cancellation, resume clear/rekey, or advance to the selected
`ProofWriting`. `ProofAvailable|ProofClaimed`, release, and cleanup cuts use the
same pair predicate with exact companion states. Required full-extent receipt
and reclaim state travel with the pair. A mismatched generation, owner, mode,
or unexplained sidecar state holds the complete handoff rather than freeing
one member. Thus the gate-before-slot and clear-before-next-mode windows are
finite recoverable states, not descriptor-free leaks.

Fenced recovery at any sidecar `Writing` state may deterministically finish the
same descriptor under its matching `ResumeRecordWriting` or `ProofWriting`
gate. It may instead cancel only an initial scheduler record or a
`ResumeCustodyTransfer` proof under the closed
`ParkSidecarWritingRecoveryPredicate`: the handoff is still `Parked`, the
destination hold remains `Complete`, no sidecar publication/claim, hold-release
frontier, or `Parked → Reclaimable` transition exists, the gate's variant,
descriptor, and owner match, and the exact builder is fenced. Next-boot
cancellation additionally preserves the complete fixed
sidecar extent in `IncompleteCrashAttempt(ClassifierSidecarWriting)` and
consumes its current `CrashReclaim`. The owner then CASes exact tagged
`Writing → Clearing`, verifies full clear/rekey, advances checked generations,
and publishes descriptor-/owner-free `Empty` last. It then CASes the gate to
the predicate's exact postcancel state: `Undecided` for a cancelled initial
record, or `ResumePrepared` when a cancelled resume proof leaves its valid
prepared record. These are two tagged predicate arms, not independent choices:
a scheduler-record cancellation cannot publish `ResumePrepared`, and a resume-
proof cancellation cannot publish `Undecided` or omit the exact matching
`Prepared` companion record. A terminal/durable `ProofWriting` state is force-forward
because its sealed terminal destination or accepted durable obligation cannot
be revoked by this protocol; it must finish the same proof and retain its
selected gate mode, or conservatively pin the handoff. Thus cancellation creates
no resume authority and never releases destination custody; a fresh bounded
attempt can be made while the context remains parked. Missing proof retains
the sidecar and hold. Each sidecar word and the complete release-mode word must
fit one native atomic operation or a fixed independent shard assigned before
the handoff; reconstructed multiword mode is not authoritative.

Before publishing a release proof `Available` and matching gate
`ProofAvailable`, its trusted writer verifies
that the normalized target fields outside the body equal the handoff and
destination-hold fields inside the selected closed body variant, computes the
self-excluding body digest, and binds all of them plus the exact one-shot
authority in `publication_id`. A releaser may win `Available → Claimed` only
after revalidating that complete identity, the target handoff in `Parked`, and
the exact matching gate variant/descriptor; it then completes gate
`ProofAvailable → ProofClaimed` before release;
neither a proof body copied from another generation nor a terminal destination
of the wrong publication kind can authorize holder-bit release.

For the resume arm, the scheduler first writes the fixed record, copies every
frame/context value needed after release, binds the exact accepted completion,
and publishes it `Prepared` before the one-shot kernel release authority can
construct `ResumeCustodyTransfer`. The record contains no graph, requirement,
or evidence pointer. Only after the claimed release proof is `Consumed`, the
destination hold is `Released`, and the handoff is `Reclaimable` may the kernel
CAS the matching resume record `Prepared → Available`. Exact `Available →
Claimed → Consumed` governs scheduler use; after the resumed context has
taken custody, verified `Clearing → Empty(next generation)` rearms it with
checked nonwrap. `TerminalCustodyTransfer` names a sealed nonreturning terminal
publication/owner; `DurableObligationTransfer` names a durable receipt whose
explicit acceptance scope includes continuing quarantine and the parked
context. Neither can be substituted for the other, and neither a bare
completion digest nor a merely `Prepared` scheduler record can resume
execution.

For `ResumeCustodyTransfer`, `Consumed`, `Released`, and `Reclaimable` are not
yet cleanup authority: the proof, handoff, and released destination hold remain
generation-held until the matching resume record successfully reaches
`Available`. A cut after custody release but before that CAS therefore resumes
the same `Prepared → Available` step from retained proof. Only then may their
verified clear/rekey protocols begin. The terminal and durable-transfer arms
apply the analogous gate to their already sealed nonreturning destination or
durable acceptance receipt and require their bound scheduler-record slot to be
proved descriptor-free `Empty` after any `Prepared` cancellation; no arm
clears the only witness needed to finish its next publication.

### Asynchronous non-disruptive report

This result permits return without a local resume token only when the rule
proves that delivery was not caused by the interrupted instruction, the return
frame and processor context are intact, no poisoned value was consumed, the
source's profile-specific acknowledgement predicate holds, and no quarantine
is required before return. That predicate names the allowed terminal value for
each source program: for example `ObservedCleared`, or
`Completed/NotRequiredByProfile` for a validated non-destructive source. An
untouched `NotStarted`, generic `Completed`, or another source's result never
suffices. `NoValidRecordObserved` and `ObservationWasAcknowledgement` are
conservative evidence states, not async-return postconditions. A “corrected”
bit alone is insufficient.

```text
AsynchronousNonDisruptive {
    capture,
    rule_id_and_hash,
    return_frame_integrity_proof,
    non_attribution_proof,
    acknowledgement_postcondition
}
```

Any later operational-ring location is recorded in a separate custody binding;
it cannot be embedded in a decision that necessarily precedes that copy.

### Local resume postcondition

Only the backend's bounded action code can construct this sealed linear token:

```text
LocalResumePostcondition {
    capture,
    rule_id_and_hash,
    exact_cpu_and_context_incarnation,
    faulting_pc_and_recovery_region,
    action_program_id,
    precondition_digest,
    completed_local_effects,
    return_envelope_digest
}

LocalResumeTokenPublication {
    lifecycle_word: Atomic<(
        Free | Writing | Available | Consumed | Revoked | Clearing,
        token_slot_generation,
        compact_local_token_build_descriptor_index_and_generation_or_none,
        compact_token_owner_tag_or_none
    )>,
    token_id,
    token_owner_and_generation,
    local_token_build_descriptor_digest,
    token_publication_id: Hash(canonical_encoding({
        intended_state: Available,
        token_slot_generation,
        token_owner_and_generation,
        local_token_build_descriptor_digest,
        compact_token_owner_tag,
        token_id,
        decision_id,
        capture,
        exact_cpu_and_context_incarnation,
        reserved_fault_record_graph_slot_and_generation,
        expected_graph_seed_digest,
        canonical_postcondition_digest,
        authority_binding
    })),
    decision_id,
    capture,
    exact_cpu_and_context_incarnation,
    reserved_fault_record_graph_slot_and_generation,
    expected_graph_seed_digest,
    canonical_postcondition_digest,
    authority_binding: ProtectedKernelReturnAuthority,
    body: LocalResumePostcondition
}

LocalResumeTokenBuildDescriptor {
    descriptor_index_and_generation,
    token_slot_and_generation,
    token_owner_and_generation,
    capture_decision_cpu_and_context_incarnation,
    reserved_fault_record_graph_slot_generation_and_seed_digest,
    authoritative_local_action_result_ref_id_generation_and_digest,
    protected_kernel_return_builder_authority_and_generation,
    canonical_descriptor_digest
}

LocalResumeTokenWritingCleanupPredicate {
    token_slot_generation_owner_and_build_descriptor,
    exact_old_builder_cpu_and_context_fence_evidence,
    no_available_token_accepted_graph_or_return_armed_record,
    local_action_result_reconciled_and_copied_into_terminal_evidence,
    complete_fixed_extent_receipt_and_current_crash_reclaim_if_next_boot,
    protected_token_cleanup_authority_and_generation
}
```

`expected_graph_seed_digest` is the digest of the decoder contract's canonical
`InitialGraphSeed`, constructed before this token is written. Its closed fields
are the reserved graph slot/generation, capture, preallocated generation-scoped
decision ID, logical raw/source-set digests, entry-snapshot semantics, pinned
machine profile, intended `OperationalRingRoot` substrate identity/generation,
and graph schema/bounds. The seed explicitly excludes this token's ID or
publication, the decision body/digest, all graph-child publication IDs, the
record-semantic ID, and the final graph/provenance IDs and digests. Nothing in
the seed is derived from an excluded field. The token can therefore commit the
future graph reservation without a hash cycle; the sealed initial graph embeds
the same seed, and the return path recomputes it from protected reservation
facts rather than trusting a copied digest.

Initial admissible examples should be limited to a generated guarded-user-copy
fixup whose mutation boundary is known, and possibly a selected corrected
asynchronous event that actually belongs in the previous category. General
machine-check continuation should remain terminal until a target-specific case
is demonstrated.

Before claiming a token, the backend validates an immutable
`LocalResumeTokenBuildDescriptor` that binds the exact capture/decision,
CPU/context, graph reservation/seed, protected owner, and already sealed local-
action result. Its native-atomic
`(Free, g, None, None) → (Writing, g, descriptor_tag, owner_tag)` claim installs
those tags before any token byte changes. It writes the postcondition,
cross-checks every field against the descriptor/result, and release-publishes
`(Available, g, descriptor_tag, owner_tag)` only after the protected authority
binding and publication ID validate. The accepted decision embeds its immutable identity, owner/
generation, publication ID, and body digest—not a reusable pointer. Component
2's matching return path validates the exact decision publication, closed
`LocalResumeProduct` tag, capture, CPU/context incarnation, return envelope,
token publication, body digest, protected authority, and the exact aggregate
graph root. Under a graph borrow it requires lifecycle `Sealed`, the reserved
graph slot/generation and seed from the token, graph ID/digest, membership of
that decision/token identity, a recomputed matching `InitialGraphSeed`, the bidirectionally matching `Live` dependency-
set entry, and `OperationalRingRoot` custody to revalidate
at the immediate boundary; a sealed orphan decision child can never suffice.
It then consumes the token with
the sole exact `(Available, g, descriptor_tag, owner_tag) → (Consumed, g,
descriptor_tag, owner_tag)` CAS at the immediate return
boundary. A racing, stale, copied, or forged token therefore cannot authorize
return. Failure after consumption is terminal; the token cannot be restored to
`Available`, transferred, or replaced by a later coordinated completion.

A `Writing` token never becomes an anonymous pool leak. Fenced recovery may
finish only the same descriptor from the still-valid authoritative local-action
result. Otherwise exact `Writing → Clearing` requires the closed
`LocalResumeTokenWritingCleanupPredicate`: no token/graph/return-arm acceptance,
the old CPU/context is fenced, and any completed local effect has been
reconciled and copied into the terminal evidence. A next-boot cleanup also
requires a full fixed-extent
`IncompleteCrashAttempt(ClassifierSidecarWriting)` receipt and current
`CrashReclaim`. Verified clear/rekey advances checked generations and publishes
`(Free, next_generation, None, None)` last. Ambiguous effects, acceptance, or
owner identity retain the token and force terminal/manual reconciliation.

Once return is no longer possible, the kernel may move `Available` to
`Revoked`; `Consumed` or `Revoked` reaches `Clearing` only under the publication
graph's exact-generation rearm gate after all readers are revoked and drained.
The fixed clear/rekey recipe covers the token body, authority, and metadata;
successful verification increments a checked-nonwrapping token generation and
publishes descriptor-/owner-free `Free` last. The complete lifecycle tuple must
fit one native atomic operation or a fixed per-CPU shard. Exhaustion retires the slot until a fresh protected CPU/
boot identity domain. The sealed postcondition payload is never mutated to
represent consumption.

```text
TerminalDispositionProduct {
    capture,
    rule_id_and_hash,
    disposition_scope,
    terminal_reason_and_failed_premises,
    required_terminal_profile_id,
    terminal_generation_reservation
}
```

### Containment requirement

```text
ContainmentRequirementBody {
    requirement_id,
    capture,
    rule_id_and_hash,
    logical_raw_block_set_digest,
    logical_source_result_and_acknowledgement_set_digest,
    reserved_requirement_slot_and_generation,
    affected_incarnations,
    required_actions: BoundedSet<ContainmentAction, MAX_ACTIONS>,
    required_completion_predicate,
    initial_park_and_access_fence_proof,
    external_effect_status,
    deadline_policy,
    fallback_scope,
    authority_template_id
}

ContainmentRequirement {
    requirement_body_digest,
    body: ContainmentRequirementBody
}
```

`requirement_id` is the hash of the canonical `ContainmentRequirementBody`
with its own field omitted. Because that body includes the nonrepeating capture
incarnation and exact reserved requirement-slot generation, this semantic ID
cannot repeat across safe slot reuse. It is still data, not authority; every
cross-owner completion or release additionally binds the exact accepted
publication below.

The requirement body is a requested predicate and names its already reserved
slot/generation. It deliberately does not contain the later-created evidence
publication or core ID, avoiding a construction cycle. Its canonical digest is
embedded in the requirement-evidence envelope described below; the outward
typed requirement reference is created only after that envelope also binds the
decision and core and is accepted as `Held`. Its
retention or durability strength comes from the separately recorded custody
state; the requirement itself conveys no authority. Higher policy joins it with
separately provisioned scoped facets for domain stop, mapping/frame retirement,
CPU offline, IRQ masking, DMA/device quiescence, or reset. Until the predicate
is complete, the affected execution remains parked and admission remains
fenced. “Fully isolated/quarantined” is reserved for the later state in which
every required CPU, translation, DMA, device, cache, and external-effect owner
has supplied its proof.

The initial proof distinguishes `AffectedExecutionParked`,
`NewAdmissionFenced`, `ExistingReachabilityClosing`, and `FullyIsolated`.
Split-phase containment is admissible only when the pinned hardware/profile can
immediately fence every possible accessor from propagating or consuming the
fault while existing reachability closes. A page-table edit alone does not
fence stale CPU translations or DMA. If no such initial fence exists, the
effective decision is terminal rather than a containment requirement.

### Requirement-evidence publication and lifecycle

The reserved requirement pool is not a collection of reusable pointers. Each
slot has one atomic generation-tagged lifecycle word and one fixed-capacity
publication:

```text
RequirementEvidenceBody {
    evidence_schema_version,
    canonical_bounds_and_lengths,
    requirement_slot_and_generation,
    capture,
    reserved_custody_owner_and_generation,
    complete_raw_block_set_copy_and_digest,
    complete_ordered_source_result_and_acknowledgement_set_copy_and_digest,
    entry_snapshot_copy_and_digest,
    prevalidated_held_acceptance_tuple: RequirementHeldAcceptanceTuple,
    containment_requirement_body_copy_and_digest,
    capture_disposition_decision_candidate_body_and_digest,
    architecture_fault_record_core_seed_body_and_digest,
    canonical_body_digest
}

RequirementEvidencePublication {
    lifecycle_word: Atomic<(
        Free | Writing | Sealed | Held | Abandoned | Reclaimable | Clearing,
        requirement_slot_generation,
        held_acceptance_tuple_index_or_none: Option<BoundedTupleIndex>,
        compact_requirement_operation_descriptor_index_and_generation_or_none,
        compact_requirement_operation_owner_tag_or_none,
        cleanup_frontier:
            None | DependenciesClosing | DependenciesDrained |
            BorrowClosing | BorrowDrained | ReclaimCommitted |
            ClearAuthorized | BodyVerifiedEmpty
    )>,
    publication_id: Hash(canonical_encoding({
        intended_initial_state: Sealed,
        requirement_slot_and_generation,
        capture,
        requirement_id,
        decision_id,
        core_seed_digest,
        reserved_custody_owner_and_generation,
        requirement_build_descriptor_digest,
        compact_requirement_builder_owner_tag,
        canonical_bounds_and_lengths,
        canonical_body_digest
    })),
    requirement_build_descriptor_digest,
    canonical_body_digest,
    body: RequirementEvidenceBody
}

RequirementEvidenceBuildDescriptor {
    descriptor_index_and_generation,
    requirement_slot_and_generation,
    capture_and_reserved_custody_owner_generation,
    exact_source_staging_raw_source_result_snapshot_and_candidate_inputs,
    prevalidated_held_acceptance_tuple_index_and_digest,
    fixed_requirement_body_bounds_schema_and_copy_plan,
    protected_requirement_builder_identity_and_generation,
    canonical_descriptor_digest
}

RequirementHeldAcceptanceTuple {
    tuple_index: BoundedTupleIndex,
    source_staging_ref_and_generation_expected_containment_committing,
    protected_staging_outcome_gate_authority_and_generation,
    accepting_custodian_identity_and_generation,
    initial_fence_proof_digest,
    acceptance_sequence,
    witness_authority_binding_id_and_generation,
    canonical_tuple_digest: Hash(canonical_encoding({
        tuple_index,
        source_staging_ref_and_generation_expected_containment_committing,
        protected_staging_outcome_gate_authority_and_generation,
        accepting_custodian_identity_and_generation,
        initial_fence_proof_digest,
        acceptance_sequence,
        witness_authority_binding_id_and_generation
    }))
}

RequirementHeldAcceptanceWitness {
    requirement_publication_ref_and_id,
    requirement_slot_and_generation,
    exact_requirement_body_digest,
    observed_lifecycle_state: Held,
    source_staging_ref_and_generation_observed_containment_committing,
    protected_staging_outcome_gate_authority_and_generation,
    accepting_custodian_identity_and_generation,
    initial_fence_proof_digest,
    acceptance_sequence,
    exact_held_acceptance_tuple_and_digest,
    witness_authority_binding: ProtectedKernelRequirementCustodyAuthority |
                               AuthenticatedKernelWitnessEnvelope,
    canonical_witness_digest
}

HeldRequirementBinding {
    requirement_id,
    requirement_publication_ref_id_and_generation,
    exact_requirement_publication_body_digest,
    requirement_held_acceptance_witness_digest
}

RequirementEvidenceReclaimProof {
    reclaim_proof_id,
    requirement_publication_ref_and_id,
    requirement_held_witness_digest,
    requirement_slot_and_generation,
    exact_body_digest,
    authenticated_independent_custody_receipt_ref_and_id,
    completion_or_transfer:
      CoordinatedCompletionCopy {
          source_completion_publication_id_at_copy,
          copied_completion_body_and_canonical_digest,
          completion_acceptance_witness
      }
    | DurableObligationTransfer {
          obligation_transfer_receipt_ref_and_id
      },
    completed_predicate_and_target_incarnations,
    resolved_external_effects,
    preallocated_cleanup_descriptor_slot_generation_acyclic_seed_and_schema,
    reclaim_authority:
      ProtectedSameBootRequirementRelease {
          component_release_authority_and_generation,
          proof_source_never_entered_crash_retention_or_external_custody
      }
    | RegisteredExternalOrCrashRetainedRelease {
          generation_current_crash_reclaim_requirement_evidence_ref_and_id,
          source_reclaim_registry_assignment_and_registration_cell
      },
    canonical_reclaim_proof_digest
}

RequirementEvidenceCleanupDescriptor {
    descriptor_index_and_generation,
    requirement_slot_old_and_next_generation,
    cleanup_variant:
      NeverHeldIncomplete {
          original_build_descriptor_ref_generation_and_digest,
          complete_requirement_attempt_receipt_ref_and_id,
          matching_current_crash_reclaim_ref_and_id
      }
    | AcceptedHeld {
          requirement_reclaim_proof_ref_and_id,
          held_acceptance_witness_digest,
          authenticated_independent_custody_receipt_ref_and_id,
          exact_completion_copy_or_durable_obligation_transfer
      },
    exact_dependency_borrow_close_drain_and_clear_rekey_plan,
    protected_cleanup_owner_identity_and_generation,
    canonical_descriptor_digest
}

RequirementIncompleteCleanupPredicate {
    requirement_publication_ref_slot_and_generation,
    observed_lifecycle_state: Writing | Sealed | Abandoned,
    compact_requirement_build_descriptor_owner_and_exact_writer_fence_evidence,
    source_staging_ref_generation_and_outcome_gate_state,
    no_held_acceptance_tuple_or_witness_proof,
    no_accepted_graph_dependency_or_action_authority,
    complete_requirement_evidence_attempt_receipt_ref_and_id,
    matching_current_crash_reclaim_ref_and_id,
    exact_dependency_and_borrow_epoch_observed_zero_or_drained,
    prevalidated_never_held_cleanup_descriptor_and_owner,
    protected_cleanup_authority_and_generation
}

RequirementCleanupResumePredicate {
    original_requirement_slot_generation_cleanup_descriptor_owner_and_capture,
    cleanup_variant:
      NeverHeldIncomplete {
          original_complete_requirement_attempt_receipt_ref_and_id,
          original_reclaim_publication_ref_id_and_state:
              Claimed | Consumed | Clearing
      }
    | AcceptedHeld {
          original_requirement_reclaim_proof_ref_and_id,
          held_witness_independent_custody_and_completion_or_transfer_binding
      },
    observed_lifecycle_state:
        Reclaimable | Clearing | FreeNextGeneration,
    exact_dependency_borrow_old_and_next_generations_and_cleanup_frontier,
    protected_cleanup_authority_and_generation
}

RequirementEvidenceBorrowEpoch {
    requirement_publication_ref_and_id,
    requirement_slot_and_generation,
    borrow_word: Atomic<(
        Open | Revoking | Drained,
        requirement_borrow_generation,
        live_requirement_reader_and_action_count:
            BoundedBorrowCount<MAX_REQUIREMENT_BORROWS>
    )>,
    authorized_holder_set_audit_digest
}

RequirementEvidenceBorrowToken {
    requirement_publication_ref_and_id,
    requirement_slot_and_generation,
    requirement_borrow_generation,
    holder_identity_and_generation,
    use_class: Reader | Coordinator | ActionOwner | Exporter,
    token_id_and_kernel_authority
}
```

Every `BoundedBorrowCount<MAX_*>` in this report obeys the parent component's
nonwrapping borrow contract: admission proves a finite holder bound, increments
only for `n < MAX`, fails closed at saturation, and permits one decrement per
exact-generation token. Underflow, double release, or wrap can never fabricate
the zero required for `Drained` or rearm.

All arrays and copies have profile-generated maxima. `canonical_body_digest`
is computed with its own field zeroed and binds every declared bound, length,
byte, embedded digest, identifier, and publication reference in the body. The
one explicit mutable-control exception is `ParkHandoffPublication`: its
canonical body digest excludes both `lifecycle_word` and the live
`release_mode_word`, and instead commits the immutable
`release_mode_plan_digest`, its initial `Undecided` generation/plan projection,
preallocated sidecar/barrier slots, pool-reservation plan, holds, context,
fence, custodian, and acceptance authority. Each live release-mode tuple is
authenticated separately by exact native-atomic state/generation/descriptor/
owner/frontier bits plus the unchanged handoff publication ID/generation and
plan digest. A gate CAS therefore does not change or invalidate handoff
identity, while a tuple that cannot reproduce that immutable binding is
rejected.
The
raw copy must contain the complete sealed raw-block set, not a selected subset;
the ordered source copy must contain every source result and its exact
acknowledgement result. The requirement, candidate decision body, and semantic
core seed retain their own canonical digests and preallocated identities, but
the candidate and seed are not independently accepted publications. The core
seed binds the decision's semantic ID/body digest, not the later decision-
publication ID or requirement-publication ID; this makes the held-root
construction acyclic. Acceptance additionally
checks that their capture, rule, raw-set, source-result, acknowledgement,
entry-snapshot, decision, and core bindings agree with the enclosing body. A
body that is truncated, padded outside its declared layout, internally valid
but assembled from different captures, or paired with another slot generation
therefore cannot validate.

The held witness is deterministically materialized only from the immutable
publication and the tuple atomically installed by the kernel/custodian that
first wins the source staging outcome gate and then wins the exact compact
`(Sealed,g,None,descriptor,owner) →
(Held,g,tuple_index,descriptor,owner)` CAS. Before those CASes, trusted code
has already stored the complete prevalidated tuple inside the sealed
requirement body: source staging identity/generation and expected
`ContainmentCommitting` state, its protected gate authority,
checked-nonwrapping acceptance sequence, protected witness-authority identity,
named custodian, and initial fence. The requirement CAS installs
only its compact in-slot `tuple_index`; hardware never atomically moves the
tuple or a digest. Its self-excluding canonical digest covers the
requirement publication identity, slot generation, exact body digest, observed
`Held` state, custodian generation, fence proof, acceptance sequence, and
the exact atomic tuple/digest plus protected authority binding. Every witness
field is therefore recoverable after a cut immediately following `Held`; no
post-CAS allocation or nondeterministic value is required. Copying this fixed value into later envelopes
preserves proof without allocating an independently retained acceptance object;
a caller cannot synthesize it from a readable requirement digest.

The lifecycle is exact:

1. admission validates an immutable `RequirementEvidenceBuildDescriptor`
   binding the slot, capture, named custody owner, every source/candidate,
   fixed layout, held-tuple index/digest, and protected builder, then
   compare/exchanges exact `(Free, g, None, None, None) → (Writing, g, None,
   descriptor, owner)` before recording or copying any body byte;
2. while the minimum fence remains active, it copies the sealed raw set,
   complete ordered per-source result/acknowledgement set, and entry snapshot,
   then adds the exact requirement body/digest and the complete candidate
   disposition-decision body/digest and semantic record-core seed/digest, then
   stores and validates the one fixed held-acceptance tuple at its bounded
   index;
3. it proves the completed body reproduces the descriptor, computes the
   self-excluding body digest and publication ID, and release-publishes
   `(Sealed, g, None, descriptor, owner)` last;
4. the named custodian acquire-loads exact
   `(Sealed, g, None, descriptor, owner)`, validates every
   bound, nested publication identity, digest, and cross-binding, then uses the
   tuple's authority to CAS the **same source-staging lifecycle word** from
   exact `(HeldForContainment, staging_generation)` to
   `(ContainmentCommitting, staging_generation)`; terminal fallback races that
   word with `HeldForContainment → HeldForTerminal`, so only one can win;
5. only while that exact staging gate remains `ContainmentCommitting`, the
   custodian revalidates the requirement and exclusively compare/exchanges its
   compact word to `(Held, g, tuple_index, descriptor, owner)`. Recovery seeing requirement `Held`
   must finish the staging gate to `ContainmentAccepted`; and
6. only after a successful transition and a final acquire validation of the
   unchanged publication ID/body digest and atomic tuple does the requirement
   slot own the evidence; the kernel/custodian or recovery deterministically
   copies the fixed `RequirementHeldAcceptanceWitness` under the already named
   protected authority and CASes staging `ContainmentCommitting →
   ContainmentAccepted`.

A queue insertion, notification, pointer copy, `Writing` body, bare `Sealed`
observation without full validation, or failed/stale outcome-gate/`Sealed →
Held` compare/exchange is not acceptance. Before the gate is claimed, a bounded
nontrapping failure may win only `HeldForContainment → HeldForTerminal`. If
containment wins the gate but the sealed requirement cannot validly reach
`Held`, fenced recovery must first CAS that exact requirement `Sealed →
Abandoned`; only that state permits `ContainmentCommitting → HeldForTerminal`.
If requirement `Held` is observed, terminal fallback is permanently forbidden
and recovery completes `ContainmentAccepted`. Once `Held`, the body and publication ID are immutable for
generation `g`. Mutable progress and completion live in separately sealed
escalation records and may only refer back to this publication ID.

`Writing`, unaccepted `Sealed`, and `Abandoned` are not permanent pool leaks,
but none may be silently rolled back. A fenced recovery owner first proves from
the shared staging word and atomic requirement tuple that no `Held` CAS or
witness can exist. If the source staging gate is still
`ContainmentCommitting`, it must first move exact valid `Sealed` to
`Abandoned`; that CAS prevents a later custodian from reaching `Held` before
terminal fallback can win. Recovery then preserves the **entire fixed
requirement extent**—including partial copies, candidate decision/core bytes,
tuple storage, and apparently untouched space—in a sealed
`IncompleteCrashAttempt(RequirementEvidenceAttempt)` receipt and obtains a
separate generation-current `CrashReclaim` for the same extent. It also proves
that the dependency set has no accepted graph/action registration and that the
pre-Held borrow epoch is zero or drained.

Only that complete `RequirementIncompleteCleanupPredicate` authorizes an
exact `(Writing|Sealed|Abandoned, g, None, descriptor, owner) →
(Reclaimable, g, None, never_held_cleanup_descriptor, cleanup_owner,
ReclaimCommitted)` CAS that atomically replaces the build tags with the
prevalidated `NeverHeldIncomplete` cleanup variant. The
ordinary close/drain and verified clear/rekey sequence below then applies. A
cut after that CAS uses `RequirementCleanupResumePredicate`, the original
variant-tagged receipt/reclaim and old/next generations, and resumes from `Reclaimable` or
`Clearing` without rerunning initial arbitration or minting a second reclaim;
a missing byte, stale staging
state, possible held tuple/witness, accepted dependency, live borrower, or
ambiguous owner permanently retires the generation. Thus abandonment is an
explicit rejection state and reclamation input, not evidence acceptance or an
unbounded allocation sink.

The complete requirement lifecycle tuple, including state, generation, held
tuple index, build descriptor, and owner, must fit one target-supported native
atomic operation or one fixed independently assigned shard. No separately
read body field or emulated multiword CAS identifies a `Writing` owner or
linearizes acceptance/reclaim.

The `Held` CAS is the single acceptance event for the containment transaction.
It installs every value needed to reproduce a fixed
`RequirementHeldAcceptanceWitness`, whose canonical digest and protected
authority bind that exact CAS result. The witness is a copied value,
not a separately allocated publication or unbounded retained slot: it is
embedded in each downstream decision/core wrapper before requirement rearm.

Containment acceptance also makes the same-capture terminal fallback
semantically impossible. Before staging may leave `ContainmentAccepted`, the
staging owner uses the held witness as the
`ContainmentHeldOutcomeWon` basis of a `GraphReservationCancellationProof` and
cancels the still-unwritten terminal-fallback graph reservation: exact header,
owner/capture/companion, zero child frontier, no dependency bit/entry, and zero
borrow must all validate before verified clear/rekey. This cancellation does
not wait for the primary containment graph, which is materialized later from
the held requirement. A cut after `Held` retains staging and the witness until
the same cancellation completes; successful containment therefore cannot leak
one fallback slot per event.

Only after the witness validates may the kernel materialize `CaptureDispositionDecisionPublication`
and `ArchitectureFaultRecordCorePublication` objects for downstream indexing;
each must embed the exact held-acceptance witness as its acceptance root
and reproduce the candidate decision body or semantic core-seed digest
committed by it. The decision publication can be materialized first; the final
core envelope then binds that accepted decision publication outside the
semantic core body. No downstream publication ID participates in computing the
held root. Readers reject a
containment decision or core lacking that root even when its internal digest is
valid. A bare requirement body or `Sealed` slot without that receipt is not an
acceptance proof. A bounded nontrapping reservation, fence, copy, validation,
or custodian rejection before `Held` leaves the candidate bodies inert orphan
evidence in a nonreusable slot and, while the current execution can still run,
seals one distinct direct terminal decision/core. An execution cut or nested
architectural fault **before** the `Held` CAS cannot assume that interrupted
writer returns: it leaves the outer candidate and staging nonauthoritative and
retained, publishes no accepted outer disposition, and seals only the
independently reserved recursive terminal record identifying the exact
interrupted phase/object. After `Held`, the accepted containment obligation and
its staging/requirement custody remain authoritative even if graph or park
materialization is interrupted. Recovery must finish or durably transfer that
obligation; it may not publish a terminal fallback disposition for the same
capture. The nested failure is a separate recursive terminal event, and the
interrupted execution never resumes. Thus there can be
multiple attempted bytes but only one accepted disposition for the capture.

The slot owns one `RequirementEvidenceBorrowEpoch` sidecar whose publication,
slot, and borrow generations are initialized before `Held`; no unbound count is
accepted. Readers borrow the held body through a generation- and borrow-epoch-bound
kernel handle, never through a retained raw pointer. Borrow acquisition first
observes lifecycle `(Held, g)`, increments exact borrow `(Open, b, n) →
`(Open, b, n + 1)` only when `n < MAX_REQUIREMENT_BORROWS`; saturation returns
no handle. It then rechecks both lifecycle and borrow words before
dereferencing; a failed recheck drops the
count without reading. The release gate may change `(Held, g) →
(Reclaimable, g)` only after validating one `RequirementEvidenceReclaimProof`.
That proof is conjunctive: independently owned authenticated custody covers the
exact publication/body, and either the matching kernel-minted
`CoordinatedContainmentCompletion` proves every required predicate and target
incarnation or a durable obligation-transfer receipt takes those exact
remaining obligations. External effects must be resolved under the pinned
profile. A timeout, suspicion, notification receipt, action request, partial
completion, or custody receipt for different bytes cannot make the slot
reclaimable. Before that transition the release owner prevalidates an immutable
`RequirementEvidenceCleanupDescriptor::AcceptedHeld` binding the reclaim
proof, held witness, complete independent-custody receipt, exact coordinated
completion copy or durable obligation transfer, old/next slot generations,
and dependency/borrow/clear plan. The lifecycle CAS atomically replaces the
build tags with this cleanup descriptor and owner while changing `Held →
Reclaimable` at frontier `ReclaimCommitted`. Thus accepted-held cleanup and
never-held crash cleanup never collapse into an indistinguishable lifecycle
tuple.

The reclaim authority is correlated with custody scope. A protected
`ProtectedSameBootRequirementRelease` is valid only for a complete internal
same-boot rehome/completion while the source never entered crash retention or
out-of-domain custody. Reset, a durable obligation transfer, or any external
custody path requires the sink registry's unique generation-current
`CrashReclaim(RequirementEvidence)` for the exact publication, slot generation,
and body digest. The cleanup descriptor retains its registration cell and
reclaim reference until final source exposure; a durable receipt cannot be
paired with the same-boot arm merely to evade retention authorization.

The independent custody reference is the [crash-safe sink](crash-safe-sink.md)
contract's sealed `CustodyReceiptPublication` with its closed
`RequirementEvidence` identity variant. It binds this requirement publication
and held-witness digest, slot generation, exact body digest and complete content
manifest, exact sealed destination-content publication, destination/custodian
generations, durability observation, freshness,
and missing set. A normal/recursive capsule receipt, transport acknowledgement,
or receipt for a subset cannot satisfy this field.

Before the requirement slot can enter `Clearing`, it closes the bounded
evidence-root dependency set and enumerates every initial or decoded-version
graph and protected binding rooted in this requirement. Each live version must
be rematerialized as a complete decision→core→optional-derived-closure→
projection aggregate graph over the same semantic identities, using
`IndependentCustodyRoot` to bind that receipt/destination and an acyclic
rehome witness, or be authoritatively revoked. Replacement bindings must head
before their sources clear, and every graph/requirement borrow must drain. A
single replacement core or graph is not evidence that all versions moved.
Only exact dependency-set `Closing → Drained` permits requirement `Clearing`,
so rearm cannot leave an immutable record or event binding dangling.

`Reclaimable` closes new borrow admission. The exclusive rearm holder, carrying
a capability for this exact slot and generation, changes exact borrow
`(Open, b, n)` to `(Revoking, b, n)`, revokes every revocable handle, and waits for the matching
active count to reach zero. A racing borrower is safe because its post-increment
state recheck fails after `Held` changes. Only after all exact-generation
borrows drain and exact `(Revoking, b, 0) → (Drained, b, 0)` succeeds may the
holder compare/exchange lifecycle `(Reclaimable, g, cleanup_descriptor,
cleanup_owner, frontier) → (Clearing, g, same_descriptor, same_owner,
ClearAuthorized)`. It
executes the fixed clear/rekey recipe over the entire body,
publication metadata, cached handles, and borrow metadata; reads back or
cryptographically verifies the cleared/rekeyed state; refuses generation wrap;
clears the authorized-holder audit, initializes the next exact
`(Open, b + 1, 0)` epoch bound to the next requirement slot/
publication generation; and release-publishes descriptor-/owner-free `(Free,
g + 1, None, None, None, None)` last. Every cleanup frontier advances before
its mutation, and `RequirementCleanupResumePredicate` carries either the
`NeverHeldIncomplete` receipt/reclaim or the `AcceptedHeld` reclaim-proof,
custody, and completion/transfer authority until final exposure. Readers of
the next occupant validate and recheck both lifecycle and borrow words.
Interruption, failed revocation, a nonzero borrower count, failed erase/rekey
verification, or a stale generation leaves the slot nonreusable. No other state
has an edge to `Free`, and a terminal-held requirement is never recycled in the
same boot/crash generation.

### Coordinated containment completion

The architecture component does not fabricate this type. A coordination
owner returns:

```text
OwnerCompletionTokenPublication {
    lifecycle_word: Atomic<(
        Empty | Writing | Available | Claimed | Consumed | Clearing |
        RearmedHeld,
        owner_token_slot_and_generation,
        compact_owner_token_build_descriptor_index_and_generation_or_none,
        compact_completion_build_descriptor_index_and_generation_or_none,
        compact_owner_token_builder_tag_or_none
    )>,
    token_id: Hash(canonical_encoding({
        intended_state: Available,
        owner_token_slot_and_generation,
        owner_token_build_descriptor_digest,
        compact_owner_token_builder_tag,
        owner_component_and_generation,
        held_requirement_binding,
        exact_target_incarnations,
        completed_predicate_fragment,
        external_effect_resolution,
        canonical_body_digest,
        authority_binding
    })),
    owner_component_and_generation,
    owner_token_build_descriptor_digest,
    held_requirement_binding: HeldRequirementBinding,
    exact_target_incarnations,
    completed_predicate_fragment,
    external_effect_resolution,
    canonical_body_digest,
    authority_binding: ProtectedOwnerCompletionAuthority |
                       AuthenticatedOwnerCompletionEnvelope
}

OwnerCompletionTokenBuildDescriptor {
    descriptor_index_and_generation,
    owner_token_slot_and_generation,
    owner_component_and_generation,
    held_requirement_binding: HeldRequirementBinding,
    exact_target_incarnations,
    authoritative_owner_result_publication_ref_id_generation_and_digest,
    completed_predicate_fragment_and_external_effect_resolution_digest,
    protected_owner_token_builder_identity_and_generation,
    canonical_descriptor_digest
}

CompletionBuildDescriptor {
    descriptor_index_and_generation,
    held_requirement_binding: HeldRequirementBinding,
    completion_slot_and_generation,
    constructor_gate_identity_and_generation,
    protected_constructor_identity_and_generation,
    ordered_complete_owner_token_ref_id_generation_and_digest_manifest,
    exact_action_target_and_predicate_conjunction_digest,
    canonical_descriptor_digest
}

CompletionConstructionGate {
    gate_word: Atomic<(
        Idle | ClaimingTokens | BuildingCompletion | CompletionSealed |
        ConsumingTokens | Released | RearmingTokens | ReleasingTokens |
        Clearing,
        gate_generation,
        compact_completion_build_descriptor_index_and_generation_or_none,
        claim_or_consume_frontier
    )>
}

CoordinatedContainmentCompletion {
    held_requirement_binding: HeldRequirementBinding,
    capture,
    exact_action_and_target_incarnations,
    consumed_owner_completion_token_publication_ids_and_digests,
    missing_or_failed_targets,
    external_effect_resolution,
    completed_predicate,
    recovery_owner_and_generation,
    kernel_release_gate_id
}

CoordinatedContainmentCompletionPublication {
    lifecycle_word: Atomic<(
        Empty | Writing | Sealed | Reclaimable | Clearing,
        completion_slot_and_generation,
        compact_completion_build_descriptor_index_and_generation_or_none
    )>,
    publication_id: Hash(canonical_encoding({
        intended_state: Sealed,
        completion_slot_and_generation,
        held_requirement_binding,
        completion_build_descriptor_digest,
        canonical_body_digest,
        authority_binding
    })),
    held_requirement_binding: HeldRequirementBinding,
    completion_build_descriptor_digest,
    canonical_body_digest,
    authority_binding: ProtectedKernelReleaseGateAuthority |
                       AuthenticatedKernelCompletionEnvelope,
    body: CoordinatedContainmentCompletion
}

CompletionAcceptanceWitness {
    source_completion_publication_id,
    completion_slot_and_generation,
    held_requirement_binding: HeldRequirementBinding,
    completion_build_descriptor_digest,
    exact_completion_body_digest,
    observed_state: Sealed,
    release_gate_identity_and_generation,
    authority_binding: ProtectedKernelCompletionWitnessAuthority |
                       AuthenticatedKernelWitnessEnvelope,
    canonical_witness_digest
}

CompletionPublicationBorrowEpoch {
    completion_publication_ref_and_id,
    completion_slot_and_generation,
    borrow_word: Atomic<(
        Open | Revoking | Drained,
        completion_borrow_generation,
        live_completion_copy_reader_count:
            BoundedBorrowCount<MAX_COMPLETION_BORROWS>
    )>,
    authorized_holder_set_audit_digest
}

CompletionPublicationBorrowToken {
    completion_publication_ref_and_id,
    completion_slot_and_generation,
    completion_borrow_generation,
    holder_identity_and_generation,
    token_id_and_kernel_authority
}
```

Each resource owner uses its protected authority to publish a generation-bound,
one-shot `OwnerCompletionTokenPublication` for only the predicate fragment it
owns. Before the first token byte changes, it validates an immutable
`OwnerCompletionTokenBuildDescriptor` whose authoritative owner-result
publication already binds the exact current targets, predicate fragment,
external-effect resolution, held requirement, and protected owner. The atomic
`Empty → Writing` claim installs that descriptor index/generation and owner tag
with no completion-builder tag. The writer deterministically copies the result,
validates the body against the descriptor, and publishes `Available`.

A cut in token `Writing` never delegates construction to an unrelated
coordinator. Fenced owner recovery validates the immutable result publication
and descriptor and rewrites/seals that same token generation; if the external
effect/result cannot be re-established, the token and requirement remain held
for reconciliation. It is not cleared merely for pool capacity. The token ID
binds the build-descriptor digest and exact held requirement
publication/body/witness, not merely its semantic ID. A coordinator may collect token references but
cannot assert their contents. Before claiming any token, a kernel-owned
constructor/release gate validates a preinitialized immutable
`CompletionBuildDescriptor` that binds the exact held requirement, complete
ordered token set, completion slot/generation, constructor/gate generations,
and target/predicate conjunction. The sole per-requirement CAS from
`Idle → ClaimingTokens` installs that descriptor index/generation and owner;
no competing builder can begin a disjoint token subset.

The gate enumerates the fixed ordered manifest. For each token it validates the
`Available` publication and authority, then CASes exact
`(Available, token_generation, owner_build_tag, None, owner_tag) → (Claimed,
token_generation, owner_build_tag, completion_descriptor_tag, owner_tag)` and
advances its claim frontier. If a cut falls between those
operations, recovery scans the bounded manifest and authoritative token words,
accepts only claims carrying that same tag, and completes the remaining claims;
it never guesses from a partial completion body. After all tokens are claimed,
the gate enters `BuildingCompletion`, claims the exact preallocated completion
slot as `(Writing, completion_generation, descriptor_tag)`, deterministically
fills the conjunction from the immutable token bodies, and release-publishes
`(Sealed, completion_generation, descriptor_tag)`. A cut at `Writing` clears
no control state: fenced recovery reinitializes every fixed body byte from the
same immutable manifest under the still-exclusive gate, recomputes the digest,
and seals that same generation, or retains it if any descriptor/token
validation fails. It cannot redirect claimed tokens to another completion.

Once the matching completion seals, the gate enters `ConsumingTokens`, changes
every exact owner/completion-descriptor-tagged `Claimed` token to `Consumed` in manifest order,
and advances its consume frontier before publishing `Released`. A stale,
already consumed, cross-requirement, wrong-owner, or differently tagged token
cannot participate. The complete gate word and token lifecycle tuple must each
fit a target-supported native atomic operation; otherwise the admitted token
bound is reduced or the requirement uses a fixed independent shard whose full
tuple fits—multiword emulated CAS is not the acceptance gate.

The sealed completion copies the immutable build-descriptor digest into its
self-excluding publication identity, so readers can validate the exact token
manifest/requirement construction without following a later-reused gate slot.
After the `CompletionAcceptanceWitness` has been copied, all tokens are
`Consumed`, and no recovery builder can remain, the protected gate owner may
CAS exact `Released → RearmingTokens`. It retains the descriptor and advances
the same bounded frontier only after each matching token has completed its
exact preparation below. Only when the whole manifest is verified next-
generation `RearmedHeld` may it CAS `RearmingTokens → ReleasingTokens`.
In `ReleasingTokens`, the gate advances its authoritative frontier for token
*i* **before** changing that exact token `RearmedHeld → Empty`. A cut before
the token CAS finds `RearmedHeld` and finishes it; a cut after the CAS may find
descriptor-free `Empty` or a new owner's `Writing`, but the already advanced
frontier proves the old gate must not inspect or modify that slot again. After
the frontier passes the complete manifest, the gate may CAS
`ReleasingTokens → Clearing`, clear/rekey the gate and descriptor extent,
advance their checked generations, and publish
`Idle(next_generation, None, zero_frontier)` last. A cut in
`RearmingTokens|ReleasingTokens|Clearing` resumes from the gate frontier and leaves
the gate unavailable; descriptor mismatch or a nonterminal token retains it.
The publication is accepted only when its self-excluding ID, complete body
digest, exact held-requirement binding, capture/target incarnations, consumed
one-shot token publication IDs/digests, release-gate generation, and
protected/authenticated authority all validate. The gate then returns a fixed `CompletionAcceptanceWitness` for that
exact seal. Requirement reclaim proofs and escalation transitions embed the
complete canonical completion body, source publication ID at copy, and this
witness; neither depends on a later-reused slot or an undefined release-gate
reference. The completion can authorize a new higher-
level transition such as terminating/restarting a domain or retiring memory. It
never goes back in time to authorize the original hard-entry return, for which
no `LocalResumePostcondition` existed.

Owner-token slots are rearmed only after the sealed completion has independent
custody, every consumer has copied the token ID/digest, and the matching
construction gate is `RearmingTokens` with a complete consume frontier and
retained descriptor. The owner or
fenced recovery changes exact owner/completion-descriptor-tagged
`Consumed → Clearing`,
clears/rekeys and verifies the body and authority metadata, advances the
checked token generation, and publishes next
`(RearmedHeld, next_generation, None, None, None)` last, then advances the
gate's token-rearm preparation frontier. `RearmedHeld` is not writer-eligible;
only the later `ReleasingTokens` frontier-first CAS exposes `Empty`. A cut
before either preparation publication resumes from the exact token word and
gate frontier; the gate can never reach `ReleasingTokens` first. `Writing`, `Available`, or `Claimed` has no direct edge to `Empty`; an
incomplete or ambiguous owner publication remains held or is completed by its
one descriptor-bound gate.

The completion-slot pool is fixed at boot. Every copy reader first acquires
exact `(Open, b, n) → (Open, b, n + 1)` in the publication-bound
`CompletionPublicationBorrowEpoch` only when `n < MAX_COMPLETION_BORROWS`;
saturation yields no copy reference. It rechecks publication/slot/borrow
generations before dereference. After every admitted consumer has published its
authenticated copy, the release gate closes admission with `Open → Revoking`,
revokes holders, and requires exact `(Revoking, b, 0) → (Drained, b, 0)`; a
separate count is not proof. It may then move the exact descriptor-tagged
`Sealed → Reclaimable → Clearing`, apply
and verify the fixed clear/rekey recipe, increment a checked-nonwrapping slot
generation, clear the holder audit, initialize exact `(Open, b + 1, 0)` bound to
the next slot occupant, and publish `(Empty, next_generation, None)` last. A cut, live borrow, missing required copy,
or exhausted generation leaves the slot unavailable; exhaustion retires it
until a fresh protected boot identity domain.

## Representative recovery profiles

### Guarded kernel access to user memory

Local resume is possible only when the faulting PC lies in a generated recovery
region, the access guard and exact copy operation match, no privileged state
mutation occurred past the commit boundary, the return envelope is valid, and
the fixup completes locally. An arbitrary kernel page fault near a copy routine
does not qualify.

### Corrected or deferred report

An asynchronous corrected report can be operational if return state is intact
and acknowledgement completes. A deferred/poison record requires identifying
the extent and every possible consumer before use. “Poison not yet consumed”
supports a containment opportunity, not automatic resume after the affected
memory could be reached by CPUs or DMA.

### Consumed user-domain memory error

If the profile gives a valid precise extent and consumption is attributable to
a user domain while kernel/shared state is intact, emit a requirement only if
an immediate hardware/profile fence prevents every possible CPU or DMA
accessor from consuming or propagating the fault. The split-phase work then
parks the domain, closes CPU mappings and translations, revokes DMA/device
reachability, retires the frame, and resolves outstanding external effects.
Unsupported page type, pin, alias, ambiguous ownership, absent initial fence,
or missing completion is terminal in the baseline.

### CPU internal/cache/TLB state error

Any processor-context-corrupt flag, invalid restart state, kernel critical
section, unknown propagation, missing address required by the profile, or
uncorrected overflow is terminal. A future CPU-offline rule must prove that
shared caches/interconnect and external effects are intact and that this CPU's
lifecycle/interrupt/translation participation was completely removed.

### Device/IOMMU/interconnect event

The classifier emits a requirement tied to requester set, device endpoint,
reset domain, mappings, queues, interrupts, and frame epochs. A reset request is
not reset completion; an accepted command with lost completion remains
indeterminate and may require service-level reconciliation.

## Terminal promotion

`TerminalDisposition` consumes a sealed staging reference and attempts exactly
one global first-fatal claim:

```text
TerminalPromotionBody {
    terminal_generation,
    winner_capture,
    winner_rule_id_and_hash,
    disposition_scope,
    loss_and_integrity_flags,
    logical_raw_block_set_digest,
    logical_source_result_and_acknowledgement_set_digest,
    payload_length,
    payload_digest,
    payload: FixedCapacity<{
        raw_set_and_per_source_results_copy,
        entry_snapshot_copy,
        capture_disposition_decision_copy
    }>,
    body_digest
}

TerminalPromotionPublication {
    lifecycle_word: Atomic<(
        Free | Writing | Sealed | Reclaimable | Clearing,
        terminal_generation,
        compact_promotion_operation_descriptor_index_and_generation_or_none,
        compact_promotion_operation_owner_tag_or_none,
        cleanup_frontier:
            None | DependenciesClosing | DependenciesDrained |
            BorrowClosing | BorrowDrained | ReclaimCommitted |
            ClearAuthorized | BodyVerifiedEmpty
    )>,
    promotion_publication_id: Hash(canonical_encoding({
        intended_state: Sealed,
        promotion_owner_and_generation,
        promotion_build_descriptor_digest,
        sealed_promotion_owner_tag,
        body_bounds_and_schema,
        body_digest
    })),
    promotion_owner_and_generation: {
        terminal_generation,
        owner_capture
    },
    promotion_build_descriptor_digest,
    sealed_promotion_owner_tag,
    body_bounds_and_schema,
    body_digest,
    body: TerminalPromotionBody
}

TerminalPromotionBuildDescriptor {
    descriptor_index_and_generation,
    terminal_slot_and_generation,
    owner_capture_and_boot_crash_generation,
    exact_sealed_staging_raw_source_result_snapshot_and_decision_inputs,
    fixed_payload_bounds_schema_and_copy_plan,
    preallocated_cleanup_descriptor_slot_generation_and_variant_seeds,
    protected_terminal_promotion_owner_and_generation,
    canonical_descriptor_digest
}

TerminalPromotionCleanupDescriptor {
    lifecycle_word: Atomic<(
        Empty | Writing | Prepared | Installed | Clearing,
        cleanup_descriptor_slot_and_generation,
        cleanup_variant_seed_and_generation_or_none,
        compact_cleanup_builder_owner_tag_or_none,
        terminal_slot_and_generation_or_none
    )>,
    cleanup_descriptor_publication_id: Hash(canonical_encoding({
        intended_state: Prepared,
        cleanup_descriptor_slot_and_generation,
        cleanup_variant_seed_and_generation,
        terminal_slot_old_and_next_generation_and_owner_capture,
        canonical_descriptor_digest
    })),
    cleanup_variant:
      IncompleteWriting {
          complete_terminal_promotion_writing_receipt_ref_and_id,
          matching_current_crash_reclaim_ref_and_id,
          no_sealed_context_or_accepted_dependency_proof
      }
    | AcceptedSealed {
          terminal_promotion_custody_receipt_ref_and_id,
          replacement_independent_custody_graph_ref_and_id,
          matching_generation_current_crash_reclaim_ref_and_id
      },
    terminal_slot_old_and_next_generation_and_owner_capture,
    exact_dependency_borrow_close_drain_clear_rekey_and_verification_plan,
    protected_cleanup_owner_identity_and_generation,
    canonical_descriptor_digest
}

TerminalPromotionWritingCleanupPredicate {
    terminal_slot_generation_descriptor_owner_and_capture_observed_writing,
    exact_old_writer_and_cpu_context_fence_evidence,
    no_sealed_promotion_normal_crash_context_or_accepted_dependency,
    complete_terminal_promotion_writing_receipt_ref_and_id,
    matching_current_crash_reclaim_ref_and_id,
    exact_borrow_and_dependency_words_observed_drained,
    prevalidated_incomplete_writing_cleanup_descriptor_and_owner,
    protected_cleanup_authority_and_generation
}

TerminalPromotionCleanupResumePredicate {
    original_terminal_slot_generation_cleanup_descriptor_owner_and_capture,
    cleanup_descriptor_observed_state:
        Prepared | Installed | Clearing | EmptyNextGeneration,
    cleanup_variant:
      IncompleteWriting {
          original_complete_writing_receipt_and_current_or_consumed_reclaim
      }
    | AcceptedSealed {
          original_promotion_receipt_replacement_graph_and_current_or_consumed_reclaim
      },
    observed_state: Reclaimable | Clearing | FreeNextGeneration,
    exact_borrow_dependency_old_and_next_generations_and_cleanup_frontier,
    source_reclaim_committed_descriptor_prepared_to_installed_resume_step,
    protected_cleanup_authority_and_generation
}

TerminalPromotionBorrowEpoch {
    promotion_publication_ref_and_id,
    borrow_word: Atomic<(
        Open | Revoking | Drained,
        terminal_generation,
        live_sink_decoder_and_forensic_reader_count:
            BoundedBorrowCount<MAX_PROMOTION_BORROWS>
    )>,
    holder_set_audit_digest
}

TerminalCollisionSummary {
    terminal_generation,
    additional_fatal_saturating_count,
    first_and_last_losing_cpu_sequence_when_available
}
```

For `TerminalPromotionCleanupDescriptor`, `canonical_descriptor_digest` hashes
only the immutable variant seed/body, terminal slot/owner old-and-next
identity, receipt/reclaim or replacement-custody authority, dependency/borrow
teardown plan, and protected cleanup owner. It omits the mutable lifecycle
word, `cleanup_descriptor_publication_id`, and the digest field itself. The
outer publication ID is computed afterward from intended `Prepared` and that
digest, so later lifecycle changes cannot create a cycle or alter identity.

The claimant first validates an immutable `TerminalPromotionBuildDescriptor`
that binds the exact owner capture, sealed inputs, payload plan, slot, and
protected authority. Successful exact CAS
`(Free, terminal_generation, None, None, None) → (Writing, terminal_generation,
descriptor, owner, None)` is the ownership linearization point and precedes every
payload byte. The claimant copies the already sealed raw set, per-source results,
entry snapshot, and classification into the fixed-capacity payload, binds
length and canonical payload digest into a self-excluding body digest, then
release-publishes `Sealed`; only that publication creates
`first_promoted_fatal`. It never releases the staging slot before publication.
A trapping copy leaves the shared slot `Writing`, so no promoted fatal exists;
a sealed
recursive record identifies the incomplete outer phase, because the interrupted
writer is not assumed able to return and publish `Torn`. A non-trapping copy
error also leaves publication `Writing`, may update only a distinct bounded
failure summary, and enters the nonwriting terminal fallback directly. It does
not mint recursive evidence or `RecursiveCrashContext`; only an actual nested
entry carrying component 2's `FatalPreclassificationProof` may do that.

`Writing` is not silently rolled back and need not consume the global slot
forever. After the machine reaches independent recovery, only
`TerminalPromotionWritingCleanupPredicate` lets a fenced-writer path change
exact `(Writing, terminal_generation, descriptor, owner, None) →
(Reclaimable, terminal_generation, incomplete_cleanup_descriptor,
cleanup_owner, ReclaimCommitted)` only when an authenticated complete fixed-extent
`IncompleteCrashAttempt(TerminalPromotionWriting)` custody receipt covers every
payload/control byte, a generation-current `CrashReclaim` targets that exact
manifest, no `Sealed` promotion or normal `CrashContext` was created, the
promotion dependency set proves no reservation or accepted bit, and its borrow
epoch is closed and drained. Exact tagged `Reclaimable → Clearing` precedes
any mutation. Before that source CAS, the owner uses the build descriptor's
reserved cleanup slot/seed to publish a descriptor-tagged
`TerminalPromotionCleanupDescriptor::IncompleteWriting` through `Empty →
Writing → Prepared`; it binds the receipt/reclaim and no-acceptance proof, and
the source CAS atomically replaces the old build tags with this cleanup
authority. It then CASes descriptor exact `Prepared → Installed`; a cut after
the source CAS with descriptor still `Prepared` is an explicit resume case and
can perform only that transition. The same verified full clear/rekey,
checked-generation advance, next borrow/dependency initialization, and
`(Free, next_generation, None, None, None)` protocol then applies while the
cleanup descriptor remains nonempty. The terminal allocator rejects that
apparently free slot until descriptor `Installed → Clearing → Empty(next)`
publishes last. A malformed extent,
ambiguous writer/context, missing receipt/reclaim, or any graph/borrow retires
the slot; a nontrapping copy error alone is never cleanup authority.
Any cut after the reclaim CAS uses `TerminalPromotionCleanupResumePredicate`,
the original receipt/reclaim state and exact old/next generations to resume
`Reclaimable|Clearing|Free(next)` without rerunning first-fatal arbitration or
issuing a second reclaim.

A loser does not touch the shared payload. It retains its sealed CPU-local raw
staging record for crash-capsule discovery and, when one safe atomic store is
available, updates the separately owned best-effort
`TerminalCollisionSummary`. That summary is outside the sealed/digested
promotion record and cannot affect the winner's immutability or validity.
If the claim observes `Sealed`, the loser enters a finite nonwriting CPU-local
halt/park leaf. If it observes `Writing`, an invalid state, or a
coherence/access failure, it does not wait and enters the same leaf with its
staging retained. The loser cannot mint `CrashContext`, write the normal
capsule, or request reset before the winner's mandatory section-zero commit;
an external preprovisioned watchdog is the bounded fallback for a stuck winner.
Merely losing the claim does not require recursive capture because no nested
entry occurred.

A sink, decoder, or forensic reader first acquires exact promotion borrow
`(Open, g, n) → (Open, g, n + 1)` only when
`n < MAX_PROMOTION_BORROWS`; saturation yields no token. It then rechecks both the promotion lifecycle
and borrow word before any dereference; a mismatch releases without reading.
While that borrow is held, it acquire-loads and accepts only a `Sealed` publication whose
`promotion_publication_id` recomputes over intended `Sealed`, terminal
owner/generation, canonical body bounds/schema, and body digest; whose owner
capture and terminal generation match the body; and whose body/payload lengths,
digests, and embedded source/decision manifests validate. A `Sealed` slot
remains immutable for the boot/crash generation and identifies
the first successfully promoted software observation, not necessarily the first
physical fault or even the earliest CPU-local capture. A `Writing` slot instead
identifies only the first claimant; the recursive record explains the failed
publication. If cross-CPU coherence is suspect, each CPU's sealed raw staging
record remains independently discoverable and the global ordering is labeled
uncertain; this baseline does not silently invent another class of per-CPU
terminal-promotion slots.

The sealed global promotion slot is bounded rather than retained forever. It may move
from exact `(Sealed, g, descriptor, owner, None)` to
`(Reclaimable, g, accepted_sealed_cleanup_descriptor, cleanup_owner,
ReclaimCommitted)` only after the crash sink has
sealed an authenticated complete `TerminalPromotion` custody receipt, the
destination capsule publication owns every promoted byte, and a replacement
fault-record publication graph over the same semantic core has sealed with
`IndependentCustodyRoot` naming that receipt and destination. It must also
consume a separately authorized, generation-current `CrashReclaim` decision
whose source identity is this exact promotion publication/terminal generation;
custody acceptance or retention policy alone is insufficient. That gate closes
the promotion's bounded graph-dependency set, enumerates every initial and
decoded-version graph/binding rooted in it, and requires each to be completely
rehomed under independent custody or authoritatively revoked with its borrows
drained. One replacement graph is insufficient. Only dependency-set
`Closing → Drained` closes new promotion graph admission. The exclusive holder compare/exchanges exact
`(Open, g, n)` to `(Revoking, g, n)`, revokes sink/decoder/forensic handles,
drains to exact `(Drained, g, 0)`. Before the original source CAS, it uses the
build descriptor's reserved slot/seed to publish
`TerminalPromotionCleanupDescriptor::AcceptedSealed` through descriptor-tagged
`Empty → Writing → Prepared`, binding the promotion receipt, independent-
custody replacement graph, current reclaim, generations, and clear plan; the
source CAS atomically installs that variant. It then compare/exchanges the
cleanup descriptor exact `Prepared → Installed`; a cut with source
`Reclaimable` and descriptor `Prepared` completes only that CAS. It then compare/exchanges the
promotion lifecycle from exact `(Reclaimable, g,
accepted_sealed_cleanup_descriptor, cleanup_owner, frontier)` to `(Clearing,
g, same_descriptor, same_owner, ClearAuthorized)` before mutating any protected byte. It
clears/rekeys and verifies body, authority/owner metadata,
collision-summary association, and borrow metadata; initializes the next
borrow epoch; increments the terminal generation with checked nonwrapping
arithmetic; and release-publishes `(Free, g + 1, None, None, None)` while the
cleanup descriptor still blocks reuse, then clears/verifies and publishes the
descriptor next-`Empty` last. `TerminalPromotionCleanupResumePredicate` carries
the exact accepted or incomplete variant and atomic frontier through every
cut. A cut, missing receipt
or replacement graph, live borrow, failed clear, or exhausted generation
leaves the slot unavailable until a fresh protected boot/crash identity domain.

Only the winning capture, and only after its `Sealed` publication, can terminal
control mint the one-shot normal `CrashContext`. A separately sealed recursive record can mint only the
restricted `RecursiveCrashContext`, which lets the sink commit that record and
an explicitly suspect outer prefix; it cannot certify the incomplete promotion
or invoke rich adapters.

## Deadlines, liveness, and fallback

Deadline expiry yields:

```text
ContainmentProgress {
    held_requirement_binding: HeldRequirementBinding,
    acknowledged,
    completed,
    missing,
    failed,
    suspected,
    retained_quarantine_owner
}
```

It does not remove a target or prove it stopped. A separately authorized policy
may retry, fence a stale coordinator generation, widen the quarantine, reset a
subsystem, or promote the machine to terminal. Safety holds without fairness:
no affected resource is reused. Eventual nonterminal completion additionally
assumes progress by every live coordinator and target, and those assumptions
belong in the model.

## Security and adversarial behavior

- Evidence values and object identifiers do not confer control authority.
- Classifier profiles and rule hashes are boot-measured and immutable during a
  decision; downgrade or unsigned replacement is rejected.
- Atom-initiated fault injection requires a separate test capability, is
  disabled or tightly scoped in production, and binds authenticated out-of-band
  injection-session provenance to the capture. Hardware/firmware interfaces
  such as RERI need not retain a normative injected bit, so an event lacking
  that Atom provenance is `injection_origin = Unknown`, not falsely marked.
- Unprivileged workloads can induce corrected-event storms or repeated guarded
  faults; quotas may coalesce reporting but cannot erase quarantine or terminal
  obligations.
- Redacted operational views omit raw addresses and payload while keeping the
  decision rule, scope class, loss, and progress auditable.
- A compromised recovery service cannot mint local-return authority. It also
  cannot release quarantine because owner completion tokens are unforgeable and
  generation-bound, and only the kernel-owned release gate can validate and
  consume their complete conjunction.

## Verification and falsification

### Rule compiler

Enumerate every finite source-validity, capture-availability, structural,
agreement, evidence-loss, producer-trust, hardware-correction, poison,
precision, context-integrity, epistemic-scope, enforced-scope, entry, and
action-result state for each profile.
Prove totality, bounded evaluation, overlap dominance, unknown default, and
monotonicity under loss/uncertainty. Produce human-readable decision tables and
test vectors from the same source.

### Product-state model

Model sealed raw/profile input, capture-time decision, local action, park,
requirement publication, later decoded policy views, escalation, each component
completion, timeout, coordinator restart, terminal promotion, and sink handoff.
Check that no decoded view changes the original decision, no resume occurs
without a current local token, no quarantine releases early, no requirement
masquerades as completion, and at most one shared terminal payload becomes
immutable while every incomplete writer remains visibly incomplete.

For every reserved requirement slot, enumerate exact generation-tagged
accepted and rejected paths: `Free → Writing → Sealed → Held → Reclaimable →
Clearing → Free(next generation)` and `Sealed → Abandoned →
Reclaimable → Clearing → Free(next generation)`, plus direct incomplete
`Writing|Sealed → Reclaimable` only under the closed never-held cleanup
predicate. Reject every other edge. Model a cut before and
after each field write, digest/publication write, release publication,
`Sealed → Held` acceptance, staging-release CAS, reclaim-proof validation,
borrow increment/recheck/decrement, revocation, clear/rekey verification, and
next-generation publication. Assert that:

- staging leaves `HeldForContainment` only through one winning same-word CAS to
  `ContainmentCommitting` or `HeldForTerminal`; `ContainmentAccepted` is
  reachable only after the custodian owns exact requirement `(Held, g)`, while
  `ContainmentCommitting → HeldForTerminal` requires exact requirement
  `Abandoned` and can never race a held witness;
- a candidate containment decision/core is unusable before `Held`; inject
  bounded nontrapping failures and execution/nested-fault cuts after each
  candidate body/digest, outer `Sealed`, and the `Held` CAS; prove that a
  nontrapping path may accept only held-root materialization or one distinct
  direct terminal fallback before `Held`; an interrupted path before `Held`
  accepts no outer disposition, while a cut after `Held` preserves the one
  accepted containment obligation and adds only the distinct recursive
  terminal event;
- no partial, mixed-generation, mixed-capture, or substituted raw set,
  per-source acknowledgement, entry snapshot, requirement, decision, or core
  passes either the nested digests or the enclosing publication ID;
- `Held → Reclaimable` requires matching independent custody plus exact
  completion or durable obligation transfer, with all external effects
  resolved;
- `Writing|Sealed|Abandoned → Reclaimable` requires the complete fixed-extent
  attempt receipt, current reclaim authority, fenced owner, no held tuple or
  witness, no accepted dependency/action authority, and zero/drained borrows;
- no new borrower becomes valid after reclamation linearizes, and `Clearing`
  is unreachable while an exact-generation borrow survives;
- a stale acceptance/reclaim/rearm capability cannot affect a later occupant;
  and
- a cut or verification failure during clear/rekey leaves the slot unavailable,
  while successful rearm exposes only cleared/rekeyed bytes at `(Free, g + 1)`.

Race the containment custodian and terminal fallback before and after every
source-gate and requirement CAS, then restart recovery at each cut. Exactly one
of held containment or direct terminal disposition may become accepted. Also
interrupt the per-requirement `CompletionConstructionGate` before and after
each token claim/frontier update, completion-slot `Writing`/`Sealed`, token
consume, and gate release. Every claimed token must carry the one winning build
descriptor and reach that descriptor's completion or remain held; two builders
may never own disjoint subsets.

For every nonterminal product, separately enumerate the preaccept hold's
`PlanWriting → Prepared → Acquiring → Complete` and transfer/release states,
interrupt both sides of each published operation frontier and source holder-bit
CAS, and assert that the fixed bitmap reconstructs the exact installed set.
For local return, inject at every `ReturnArmed` publication, hold-transfer,
architecture-return, return-leaf reentry, next-protected-entry proof, and
release frontier; a successful return cannot release early and an ambiguous
return cannot reuse the context. For containment park, inject before and after
`ParkHandoff` `Sealed → Parked`, destination-hold acquisition, source-hold
transfer/release, and entry-depth reset. Assert that depth resets only after
the source hold is `Released`, while the destination hold remains owned by the
parked custodian.

Enumerate each closed parked-release proof variant. In the resume arm, cut
after the resume record is `Prepared`, after proof `Consumed`, after the hold
is `Released`, after handoff `Reclaimable`, and around `Prepared → Available`;
the proof/handoff/hold must remain generation-held until availability wins.
Cross-substitute terminal-promotion versus recursive-record destinations,
handoff generations, holder bitmaps, proof authorities, and prepared resume
records and require complete publication-ID validation to reject them.

Also substitute terminal bodies, owners, bounds, and generations independently
and require `promotion_publication_id` validation to reject every mix-and-match
combination before a sink can accept custody.

### Injection and oracles

Combine raw-record enumeration with realistic multi-bit/recurring memory
patterns, faults during every local action, stuck pins, TLB/DMA/IRQ completion
loss, full escalation queues, stale generations, conflicting firmware/CPU
records, and nested terminal promotion. Include stale requirement-slot
acceptors, mismatched custody/completion receipts, partial source manifests,
borrowers paused on both sides of their post-increment recheck, revocation
failure, generation exhaustion, and interruption at every clear/rekey boundary.
Run the controller and correctness
oracles outside the faulted domain. Score silent corruption and wrong-scope
continuation, not only reboot rate.

### Metrics

Track rule coverage and default-rule rate; distribution of scope/disposition;
local-action maximum latency; park duration; incomplete containment count;
quarantined bytes/CPUs/devices; false-narrowing incidents; terminal collisions;
and post-recovery invariant, data-integrity, and duplicate-external-effect
failures.

## Staged implementation

1. Generate a total all-terminal classifier for the fake backend.
2. Add terminal promotion and prove its publication/loss invariants.
3. Add guarded-user-copy local recovery as the only synchronous resume rule.
4. Add asynchronous corrected reporting with explicit non-disruption premises.
5. Add one memory-extent containment profile after VM/TLB/DMA/domain completion
   proofs exist.
6. Add CPU/device cases only after their lifecycle protocols produce exact
   terminal exclusion and indeterminate-effect results.

## Alternatives rejected

- **Trust producer severity.** CPER “recoverable,” Arm UER, RISC-V containable,
  and x86 recovery classes still require software/object postconditions.
- **Put the classifier in the entry stub.** Profile/errata decision logic and
  cross-object scope exceed the irreducible capture boundary.
- **Resume and quarantine later.** Consumed corrupt state can escape before
  split-phase containment completes.
- **Timeout and assume the CPU/device is dead.** Missing progress is not
  terminal exclusion.
- **Restart the smallest named component.** The reporting component may be a
  symptom, while shared state or external effects cross that boundary.

## Unresolved questions

- Which target-specific event, beyond guarded user access, should be the first
  nonterminal hardware rule?
- What exact postcondition proves a poison extent unreachable by every CPU,
  page-table alias, IOMMU, device queue/cache, and persistent writer?
- How should incomparable CPU, memory, and device scopes be represented in the
  public policy event without leaking sensitive topology?
- Which external effects can expose idempotent/fenced recovery, and which must
  remain permanently indeterminate?
- What evidence permits CPU-local continuation after a shared-cache or
  interconnect report?

## Connections

- [Architecture faults and diagnostics](../architecture-faults-and-diagnostics.md)
- [Fault decoder](fault-decoder.md)
- [Escalation channel](escalation-channel.md)
- [Crash-safe sink](crash-safe-sink.md)
- [Address translation and protection transitions](../address-translation-and-protection-transitions.md)
- [Protected I/O and DMA ownership](../protected-io-and-dma-ownership.md)
- [Fault capture and containment](../../minimal-privileged-kernel-components/fault-capture-and-containment.md)
