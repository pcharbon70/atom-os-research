---
title: "Relationship authority"
kind: note
created: "2026-09-04"
maturity: developing
tags:
  - authorization
  - distributed-systems
  - rebac
  - relationships
  - security
aliases:
  - "Relationship authorization store"
---

# Relationship authority

The recommended component is a **realm-scoped, versioned relationship graph
with causally constrained reads**. It stores authenticated ownership,
membership, sharing, delegation, and revocation facts under immutable model
versions. A check returns a relation result plus the exact model and commit
revision; it does not issue a grant or touch the protected object.

This is component 6 of the [authentication and authorization service
set](README.md).

## Question, scope, and operational standard

> How can Atom answer relationship questions across replicas without stale
> removals, model skew, object-ID reuse, recursive explosion, or an authorization
> graph that becomes a universal resource authority?

The service is acceptable only when:

- every tuple includes tenant/realm, object type/id/generation, relation,
  subject type/id or userset, model ID, provenance, and commit revision;
- every mutation is authenticated and authorized, schema-validated,
  idempotent, quorum-committed, and represented by a revisioned record or
  tombstone;
- a check pins an immutable model and can require at least a caller-supplied
  causal revision;
- a replica unable to meet freshness returns `stale` or `indeterminate`, never
  a best-effort boolean disguised as current;
- traversal depth, fan-out, intermediate set size, CPU, memory, and deadline
  are bounded per realm and request;
- caches include model, object generation, tuple revision/watermark, and every
  negative/exclusion dependency;
- query and list interfaces are authorized because object existence and
  membership are sensitive; and
- a storage, consensus, watcher, or model-migration failure cannot widen
  authority.

## Evidence and synthesis

[Zanzibar](../../30-sources/pang-et-al-2019-zanzibar.md) supplies relation
tuples, set operations, opaque consistency tokens, and the “new enemy” example:
authorization following a content/ACL mutation may need at least the causal
revision of that mutation. Its Google/Spanner setting does not establish Atom's
storage or effect-atomicity design.

[Chubby](../../30-sources/burrows-2006-chubby.md) provides engineering
precedents for a small replicated metadata service, cache invalidation,
sessions, generations, and fencing external users rather than trusting an old
lock holder. [Raft](../../30-sources/ongaro-ousterhout-2014-raft.md) defines a
crash-fault replicated log and term/index ordering; it neither deduplicates
client effects nor tolerates Byzantine peers.

[The NIST RBAC
model](../../30-sources/sandhu-et-al-2000-nist-rbac-model.md) separates users,
roles, permissions, sessions, hierarchy, and separation-of-duty constraints.
Atom uses those as possible graph/policy inputs, not as ambient kernel roles.

## Authority boundary

The authority runs per tenant or security realm in a distinct protected domain.
It holds only tuple mutation/query, consensus-peer, immutable model,
snapshot/watch, and audit-append capabilities.

It does not hold protected-resource capabilities, credential or attribute
roots, grant-signing authority, policy-authoring rights, or audit deletion.
Writers receive narrow relation- and object-scope capabilities; the service
cannot infer write authority from membership in the graph it is changing.

## Data and model objects

```text
RelationTuple {
    realm,
    object_type,
    object_id,
    object_generation,
    relation,
    subject_type,
    subject_id,
    optional_subject_relation,
}

MutationRecord {
    tuple_or_tombstone,
    immutable_model_id,
    writer_principal_and_actor,
    authorization_ref,
    idempotency_key,
    commit_revision,
    causal_token,
    provenance,
}

RelationResult {
    member | not_member | indeterminate,
    model_id,
    evaluated_revision,
    dependency_digest,
    bounded_explanation,
}
```

Object generation prevents delete/recreate from reviving an old share. Logical
names resolve to a generation before tuple evaluation. Exclusion, deny, and
set-difference dependencies are retained in cache keys; absence at an old
revision is not necessarily conservative.

## Model and tuple lifecycle

Authorization models follow:

```text
staged -> schema_validated -> differential_tested -> shadowed -> active
       -> retired
```

An active model is immutable. Migration writes tuples valid under a named new
model, evaluates old/new in shadow, and atomically advances the realm's active
model epoch only after invariants pass. Rollback requires a newly authorized
higher activation epoch, not reuse of an old epoch.

Tuple mutation follows:

```text
received -> writer_authorized -> validated -> consensus_committed(revision)
         -> visible -> watched/checkpointed
```

