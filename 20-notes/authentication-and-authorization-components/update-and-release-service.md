---
title: "Update and release service"
kind: note
created: "2026-09-04"
maturity: developing
tags:
  - anti-rollback
  - software-supply-chain
  - software-update
  - security
aliases:
  - "Secure update service"
  - "Release verification service"
---

# Update and release service

The recommended design separates **release authoring/signing from node-side
verification, staging, trial activation, independent health, commitment, and
recovery**. The online updater has no root signing key and no arbitrary live-
filesystem or kernel write. It can write only a typed inactive slot/content-
addressed store and request a lower-layer boot verifier to trial an already
authorized artifact.

This is component 14 of the [authentication and authorization service
set](README.md).

## Question, scope, and operational standard

> How can Atom accept software, firmware, policy, configuration, and state-
schema releases despite compromised mirrors or online keys, interrupted
downloads, rollback/freeze/mix-and-match attacks, malicious bundles, power
loss, incompatible migrations, and false self-reported health?

Acceptance requires:

- root, targets, snapshot/release, timestamp/freshness, provenance, rollout,
  install, health, and recovery powers are separate and thresholded according
  to impact;
- a client verifies sequential root rotation, signatures/thresholds, versions,
  expiry, hashes, lengths, repository consistency, delegation bounds, and
  target applicability before staging;
- an approved supply-chain provenance predicate identifies authorized builders,
  steps, materials, products, and inspections rather than trusting only the
  final signature;
- every release pins hardware/model, boot/runtime/BEAM compatibility, service
  dependencies, policy/schema versions, state migration, rollback boundary,
  and resource budgets;
- downloads, metadata chains, delegation visits, decompression, disk use, and
  retries are bounded before expensive work or writes;
- activation uses immutable generations/inactive slots, explicit quiescence,
  trial boot/service start, and independent health evidence;
- operational rollback selects only a still-authorized generation and never
  decreases security high-water state; and
- power loss or updater compromise cannot modify the boot trust root, live
  kernel, identity/audit/recovery roots, or declare itself healthy.

## Evidence and synthesis

[The Update Framework
paper](../../30-sources/samuel-et-al-2010-tuf.md) distinguishes content,
timeliness, and repository-consistency authentication and introduces role/
threshold separation. The current [TUF
specification](../../30-sources/tuf-project-2026-specification-1-0-36.md)
details sequential root rotation, metadata ordering, target verification, and
client resource bounds; its scope ends before installation.

[in-toto](../../30-sources/torres-arias-et-al-2019-in-toto.md) verifies
authorized supply-chain steps and artifacts, complementing delivery metadata.
[Uptane](../../30-sources/uptane-community-2023-standard-2-1-0.md) adds target-
specific inventory/version reports, Director/Image repository separation, and
embedded/intermittent attack handling. [SUIT architecture](../../30-sources/moran-et-al-2021-firmware-update-architecture.md)
separates author, operator, status tracker, consumer, server, and boot verifier;
the [SUIT information
model](../../30-sources/moran-et-al-2022-firmware-manifest-information-model.md)
makes applicability, dependencies, component IDs, payload bounds, sequence,
and secure time explicit.

[NixOS](../../30-sources/dolstra-et-al-2008-nixos.md) provides immutable store
paths/generations and atomic profile switching, but activation and mutable data
are not automatically transactional. These sources motivate the composition;
they do not prove an Atom multi-component state migration safe.

## Authority split

Release authoring can assemble a candidate but cannot sign all roles. Offline
or independently controlled keys authorize root and high-impact targets.
Online freshness keys are narrow and replaceable. Provenance functionaries
sign only their declared supply-chain step.

The node updater holds trusted public metadata/high-water state, bounded fetch
and cache, content-addressed staging, a typed inactive-slot writer, trial-
activation request, and audit append. It does not hold signing roots, arbitrary
live writes, unilateral high-water reset, or identity/audit/recovery keys.

The lower-layer boot verifier independently rechecks the selected boot
artifact. Health evidence comes from an independently authorized monitor or
test workload; the updated component cannot self-certify success.

## Objects

```text
ReleasePlan {
    release_id_and_sequence,
    trusted_root_and_metadata_set_digests,
    provenance_layout_and_link_digests,
    target_descriptors,
    device_service_inventory_predicate,
    hardware_boot_runtime_BEAM_compatibility,
    dependency_closure,
    policy_configuration_and_state_schema_versions,
    migration_and_rollback_boundary,
    activation_cohort_and_deadlines,
    health_predicate_and_authority,
}

TargetDescriptor {
    component_id,
    artifact_digest_and_length,
    type_and_decompression_bound,
    vendor_class_hardware_applicability,
    prerequisite_versions,
    installation_slot_or_store_namespace,
}

ActivationRecord {
    old_and_trial_generation,
    plan_digest,
    quiescence_result,
    state_migration_checkpoint,
    boot_or_service_attempt,
    independent_health_result,
    committed_high_water_or_rollback,
}
```

## Verification, staging, and activation state machine

```text
discovered
 -> root_updated_sequentially_and_persisted
 -> timestamp_fresh
 -> snapshot_consistent
 -> targets_and_delegations_valid
 -> provenance_accepted
 -> applicability_and_dependency_closed
 -> bounded_download_verified
 -> inactive_generation_staged
 -> quiesced_and_migration_prepared
 -> trial_activated
 -> independent_health_pass
 -> committed_and_fenced
```

