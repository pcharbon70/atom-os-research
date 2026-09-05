---
title: "Bounded architecture-fault capture routine"
kind: note
created: "2026-09-05"
maturity: developing
tags:
  - architecture-support
  - diagnostics
  - exception-entry
  - fault-containment
  - ras
aliases:
  - "Bounded raw-fault capture"
---

# Bounded architecture-fault capture routine

The bounded capture routine should be a generated, profile-specific program
whose only success claim is that it copied the permitted raw evidence into an
independently reserved CPU-local slot and release-published that raw subrecord
before any separate destructive acknowledgement. An explicitly admitted
observation-is-acknowledgement source such as clear-on-read MMIO cannot make
that pre-ack claim and records the exception. The routine then executes a
separately bounded acknowledgement program and publishes per-source
acknowledgement results. It must not run
the rich decoder, format text, allocate, wait for another CPU, invoke an
ordinary logger, choose recovery policy, or claim persistence.

“Bounded” must mean fixed source count, fixed register/byte count, fixed retry
count, and statically bounded stack and call graph. A cycle/latency ceiling may
be claimed only when every primitive access has an architectural or measured
platform response bound; one fixed-count MMIO operation can still wedge behind
a failed bus. Otherwise the truthful guarantee is bounded issued software work
plus an independent watchdog/terminal path, not bounded return latency. Merely
calling the path lock-free or nonblocking is insufficient.

This is proposed Atom architecture. No implementation or worst-case bound has
yet been demonstrated.

## Question, scope, and operational standard

The question is:

> How can the first software-visible evidence be retained when fault entry can
> interrupt any kernel state, the source may be destructive to acknowledge,
> and the handler itself can fail?

The routine owns:

- a CPU-local `RawStagingSlot` and its one-way publication protocol;
- source-register access order, validity-dependent reads, bounded retry, and
  exact acknowledgement program selected from a sealed boot profile;
- capture-time loss, overwrite, truncation, and structural-integrity metadata;
- the handoff from an architecture-entry frame to sealed raw evidence; and
- a minimal `CaptureOutcome` which permits only the generated capture-time
  disposition classifier or terminal fallback.

Component 1 owns irreducible assembly/register leaves. Component 2 owns vector
configuration, emergency stacks, raw frame construction, nesting depth, and
the typed entry context. A tiny generated `CaptureDispositionClassifier` owns
the entry-time return/park/terminal decision from sealed raw facts, fixed
profile predicates, and acknowledgement state. The richer fault decoder runs
later in the policy plane; the sink owns post-seal custody.

A candidate passes only if:

1. entry state that hardware could overwrite is saved before calling the
   routine;
2. the routine accepts only `HardEntryContext`, `NmiContext`, or the separate
   terminal path's `FatalCaptureContext`;
3. source access is generated from a signed/pinned profile and never discovered
   by unbounded enumeration during the fault;
4. every admitted raw subrecord is release-published before the profile's
   destructive clear or acknowledgement; the only exception is an explicitly
   profiled clear-on-read source whose observation is itself acknowledgement and
   therefore cannot support narrow recovery; a source-specific coherent-read
   retry uses another preallocated immutable attempt slot rather than rewriting
   the first observation;
5. a reader cannot accept `Writing`, malformed, wrong-generation, or integrity-
   failing data as sealed, and the integrity envelope binds parser/policy-
   critical metadata as well as payload bytes;
6. operational-ring exhaustion cannot prevent terminal promotion;
7. every retry and poll has a hard local count limit and produces explicit loss
   or uncertainty when exhausted, while every access without a response-latency
   bound is excluded from a bounded-return profile;
8. no branch requires another CPU, firmware, scheduler, allocator, filesystem,
   general driver, or unbounded device response;
9. nested entry at every instrumented instruction either uses the independent
   recursive path or reaches the finite halt/reset leaf; and
10. every shared hardware source has an exclusive reader/route generation or a
    non-destructive conservative fallback; `rdip`, W1C, and validity bits are
    not treated as locks between competing software handlers.

## Evidence and limits

| Evidence | Supported conclusion | Limit |
| --- | --- | --- |
| [Intel system-programming documentation](../../../30-sources/intel-2026-system-programming-documentation.md) | x86 MCA validity, overflow, processor-context-corrupt, restart-IP, and address/misc fields are independent; status/address/misc must be saved before clearing | Bank meaning and recovery rules remain model/vendor/erratum specific |
| [Machine-check handling on Linux](../../../30-sources/kleen-2004-machine-check-handling-linux.md) | Machine checks can interrupt locked/disabled-interrupt regions; fixed raw collection and deferred decoding reduce dependencies | Historical Linux implementation, not a current proof |
| [Arm RAS specification](../../../30-sources/arm-2019-ras-specification.md) | Arm record access has explicit validity, ordering, overwrite, and write-one-to-clear rules | Node inventory and extended syndrome are platform-specific |
| [RISC-V privileged architecture](../../../30-sources/risc-v-international-2026-privileged-architecture.md) | Early trap state is vulnerable to nested overwrite; scratch state and optional double-trap/RNMI facilities must be profile-pinned | Platform critical-error behavior is external |
| [RISC-V RERI](../../../30-sources/risc-v-international-2024-ras-error-record-interface.md) | Version/layout-first decoding and `rdip`/invalidate/recheck can expose overwrite during a multi-register read | RERI is optional and an unbounded reread would violate this service's contract |
| [Linux entry/exit handling](../../../30-sources/linux-kernel-community-2026-entry-exit-handling.md) | NMI-like early entry must exclude instrumentation and helpers whose context is not established | Linux discipline is precedent, not an ISA rule |
| [Linux lockless ring-buffer design](../../../30-sources/rostedt-2009-lockless-ring-buffer-design.md) | Reserve/commit and nested same-CPU writer ordering are useful publication patterns | A tracing ring is not corruption tolerant or first-fatal preserving |
| [Linux crash-dump evaluation](../../../30-sources/vazquez-cao-2006-evaluating-linux-crash-dumping.md) | Stack, CPU identity, recursive fault, interrupt state, DMA, load, and device state must be varied in tests | Results are Linux 2.6-era and x86-focused |

The evidence supports strict context, preallocation, source-order, and
publication requirements. The exact object schema and generated program below
are Atom synthesis.

## Capture profile and generated program

Boot creates a sealed profile only after feature discovery and platform
validation:

```text
CaptureProfile {
    profile_id,
    profile_hash,
    isa_and_privilege_profile,
    cpu_vendor_family_model_stepping,
    microcode_firmware_virtualization_versions,
    errata_set_hash,
    source_programs: BoundedArray<CaptureProgram, MAX_SOURCES>,
    cross_source_alias_and_ack_effect_matrix_hash,
    validated_capture_ack_schedule,
    maximum_raw_bytes,
    maximum_stack_bytes,
    maximum_instructions,
    permitted_entry_contexts,
    terminal_fallback_leaf
}

CaptureProgram {
    source_id,
    source_owner_and_generation,
    signal_route_generation,
    software_reader_contract: CpuLocal | ExclusiveOwner | ReadOnlyShared,
    destructive_acknowledgement_authority,
    access_kind: Csr | Msr | SystemRegister | DeviceMmio | FirmwareBuffer,
    raw_attempt_programs: BoundedArray<CaptureAttemptProgram, MAX_ATTEMPTS>,
    acknowledgement_operations: BoundedArray<AcknowledgeOp, MAX_ACK_OPS>,
    acknowledgement_may_affect_source_ids,
    shared_aggregator_and_deassertion_effects,
    retry_decision_table,
    retry_budget,
    response_bound_basis,
    maximum_response_cycles,
    acknowledgement_effect,
    ordering_recipe,
    required_mapping_attributes,
    output_layout_id,
    failure_fallback
}

CaptureAttemptProgram {
    attempt_index,
    fixed_operations: BoundedArray<PrimitiveOp, MAX_CAPTURE_OPS>,
    reserved_output_slot,
    seal_recipe
}

PrimitiveOp =
    ReadAlways(register, destination)
  | ReadIf(raw_predicate, register, destination)
  | CopyFixed(source, length, destination)
  | Barrier(kind)
  | ReriSetReadInProgress(record)

AcknowledgeOp =
    Barrier(kind)
  | ClearExact(register, value_derived_from_captured_bits)
  | ReadBack(register, destination)
  | ReriInvalidateSelectedRecord
  | ReriRecheckValidityAndReadInProgress
  | ContinueWithReservedAttemptIf(result, attempt_index)
  | SealLoss(flag)
```

The program is validated while the machine is healthy. Fault-time execution
contains no parser, indirect plugin discovery, allocation, or variable-length
loop. An unrecognized source or profile mismatch produces a minimal
`UnknownSource` capture and terminal/conservative disposition; it never runs a
nearby-looking recipe.

Representative programs are materially different:

| Profile | Minimum safe pattern | Mandatory uncertainty |
| --- | --- | --- |
| x86 MCA | read `MCG_STATUS`; for each fixed, locally owned bank read `MCi_STATUS` and conditionally address/misc; seal; acknowledge only profile-owned bank status as permitted and serialize; retain `MCG_STATUS.MCIP` until a validated #MC return leaf commits | `OVER`, invalid `ADDRV/MISCV`, corrupt processor context, broadcast/shared-bank ownership, and model-specific codes; shared/broadcast banks are not cleared unless the profile proves ownership/serialization; bank acknowledgement is not MCIP return commit |
| Arm RAS | read selected status, then only validity-authorized address/misc fields; seal; apply profile ordering; write the exact captured W1C mask and perform the required bounded status readback | overflow, unknown fields, implementation-defined syndrome/priority, SError precision, firmware mediation, and a new record concurrent with clear/readback |
| RISC-V RERI | select the fixed record; read version/layout and the initial status (including `v`/`rdip`) as-is; if valid, read the remaining fields into attempt 0, seal attempt 0, write `sinv`, then recheck `v` and `rdip`; only after observing the overwrite case does one reserved retry set read-in-progress before reading attempt 1 | aligned 4-byte accesses are single-copy atomic while 8-byte single-copy atomicity is unspecified; initial and rechecked `v`/`rdip`, optional fields, timestamp, custom code, and platform signal route remain explicit |
| Clear-on-read MMIO | admit only a profile-proved response-bounded access; perform exactly one destructive read directly into the raw attempt and mark observation-as-acknowledgement | the source cannot offer a pre-acknowledgement software publication; later reread is not equivalent evidence, so this exception is explicit in the record and cannot authorize narrow recovery |

The common layer exposes effects, not register names. A profile is invalid if
its requested mapping attributes, access width, barrier, or acknowledgement
cannot be represented on that target. `DeviceMmio` and firmware-buffer access
are rejected from a bounded-return profile unless the target contract supplies
a defensible response bound; an independent watchdog may make the overall path
finite but does not turn a wedged access into a completed capture.

For RERI v1.0, attempt 0 first preserves the hardware-provided `rdip` value;
it must not write `srdp` before that read because doing so would erase evidence
that a valid record had already been overwritten. If its initial `v` is zero,
there is no valid record to acknowledge and the source result is
`Completed/NoValidRecordObserved`; that conservative result never authorizes an
asynchronous return. For an initially valid record, the
post-`sinv` result table is exact:

| Rechecked state | Meaning for the sealed attempt | Bounded action |
| --- | --- | --- |
| `v = 0` | The selected record was read and invalidated without a replacement remaining valid | Accept the sealed attempt; no retry |
| `v = 1, rdip = 1` | A new record arrived after invalidation; the prior sealed attempt was coherent | Accept the prior attempt and record `new_record_after_invalidation`; do not mislabel it as overwritten |
| `v = 1, rdip = 0` | A valid record may have overwritten the selected record during collection | Record overwrite; if the fixed retry budget is one, set read-in-progress again and append into reserved attempt 1, otherwise stop with explicit loss |

