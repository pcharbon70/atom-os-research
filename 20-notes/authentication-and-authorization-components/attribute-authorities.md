---
title: "Attribute authorities"
kind: note
created: "2026-09-04"
maturity: developing
tags:
  - abac
  - attributes
  - authorization
  - privacy
  - security
aliases:
  - "Authoritative attribute services"
---

# Attribute authorities

The recommended architecture uses **multiple narrow, typed attribute
authorities**, not one global identity/profile database. Each authority may
assert only a registered namespace and subject/resource class, from declared
evidence, for a bounded validity interval. It returns provenance-carrying
claims; it never decides policy or mints a grant.

This is component 7 of the [authentication and authorization service
set](README.md).

## Question, scope, and operational standard

> How can Atom use human, workload, device, resource, and environmental facts
> in policy without accepting caller self-assertion, stale privilege, namespace
> collisions, semantic ambiguity, or an invasive universal attribute oracle?

Acceptance requires:

- every attribute name is registered with a type, schema version, unit,
  subject class, disclosure class, and permitted issuer set;
- assertions bind subject/resource generation, issuer, source evidence,
  assurance, effective/expiry time, revision, boot/session epoch, and
  revocation identifier;
- one authority cannot assert another authority's namespace or decide what an
  assertion permits;
- security-relevant caller-supplied context is either replaced by an
  authoritative value or labeled untrusted and unusable for permit rules;
- the PDP evaluates a coherent snapshot and treats missing, conflicting,
  unknown-schema, expired, or insufficient-assurance input as `indeterminate`;
- cache and stream consumers detect removal, rollback, sequence gaps, and
  subject-generation reuse;
- collection and disclosure are minimized for the particular decision; and
- outages and stale/offline use follow per-attribute policy and never broaden
  high-risk access.

## Evidence and synthesis

[NIST SP
800-162](../../30-sources/hu-et-al-2014-attribute-based-access-control.md)
defines ABAC over subject, object, action, and environment attributes and makes
authoritative sources, timeliness, interoperability, and privacy part of the
authorization system. [XACML
3.0](../../30-sources/oasis-2017-xacml-3-0.md) supplies a useful separation of
policy information, decision, administration, and enforcement points and
allows an issuer to be part of an attribute's identity.

[RATS](../../30-sources/birkholz-et-al-2023-rats-architecture.md) and
[EAT](../../30-sources/lundblade-et-al-2025-entity-attestation-token.md) show
that evidence, verifier appraisal, and relying-party use remain distinct.
[SPIFFE](../../30-sources/spiffe-project-2026-workload-api.md) demonstrates
short-lived workload identity and complete-snapshot stream semantics; an SVID
authenticates an identity but does not authorize it.

Atom's namespace registry, assurance vector, conflict protocol, and privacy
budget are proposed composition rules.

## Authority partition

Initial authority classes should be separate protection domains and roots:

- human account and authenticator-assurance facts;
- workload identity and launch/incarnation facts;
- device/boot attestation results;
- resource labels, ownership metadata, and object lifecycle facts;
- environment facts such as physical seat, network zone, safety mode, and
  trusted-time confidence; and
- institutional facts such as employment/role status, where a deployment has
  an external source.

Each holds only observation/validation and signing or authenticated-IPC output
for its namespace. It cannot call protected resources, edit policies or
relationships, or aggregate all other namespaces. The namespace registry is
separately administered and versioned.

## Assertion object

```text
AttributeAssertion<T> {
    assertion_id,
    subject_or_resource_id_and_generation,
    namespace,
    name,
    typed_value_and_unit,
    schema_version,
    issuer_and_issuer_generation,
    source_evidence_digest,
    assurance_and_confidence,
    effective_not_before_expiry,
    monotonic_revision,
    boot_or_session_epoch,
    revocation_id,
    disclosure_class_and_purpose,
}
```

`assurance` describes how the value was obtained and protected; `confidence`
describes uncertainty where the source is inherently probabilistic. Neither is
collapsed into the value. An attestation result retains verifier and policy
digests. A location observation retains sensor/source and freshness rather than
claiming “trusted network.”

## Lifecycle, snapshots, and conflicts

```text
observed -> source_validated -> asserted -> active
                                      \-> superseded | revoked | expired
```

Persistent or remote assertions are signed/authenticated; local assertions may
use kernel-authenticated IPC but still carry provenance and revision. Complete
snapshot streams use omission as removal. Sequence gaps make the consumer
discard the incremental view and request a new authenticated snapshot.

