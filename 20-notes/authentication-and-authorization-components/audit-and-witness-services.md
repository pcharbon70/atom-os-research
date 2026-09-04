---
title: "Audit and witness services"
kind: note
created: "2026-09-04"
maturity: developing
tags:
  - audit
  - logging
  - security
  - transparency
  - witnesses
aliases:
  - "Security audit service"
  - "Tamper-evident audit witnesses"
---

# Audit and witness services

The recommended design composes **bounded durable local admission,
forward-integrity producer streams, append-only Merkle segment commitments,
and independent witnesses**. Producers receive append-only capability; query,
retention, deletion, encryption keys, and witness signing remain separate.
The system claims tamper evidence and gap detection under stated assumptions,
not that every event is true or that a compromised producer emitted everything
it should.

This is component 12 of the [authentication and authorization service
set](README.md).

## Question, scope, and operational standard

> How can Atom preserve useful, privacy-conscious evidence of authorization
and effects across compromise, crash, partition, truncation, equivocation, and
storage exhaustion without making a remote log service part of every critical
effect's synchronous availability path?

Acceptance requires:

- every producer has a kernel-authenticated identity, boot epoch, monotonic
  sequence, append-only capability, and quota, while forward-secure chain-key
  state stays behind a confined key-service operation facet;
- events bind request/idempotency, subject/current actor, action, resource
  generation/version, decision/grant digests, policy/evidence epochs,
  enforcement point, and intent/outcome/uncertainty;
- critical effects durably admit an intent locally before invocation and later
  correlate a committed or indeterminate outcome;
- segments are sealed under signed roots, incorporated into an append-only
  Merkle structure, and committed to independent witnesses with verifiable
  inclusion and consistency;
- sequence gaps, spool loss, clock uncertainty, witness lag, retention, and
  cryptographic erasure are explicit records, never silent deletion;
- logs exclude bearer tokens, private keys, raw secrets, and unnecessary
  sensitive attributes;
- each action class defines fail-closed, bounded-local-spool, or emergency
  behavior when durable audit is unavailable; and
- log floods cannot consume all CPU, memory, storage, or emergency-control
  capacity.

## Evidence and synthesis

[Schneier and Kelsey](../../30-sources/schneier-kelsey-1999-secure-audit-logs.md)
provide forward-integrity key evolution and periodic commitment to a trusted
machine, while explicitly leaving producer truth/completeness and post-
compromise records outside the guarantee. [Signed
syslog](../../30-sources/kelsey-et-al-2010-signed-syslog-messages.md) contributes
origin authentication, reboot-session identifiers, sequencing, missing-message
detection, and collector-flooding threats; its dated cryptographic suite is not
an Atom choice.

[Crosby and
Wallach](../../30-sources/crosby-wallach-2009-tamper-evident-logging.md)
demonstrate logarithmic inclusion/consistency proofs and authenticated search
on a large trace. [Certificate Transparency
v2](../../30-sources/laurie-et-al-2021-certificate-transparency-v2.md) specifies
signed tree heads and independent monitor/auditor roles while exposing split-
view and maximum-merge-delay assumptions. [NIST SP
800-92](../../30-sources/kent-souppaya-2006-log-management.md) supports tiered
collection, local buffering, redundancy, retention, and treating
confidentiality/availability as well as integrity.

[ARIES](../../30-sources/mohan-et-al-1992-aries.md) supplies a crash-recovery
discipline—write-ahead intent, explicit commit, ordered identifiers, restart
analysis/redo/undo—but a database WAL cannot make arbitrary external device or
network effects atomic. Atom's intent/outcome model is an adaptation with
explicit indeterminate reconciliation.

## Authority and trust-domain split

- Producers can append only to their own stream and cannot read, rewrite, or
  delete history.
- Local collectors admit and seal bounded records but cannot invoke the
  audited resource.
- Tree builders can aggregate sealed segments but cannot forge producer chains.
- Witnesses run in different protection—and preferably operator/machine—trust
  domains and can sign/anchor heads but cannot produce events.
- Query/export is separately authorized and redacted.
- Retention deletion and audit-encryption-key destruction require independent
  policy/approvals and leave verifiable commitments/tombstones.

No general administrator owns all of these powers.

## Event and segment model

```text
AuditEvent {
    producer_domain_generation,
    boot_epoch_and_sequence,
    event_schema,
    request_and_idempotency_id,
    subject_and_current_actor,
    action_and_resource_generation_version,
    policy_relation_attribute_session_epochs,
    decision_and_grant_digest,
    enforcement_point,
    intent | outcome | uncertainty | loss_marker,
    monotonic_time_and_optional_wall_time_confidence,
    previous_chain_digest,
    disclosure_class,
}

SealedSegment {
    producer_and_boot_epoch,
    first_and_last_sequence,
    event_count_and_gap_markers,
    chain_terminal,
    content_commitment,
    encryption_key_generation,
    collector_signature,
}

WitnessReceipt {
    tree_log_id,
    tree_size_and_root,
    prior_root_reference,
    witnessed_at,
    witness_id_and_signature,
}
```

Per-producer sequence and boot epoch establish order; wall time is contextual
and can be uncertain. Grant digests, not transferable grant bytes, enter logs.
Sensitive payload fields are encrypted/committed under separate disclosure
authority or omitted.

## Intent, outcome, and effect boundary

For a critical effect:

```text
authorize -> durable_intent -> effect_attempted
          -> committed_outcome | indeterminate -> reconciliation
```

The intent records the exact admitted request and idempotency key before the
resource acts. If the resource can atomically commit its own state and outcome,
it does so. For external/irreversible effects, crash can leave uncertainty; the
reconciler queries device/network state or records that truth is unknowable.
The log never fabricates a successful outcome to close a pair.

## Forward integrity and witnessing

Producers submit bounded events through append-only capabilities; they never
hold chain-key bytes in a managed heap. A confined native operation facet of
the [key and secret service](key-and-secret-service.md) evolves chain keys and
destroys prior states after bounded groups of events. Compromise of the current
key can forge future events but should not enable rewriting already sealed,
independently committed history. Segments enter a Merkle tree; inclusion proves
membership and consistency proves append-only extension relative to a
previously observed root.

A single signed tree head can equivocate. Multiple independent witnesses and
cross-witness comparison/gossip are required to expose split views. The system
records maximum seal, merge, and witness delays and the highest witnessed tree
size. A witness outage does not invalidate already witnessed history but may
stop new high-risk effects after the local spool/lag bound.

## OTP-like protocol and supervision

```text
append_intent(producer_cap, event, durability_class, deadline)
  -> durable_receipt | busy | unavailable
append_outcome(intent_receipt, result) -> correlated_receipt | typed_error
seal(stream, through_sequence) -> segment_ref
witness(tree_head, prior_head) -> witness_receipt | inconsistent | unavailable
query(scope, predicate, disclosure_cap, budget) -> proved_redacted_results
```

Admission, local spool, segment seal, tree build, witness client, query, and
reconciliation are separate supervised children. Reserved preallocated buffers
and storage quotas keep lock/revoke/recovery lanes usable. Restart scans durable
sequence/chain state, records any interrupted tail, and never continues under a
reused boot/key epoch.

## Failure, attack, and privacy analysis

| Hazard | Required handling |
| --- | --- |
| Producer lies or omits | State limitation explicitly; independent observations where possible |
| Current signing key compromised | Forward key evolution protects earlier sealed entries only |
| Tail truncation before witness | Local durable segment, bounded witness delay, independent root retention |
| Split-view log | Multiple witnesses and head comparison/gossip |
| Boot/key rollback | Protected boot epoch/high-water and witness continuity |
| Spool exhaustion/log flood | Per-producer quotas, schemas, aggregation, reserved critical capacity, explicit loss marker |
| Audit outage | Per-action fail policy; never silently drop and allow |
| Sensitive-data leakage | Data minimization, field commitments/encryption, separate query keys, retention |
| Intent without outcome | Reconciliation and explicit indeterminate state |

## Verification and evaluation plan

- Power-cut/crash at sequence allocation, local WAL, intent receipt, effect,
  outcome, key evolution, seal, tree merge, witness, and retention boundaries.
- Delete, truncate, reorder, duplicate, replay, and mutate records/segments;
  independently verify chain, inclusion, and consistency proofs.
- Compromise an old erased key and current key; test exactly which history can
  be forged under the documented claim.
- Present divergent roots to witnesses/monitors and test cross-witness
  detection and partition healing.
- Saturate producers, crypto, spool, tree builder, witness link, query, and
  storage; assert quotas/fairness and emergency lane availability.
- Scan valid and failure-path logs/dumps for secrets, tokens, PII, sensitive
  attributes, and authorization-graph leakage.
- Reconcile intent/outcome pairs for idempotent local state, external network,
  and irreversible device operations; report unknowable cases honestly.

## Staged implementation

1. Local per-producer durable sequences and intent/outcome records with quotas.
2. Forward-evolving chain and sealed segments with crash recovery.
3. Merkle tree, independent verifier, and one external witness.
4. Multi-witness comparison, proved queries, retention, and cryptographic
   erasure.
5. Action-specific audit outage policies proven with end-to-end resource tests.

## Supported decisions and open questions

Supported: append-only capability separation; forward integrity plus external
witnesses; durable intent before critical effects; explicit gaps and
uncertainty; no truth/completeness overclaim.

Open: forward-secure primitive, witness protocol/topology/quorum, trusted time,
anti-rollback anchor, schema/privacy/retention law, cryptographic erasure, and
safe action behavior at spool/witness exhaustion.

## Connections

- [Grant compiler and issuer](grant-compiler-and-issuer.md)
- [Key and secret service](key-and-secret-service.md)
- [Revocation and epoch service](revocation-and-epoch-service.md)
- [Recovery coordinator](recovery-coordinator.md)
- [Update and release service](update-and-release-service.md)
- [Main authentication and authorization synthesis](../authentication-and-authorization-across-the-five-layer-architecture.md)

## Sources

- [Secure audit logs](../../30-sources/schneier-kelsey-1999-secure-audit-logs.md)
- [Signed syslog messages](../../30-sources/kelsey-et-al-2010-signed-syslog-messages.md)
- [Efficient tamper-evident logging](../../30-sources/crosby-wallach-2009-tamper-evident-logging.md)
- [Certificate Transparency v2](../../30-sources/laurie-et-al-2021-certificate-transparency-v2.md)
- [NIST log-management guidance](../../30-sources/kent-souppaya-2006-log-management.md)
- [ARIES](../../30-sources/mohan-et-al-1992-aries.md)