The profile validator forbids `ReriSetReadInProgress` in attempt 0. A reserved
retry is reachable only after the sealed first attempt and a recheck of
`v = 1, rdip = 0`; that retry begins by setting `rdip` through `srdp` before
reading the record again. Attempt 1 then runs the same finite closure: copy the
remaining fields, seal attempt 1, write `sinv`, and recheck `v`/`rdip`. A final
`v = 0` accepts attempt 1 as coherent; `v = 1, rdip = 1` accepts it and records
`new_record_after_invalidation`; and `v = 1, rdip = 0` records
`retry_exhausted_overwrite` and explicit evidence loss. No third attempt is
made. Thus a replacement during the retry is observed rather than presenting
attempt 1 as silently coherent. No branch overwrites attempt 0 or loops until
quiet.

For x86 `#MC`, the profile distinguishes per-bank acknowledgement from the
global in-handler state. Clearing an owned `MCi_STATUS` after its raw attempt is
sealed does not clear `MCG_STATUS.MCIP`. MCIP remains set through capture and
classification; only component 2's generation-matched committed return leaf
may clear it immediately before the architectural return. Terminal paths never
report MCIP acknowledged merely because bank status was cleared.

For an Arm W1C record, write retirement is not proof that the record is clear.
The fixed acknowledgement program reads status back and publishes one of
`WriteIssued`, `ObservedCleared`, `ValidRecordStillPending`, or `Indeterminate`.
`ObservedCleared` requires a valid readback with `V=0`; a valid post-clear
record yields `ValidRecordStillPending` and is preserved. Without an additional
target-specific identity/version contract, that state means either that the
conditional clear was not accepted and the prior record remains or that a
concurrent replacement/update is visible; Atom does not label it a new record.
Only `ObservedCleared` can satisfy the acknowledgement premise of an
`AsynchronousNonDisruptive` return rule.

## CPU-local object and publication protocol

```text
FaultCaptureIncarnation =
    (boot_crash_generation,
     cpu_identity,
     cpu_incarnation,
     capture_sequence: BoundedSequence<MAX_CAPTURE_SEQUENCE>)

RawAttempt {
    state: Empty | Writing | Sealed,
    attempt_index,
    payload_length,
    capture_completion_bitmap,
    capture_loss_flags,
    sealed_attempt_digest,
    bytes: [byte; MAX_RAW_BYTES_PER_ATTEMPT]
}

SourceCaptureResult {
    source_state: Empty | WritingAttempt | AttemptsOpen | SourceComplete,
    source_id,
    source_owner_and_generation,
    signal_route_generation,
    program_id_and_hash,
    profile_id_and_hash,
    ordered_attempt_digest_manifest,
    source_attempt_set_digest,
    attempts: BoundedArray<RawAttempt, MAX_ATTEMPTS_PER_SOURCE>,
    acknowledgement_state: NotStarted | InProgress | Completed | Failed,
    acknowledgement_result: {
        capture: FaultCaptureIncarnation,
        capture_set_identity_digest,
        source_id,
        source_owner_and_generation,
        signal_route_generation,
        program_id_and_hash,
        profile_id_and_hash,
        source_attempt_set_digest,
        attempt_acknowledgement_manifest,
        completion_bitmap,
        first_unfinished_operation,
        source_postcondition: NotRequiredByProfile | WriteIssued |
                              ObservedCleared | ValidRecordStillPending |
                              NoValidRecordObserved |
                              ObservationWasAcknowledgement | Indeterminate,
        overwrite_and_loss_flags,
        acknowledgement_digest
    },
    source_result_digest
}

SourceResultAndAcknowledgementSetBody {
    capture: FaultCaptureIncarnation,
    capture_set_identity_digest,
    source_result_count,
    set_schema_and_bounds,
    ordered_source_result_digest_manifest,
    source_results: BoundedArray<SourceCaptureResult, MAX_SOURCES>
}

SourceResultAndAcknowledgementSetPublication {
    state: Empty | Writing | Sealed,
    storage_owner_and_generation,
    publication_id: Hash(canonical_encoding({
        intended_state: Sealed,
        storage_owner_and_generation,
        capture,
        set_schema_and_bounds,
        logical_source_result_and_acknowledgement_set_digest
    })),
    logical_source_result_and_acknowledgement_set_digest,
    body: SourceResultAndAcknowledgementSetBody
}

RawStagingOwnerDescriptor {
    descriptor_index_and_generation,
    cpu_identity_and_incarnation,
    capture: FaultCaptureIncarnation,
    staging_slot_and_generation,
    boot_crash_generation,
    protected_component_9_writer_authority_and_generation,
    canonical_descriptor_digest
}

RawStagingSlot {
    lifecycle_word: Atomic<(
        Free | WritingRaw | AttemptsOpen | RawSetSealed |
        CopyingOperational | HeldForContainment | ContainmentCommitting |
        ContainmentAccepted | HeldForTerminal | Reclaimable | Clearing,
        slot_generation,
        compact_cpu_owner_tag_or_none
    )>,
    owner: Option<FaultCaptureIncarnation>,
    header: {
        capture: FaultCaptureIncarnation,
        slot_generation,
        raw_staging_owner_descriptor_digest,
        schema_version,
        profile_id,
        profile_hash,
        capture_set_identity_digest,
        entry_class,
        nesting_depth,
        raw_frame_layout,
        payload_length,
        capture_flags,
        source_result_count,
        source_result_and_acknowledgement_set_publication_id,
        logical_source_result_and_acknowledgement_set_digest,
        logical_raw_block_set_digest,
        ordered_source_result_digest_manifest,
        source_completion_bitmap,
        checksum_kind,
        staging_raw_set_digest
    },
    source_result_and_acknowledgement_set:
        SourceResultAndAcknowledgementSetPublication,
    borrow_word: Atomic<(
        Open | Revoking | Drained,
        staging_borrow_generation,
        live_recursive_sink_and_recovery_reader_count:
            BoundedBorrowCount<MAX_STAGING_BORROWS>
    )>,
    evidence_dependency_set_ref_and_generation
}

RawStagingBorrowToken {
    capture_and_staging_slot_generation,
    staging_borrow_generation,
    holder_identity_and_generation,
    use_class: RecursiveSinkReader | RecoveryCopier,
    token_id_and_kernel_authority
}

RawStagingReclaimPredicate {
    capture_and_staging_slot_generation,
    compact_cpu_owner_tag_and_fence_evidence,
    observed_lifecycle_state:
        WritingRaw | AttemptsOpen | RawSetSealed | CopyingOperational |
        HeldForContainment | ContainmentCommitting | ContainmentAccepted |
        HeldForTerminal,
    source_attempt_acknowledgement_and_copy_frontier_manifest,
    disposition_resolution:
      NeverAccepted {
          no_live_or_accepted_graph_dependency,
          no_held_requirement_witness,
          no_sealed_terminal_promotion_for_this_source
      }
    | AcceptedCustodyRehomed {
          complete_dependency_set_drained,
          all_graph_requirement_terminal_and_recursive_custody_receipts,
          no_live_pointer_to_source_staging
      },
    complete_raw_staging_attempt_receipt_ref_and_id,
    matching_current_crash_reclaim_ref_and_id,
    exact_borrow_epoch_observed_or_drained,
    protected_reclaim_authority_and_generation
}

CaptureOutcome =
    RawSetSealed(FaultCaptureIncarnation,
                 RawEvidenceRef,
                 SourceResultAndAcknowledgementSetPublicationRefAndId,
                 DerivedRequiredPostconditionSummary)
  | RecursiveTerminal(RecursiveRecordRef)

OperationalEvidenceBody {
    capture,
    raw_block_set_publication,
    source_result_and_acknowledgement_set_publication,
    copied_entry_snapshot_body_and_digest,
    copied_capture_disposition_candidate_body_and_digest,
    machine_profile_id_and_hash,
    evidence_bounds_and_schema
}

LogicalOperationalEvidenceManifest {
    capture,
    logical_raw_block_set_digest,
    logical_source_result_and_acknowledgement_set_digest,
    entry_snapshot_semantic_id_and_digest,
    capture_disposition_decision_semantic_id_and_digest,
    machine_profile_id_and_hash,
    evidence_bounds_and_schema
}

RestrictedOperationalEvidencePublication {
    publication_word: Atomic<(
        Empty | Writing | Sealed | Exporting | Exported | Clearing,
        storage_owner_and_generation,
        compact_operational_transfer_descriptor_index_and_generation_or_none,
        compact_transfer_owner_tag_or_none
    )>,
    publication_id: Hash(canonical_encoding({
        intended_state: Sealed,
        storage_owner_and_generation,
        canonical_body_digest,
        logical_operational_evidence_digest,
        evidence_bounds_and_schema
    })),
    canonical_body_digest,
    logical_operational_evidence_digest:
        Hash(canonical_encoding(LogicalOperationalEvidenceManifest)),
    logical_operational_evidence_manifest: LogicalOperationalEvidenceManifest,
    body: OperationalEvidenceBody
}

OperationalRingBorrowEpoch {
    ring_root_publication_ref_and_id,
    borrow_word: Atomic<(
        Open | Revoking | Drained,
        ring_borrow_generation,
        live_ring_evidence_reader_count:
            BoundedBorrowCount<MAX_RING_EVIDENCE_BORROWS>
    )>,
    holder_set_audit_digest
}

OperationalQueueReceiptPublication {
    receipt_slot_ref,
    lifecycle_word: Atomic<(
        Empty | Writing | Sealed | Clearing,
        receipt_generation,
        compact_operational_transfer_descriptor_index_and_generation_or_none,
        compact_transfer_owner_tag_or_none
    )>,
    receipt_id: Hash(canonical_encoding({
        intended_state: Sealed,
        receipt_slot_ref,
        receipt_generation,
        historical_source_ring_publication_id_and_storage_generation,
        queue_publication_ref_and_id,
        exact_source_root_body_digest,
        exact_destination_root_body_digest,
        logical_operational_evidence_digest,
        logical_operational_evidence_manifest_digest,
        queue_owner_and_generation,
        operational_transfer_descriptor_digest
    })),
    historical_source_ring_publication_id_and_storage_generation,
    queue_publication_ref_and_id,
    exact_source_root_body_digest,
    exact_destination_root_body_digest,
    logical_operational_evidence_digest,
    logical_operational_evidence_manifest:
        LogicalOperationalEvidenceManifest,
    logical_operational_evidence_manifest_digest,
    queue_owner_and_generation,
    operational_transfer_descriptor_digest
}

OperationalQueueBorrowEpoch {
    queue_root_publication_ref_and_id,
    borrow_word: Atomic<(
        Open | Revoking | Drained,
        queue_borrow_generation,
        live_decoder_evidence_reader_count:
            BoundedBorrowCount<MAX_QUEUE_BORROWS>
    )>,
    holder_set_audit_digest
}

OperationalEvidenceTransferDescriptor {
    descriptor_index_and_generation,
    transfer_kind:
      StagingToRing {
          source_staging_capture_slot_and_generation,
          destination_ring_root_children_slot_and_generation,
          primary_and_terminal_fallback_graph_reservations
      }
    | RingToQueue {
          source_ring_root_children_and_generations,
          destination_queue_root_children_and_generations,
          queue_receipt_slot_and_generation,
          source_dependency_set_and_borrow_generations,
          graph_rehome_destination_reservations
      }
    | StagingToLoss {
          source_staging_capture_slot_and_generation,
          sticky_loss_slot_and_expected_generation,
          destination_loss_transfer_slot_and_generation,
          loss_root_graph_reservation
      },
    complete_source_destination_receipt_graph_and_control_extent_manifest,
    fixed_source_borrow_dependency_and_holder_bit_plan,
    fixed_member_reuse_gate_cell_schedule_and_old_next_generation_plan,
    protected_transfer_owner_identity_and_generation,
    canonical_descriptor_digest
}

OperationalEvidenceTransferControl {
    transfer_word: Atomic<(
        Empty | CommitmentWriting | SourceCommitted | SourceClosing |
        SourceExportExclusive | DestinationWriting | DestinationSealed |
        ReceiptWriting | ReceiptSealed | GraphsRehoming | Committed |
        Cancelling | Released | Clearing,
        transfer_slot_and_generation,
        compact_operational_transfer_descriptor_index_and_generation_or_none,
        compact_transfer_owner_tag_or_none,
        transfer_frontier,
        accepted_destination_receipt_and_graph_bitmap,
        reserved_and_rearmed_member_gate_bitmaps,
        member_exposure_authorized_bitmap
    )>,
    descriptor_digest,
    source_commitment: {
        source_publication_identity_and_generation,
        exact_source_root_and_child_body_digests,
        logical_operational_evidence_manifest_and_digest,
        source_borrow_and_dependency_generations,
        canonical_source_commitment_digest
    },
    destination_receipt_and_graph_publication_manifest,
    canonical_control_body_digest
}

OperationalTransferMemberReuseGate {
    gate_word: Atomic<(
        Free | Reserved | MemberRearmed | ExposureAuthorized | Clearing,
        gate_generation,
        compact_transfer_descriptor_index_and_generation_or_none,
        compact_transfer_owner_tag_or_none,
        transfer_control_slot_and_generation_or_none,
        exact_member_identity_old_and_next_generation_or_none
    )>
}

OperationalTransferMemberGateCleanupPredicate {
    exact_gate_cell_generation_descriptor_owner_and_member_binding,
    member_observation:
      BeforeMemberExposure {
          transfer_control_exposure_bit_observed_clear_and_matching,
          gate_observed_state: Reserved | MemberRearmed,
          member_observed_old_generation_or_empty_next_generation
      }
    | AfterMemberExposureAuthorized {
          transfer_control_observation:
              MatchingControlWithExposureBitSet |
              DescriptorFreeEmptyNextGeneration |
              AtLeastNextControlGenerationWithoutBodyAccess,
          gate_observed_member_rearmed_exposure_authorized_clearing_or_at_least_next_generation,
          member_observed_at_least_exact_next_generation_without_body_access,
          no_old_control_gate_or_member_body_read_or_mutation
      },
    action: Retain | MarkMemberRearmed | MarkExposureAuthorized |
            ClearGate | PublishGateFreeNextGeneration,
    protected_transfer_or_gate_cleanup_authority_and_generation
}

OperationalTransferRecoveryPredicate {
    transfer_control_ref_generation_descriptor_owner_state_and_frontier,
    source_commitment_observation:
      ValidatedCommitment {
          exact_source_commitment_and_observed_source_state
      }
    | CommitmentWritingCut {
          observed_transfer_state: CommitmentWriting,
          immutable_descriptor_and_exact_authoritative_source_identity_generation,
          fenced_old_transfer_owner,
          no_destination_receipt_graph_or_sticky_loss_mutation,
          no_accepted_destination_or_rehome_bit
      }
    | CommitmentAbsentByCommittedUntouchedCancellation {
          observed_transfer_state: Cancelling,
          exact_cancel_decision_from_commitment_writing,
          source_unchanged_and_no_destination_mutation
      },
    complete_source_destination_receipt_graph_and_control_extent_manifest,
    exact_source_destination_dependency_borrow_and_holder_observations,
    exact_member_reuse_gate_states_and_reserved_rearmed_bitmaps,
    resolution:
      RecoverCommitmentWriting {
          required_source_commitment_observation: CommitmentWritingCut,
          action:
            CompleteFromAuthoritativeSource {
                exact_protected_source_read_authority_and_borrow_plan
            }
          | CancelUntouchedTransaction {
                complete_operational_transfer_attempt_receipt_ref_and_id,
                matching_current_crash_reclaim_ref_and_id
            }
      }
    | CompleteForward {
          required_source_commitment_observation: ValidatedCommitment,
          forcing_frontier:
            StagingDestinationAccepted {
                transfer_kind: StagingToRing | StagingToLoss,
                exact_destination_graph_accepted_bit,
                dependency_entry_state: ReadyToAccept | Live,
                validated_complete_hold_and_readable_destination_root
            }
          | RingExportAuthorityCommitted {
                transfer_kind: RingToQueue,
                exact_control_state_and_closure_frontier:
                    SourceClosing | SourceExportExclusive |
                    DestinationWriting | DestinationSealed |
                    ReceiptWriting | ReceiptSealed | GraphsRehoming |
                    Committed | Released | Clearing,
                source_root_observation:
                  BeforeSourceExposure {
                      source_exposure_bit_observed_clear,
                      source_root_state:
                          Sealed | Exporting | Exported | Clearing |
                          EmptyNextGeneration
                  }
                | AfterSourceExposureAuthorized {
                      source_exposure_bit_observed_set,
                      source_root_observed_at_least_next_generation_without_body_access
                  },
                exact_dependency_graph_and_borrow_close_or_drain_frontier,
                exact_partial_destination_receipt_graph_and_source_release_frontier,
                exclusive_exporter_lease_or_committed_successor_custody
            },
          exact_remaining_copy_receipt_rehome_and_source_release_plan
      }
    | CancelBeforeAcceptance {
          required_source_commitment_observation: ValidatedCommitment,
          cancellation_frontier:
            StagingDestinationNeverAccepted {
                transfer_kind: StagingToRing | StagingToLoss,
                destination_state: Empty | Writing | Sealed,
                destination_graph_accepted_bitmap: Empty
            }
          | RingExportNotBegun {
                transfer_kind: RingToQueue,
                transfer_control_state: SourceCommitted,
                source_state: Sealed,
                no_exclusive_exporter_lease,
                dependency_and_borrow_words_observed_open,
                destination_and_receipt_states: Empty | Writing,
                no_graph_rehome_begun
            },
          source_remains_authoritative_and_readable,
          no_destination_graph_accepted,
          no_sealed_receipt_or_committed_rehome_head,
          every_destination_dependency_and_holder_bit_absent,
          complete_operational_transfer_attempt_receipt_ref_and_id,
          matching_current_crash_reclaim_ref_and_id
      }
    | ResumeCancellation {
          required_source_commitment_observation:
              ValidatedCommitment |
              CommitmentAbsentByCommittedUntouchedCancellation,
          transfer_control_observed_state: Cancelling,
          committed_cancel_variant_and_exact_cleanup_frontier,
          original_source_still_authoritative_and_unmodified,
          no_destination_graph_accepted_or_rehome_committed,
          complete_operational_transfer_attempt_receipt_ref_and_id,
          matching_reclaim_publication_ref_id_and_state:
              Claimed | Consumed | Clearing,
          member_cleanup_manifest_observations:
            BeforeMemberExposure {
                member_exposure_bit_observed_clear,
                member_state:
                    Empty | Writing | Sealed | Clearing |
                    EmptyNextGeneration
            }
          | AfterMemberExposureAuthorized {
                member_exposure_bit_observed_set,
                member_observed_at_least_next_generation_without_body_access
            },
          exact_old_and_next_member_generations_descriptor_and_owner_tags
      },
    protected_recovery_authority_and_generation
}
```