The namespace registry defines one of these conflict modes per attribute:

- `single-authority`: any second issuer is invalid;
- `ordered-authorities`: use the highest authorized available source but expose
  fallback and reduced assurance;
- `set-valued`: retain every provenance-tagged value;
- `agreement-required`: different values are indeterminate; or
- `domain-specific-merge`: a small, versioned, tested rule.

The PDP, not the authority, decides whether a resolved value supports an
action. Absence is never a positive fact unless policy explicitly uses a
closed-world source with a pinned complete snapshot.

## OTP-like protocol and supervision

```text
get(subject, attribute_set, minimum_revision, purpose, deadline)
  -> snapshot | stale | indeterminate | forbidden
subscribe(scope, after_sequence, purpose) -> complete_snapshots | gap
assert(observation, source_cap, expected_epoch) -> revision | typed_error
```

Source adapters are isolated supervised children. A compromised sensor/parser
can affect only its namespace and source class. Restart rebuilds from signed or
protected state and emits a complete snapshot; it never extends an assertion's
expiry or converts missing source data into the previous value.

## Failure, overload, and privacy analysis

| Hazard | Required handling |
| --- | --- |
| Caller self-asserts privilege | Ignore for permit rules unless authenticated by registered authority |
| Removed attribute remains cached | Short validity, revision/epoch binding, complete snapshots, revocation stream |
| Namespace or unit collision | Registry-pinned issuer, type, schema, unit, and canonical encoding |
| Conflicting authorities | Explicit conflict mode; default indeterminate |
| Clock/boot rollback | Monotonic protected epoch and bounded expiry; reject uncertain freshness |
| Central aggregator compromise | Multiple scoped authorities; PDP assembles minimum snapshot |
| Sensitive attribute/query leakage | Purpose-bound disclosure, minimization, access-controlled queries, redacted audit |
| Fan-out/rotation storm | Bounded requested set, batching, cache by full provenance, randomized renewal, fairness |

Offline use is a conscious risk envelope: an assertion may remain usable only
until its declared expiry and only for action classes whose policy accepts that
maximum staleness. An unavailable source is not equivalent to a false value.

## Verification and evaluation plan

- Inject wrong issuer, namespace, type, unit, schema, subject generation,
  assurance, validity, and boot/session epoch for every attribute class.
- Remove and supersede assertions while caches, streams, and PDP snapshots are
  active; drop/reorder/duplicate events and require gap recovery.
- Roll wall time, boot counters, issuer revisions, and persistent snapshots
  backward; assert no privilege resurrection.
- Supply missing and conflicting values for every conflict mode and
  differential-test resolver/reference implementations.
- Prove request-supplied fields cannot shadow authoritative fields and test
  cross-tenant enumeration.
- Measure minimal disclosed attributes, correlation, explanation leakage,
  source fan-out, p99 freshness, cache exposure, and fairness during synchronized
  rotation/outage.

## Staged implementation

1. Typed namespace registry and two local authorities: workload incarnation and
   resource generation/label.
2. Immutable snapshots consumed by the pure PDP with indeterminate semantics.
3. Human/session assurance and RATS result authorities.
4. Signed remote assertions, streaming, revocation, and privacy policy.
5. External institutional/environment adapters only after issuer governance and
   offline behavior are specified.

## Supported decisions and open questions

Supported: multiple scoped authorities; issuer is part of attribute identity;
provenance/freshness always carried; missing/conflict defaults indeterminate;
minimum disclosure.

Open: namespace/schema registry, assurance lattice, trusted time, privacy
budget, conflict rules, per-attribute freshness SLAs, and which environment
facts are reliable enough to influence high-impact policy.

## Connections

- [Workload identity issuer](workload-identity-issuer.md)
- [RATS Verifier and Appraisal Policy](rats-verifier-and-appraisal-policy.md)
- [Relationship authority](relationship-authority.md)
- [Policy decision point](policy-decision-point.md)
- [Main authentication and authorization synthesis](../authentication-and-authorization-across-the-five-layer-architecture.md)

## Sources

- [NIST SP 800-162](../../30-sources/hu-et-al-2014-attribute-based-access-control.md)
- [XACML 3.0](../../30-sources/oasis-2017-xacml-3-0.md)
- [RATS architecture](../../30-sources/birkholz-et-al-2023-rats-architecture.md)
- [Entity Attestation Token](../../30-sources/lundblade-et-al-2025-entity-attestation-token.md)
- [SPIFFE Workload API](../../30-sources/spiffe-project-2026-workload-api.md)
