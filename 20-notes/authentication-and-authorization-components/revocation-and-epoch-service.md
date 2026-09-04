---
title: "Revocation and epoch service"
kind: note
created: "2026-09-04"
maturity: developing
tags:
  - authorization
  - distributed-systems
  - revocation
  - security
aliases:
  - "Authority revocation service"
---

# Revocation and epoch service

The recommended component is a **scoped revocation transaction and ordered
epoch-distribution service**. It distinguishes authority committed, invalidation
distributed, new admission blocked, in-flight work quiesced, sensitive state
sanitized, and lineage retired. “Revoked” is not one instantaneous global bit.

This is component 10 of the [authentication and authorization service
set](README.md). Layer 4 decides and distributes revocation; Layer 2 performs
local capability-tree/object-generation checks and bounded revoke traversal.

## Question, scope, and operational standard

> How can Atom stop new uses, bound remote stale use, handle already-running
> effects, and prevent authority resurrection across partitions, crashes,
> rollbacks, cloned images, and object reuse?

Acceptance requires:

- separate object, session, relationship, issuer, trust-bundle, boot, and
  lineage epochs with scoped mutation authority;
- each revocation has a unique transaction, reason, authority, effective
  revision, ordered event sequence, consumer watermarks, and quiescence result;
- receivers validate issuer/audience/sequence, apply events idempotently, detect
  gaps, and replace uncertain incremental state from an authenticated snapshot;
- local admission checks current object generation and revocation anchor in the
  same transaction as accepting the operation;
- critical distributed operations require a minimum watermark or live
  introspection, while offline grants have a declared maximum lifetime and risk
  class;
- epochs/high-water state survive restart and resist rollback, or a fresh boot
  epoch invalidates all old-instance grants;
- service/unreachable responses are `unavailable`, never “inactive” or
  “revoked”; and
- measured maximum unauthorized-use windows and in-flight semantics are stated
  per action class.

## Evidence and synthesis

[OAuth token
revocation](../../30-sources/lodderstedt-et-al-2013-oauth-token-revocation.md)
both asks for invalidation and acknowledges propagation delay; it explicitly
makes service-unavailable different from success. [Token
introspection](../../30-sources/richer-2015-oauth-token-introspection.md) shows
the local-validation versus online-state trade-off and that cache lifetime
creates a revocation window. [Security Event
Token](../../30-sources/hunt-et-al-2018-security-event-token.md) treats a
security event as an issuer statement rather than an executable command and
does not use clocks alone as event order.

[Zanzibar](../../30-sources/pang-et-al-2019-zanzibar.md) contributes causal
revisions for relationship freshness. The [seL4 reference
manual](../../30-sources/sel4-foundation-2026-reference-manual.md) contributes
local capability derivation and descendant revoke semantics; an Atom kernel
needs its own bounded traversal and proof. [EAT](../../30-sources/lundblade-et-al-2025-entity-attestation-token.md)
provides boot-count/seed claim precedents but not trustworthy monotonic storage.

## Authority boundary

The service holds only scoped epoch/revocation-anchor mutation, authenticated
event/snapshot publication, introspection, watermark tracking, and audit append.
It cannot issue grants, edit policy/relationships/attributes, disclose secrets,
or cancel arbitrary operations without a named revocation relation.

Because it can deny service, it is a powerful availability root. Partition it
by realm and revocation scope, require threshold authority for global issuer or
root changes, and reserve capacity for urgent invalidations.

## State objects

```text
RevocationTransaction {
    transaction_id,
    authority_and_scope,
    target_anchor_or_epoch,
    reason,
    previous_and_new_revision,
    effective_sequence,
    requested_in_flight_policy,
    initiator_and_approvals,
}

InvalidationEvent {
    issuer,
    audience_or_stream,
    sequence,
    transaction_digest,
    changed_epochs_and_anchors,
    issued_at,
    snapshot_base_revision,
}

ConsumerWatermark {
    consumer_generation,
    stream,
    highest_contiguous_sequence,
    applied_epoch_snapshot_digest,
    acknowledged_at,
}
```

Sequence and epoch fields are wide, nonwrapping counters. Restoring state below
the protected high-water makes the service restricted. A cloned disk image
receives a distinct boot/node epoch; it cannot continue the original node's
leases without an explicit migration protocol.

## Revocation lifecycle

```text
requested
  -> authority_committed
  -> distribution_started

for each required enforcement point p:
  delivered(p, watermark)
    -> enforced(p, no_new_admission)
    -> quiesced(p, in_flight ended/cancelled/declared irreversible)
    -> sanitization_result(p, confirmed | not_applicable | uncertain_or_failed)

required_progress_vector_satisfied
  -> retired_or_quarantined
```

Progress is a monotonic partial order, not one global serial chain: one PEP may
enforce before another has received the invalidation, and quiescence and
sanitization advance independently by resource. The service therefore reports
a vector of per-enforcement-point watermarks and stages plus the exact
predicate used for any aggregate result, never one misleading global
completion flag. Copied data and irreversible effects are not recallable;
`not_applicable`, `uncertain`, or `failed` sanitization remains visible and
forces the action profile's quarantine or recovery rule rather than fabricated
success.