`DerivedRequiredPostconditionSummary` is recomputed from the sealed ordered
per-source results and the exact classifier profile. It is a convenience, not
evidence that can replace the source IDs, program/profile hashes, attempt-set
digests, and acknowledgement results on which it depends.

Every `BoundedBorrowCount<MAX_*>` in this report uses the parent component's
nonwrapping borrow contract: increment only below a statically proved maximum,
fail closed at saturation, decrement once per exact-generation token, and
permit `Drained` only from the atomic revoking tuple at zero.

The complete operational transfer word—state, nonwrapping generation,
descriptor/owner tags, frontier, accepted bitmap, gate-state bitmaps, and
exposure bitmap—must fit one supported native atomic operation. If a target
cannot fit the bounded bitmaps, the boot
profile uses a fixed immutable shard manifest, assigns an entire transfer group
and all of its acceptance bits to exactly one shard before admission, and
closes that shard before any member clears. No global state reconstructed from
multiple independently mutable words and no emulated multiword compare/
exchange is a recovery or acceptance linearization point.

The compact tag indexes an immutable, prevalidated `RawStagingOwnerDescriptor`;
the claim CAS installs it before header or payload mutation, and every later
state cross-checks it against the completed header. The complete raw-staging
lifecycle tuple—state, nonwrapping generation, and compact CPU owner tag—and
its complete borrow tuple must each fit one
target-supported native atomic operation. The natural implementation is one
fixed shard per admitted CPU; locks, interrupt masking as a substitute, and
emulated multiword compare/exchange are not valid recovery linearization.

`capture_sequence` also uses checked nonwrapping arithmetic. The producer may
allocate sequence `s + 1` only after proving it is representable and unused in
the current `(boot_crash_generation, cpu_identity, cpu_incarnation)` domain.
At exhaustion that CPU incarnation stops admitting ordinary captures; boot
control must provision a fresh protected, nonrepeating CPU incarnation or boot/
crash generation before capture resumes. It never wraps to zero, aliases a
retained capture, or relies on a timestamp for uniqueness.

The aggregate per-source publication is the only decoder-facing identity for
that result set. Its storage-independent
`logical_source_result_and_acknowledgement_set_digest` covers capture/
set identity,
schema/bounds, ordered manifest, and every complete `SourceCaptureResult`; its
publication ID additionally covers intended `Sealed` state and the exact
storage owner/generation. Staging, ring, and queue copies therefore acquire new
publication IDs even when their canonical bodies match. A consumer validates
the exact publication identity, state, bounds, outer digest, every source
terminal state/digest, and every acknowledgement digest before use.

The CPU-local normal slot is single-writer at depth one. It does not spin on a
global compare/exchange. The transition is:

1. validate the context token, CPU incarnation, profile, and exact
   `(Free, slot_generation, None)` lifecycle word plus the immutable
   `RawStagingOwnerDescriptor` and its compact tag;
2. claim the slot by compare/exchanging that exact word to
   `(WritingRaw, slot_generation, compact_cpu_owner_tag)`, then copy the full
   owner, fixed header, and a
   `capture_set_identity_digest` over capture/slot/profile and the ordered
   admitted source-program descriptors before touching payload;