Any step can reject or leave a resumable staged object. After the point of no
return for an irreversible state migration, automatic binary rollback may be
unsafe; the plan must instead specify forward recovery or quarantine. A
rollback request is a new higher-sequence signed release selecting older bytes,
not a decrement of trusted metadata or vulnerability high-water.

Root rotation accepts version `N+1` sequentially under both the old and new
required thresholds and persists it before continuing. Expiry depends on a
declared secure-time profile; where no trustworthy wall clock exists, a
monotonic release sequence only rejects metadata older than state already
seen—it cannot detect a withheld current release or freeze attack. A bounded
offline procedure can cap accepted exposure and eventually force an explicit
recovery ceremony, but cannot claim freshness without an authenticated
freshness input.

## OTP-like protocol and supervision

```text
check(metadata_set, inventory_snapshot, resource_budget, deadline)
  -> verified_plan | typed_error
stage(plan, source, idempotency, budget) -> staged_generation | progress | error
activate(staged, approvals, expected_high_water)
  -> trial_ref | indeterminate | typed_error
report_health(trial_ref, monitor_evidence) -> commit | rollback | quarantine
status(release_ref) -> exact_stage_and_recovery_action
```

Metadata/parser, downloader, provenance, applicability, stage writer,
quiescence/migration, trial coordinator, and health adapter are separate
supervised children. A parser or network worker cannot write a slot. Restart
reads durable stage records and content digests; it never repeats a non-
idempotent migration without its checkpoint protocol.

## Failure, attack, and overload analysis

| Hazard | Required handling |
| --- | --- |
| Mirror/network compromise | Verify all metadata/artifact bytes; availability remains untrusted |
| Online signing key compromise | Narrow role, threshold/delegation, expiry, root recovery |
| Freeze/clock rollback | Trusted time or authenticated freshness input; offline sequence rejects only previously seen rollback and must expire into bounded recovery |
| Rollback/fast-forward/mix-and-match | Protected high-water, snapshot versions/hashes, sequence bounds |
| Endless data/decompression/delegation | Predeclared byte/ratio/role/depth/time/disk budgets |
| Partial multi-component activation | Dependency-closed release, explicit ordering/quiescence, trial generation |
| False self-health | Independent monitor/attestation and stable observation window |
| Irreversible migration | Declared point of no return, forward recovery/quarantine |
| Fleet thundering herd | Canaries/cohorts, randomized backoff, quotas, content cache, pause authority |
| Updater compromise | Typed inactive writer; lower-layer boot revalidation; no signing roots |

## Verification and evaluation plan

- Run TUF/Uptane/SUIT conformance and attack corpora: key thresholds, sequential
  root rotation, expiry, rollback, freeze, fast-forward, mix-and-match,
  delegation cycles, endless data, wrong artifact, and wrong target.
- Fuzz every metadata/provenance/manifest/archive/parser with byte, nesting,
  count, decompression, disk, and deadline limits.
- Compromise one signing role/functionary/mirror/updater/health source at a time
  and prove maximum install authority.
- Power-cut at every metadata persist, download, stage, quiescence, migration,
  slot switch, boot, health, commit, and rollback point.
- Test hardware/model/boot/runtime/BEAM/OTP/policy/schema/dependency mismatch and
  partially available bundles.
- Exercise canary, cohort pause, network partition, disk pressure, recovery
  image, root-key loss, and self-update of the verifier/updater.
- Measure download/stage/activation/rollback time, downtime, state loss,
  validation resource ceilings, and fleet peak load.

## Staged implementation

1. TUF-profiled artifacts into a content-addressed inactive store with protected
   high-water.
2. Immutable service generations, quiescence, trial start, independent health,
   and rollback.
3. in-toto provenance and full compatibility/dependency manifest.
4. State migration checkpoints, cohort/canary rollout, and offline recovery.
5. Firmware/kernel update only after a small lower-layer boot verifier and
   recovery root are specified and tested.

## Supported decisions and open questions

Supported: signer/installer split; role/threshold metadata; provenance plus
delivery; exact applicability; inactive staging; independent health; security
high-water never rolls back.

Open: exact TUF/SUIT profile, trusted time/counter, root recovery, BEAM/OTP
compatibility closure, atomic multi-service state migration, independent
health authority, fleet consensus, and safe updater/boot-verifier self-update.

## Connections

- [Key and secret service](key-and-secret-service.md)
- [Audit and witness services](audit-and-witness-services.md)
- [Recovery coordinator](recovery-coordinator.md)
- [RATS Verifier and Appraisal Policy](rats-verifier-and-appraisal-policy.md)
- [OTP-like system services layer](../otp-like-system-services-layer.md)

## Sources

- [The Update Framework paper](../../30-sources/samuel-et-al-2010-tuf.md)
- [TUF specification](../../30-sources/tuf-project-2026-specification-1-0-36.md)
- [in-toto](../../30-sources/torres-arias-et-al-2019-in-toto.md)
- [Uptane 2.1.0](../../30-sources/uptane-community-2023-standard-2-1-0.md)
- [Firmware update architecture](../../30-sources/moran-et-al-2021-firmware-update-architecture.md)
- [Firmware manifest information model](../../30-sources/moran-et-al-2022-firmware-manifest-information-model.md)
- [NixOS](../../30-sources/dolstra-et-al-2008-nixos.md)