Deletion commits a tombstone. A dependent content operation persists the
returned causal token beside its object metadata. Later authorization can
request `minimum_revision = content.authorization_revision` to prevent the
new-enemy schedule.

## Query and watch protocol

```text
check(expected_active_model_revision, tuple_query, minimum_revision,
      budget, deadline)
  -> member(revision, proof) | not_member(revision, proof)
   | stale(current_revision) | indeterminate(reason)
preview(candidate_model, tuple_query, snapshot_revision, budget)
  -> explicitly_non_authorizing_preview | typed_error
mutate(batch, expected_active_model_revision, idempotency, authorization)
  -> committed(revision, causal_token) | typed_error
watch(after_revision, realm, filters) -> ordered_stream | gap(snapshot_ref)
```

Authorizing checks and mutations load the realm's current active model
internally; the caller's revision is only a stale-state guard and cannot select
a retained historical model. Migration, audit, and shadow evaluation use the
disjoint `preview` result type, which the PDP request builder and grant path do
not accept as an authoritative relationship fact.

Watches are revisioned and detect gaps. A subscriber that loses events obtains
a complete authenticated snapshot and resumes after its revision. A cache
bypass without a defined backing-store consistency guarantee is not equivalent
to causal freshness.

## Failure and partition semantics

| Hazard | Required behavior |
| --- | --- |
| Removal followed by stale permit | Require minimum causal revision or deny/indeterminate |
| Grant followed by stale denial | May harm availability; surface revision and retry within deadline |
| Split-brain writers/quorum loss | Stop mutations and freshness-sensitive checks |
| Negative relation with stale data | Never assume staleness is conservative; include exclusions in dependency set |
| Object name reuse | Bind tuple and result to object generation |
| Recursive cycle/fan-out attack | Static cycle rules plus hard depth/set/work budget |
| Watch gap/cache poisoning | Authenticated sequence and full snapshot resync |
| Hot tenant/object | Per-realm fairness, request budgets, admission control, bounded explanation |

Low-risk cached checks during partition are allowed only by an explicit action-
class policy with maximum staleness. High-risk mutation and access checks stop.
The service reports its consistency level; callers cannot request “fast” and
then treat the answer as current.

## Verification and evaluation plan

- Reproduce Zanzibar new-enemy schedules with concurrent content creation,
  rename, object deletion/recreation, and ACL removal.
- History-check mutations and minimum-revision reads across leader failure,
  partitions, replica lag, restart, snapshot install, and configuration change.
- Differential-test old/new models on production-shaped snapshots before
  activation and fuzz tuple/model parsers.
- Generate cycles, deeply nested usersets, worst-case fan-out, exclusions, hot
  objects, and cross-realm identifiers; assert work and disclosure bounds.
- Compromise a relation writer and prove its capability cannot mutate another
  relation/object scope or obtain resource/grant authority.
- Measure p50/p99/worst check/mutation latency, stale/indeterminate rate,
  watermark lag, cache correctness, and tenant fairness.

## Staged implementation

1. Single-node immutable model and append-only tuple log with object
   generations.
2. Bounded evaluator and causal revision returned/persisted with effects.
3. Replicated crash-fault log, authenticated watches, snapshots, and fencing.
4. Shadow model migration and cache dependency proofs.
5. Offline/stale profiles only after action-specific exposure bounds exist.

## Supported decisions and open questions

Supported: realm separation; immutable models; causally constrained checks;
tombstones and object generations; bounded traversal; relation facts are input,
not authority.

Open: storage/consensus system, Byzantine threat, tuple/schema language,
freshness classes, model migration tooling, privacy of list/check interfaces,
and proof carried from relation read to resource admission.

## Connections

- [Attribute authorities](attribute-authorities.md)
- [Policy decision point](policy-decision-point.md)
- [Grant compiler and issuer](grant-compiler-and-issuer.md)
- [Revocation and epoch service](revocation-and-epoch-service.md)
- [Main authentication and authorization synthesis](../authentication-and-authorization-across-the-five-layer-architecture.md)

## Sources

- [Zanzibar](../../30-sources/pang-et-al-2019-zanzibar.md)
- [Chubby](../../30-sources/burrows-2006-chubby.md)
- [Raft](../../30-sources/ongaro-ousterhout-2014-raft.md)
- [The NIST RBAC model](../../30-sources/sandhu-et-al-2000-nist-rbac-model.md)