Local capability revocation advances an anchor and begins bounded descendant
traversal. Admission consults the anchor immediately; traversal reclaims
representations later. Object deletion advances generation before memory/name
reuse. Running operations obey a declared policy: complete, cooperative
cancel, forcibly terminate domain, compensate/reconcile, or irreversibly
already committed.

Remote grants combine short expiry with ordered invalidations. Critical PEPs
may introspect a grant digest under authenticated access. Introspection caches
declare their maximum age; that age is part of the published exposure bound.

## Partition and offline semantics

During loss of quorum or an event gap:

- no revocation mutation is reported committed;
- critical PEPs requiring a newer watermark stop new admission;
- low-risk actions may use a cached snapshot only within an explicit freshness
  policy and existing grant expiry;
- offline/safety authority remains usable only under its predeclared scope and
  cannot promise immediate revocation or global consumptive quota; and
- reconnect first obtains an authenticated snapshot, then resumes ordered
  events.

No policy says “revocation service failed, therefore allow.”

## OTP-like protocol and supervision

```text
revoke(scope, target, reason, approvals, idempotency, deadline)
  -> {committed, transaction, revision} | indeterminate | typed_error
status(transaction) -> stage_vector_and_watermarks
snapshot(stream, minimum_revision) -> authenticated_snapshot | stale
introspect(grant_digest, audience, minimum_epoch)
  -> active | inactive | indeterminate | unavailable
ack(stream, contiguous_sequence, snapshot_digest) -> accepted | gap
```

Commit, publisher, snapshot, introspection, traversal, and quiescence workers
are separate supervised children. Publisher failure cannot roll back committed
authority; it increases lag and may stop dependent operations. Batching and
deduplication preserve a reserved emergency lane during revocation storms.

## Failure and attack analysis

| Hazard | Required handling |
| --- | --- |
| Lost/duplicate/out-of-order event | Idempotent transaction IDs, contiguous sequence, gap snapshot |
| Stale introspection cache | Maximum age in action policy and measured exposure |
| Epoch rollback/wrap | Protected high-water, nonwrapping representation, fresh boot epoch |
| Parent revoke misses child | Explicit lineage DAG/derivation tree and completeness tests |
| Already-running irreversible effect | Report committed/indeterminate truth; reconcile, never pretend clawback |
| Revoker compromise | Scope partition, separated approvals, audit/witness, recovery epoch |
| Revocation storm | Reserved resources, batch/deduplicate, per-realm fairness |
| Privacy/token scanning | Authenticate introspector and return minimal inactive response |

## Verification and evaluation plan

- Drop, duplicate, reorder, delay, and corrupt invalidation events; force
  sequence gaps and snapshot recovery across restarts and leader changes.
- Partition every producer/consumer pair and measure maximum unauthorized-use
  window for each action class against the stated SLA.
- Revoke parent/child/sibling lineages and verify exact descendants stop while
  unrelated grants remain; interrupt kernel traversal at every step.
- Roll clocks, boot counters, epochs, disks, and VM snapshots backward; clone a
  node and attempt old grants.
- Race revoke with admission, one-shot consumption, long-running operation,
  object delete/recreate, session logout, and issuer rotation.
- Saturate event, introspection, traversal, and acknowledgement paths; verify
  reserved revocation capacity and tenant fairness.

## Staged implementation

1. Single-node object/session epochs and local capability anchor checks.
2. Durable high-water state, bounded traversal, explicit in-flight outcomes.
3. Ordered event stream, consumer watermarks, and authenticated snapshots.
4. Critical introspection and measured partition SLAs.
5. Offline profiles only after formal exposure and quota limitations are
   accepted.

## Supported decisions and open questions

Supported: staged revocation; epochs/generations at admission; authenticated
ordered events; gap recovery; service failure is not success; short remote
leases.

Open: exact per-action SLAs, monotonic hardware, kernel traversal/cancellation,
lineage scale, snapshot protocol, hostile-replica model, and semantics for each
irreversible external device/network effect.

## Connections

- [Grant compiler and issuer](grant-compiler-and-issuer.md)
- [Session service](session-service.md)
- [Relationship authority](relationship-authority.md)
- [Audit and witness services](audit-and-witness-services.md)
- [Main authentication and authorization synthesis](../authentication-and-authorization-across-the-five-layer-architecture.md)

## Sources

- [OAuth token revocation](../../30-sources/lodderstedt-et-al-2013-oauth-token-revocation.md)
- [OAuth token introspection](../../30-sources/richer-2015-oauth-token-introspection.md)
- [Security Event Token](../../30-sources/hunt-et-al-2018-security-event-token.md)
- [Zanzibar](../../30-sources/pang-et-al-2019-zanzibar.md)
- [seL4 reference manual](../../30-sources/sel4-foundation-2026-reference-manual.md)
- [Entity Attestation Token](../../30-sources/lundblade-et-al-2025-entity-attestation-token.md)