3. follow the generated cross-source schedule: publish `WritingAttempt` and
   execute each required raw-read/copy frontier, recording completion/loss and
   release-publishing its attempts `Sealed`; before acknowledging source A,
   every source named in A's alias/effect set must already have the affected
   attempt sealed (commonly every source's attempt 0 is captured first);
4. only at that validated frontier, publish source A's acknowledgement
   `InProgress`, execute its fixed clear/invalidate/recheck portion, and bind
   every acknowledgement step to the
   preceding attempt index and digest, and publish a separate `Completed` or
   normally returned `Failed` result; a source whose validated program has no
   destructive acknowledgement publishes `Completed/NotRequiredByProfile`,
   never an ambiguous untouched `NotStarted`;
5. when that program permits a coherent-read retry, append into another
   source-local reserved attempt, seal it before its following destructive
   operation, and never edit an earlier attempt;
6. after one source's bounded acknowledgement/retry program terminates, seal
   its ordered attempt-set digest, acknowledgement digest, and
   `source_result_digest`, then release-publish `SourceComplete`;
7. after every admitted source is `SourceComplete`, seal the bounded
   `SourceResultAndAcknowledgementSetPublication`, bind its publication ID into
   the raw-set header, then checksum and release-publish the outer slot as
   `RawSetSealed`; and
8. return only typed references to that immutable set and its per-source
   acknowledgement results.

The profile generator rejects cycles or shared-aggregator effects for which no
finite schedule can seal all affected observations before the first destructive
operation. A per-source ownership proof is insufficient when acknowledging one
bank/node can clear, deassert, replace, or otherwise change another source.
For a clear-on-read program, the destructive read itself is treated as the
acknowledgement boundary: its entire cross-source alias/effect frontier must be
sealed before issuing that read, and the result records
`ObservationWasAcknowledgement`. That result never satisfies a narrow-return
premise. If the needed frontier includes a destructive cycle that cannot be
latched nondestructively, the profile is inadmissible.
Such a target must use an architecture-supported nondestructive snapshot/latch,
capture the whole affected frontier first, or conservatively terminate without
issuing the acknowledgement.

If an exception occurs before the first source's attempt 0 seals, the slot
remains `WritingRaw`; the independent recursive record names the last completed
raw operation. If a later source faults in `WritingAttempt`, the outer set
remains `AttemptsOpen`: all earlier `SourceComplete` results remain sealed and
the current partial source is explicitly incomplete. An exception during any
acknowledgement or retry likewise leaves `AttemptsOpen`; every previously
sealed attempt and source result stays immutable, but the set is not falsely
presented as final while acknowledgement remains `InProgress`. The recursive
terminal path records that phase. No interrupted outer writer is assumed able
to resume and bless partial bytes as `Torn`.

The ordinary classifier/consumer proceeds only after acquire-loading
`RawSetSealed`, then validates schema, incarnation, slot/profile/source
manifest, the raw-set and every source-result digest, and every attempt's
length, operation bitmap, state, and digest. It reads each source's
acknowledgement result only through that source's terminal acknowledgement
state. A recursive crash
reader may preserve individually sealed attempts from an `AttemptsOpen` set as
explicitly incomplete outer evidence. A checksum detects some torn or corrupt
bytes; it does not authenticate a producer or prove the memory hierarchy was
healthy.

Each attempt digest covers a canonical encoding of attempt index, declared
length, completion/loss bits, and payload—not payload alone. A
`source_attempt_set_digest` covers source ID, owner/route generations,
program/profile identity, and its ordered attempt-digest manifest. Each entry
in `attempt_acknowledgement_manifest` binds an acknowledgement operation to the
attempt index and digest whose observation preceded it.
`staging_raw_set_digest` is computed with its own field canonically zeroed and excludes
the separately mutable atomic lifecycle/generation word. It otherwise covers
every immutable header field—including capture incarnation, slot generation,
profile, and `capture_set_identity_digest`—and the ordered source-result-digest
manifest. Separately, `logical_raw_block_set_digest` covers only capture,
storage-independent source-set digest, logical bounds/schema, ordered canonical
block manifests, and block metadata/bytes; it excludes staging slot/generation,
physical publication refs, and custody state. The logical source-set digest
likewise excludes storage owner/generation and publication ID. These two values
remain identical across validated staging/ring/queue/requirement/terminal
copies, while each physical envelope gets a new publication ID.
`acknowledgement_digest` separately covers capture incarnation,
capture-set identity, source ID, owner/route generations, program/profile
identity, the exact source-attempt-set digest, attempt/acknowledgement manifest,
intended terminal acknowledgement state (with its own digest field zeroed),
operation bitmap, first unfinished operation, source postcondition, and loss
flags before its terminal state publishes. `source_result_digest` then binds
the source identity, attempt set, and acknowledgement result, and the outer
digest binds every source result. A valid acknowledgement from an older slot,
another source, or another profile therefore cannot be paired with these raw
bytes. A corrupt layout, length, critical flag, source/attempt order, or route
generation cannot validate under an intact payload-only checksum.

Every staging-to-ring, ring-to-queue, and staging-to-loss mutation is one
predeclared `OperationalEvidenceTransferDescriptor` transaction. Before its
first destination, receipt, graph, or sticky-loss byte changes, the protected
owner claims exact descriptor-free transfer control
`Empty → CommitmentWriting`, installing the compact descriptor and owner tags,
zero frontier, and zero accepted, rearmed, and exposure bitmaps in that same
native-atomic word. It then reserves every descriptor-assigned
`OperationalTransferMemberReuseGate` by exact `Free → Reserved` CAS and records
each result in the control; a cut between a gate CAS and its bitmap update is
resolved by scanning only the descriptor's fixed gate schedule and matching
atomic tags. No member is read for transfer, claimed as a destination, or
cleared until every assigned gate is reserved. All writers and rearmers require
the member's exact-generation gate `Free` in addition to the member lifecycle
CAS. It
copies and validates the exact source identity, physical and logical digests,
source generations, and fixed extent plan into the control, then publishes
`SourceCommitted`. Every claimed destination root and queue receipt installs
the same descriptor and owner tags in its own `Empty → Writing` CAS. Tags remain
until an exact `Clearing → Empty(next generation, None, None)` publication;
partial bodies never identify their owners by interpreting bytes they may not
have written.

An operational or containment plan first reserves exact-generation primary and
distinct terminal-fallback aggregate graph slots while staging still owns every
byte; a terminal plan reserves its one graph slot. An operational or loss plan
also preclaims the transfer descriptor/control just described. Failure to
reserve the required set selects terminal only if its distinct destination is
available, otherwise retains staging and takes the nonwriting terminal leaf.
An admitted staging-to-ring control publishes `DestinationWriting` before the
ring-root claim. The staging slot then enters `CopyingOperational` only by an
exact-generation transition from `RawSetSealed`. The producer copies the full
raw-block set, ordered per-source result/acknowledgement set, entry snapshot,
decision candidate, profile identity, and bounds into a claimed restricted ring slot and
release-publishes the descriptor-tagged
`RestrictedOperationalEvidencePublication` as `Sealed`, followed by transfer
control `DestinationSealed`.
That root and a sealed fault-record publication graph with
`OperationalRingRoot` are only preconditions. Ownership/decision acceptance is
the later same-word accepted-bit CAS, after the matching entry reaches
`ReadyToAccept`, the reservation-bound continuation hold is `Complete` with all
required source holder bits, and the ring root is revalidated readable; recovery
must finish accepted-bit+`ReadyToAccept` to `Live`. Before staging enters
`Clearing`, the owner verifies this accepted bit/`Live` pair and complete hold,
publishes the transfer control `Committed`, and also cancels and rekeys the
still-untouched terminal-fallback graph reservation
under its exact owner/capture/seed proof, zero-borrow check, and empty-or-
revoked dependency entry. A cut resumes that `Reserved → Clearing → Empty`
cancellation; it never leaks one fallback slot per successful capture. A
bounded nontrapping graph-construction failure marks the partial primary graph
`Abandoned` only if no accepted bit/`Live` entry became authoritative; a sealed
root that lost the accepted-bit race must satisfy the decoder's exact
`SealedButNeverAccepted` proof and release its hold bits,
uses the separately reserved terminal graph slot, and promotes from still-
sealed staging; it first moves the preaccept transfer control to `Cancelling`
under the closed recovery predicate and cancels an untouched primary
reservation, while a
partially written primary follows `Abandoned` cleanup, and it never rewrites an
already sealed child. A terminal-promotion loser cancels its unused reserved
graph destination by the same proof while retaining CPU-local staging. A nested cut leaves staging/ring/graph phases intact
and uses the recursive record. If the
ring is full, only an already proved asynchronous-nondisruptive outcome
may instead take `OperationalDropped`: it must atomically transfer capture
sequence, class, and conservative loss ownership into that CPU's sticky
`OperationalLoss` record, seal the exact compact loss-transfer publication and
its `OperationalLossRoot` record graph, and release-publish `LossTransferred`
before staging is recycled. Local resume on ring admission failure is terminal.
Failure of that bounded transfer is terminal rather than a leaked
or silently dropped staging slot. A
containment plan atomically changes the lifecycle to `HeldForContainment`.
After the pre-reserved requirement slot seals a full bounded evidence/candidate
copy, its named custodian must win the same staging word's
`HeldForContainment → ContainmentCommitting` CAS before attempting requirement
`Sealed → Held`; terminal fallback races with `HeldForContainment →
HeldForTerminal`. Requirement acceptance therefore cannot race an independently
selected terminal disposition. On `Held`, recovery or the custodian publishes
`ContainmentAccepted`, mints the protected witness, cancels the untouched
terminal-fallback graph reservation under the exact held-outcome proof, and
only then releases staging. A bounded nontrapping failure before the shared
gate wins may take the direct terminal path; a
nested architectural fault retains the interrupted outer state and uses only
the independent recursive terminal path. A terminal classification atomically changes lifecycle to
`HeldForTerminal` before trying the global promotion claim. Both the promotion
claimant and every loser remain nonreusable for the boot/crash generation so
crash discovery cannot race slot recycling.

Those terminal fallbacks are exact lifecycle transitions only for bounded
nontrapping failures. Such a failure before a ring publication owns the
complete copy, or failure of sticky-loss transfer,
compare/exchanges `(CopyingOperational, g, owner_tag)` to
`(HeldForTerminal, g, owner_tag)` before
promotion; any partial ring destination remains nonauthoritative and
nonreusable. A nested architectural fault or execution cut cannot execute that
outer CAS: it leaves staging, partial ring/loss/graph state exactly as
interrupted and publishes only the independent recursive terminal record. A
bounded nontrapping containment reservation/fence failure moves exact
`(RawSetSealed, g, owner_tag)` directly to
`(HeldForTerminal, g, owner_tag)`. Failure after staging entered
`HeldForContainment` may move exact `(HeldForContainment, g, owner_tag)` to
`(HeldForTerminal, g, owner_tag)` only by winning the shared gate before the custodian. If
containment already won `ContainmentCommitting`, terminal fallback remains
blocked until fenced recovery proves the exact requirement never became
`Held`, CASes its sealed generation to `Abandoned`, and only then changes
`ContainmentCommitting → HeldForTerminal`. A requirement observed `Held`
instead forces `ContainmentAccepted`; it can never coexist with the terminal
state. The failed requirement remains nonreusable until its exact abandonment
cleanup, and the terminal branch seals the distinct direct terminal decision.
A nested architectural fault or
execution cut instead leaves outer staging/requirement/candidate bytes exactly
as interrupted, accepts no outer decision, and publishes only the independent
recursive terminal record. That edge is forbidden after successful
requirement acceptance: a later nested failure is a new recursive/terminal
event and cannot relabel the accepted containment decision.

Every staging release is an exclusive exact-generation state transition, not a
write to a separate reusable flag. After one of the authorized custody outcomes
above, the owner compare/exchanges the current lifecycle state to `Clearing`,
executes and verifies the fixed clear/rekey recipe over payload, header, owner,
and source results, increments `slot_generation`, and release-publishes
`(Free, next_generation, None)` last. A stale release CAS fails; a crash or fault in
`Clearing` leaves the slot nonreusable. Terminal-held slots never take this path
in the same boot/crash generation. For a completed staging-to-ring or
staging-to-loss transaction, only that verified source `Free(next)` publication
permits matching transfer control `Committed → Released → Clearing`; its own
body/tags are cleared and next descriptor-free `Empty` is published last. A
cut in either clearing phase resumes from both exact words and never makes the
control reusable ahead of its source. Staging, ring, queue, receipt, and loss
generations use checked nonwrapping arithmetic; exhaustion retires that slot
until a fresh protected boot/CPU incarnation supplies a nonrepeating identity
domain.

An interrupted or terminal-held staging generation has a separate, exact
next-boot reclaim path; boot reset is not an implicit clear. The compact CPU
owner tag is installed in the same native-atomic lifecycle claim as
`Free → WritingRaw`, so recovery can fence the exact old CPU/entry owner without
trusting a partial header. A recursive sink or recovery copier may read even a
suspect prefix only after installing one bounded exact-generation staging
borrow and rechecking the lifecycle, generation, owner tag, and borrow word.
No other reader may dereference staging directly.

Recovery first copies the **entire fixed physical staging extent**, including
all attempt storage, acknowledgement fields, header/control bytes, apparently
untouched bytes, and malformed or partial destinations named by its bounded
frontier, into a sealed crash-sink
`IncompleteCrashAttempt(RawStagingAttempt)` receipt. It then obtains a separate
generation-current `CrashReclaim` for that exact extent. For a pre-acceptance
cut, it must additionally prove that no graph accepted bit/live dependency,
held requirement witness, or sealed terminal promotion ever took custody. For
an accepted containment, operational, terminal, or recursive path, it instead
closes and drains the complete dependency set and proves that every accepted
graph, requirement, terminal capsule, and recursive reference was copied or
rehomed under independent custody; a source pointer or one copied core is not
enough. Partial ring, graph, requirement, promotion, and handoff destinations
remain separately retired unless their own cancellation/reclaim predicates
complete.

Only the complete `RawStagingReclaimPredicate` lets recovery CAS the exact
observed state and generation to `Reclaimable`. It then closes staging-borrow
admission, drains exact `(Revoking, b, 0) → (Drained, b, 0)`, changes
`Reclaimable → Clearing`, clears and verifies the full source extent and holder
metadata, initializes the next zero-borrow epoch and dependency set, advances
the nonwrapping slot generation, and publishes `(Free, next_generation, None)`
last. A cut resumes from those words. Missing extent, ambiguous acceptance,
unfenced ownership, a live borrower/dependency, or generation exhaustion
retires the slot rather than guessing.

The restricted ring uses the publication's one atomic
state/generation/descriptor/owner word; there is no second lifecycle flag that
can disagree. Its staging-to-ring producer claims exact
`(Empty, ring_generation, None, None) → (Writing, ring_generation,
transfer_descriptor, transfer_owner)` before changing bytes, fills the body and
metadata, and release-publishes `Sealed` while retaining both tags. Every
ordinary reader validates that tuple and publication, increments the exact
ring-root `BoundedBorrowCount` only below `MAX_RING_EVIDENCE_BORROWS`, receives
one generation-bound token, and then rechecks `Sealed`, owner/generation,
publication ID/body digest, and borrow `Open` before copying. A failed recheck
releases without dereference; every successful holder decrements exactly once.

Deferred ring-to-queue export first claims its own descriptor-tagged transfer
control while the ring root is still `Sealed`. Under one ordinary exact ring
borrow, it independently validates both children and normalizes the source to
the storage-independent logical manifest; it writes the source identity,
physical body digests, logical manifest/digest, and current borrow/dependency
generations into the immutable transfer commitment, validates its digest,
release-publishes `SourceCommitted`, and releases that ordinary borrow. It then
publishes `SourceClosing`, CASes the ring dependency set from exact `Open` to
`Closing`, and CASes the borrow epoch from `Open` to `Revoking`. This stops new
registration bits and direct root readers before any root-state change. It
resolves every bit/entry cut, rejects or adopts each sealed-root/`Reserved` pair
under the decoder protocol, and enumerates every `Live` initial or decoded
graph. Each source graph closes borrow admission, drains the component-2
return/park borrower and every other graph reader, and exclusively enters
`Sealed → Rehoming`. Every direct ring reader releases its exact-generation
token; only `(Revoking, r, 0) → (Drained, r, 0)` proves root-borrow drain.

A publisher racing dependency closing may never expose success: its final
accepted-bit CAS and `ReadyToAccept → Live` publication require the same atomic
`Open` dependency word and unchanged readable root. If closing wins, the entry
remains unaccepted and revocable; if acceptance wins, the closer owns that
accepted entry and its preissued holds. Only after every registration settles,
each source graph is exclusively held, and the ring-root borrow is `Drained`
may the owner CAS the exact source tuple
`(Sealed, source_generation, prior_descriptor, prior_owner) → (Exporting,
source_generation, ring_to_queue_descriptor, exporter_owner)`. The conjunction
of that descriptor-tagged `Exporting` tuple, drained borrow/dependency words,
and matching `SourceClosing` transfer control is the **exclusive exporter-read
lease**. It is not an ordinary borrow. Only that exporter or fenced recovery
may read the immutable source while `Exporting`; it revalidates every byte and
child against the already sealed source commitment, then publishes transfer
control `SourceExportExclusive`. `OperationalRingRoot` remains defined only for
physical `Sealed`, so no ordinary graph or reader can treat this lease as a
readable custody root.

The exporter publishes `DestinationWriting`, claims the queue-owned root and
children with the same descriptor/owner tags, copies the complete body, and
validates and seals them before publishing `DestinationSealed`. It then
publishes `ReceiptWriting`, claims the queue receipt with those same tags,
and seals a receipt binding the precommitted historical source publication,
generation, body and logical digests as inert values; the live destination
root and children; the destination-specific body digest; the common logical
manifest/digest; destination and receipt generations; and the transfer
descriptor digest. The exporter verifies the source against its commitment
under the exclusive lease and the destination under its private construction
authority. It never pretends to hold an ordinary source borrow after
`Exporting`. The sealed receipt contains no source pointer and never authorizes
a later ring dereference.

After `ReceiptSealed`, transfer control enters `GraphsRehoming`. Each enumerated
source graph must seal a complete replacement
`FaultRecordPublicationGraphSlot` under `OperationalQueueRoot`, with graph-local
children and acyclic rehome provenance, and head any binding migration, or be
authoritatively revoked; one replacement is insufficient. Only after every
entry publishes `Rehomed|Revoked`, clears its accepted and reservation bits,
and exact dependency-set `Closing → Drained` validates the complete scan may
the transfer publish `Committed` and the evidence word become `Exported`.

`OperationalTransferRecoveryPredicate` gives every interrupted operational
group one disjoint decision. For `StagingToRing` and `StagingToLoss`, only the
exact destination graph accepted-bit with a validated complete hold/root and
entry `ReadyToAccept|Live` forces
`CompleteForward`; an as-yet `Empty`, merely `Writing`, or merely `Sealed`
destination remains an
unaccepted candidate and must be cancelled if recursive terminalization or the
terminal fallback won. Recovery can never late-accept it. For `RingToQueue`,
the exact `SourceClosing` control CAS is already a force-forward frontier:
dependency/borrow admission may have closed and source graphs may have entered
`Rehoming`, so recovery completes every published close/drain frontier and then
wins the descriptor-tagged source `Sealed → Exporting` CAS. At or after that
CAS, the drained controls and `Exporting` tuple form the exclusive exporter
lease. Destination/receipt sealing and rehome follow. Fenced recovery follows the
immutable commitment and descriptor to finish the exact copy, receipt, every
graph/binding rehome, and source release. It cannot cancel back to an ordinary
ring reader. Every later control state—destination/receipt writing or sealed,
graph rehome, committed source cleanup, transfer release, and transfer
clearing—remains in this same force-forward arm with exact member/frontier
observations; `ReadyToAccept` is completed to `Live` before staging release.
`CancelBeforeAcceptance` is limited to an unaccepted staging
destination, or to ring export still in `SourceCommitted` with dependency and
borrow words `Open`, before `SourceClosing`, the exclusive lease, any
destination/receipt seal, or graph rehome, while the original source remains
authoritative and readable and every destination dependency and holder bit is
absent. At the next boot that cancellation also
requires a complete fixed-extent
`IncompleteCrashAttempt(OperationalTransferAttempt)` receipt covering the
control and every source/destination/receipt/graph/loss slot named by the
descriptor, plus a matching current `CrashReclaim`. The protected owner CASes
the exact transfer word to `Cancelling`, CASes each tagged partial publication
to `Clearing` before byte mutation, verifies clear/rekey, and publishes each
next-generation descriptor-free `Empty` last. A staging-to-loss cancellation
never rolls back a conservatively published sticky-loss summary. A cut in
`CommitmentWriting` is handled before either branch: after fencing the tagged
owner, `RecoverCommitmentWriting` either reacquires the exact authoritative
source and deterministically rebuilds/validates the commitment before
`SourceCommitted`, or—because the protocol has not yet touched a destination,
receipt, graph, or sticky-loss word—preserves the complete control extent and
uses current reclaim authority to commit an untouched cancellation. A later
cut in that cancellation carries the explicit commitment-absent cancel case;
it never tries to validate partial commitment bytes. A missing descriptor or
extent, an unreadable/changed authoritative source, unexplained bit, or ambiguous acceptance retires
the complete group rather than leaking a partially reusable member.

`Cancelling` is itself a durable decision, not a transient pseudo-state. Every
member clear advances an exact frontier in the control before its CAS, and its
post-CAS observation records either old-generation `Clearing` or verified
next-generation descriptor-free `Empty`; the member gate then advances
`Reserved → MemberRearmed`. A cut re-enters only through
`ResumeCancellation`, using the original complete attempt receipt and the
same reclaim publication in `Claimed|Consumed|Clearing`; it never demands a
second token or reopens `CompleteForward`. Recovery finishes each remaining
idempotent clear and CASes control `Cancelling → Clearing`. For each rearmed
member it first sets that member's exposure-authorized bit in the control, then
advances its gate `MemberRearmed → ExposureAuthorized → Clearing → Free(next)`.
Only that ordering permits a new writer. Once exposed, old recovery treats the
member **and gate** as opaque observations at least at their assigned next
generations and neither reads nor mutates their possibly reused bodies. After
all exposure bits are set, recovery no longer waits for or rereads exposed
gates; their descriptor-bound cleanup can finish independently even if the
control publishes or passes its next generation. Recovery clears/rekeys the
control and publishes exact `(Empty, next_transfer_generation, None, None,
zero_frontier, zero_accepted_bitmap, zero_reserved_and_rearmed_gate_bitmaps,
zero_exposure_bitmap)` last. Thus a cut before
the first destination claim and a cut after the last member clear are both
total, generation-bound cases.

After a committed ring-to-queue transfer, the already-drained source graph and
evidence epochs must still match before the source enters exact descriptor-
tagged `Clearing`. Clear/rekey covers the ring root, children, and metadata and
verifies them empty. While unreadable, the owner advances storage and borrow
generations with checked nonwrap, initializes the next immutable holder table
and empty dependency set, and CASes exact `(Drained, old_borrow_generation,
zero) → (Open, next_borrow_generation, zero)`. Only then does it publish the
source root `(Empty, next_generation, None, None)` last, followed by transfer
control `Released → Clearing`. The source and every other rearmed member remain
writer-ineligible under reserved gates. The controller authorizes reuse one
member at a time by setting its exposure bit **before** releasing its gate;
after that bit, old recovery accepts any state at or beyond the assigned next
generation but must not inspect or mutate the member or gate. Once every
exposure bit is set, the controller may clear/rekey itself and publish
exact `(Empty, next_transfer_generation, None, None, zero_frontier,
zero_accepted_bitmap, zero_reserved_and_rearmed_gate_bitmaps,
zero_exposure_bitmap)` last without rereading exposed gates. A gate still in
`ExposureAuthorized|Clearing` finishes from its own descriptor, accepting the
old control as matching, descriptor-free next-`Empty`, or at least its next
generation without body access. A cut in either `Clearing`
resumes from the tagged control/gate words. The queue
receipt remains sealed with the destination graph and is not erased during
source-ring rearm. The destination queue owns an exclusive generation/rearm
protocol and may retain no pointer into ring or staging.

`RestrictedOperationalEvidencePublication` is also the aggregate queue graph
root: its storage-specific canonical body digest commits the exact raw-block-set child
publication ID/digest, source-result/acknowledgement-set child publication
ID/digest, entry snapshot, decision, profile, and bounds. A destination copy
creates and seals both queue-owned child publications first, then seals the
root that names them. The handoff receipt's `queue_publication_ref_and_id`
therefore authenticates the whole graph, not a generic pointer; a decoder
validates root and both children before constructing `DecoderInput`, so valid
children from different copies cannot be mixed. It recomputes the live queue
root's `LogicalOperationalEvidenceManifest` by replacing storage-specific
child references with their validated logical raw/source digests and rejects
the queue unless that manifest and logical digest equal the receipt. The
receipt's historical source identity and source-body digest are provenance
data validated when the receipt sealed; later consumers do not resolve them or
recompute the cleared ring root. A core's
operational custody root binds this incoming receipt alongside the queue root
and both children.

The copied disposition in either ring or queue is explicitly a candidate, not
an accepted decision publication. Its closed effective-product body, semantic
decision ID, rule, and digest are immutable inputs to the copy. Only after the
evidence substrate is independently valid—a sealed ring root, a sealed queue
root plus handoff receipt during rehome, or a sealed compact loss-transfer
publication plus stable sticky-loss generation—may the trusted graph publisher
materialize and seal the accepted decision, core, projection, and aggregate
root. If either transfer fails while execution remains nontrapping, the async/
local candidate is discarded without publication, an unconsumed local token is
revoked, and the one graph eventually sealed for that capture carries the
terminal product. A nested fault accepts neither candidate and records only the
recursive terminal event.

The queue graph is not cleared merely because one decoder finished. Every
decoder/evidence reader first increments exact `(Open, q, n)` to
`(Open, q, n+1)` only when `n < MAX_QUEUE_BORROWS`; saturation returns no
pointer. It then rechecks the root and both child IDs/generations before
dereference; release decrements the same generation. Before queue rearm, an
authenticated complete custody receipt must bind the exact queue root, both
child publications, and sealed destination publication. The queue dependency
set must close and every live aggregate graph/binding must install a complete
`IndependentCustodyRoot` replacement with all child references graph-local and
rehome provenance sealed, or be authoritatively revoked; every graph borrow
drains before dependency-set `Drained`. Reclaim authority is a closed scope:
a protected same-boot internal release may use the complete receipt/rehome plus
kernel queue-release authority only when the queue never entered crash
retention or out-of-domain custody; after reset or for any external/durable
handoff it additionally requires the uniquely registered generation-current
`CrashReclaim(OperationalQueueGraph)` for the exact root/children/incoming-
receipt manifest. The external receipt cannot be paired with the same-boot arm.
Rearm then
CASes `(Open, q, n)` to `(Revoking, q, n)`, rejects new borrows, drains or
forcibly fences every existing reader, and accepts only exact
`(Revoking, q, 0) → (Drained, q, 0)`. It CASes the exact queue-root tuple
`(Sealed, old_root_generation, transfer_descriptor, transfer_owner) →
(Clearing, old_root_generation, transfer_descriptor, transfer_owner)`,
then compare/exchanges the exact queue-owned incoming receipt
`(Sealed, old_receipt_generation, transfer_descriptor, transfer_owner) →
(Clearing, old_receipt_generation, transfer_descriptor, transfer_owner)`,
clears/rekeys and verifies the root, both children, receipt, and old control
metadata, advances the receipt generation with checked nonwrap, and
release-publishes exact `(Empty, next_receipt_generation, None, None)` last for that
receipt. While the root is still unreadable, it initializes the next empty
dependency set and immutable holder-bit table/audit bound to the next queue
identity and compare/exchanges exact `(Drained, old_borrow_generation, zero)`
to `(Open, next_borrow_generation, zero)`. Only after all child, receipt,
dependency, and borrow generations agree does it publish the tagged queue root
from exact `Clearing` to `(Empty, next_root_generation, None, None)` **last**.
A cut at any receipt/control/root rearm frontier leaves the
root unavailable; a reused queue never retains the prior incoming receipt.
Without that rehome/projection and zero-borrow proof, the entire queue graph is
nonreusable.

## Capture-time disposition handoff

After raw publication and the bounded acknowledgement attempt, hard entry calls
the generated `CaptureDispositionClassifier`. Its input is deliberately much
smaller than a decoded policy view:

```text
CaptureDispositionInput {
    sealed_raw_ref_and_digest,
    sealed_ordered_source_result_and_acknowledgement_manifest,
    sealed_entry_snapshot_ref_and_digest,
    capture_profile_and_rule_table_hash
}
```

The entry snapshot is the fixed `EntrySnapshotPublication` defined by the
classifier contract. Component 2 and the staging allocator bind it to the same
capture incarnation before raw reads; a non-`Sealed`, digest-invalid, or
generation-mismatched snapshot cannot support any return rule.

Its finite output is `AsynchronousNonDisruptive`,
`LocalResumePostcondition`, `ContainmentRequirement`, or
`TerminalDisposition`. The full [fault decoder](fault-decoder.md) is not on this
dependency path. It later creates append-only normalized views for policy,
diagnostics, and maintenance. A later interpretation can widen future recovery
or trigger review, but can never retroactively authorize the original return.

## First observation, first fatal, and loss truthfulness

The routine must use exact terminology:

- `first_local_observation` is the earliest record this CPU successfully
  sealed in its current sequence;
- `first_terminal_claim` is the capture whose promotion CAS first changed the
  system terminal slot from `Free` to `Writing`;
- `first_promoted_fatal` exists only if that claimant subsequently
  release-published `Sealed`; if it faults and leaves `Writing`, there is no
  promoted fatal record and the independently sealed recursive record is the
  terminal explanation;
- neither is necessarily the first physical error; and
- cross-CPU chronological ordering is `unknown` unless a profile supplies a
  trustworthy arbitration source. Unsynchronized timestamps are correlation
  hints only.

Hardware may overwrite a bank before software arrives or during collection.
Raw `OVER`/`OF`/`rdip`, multiple-error, and record-lost flags therefore survive
normalization. A losing terminal claimant writes only its CPU-local sealed
record and increments a saturating additional-fatal summary when safe. It
never overwrites the winner.

## Operational ring and admission failure

The restricted raw operational ring is distinct from raw staging and terminal storage. Its
fixed policy is drop-newest for records that cannot be admitted, because
overwriting a reader-owned slot would complicate custody. The following loss
metadata is a redacted summary and remains sticky until the policy consumer
acknowledges it:

```text
OperationalLoss {
    publication_word: Atomic<(
        Empty | Updating | Pending | Reclaimable | Clearing,
        loss_generation,
        compact_loss_operation_descriptor_index_and_generation_or_none,
        compact_loss_operation_owner_tag_or_none,
        operation_frontier:
            None | SummaryHolderHeld | BodyComplete | HolderClosing |
            HolderDrained | ReclaimCommitted | ClearAuthorized |
            BodyVerifiedEmpty
    )>,
    boot_crash_generation,
    cpu_incarnation,
    first_dropped_sequence,
    last_dropped_sequence,
    saturating_count,
    class_bitmap,
    containment_notice_pending,
    canonical_summary_digest,
    summary_holder_word: Atomic<(
        Open | Revoking | Drained,
        summary_holder_generation,
        live_update_transfer_ack_reader_count:
            BoundedBorrowCount<MAX_OPERATIONAL_LOSS_HOLDERS>,
        exact_holder_bitmap: BoundedBitmap<MAX_OPERATIONAL_LOSS_HOLDERS>
    )>
}

OperationalLossUpdateDescriptor {
    descriptor_index_and_generation,
    loss_slot_and_next_generation,
    cpu_identity_incarnation_and_boot_crash_generation,
    prior_stable_state_generation_complete_canonical_summary_and_digest_or_empty,
    exact_new_drop_capture_sequence_class_and_notice_delta,
    fixed_summary_layout_bounds_and_saturating_merge_plan,
    preallocated_exact_generation_summary_holder_token_and_bit,
    protected_update_owner_identity_and_generation,
    canonical_descriptor_digest
}

OperationalLossCleanupDescriptor {
    descriptor_index_and_generation,
    loss_summary_slot_old_and_next_generation,
    cleanup_variant:
      AcknowledgedStableSummary {
          acknowledgement_publication_ref_generation_and_id,
          exact_pending_summary_digest
      }
    | InterruptedUpdate {
          update_descriptor_ref_generation_and_digest,
          complete_fixed_extent_attempt_receipt_ref_and_id,
          matching_current_crash_reclaim_ref_and_id
      },
    exact_summary_holder_generation_close_and_drain_plan,
    fixed_summary_extent_clear_rekey_and_verification_plan,
    protected_cleanup_owner_identity_and_generation,
    canonical_descriptor_digest
}

OperationalLossAcknowledgementBuildDescriptor {
    descriptor_index_and_generation,
    acknowledgement_slot_and_generation,
    acknowledged_loss_slot_generation_descriptor_owner_and_canonical_digest,
    policy_consumer_identity_generation_authority_and_sequence,
    preallocated_exact_generation_summary_holder_token_and_bit,
    protected_builder_identity_and_generation,
    canonical_descriptor_digest
}

OperationalLossAcknowledgementPublication {
    lifecycle_word: Atomic<(
        Empty | Writing | Sealed | Claimed | Consumed | Clearing,
        acknowledgement_slot_and_generation,
        compact_acknowledgement_build_descriptor_index_and_generation_or_none,
        compact_acknowledgement_owner_tag_or_none,
        acknowledgement_frontier:
            None | SummaryHolderHeld | BodyComplete | SourceReclaimCommitted |
            SourceEmptyObserved | ClearAuthorized | BodyVerifiedEmpty
    )>,
    acknowledgement_publication_id: Hash(canonical_encoding({
        intended_state: Sealed,
        acknowledgement_slot_and_generation,
        acknowledgement_build_descriptor_digest,
        acknowledged_loss_slot_generation_descriptor_owner_and_canonical_digest,
        policy_consumer_identity_and_generation,
        acknowledgement_authority_and_sequence,
        canonical_acknowledgement_digest
    })),
    acknowledgement_build_descriptor_digest,
    acknowledged_loss_slot_generation_descriptor_owner_and_canonical_digest,
    policy_consumer_identity_and_generation,
    acknowledgement_authority_and_sequence,
    canonical_acknowledgement_digest
}

OperationalLossAcknowledgementRecoveryPredicate =
    CompleteWriting {
        exact_build_descriptor_owner_slot_generation_and_frontier,
        matching_pending_summary_observed_unchanged,
        exact_summary_holder_token_observed_held,
        action: CompleteCanonicalBodyAndSeal
    }
  | AbandonUnacceptedWriting {
        exact_build_descriptor_owner_slot_generation_and_frontier,
        fenced_builder_and_no_sealed_publication_identity,
        summary_no_longer_matches_or_policy_operation_cancelled,
        exact_summary_holder_token_release_plan,
        action: ClearVerifyAndPublishEmptyNextGeneration
    }
  | ResumeSealedHolderRelease {
        exact_sealed_acknowledgement_ref_generation_id_descriptor_and_owner,
        exact_descriptor_assigned_summary_holder_bit_observed_held_or_released,
        matching_pending_summary_generation_and_digest,
        action: ReleaseExactHolderBitOnceAndRetainSealed
    }
  | CancelStaleSealed {
        exact_sealed_acknowledgement_ref_generation_id_descriptor_and_owner,
        exact_descriptor_assigned_summary_holder_bit_observed_held_or_released,
        source_observation:
            UpdatingOrPendingDifferentGenerationOrDescriptor | Empty,
        proof_no_acknowledgement_claim_or_source_reclaim_used_this_publication,
        action: ReleaseExactHolderBitIfPresentThenClaimClearingAndPublishEmptyNextGeneration
    }
  | CompleteClaimedAfterSummaryReclaim {
        exact_claimed_acknowledgement_ref_generation_id_descriptor_and_owner,
        matching_summary_cleanup_descriptor_observed_at:
            Reclaimable | Clearing | EmptyNextGeneration,
        proof_summary_reclaim_cas_committed_this_acknowledgement,
        action: PublishAcknowledgementConsumed
    }
  | CleanupConsumed {
        exact_build_descriptor_owner_slot_generation_and_frontier,
        observed_state: Consumed | Clearing | EmptyNextGeneration,
        matching_summary_observed_empty_next_generation,
        action: FinishClearVerifyAndPublishEmptyNextGeneration
    }

OperationalLossCleanupPredicate =
    AcknowledgedPending {
        exact_pending_slot_generation_descriptor_owner_and_digest,
        sealed_loss_acknowledgement_publication_ref_and_id,
        acknowledgement_observed_state: Sealed | Claimed | Consumed,
        exact_summary_holder_generation_observed_revoking_or_drained_at_zero,
        no_live_loss_transfer_or_graph_requires_the_summary_body,
        prevalidated_cleanup_descriptor_and_owner,
        protected_cleanup_authority_and_generation
    }
  | InterruptedUpdateReclaim {
        exact_updating_slot_generation_descriptor_and_fenced_owner,
        complete_fixed_extent_operational_loss_attempt_receipt_ref_and_id,
        matching_current_crash_reclaim_ref_and_id,
        no_pending_publication_or_accepted_loss_transfer_for_this_generation,
        exact_summary_holder_generation_observed_revoking_or_drained_at_zero,
        prevalidated_cleanup_descriptor_and_owner,
        protected_cleanup_authority_and_generation
    }
  | CleanupResume {
        original_slot_generation_cleanup_descriptor_owner_and_variant,
        observed_state: Reclaimable | Clearing | EmptyNextGeneration,
        original_acknowledgement_or_receipt_reclaim_refs,
        exact_old_and_next_generations_holder_state_and_atomic_cleanup_frontier,
        protected_cleanup_authority_and_generation
    }

OperationalLossTransferPublication {
    lifecycle_word: Atomic<(
        Empty | Writing | Sealed | Reclaimable | Clearing,
        loss_slot_and_generation,
        compact_loss_transfer_operation_descriptor_index_and_generation_or_none,
        compact_operation_owner_tag_or_none,
        cleanup_frontier:
            None | DependenciesClosing | DependenciesDrained |
            BorrowClosing | BorrowDrained | ReclaimCommitted |
            ClearAuthorized | BodyVerifiedEmpty
    )>,
    loss_transfer_publication_id: Hash(canonical_encoding({
        intended_state: Sealed,
        loss_slot_and_generation,
        capture,
        candidate_decision_semantic_id_and_digest,
        logical_raw_and_source_set_digests,
        entry_snapshot_semantic_id_and_digest,
        machine_profile_id_and_hash,
        sticky_loss_publication_generation_descriptor_owner_and_digest,
        logical_core_evidence_manifest_digest,
        canonical_body_digest,
        operational_transfer_descriptor_digest
    })),
    capture,
    candidate_decision_semantic_id_and_digest,
    candidate_effective_product_tag: AsynchronousNonDisruptiveProduct,
    logical_raw_and_source_set_digests,
    entry_snapshot_semantic_id_and_digest,
    machine_profile_id_and_hash,
    logical_core_evidence_manifest_and_digest,
    raw_evidence_availability: UnavailableAfterLossTransfer,
    sticky_loss_publication_generation_descriptor_owner_and_digest,
    operational_transfer_descriptor_digest,
    canonical_body_digest,
    borrow_word: Atomic<(
        Open | Revoking | Drained,
        loss_borrow_generation,
        live_graph_and_policy_reader_count:
            BoundedBorrowCount<MAX_LOSS_TRANSFER_BORROWS>
    )>,
    dependency_word: Atomic<(
        Open | Closing | Drained,
        loss_dependency_generation,
        reservation_bitmap,
        accepted_graph_and_binding_bitmap
    )>
}

OperationalLossTransferReclaimDescriptor {
    descriptor_index_and_generation,
    loss_transfer_slot_old_and_next_generation,
    original_operational_transfer_descriptor_ref_generation_and_digest,
    authenticated_complete_loss_transfer_custody_receipt_ref_and_id,
    matching_generation_current_crash_reclaim_ref_and_id,
    exact_dependency_rehome_receipt_manifest_and_close_drain_plan,
    exact_borrow_close_drain_clear_rekey_and_verification_plan,
    protected_reclaim_owner_identity_and_generation,
    canonical_descriptor_digest
}

OperationalLossTransferReclaimPredicate {
    exact_sealed_loss_transfer_publication_ref_generation_and_digest,
    authenticated_complete_loss_transfer_custody_receipt_ref_and_id,
    matching_generation_current_crash_reclaim_ref_and_id,
    every_accepted_graph_and_binding_rehomed_under_complete_independent_custody,
    no_authoritative_revocation_removes_the_last_complete_evidence_copy,
    dependency_word_observed_closing_or_drained_with_zero_accepted_bits,
    borrow_word_observed_revoking_or_drained_at_zero,
    prevalidated_reclaim_descriptor_owner_and_atomic_cleanup_frontier,
    observed_state: Sealed | Reclaimable | Clearing | EmptyNextGeneration,
    protected_reclaim_or_resume_authority_and_generation
}
```

The per-CPU loss object uses a generated single-writer-at-depth-one publication
protocol, but `Updating` is never anonymous. Before changing any field, the
producer prevalidates an immutable `OperationalLossUpdateDescriptor` that binds
the exact old stable generation, the **complete canonical prior summary and its
digest** (or the explicit empty case), new drop delta, slot/next generation,
fixed merge plan, CPU/boot identity, and protected writer. A digest alone is
not recovery data. Before the lifecycle CAS, the writer installs its unique
descriptor-assigned bit and increments the exact-generation summary holder,
then rechecks holder `Open` and the unchanged `Empty|Pending` tuple. Its one
native-atomic CAS changes that full tuple to `(Updating, g+1, new_descriptor,
new_owner, SummaryHolderHeld)` before the first body byte changes. If it
replaced `Pending`, recovery can deterministically reproduce the conservative
saturating merge from the descriptor's complete prior value; if it replaced
`Empty`, it initializes the canonical empty value plus the delta. While
`Updating`, a consumer may not accept or clear the object. After all fields
reproduce the descriptor and the self-excluding summary digest validates, the
producer release-publishes `(Pending, g+1, new_descriptor, new_owner,
BodyComplete)` and releases its exact holder bit once.

A policy reader or `StagingToLoss` copier first acquires its unique
exact-generation summary-holder bit and count, rechecks holder `Open`, then
accepts only two identical `Pending` observations around its bounded copy. It
releases that holder only after its acknowledgement or compact loss copy has
sealed. The acknowledgement claim installs a prevalidated build descriptor and
owner in exact descriptor-free `Empty → Writing`; the body reproduces the
descriptor, then release-publishes a self-excluding, identity-bound
`acknowledgement_publication_id` in `Sealed`. Its closed recovery predicate can
finish a canonical `Writing` body while the matching summary and holder remain,
or clear an unaccepted write after fencing the builder; partial bytes are never
treated as a sealed acknowledgement. A cut after `Sealed` but before the
builder releases its descriptor-assigned summary bit enters
`ResumeSealedHolderRelease`, which releases exactly that bit once and leaves the
publication sealed. If the source has already advanced so that this sealed
acknowledgement can no longer be claimed, `CancelStaleSealed` races the claim
with an exact `Sealed → Clearing` CAS, releases its assigned holder bit if still
present, and verified-clears to next `Empty`; source-generation mismatch is not
permission to reinterpret its body. A cut after the source reclaim CAS but before
`Claimed → Consumed` enters `CompleteClaimedAfterSummaryReclaim`, whose matching
cleanup descriptor proves that this acknowledgement authorized the CAS.

The policy owner claims acknowledgement `Sealed → Claimed`, changes the
summary holder exact `Open → Revoking`, and waits for its bounded count/bitmap
to drain to zero. It then rechecks the exact `Pending` tuple and atomically
installs an immutable `AcknowledgedStableSummary`
`OperationalLossCleanupDescriptor`, cleanup owner, and `HolderDrained` frontier
while changing `Pending → Reclaimable`. That CAS is both the no-new-reader gate
and the persistent cleanup decision; a transfer or producer that acquired
before close must finish and release, while one racing afterward cannot acquire
or dereference. The acknowledgement advances `Claimed → Consumed`; summary
`Reclaimable → Clearing` retains cleanup tags/frontier, clear/rekey verifies the
complete extent, and descriptor-/owner-free `Empty(next)` publishes last. Only
after observing that source successor may the consumed acknowledgement clear
and publish its own `Empty(next)`. A concurrent producer that first moves the
old `Pending` generation to `Updating` makes the cleanup CAS fail, so the
acknowledgement cannot erase the newer drop.

A producer fault while `Updating`, inability to acquire the bounded ownership
transition, or failure to release-publish `Pending` is terminal for the current
execution, but does not authorize reset-time erasure. Fenced next-boot recovery
must preserve the entire fixed summary extent—including partial and apparently
untouched bytes—in
`IncompleteCrashAttempt(OperationalLossSummaryUpdating)`, obtain the unique
generation-current `CrashReclaim`, and prove no `Pending` publication or
accepted loss-transfer/graph used that generation. Recovery fences the old
holder owners, closes the exact holder generation, and accounts for every fixed
bitmap entry before `Drained`. Only `InterruptedUpdateReclaim` may atomically
replace the update tags with the immutable `InterruptedUpdate` cleanup
descriptor/owner while CASing exact tagged `Updating → Reclaimable`.
`Reclaimable → Clearing` and every clear frontier retain that descriptor;
`CleanupResume` therefore recovers the original acknowledgement or complete
receipt/reclaim, holder drain, old/next generations, and next idempotent step
without consulting bytes being erased. A missing
descriptor, extent byte, reclaim, or no-acceptance proof retires the summary.
Its complete lifecycle and holder tuples must each fit one target-supported
native atomic word or one fixed per-CPU shard.
For an asynchronous-nondisruptive candidate only, loss transfer additionally
uses a preclaimed `StagingToLoss` descriptor/control, publishes its exact
staging source commitment, updates the sticky summary, and only after the
winning `Pending` generation is visible acquires and rechecks an exact summary
holder. It then publishes `DestinationWriting` and
claims exact `(Empty, loss_generation, None, None) → (Writing,
loss_generation, transfer_descriptor, transfer_owner, None)` for one fixed compact
`OperationalLossTransferPublication` slot. It copies the
capture, complete decision semantic identity/digest and product tag, logical
raw/source-set digests, entry-snapshot semantic identity/digest, machine
profile identity/hash, their canonical storage-independent core-evidence
manifest/digest, exact sticky-loss generation, and descriptor digest. Its
`canonical_body_digest` is explicitly the hash of those immutable semantic
fields with the digest field itself omitted; it excludes the publication ID,
lifecycle word, borrow word, and dependency word. The outer publication ID
hashes intended `Sealed`, slot/generation, that body digest, and the immutable
identity fields, so neither digest is cyclic or changed by later borrows. The
producer seals the compact publication before publishing transfer control
`DestinationSealed`, then releases the summary holder; a summary cleanup can
never erase a body still being copied.
`LossTransferred` may release raw staging
only after this exact compact publication is `Sealed` and a complete fault-
record graph using `OperationalLossRoot` has passed the same
`ReadyToAccept` + complete-hold + accepted-bit + `Live` gate against the
unchanged loss root. Acceptance publishes transfer control `Committed`; a cut
before it is resolved by the generic complete-forward or preaccept-cancel
predicate, never by treating the sticky summary alone as custody. The root
cross-checks that
whole manifest against the semantic core and explicitly records
that raw bytes are unavailable and can never form a `DecoderInput`. A local-
resume candidate, a containment/terminal case, compact-loss-pool exhaustion,
or failure to seal either loss object is terminal before any decision graph
accepts. A new slot generation cannot be reused until either an
operational copy owns the evidence or that loss transfer has succeeded. The
policy consumer acknowledges the exact stable loss generation before clearing
`Pending`; containment and terminal records are never eligible for this
degradation path.

The compact loss slot has its own exact-generation borrow/rehome lifecycle.
Acknowledgement of the mutable sticky summary is a separate policy operation;
it is neither a prerequisite for nor authority to reclaim this independently
sealed compact evidence source, and its acknowledgement need not outlive the
summary. The compact-source owner first
seals an authenticated `OperationalLossTransfer` custody receipt covering the
complete immutable compact publication at an independent destination, obtains
the uniquely registered generation-current
`CrashReclaim(OperationalLossTransfer)`, and closes its bounded dependency set.
Every live initial/derived graph and binding must be completely rehomed under a
complete independent custody receipt; authoritative revocation alone may
remove a redundant reference but may never delete the last complete evidence
copy. A single replacement does not suffice. Only after exact dependency-set
`Closing → Drained` and zero accepted bits, then borrow admission
`Open → Revoking → Drained` at zero, may the owner atomically replace the
original transfer tags with a prevalidated
`OperationalLossTransferReclaimDescriptor` and change `Sealed → Reclaimable`
at frontier `ReclaimCommitted`. The descriptor retains the exact complete-copy
receipt, source-specific reclaim, dependency-rehome receipts, old/next
generations, and clear recipe. Before changing one body or control byte, it
CASes the full tagged tuple `Reclaimable → Clearing` and advances the atomic
frontier before each idempotent clear/rekey step. Thus a cut in `Reclaimable` or
`Clearing` resumes only through `OperationalLossTransferReclaimPredicate`, not
from partially erased bytes. Only after verified clear, checked-nonwrapping
loss/borrow/dependency generation advances, and next zero-borrow/dependency
controls validate may it publish descriptor-/owner-free
`(Empty, next_loss_generation, None, None, None)` last. The receipt registration
cell and reclaim token remain held until that final publication, then clear in
their generic ordered teardown. Exhaustion retires the slot until a fresh protected
boot/CPU identity domain; it never aliases an older loss root.

A corrected-event storm can lose detail, but it cannot occupy the raw staging
slot permanently, overwrite terminal storage, or release an affected object.
A containment requirement and its evidence remain in the dedicated requirement
slot and are never dropped through `OperationalDropped`; only its optional
redacted notification may be lost/coalesced. `containment_notice_pending` is a
sticky wakeup hint for that case, not custody of the requirement or permission
to release the park/quarantine obligation.

## Context and forbidden dependency audit

The generated call graph must prove absence of:

- ordinary or recursive allocators;
- blocking/spinning locks whose owner may be interrupted;
- scheduler, IPC, console, filesystem, network, firmware, or general driver
  entry;
- pageable mappings or user-owned memory;
- lazy FP/vector state, stack unwinding, symbolization, sanitizers, profiling,
  tracing, and coverage hooks;
- cross-CPU rendezvous or an unbounded atomic retry;
- indirect calls outside a sealed target set; and
- panic helpers whose implementation is larger than the validated terminal
  leaf.

The code, data, mappings, source tables, and both normal and recursive stacks
are pre-fault pinned and measured. “Memory reserved” is not sufficient: the
profile must state cacheability, atomic support, accessibility at the entry
privilege, and DMA/IOMMU exposure.

## Concurrency and memory ordering

CPU-local single-writer storage avoids depending on cross-CPU atomic progress
for the first raw record. Release/acquire publication is valid only while the
target's coherent memory substrate remains functional. The record states that
assumption; a machine error affecting its cache, memory controller, or
interconnect may make the record unavailable or suspect.

CPU-local *storage* does not make a hardware source CPU-local. For a shared
Arm/RERI/platform bank, the sealed profile binds one owner and signal-route
generation plus the handoff/serialization contract established while healthy.
Only that owner may destructively acknowledge. A non-owner may preserve a
read-only observation and `software_reader_conflict`, but cannot clear the
source or claim acknowledgement; if exclusive routing cannot be proved, the
classifier takes the conservative/terminal rule.

Hardware register access ordering and memory publication ordering are separate
recipes. Compiler barriers do not replace device access ordering; an ISA memory
barrier does not itself make a record persistent across reset. The crash sink
adds any cache-clean, persistence-domain, or firmware handoff operation only
after local sealing.

## Failure analysis

| Failure | Required result |
| --- | --- |
| Unknown profile or source | Seal minimal frame and `unsupported_source`; never guess a register layout |
| Validity-dependent register absent | Leave field absent/unknown and retain source validity bits |
| Source overwritten during read | Use the bounded source protocol; on exhausted retry seal `overwritten_during_capture` |
| Fault before payload copy | Recursive guard records outer incarnation and first unfinished operation |
| Fault during acknowledgement | Keep individually sealed attempts, leave the set `AttemptsOpen` and acknowledgement `InProgress`/unknown, record the phase through the recursive path, and force terminal handling |
| Shared source observed by non-owner or stale route generation | Preserve read-only evidence and `software_reader_conflict`; do not invalidate/clear or claim acknowledgement; use conservative disposition |
| Operational ring full | For an eligible safe report, publish exact-generation `LossTransferred` then recycle staging; retain any containment requirement/park independently; transfer failure is terminal and never repurposes terminal storage |
| Terminal promotion lost to another CPU | Preserve CPU-local record and record bounded collision metadata |
| Release/acquire substrate suspect | Mark evidence integrity suspect; do not infer record absence or resume safety |
| Counter wraps | Refuse slot reuse without a new boot/crash generation; never compare bare sequence numbers |

## Verification and falsification

### Executable model

Model per-source/per-attempt publication, cross-source acknowledgement effects
and capture frontiers, final source-result-set publication, separate
acknowledgement, capture-time classification, operational copy/loss transfer,
terminal promotion, retention/recycle, and recursive entry. Check single ownership,
immutable sealed metadata and payload, generation rejection, no accepted
`WritingRaw`/`AttemptsOpen` set, operational/terminal independence, bounded transition
count, and the reachability of a terminal outcome from every injected failure.
Interleave every producer loss-summary update with consumer snapshot and
generation-matched CAS-clear; no newly published loss may disappear. Reject a
capture profile whenever one source's acknowledgement can mutate an unsealed
source and no finite nondestructive frontier exists.

### Static and binary checks

- prove stack use and call depth for each generated program;
- reject unexpected relocations, indirect branches, stack probes, compiler
  helpers, instrumentation, or pageable references in the linked image;
- inspect entry-to-seal disassembly and compare it with the approved operation
  list; and
- derive a maximum register count, raw bytes, retry count, and instructions
  from the exact profile artifact.

### Fault campaigns

Inject a nested fault before and after every primitive operation; every raw
validity combination; overwrite between source reads; full operational and
containment queues; simultaneous fatal events; stale generations; corrupted
length/checksum; stack guards; missing mappings; and acknowledgement faults.

Run separate layers of tests: fake-record injection validates software state
space; emulator traps validate entry control; ACPI/RERI record injection
validates handler routing; platform error injection validates more of the
hardware/firmware stack; real field faults remain a distinct evidence class.

The cut-point campaign must also:

- drive `capture_sequence` to its checked maximum and prove the CPU/boot
  incarnation is replaced or capture stops, never wraps;
- interrupt every ring-root and queue-root borrow registration, revocation,
  drain, clear/rekey, checked-generation advance, and final `Empty`
  publication, including exhaustion of each fixed holder bitmap;
- interrupt queue-receipt `(Empty → Writing → Sealed → Clearing →
  Empty(next generation))` before and after every CAS or body write, and prove
  no root becomes reusable while an old receipt generation is readable; and
- interrupt every raw-staging state, owner-tag claim, suspect-prefix borrow,
  full-extent receipt, source-specific reclaim CAS, dependency drain, and
  `Reclaimable → Clearing → Free(next)` edge; require either a proved
  never-accepted disposition or complete rehome of every accepted dependent;
  and
- race graph `ReadyToAccept`, continuation-hold acquisition, the accepted-bit
  CAS, dependency closing, staging release, ring export, and queue rehome; only
  a live accepted graph or an exact sealed-but-unaccepted abandonment may
  release its corresponding custody.

### Metrics

Record maximum instructions, cycles, stack high-water mark, bytes touched,
source and acknowledgement completion, retry/loss counts, terminal collision
rate, first-record seal rate, and outcome by entry context. Report distributions
and worst observed values per pinned profile; do not merge emulated and real
hardware results.

## Staged implementation

1. Implement a fake fixed source and CPU-local per-attempt seal followed by
   the unified exact-generation `Free → WritingRaw → AttemptsOpen →
   RawSetSealed` lifecycle, a sealed aggregate source-result/acknowledgement
   publication, and generated layout checks; exercise the sole authorized
   `Clearing → Free(next generation)` rearm rather than a separate retention
   flag.
2. Add a terminal promotion stub and recursion injection before any real RAS
   decoder.
3. Implement one x86 exception/MCA or one RISC-V trap/RERI profile with all
   unknown cases terminal.
4. Add the operational-copy and sticky-loss protocol outside entry.
5. Port to a materially different ISA and preserve the same semantic test
   suite while replacing the access program.
6. Admit one nonterminal rule at a time only after the classifier's full
   postcondition is testable.

## Alternatives rejected

- **Write directly into a shared ring.** Corrected storms and nested writers
  can consume or overwrite the only fatal record.
- **Decode while reading hardware.** Decoder complexity, variable-length
  parsing, and profile bugs enlarge the irrecoverable entry path.
- **Retry until a coherent record appears.** A continuously changing or broken
  source turns the fault path into an unbounded loop.
- **Use a global lock to name the first fault.** The interrupted owner or
  damaged coherence substrate can make capture impossible, and “first
  publisher” still is not “first physical error.”
- **Call the normal panic/logger stack.** Those paths may allocate, lock,
  recurse, or depend on the subsystem that failed.

## Unresolved questions

- Which exact first CPU and board profile supplies the source list and
  measurable worst-case program?
- Can its CPU-local reserved memory be excluded from every enabled DMA
  requester and retained across the chosen reset class?
- Which architecture/compiler mechanism best enforces the approved no-
  instrumentation call graph?
- Is one RERI reread within budget, or should every overwrite-during-read become
  immediate uncertainty on the first target?
- How is evidence integrity labeled when the reporting source names the cache
  or memory holding the slot as affected?

## Connections

- [Architecture faults and diagnostics](../architecture-faults-and-diagnostics.md)
- [Privileged entry, exit, and execution context](../privileged-entry-exit-and-execution-context.md)
- [Fault decoder](fault-decoder.md)
- [Containment classifier and promotion](containment-classifier-and-promotion.md)
- [Double-fault guard](double-fault-guard.md)
- [Observability and crash evidence](../../minimal-privileged-kernel-components/observability-and-crash-evidence.md)
