---
title: "Policy decision point"
kind: note
created: "2026-09-04"
maturity: developing
tags:
  - authorization
  - formal-methods
  - policy
  - security
aliases:
  - "Authorization policy evaluator"
  - "PDP"
---

# Policy decision point

The recommended component is a **pure, deterministic, total, resource-bounded
evaluator over one immutable input snapshot**. It can authenticate a decision
envelope to a grant issuer, but it has no resource capabilities, mutable
lookups, policy-write authority, or side effects. Only an explicit `permit` can
advance; missing data, no applicable rule, unsupported functionality, timeout,
and internal error are distinct non-permit results.

This is component 8 of the [authentication and authorization service
set](README.md).

## Question, scope, and operational standard

> How can Atom combine session assurance, workload/device facts,
> relationships, attributes, action/resource schemas, and context into a
> reproducible decision whose semantics cannot change during evaluation or be
> confused with an effect?

Acceptance requires:

- a request names subject, current actor, action, exact resource generation,
  trusted context, and every policy/relation/attribute/session/boot/epoch
  revision;
- the evaluator performs no network, storage, clock, random, logging, key, or
  mutable global operation while deciding;
- the policy bundle and entity schema are signed, immutable, statically
  checked, feature-pinned, rollback-protected, and atomically activated;
- decisions are `permit`, `deny`, `not_applicable`, or `indeterminate`, with
  typed reason, request digest, input revisions, obligations, and maximum grant
  lifetime;
- explicit forbid/deny overrides permit and an unsupported or unenforceable
  obligation invalidates a permit;
- language recursion, AST size, entity count, relation expansion, steps,
  memory, output, and deadline are bounded;
- production evaluation agrees with a small executable/reference semantics
  across generated and adversarial cases; and
- PDP crash or outage causes no new grant and cannot extend an existing grant.

## Evidence and synthesis

[Cedar](../../30-sources/cutler-et-al-2024-cedar.md) supplies a typed,
expressive, analyzable policy model with explicit principal, action, resource,
context, schemas, forbid-overrides behavior, and bounded pure evaluation.
[Verification-guided Cedar
development](../../30-sources/disselkoen-et-al-2024-verification-guided-cedar.md)
shows the value of an executable formal model, production differential testing,
property tests, and generators that found real validator/evaluator defects.

[XACML 3.0](../../30-sources/oasis-2017-xacml-3-0.md) provides durable
architectural lessons: separate policy administration/information/decision/
enforcement roles, four-valued outcomes, explicit combining semantics, and the
difference between obligations and advice. Atom should not copy its large XML
surface or arbitrary extension points.

[NIST SP
800-162](../../30-sources/hu-et-al-2014-attribute-based-access-control.md)
makes authoritative, timely attribute sources part of decision correctness.
[Zero Trust
Architecture](../../30-sources/rose-et-al-2020-zero-trust-architecture.md)
separates policy decision and enforcement without granting trust based on
network location. The specific Atom policy language remains unselected.

## Authority boundary

The PDP service holds read-only immutable policy/entity bundles and normalized
decision requests. The pure evaluator itself is keyless. A narrow post-
evaluation wrapper in a separate confined child authenticates the evaluator's
request-and-result envelope for the grant issuer; that wrapper cannot alter
the decision fields or select policy.

The service receives complete relation/attribute/session/attestation snapshots
assembled by a separate request builder.

It cannot edit those inputs, fetch missing state, mint a kernel capability,
invoke a resource, append arbitrary audit history, or change an epoch. Policy
administration and signing are separate; a staged bundle cannot activate
itself. PDPs are partitioned by realm/resource class so compromise is bounded
by the associated grant issuer envelope.

## Request, bundle, and result

```text
PolicyBundle {
    bundle_id_and_hash,
    policy_language_and_feature_profile,
    entity_schema_and_action_resource_model,
    signer_and_approvals,
    version_and_activation_epoch,
}

DecisionRequest {
    request_id_and_canonical_digest,
    subject,
    current_actor_and_delegation_chain,
    action,
    resource_id_generation_and_expected_version,
    session_assurance_and_age,
    relationship_snapshot_and_revision,
    attribute_assertions_and_revisions,
    attestation_and_boot_epoch,
    revocation_watermarks,
    trusted_context,
}

Decision {
    permit | deny | not_applicable | indeterminate,
    decision_id,
    request_and_bundle_digest,
    all_input_revisions,
    obligations_and_advice,
    reason_class_and_redacted_explanation,
    maximum_grant_lifetime,
    evaluator_version,
}
```

The request builder must distinguish authoritative context from application
hints. Canonical encoding rejects duplicate fields, unknown critical fields,
ambiguous numbers/strings, and noncanonical entity identifiers.

## Evaluation semantics

The minimum semantics are:

1. Validate schema, types, feature profile, canonical request digest, and all
   required revisions before rule evaluation.
2. Evaluate explicit forbids; any matching forbid yields `deny`.
3. Evaluate permits within the resource/action schema and work budget.
4. If no rule applies, return `not_applicable`; if data/functionality is
   missing or evaluation fails, return `indeterminate`.
5. Validate that every mandatory obligation is supported by the target
   enforcement profile; otherwise return `indeterminate`.
6. Bound grant lifetime by policy, evidence expiries, session deadlines,
   revocation freshness, and issuer envelope.

No caller may configure `not_applicable` or `indeterminate` to mean allow. A
deployment can write an explicit public/anonymous permit rule instead.

### Obligations

An obligation is a typed precondition or same-admission action the resource
enforcement point can prove, such as consume idempotency key, require audit
intent, decrement a budget, redact fields, or use a protected output channel.
If the target cannot enforce it atomically enough for the operation, no grant
is issued. Advice is nonsecurity guidance and is labeled separately.

## Policy lifecycle

```text
authored -> signed -> parsed -> schema_checked -> statically_analyzed
         -> differential_tested -> shadowed -> threshold_activated
         -> retired
```

An independently supervised policy-administration and activation service—not
the PDP—atomically publishes the policy, schema, action/resource model, and
feature profile under one epoch. A tightening that must invalidate extant
grants also advances the relevant authorization epoch. Operational rollback is
a newly approved higher-epoch activation, never a decrement. The PDP can only
validate and load the immutable active revision identified by that separately
authenticated activation record.

Shadow evaluation compares old/new outcomes and cost on representative traces
without granting from the new bundle. Explanations are access-controlled and
redacted because rule matches, relationships, and attributes can be sensitive.

## OTP-like protocol and supervision

```text
evaluate(expected_active_revision, canonical_request, work_budget, deadline)
  -> decision | {error, overload | unsupported_bundle | internal}
preview(candidate_bundle, canonical_request, work_budget, deadline)
  -> explicitly_non_authorizing_preview | typed_error
load_active(bundle, activation_record, expected_epoch)
  -> {loaded, bundle_id, epoch} | typed_error
explain(decision_id, disclosure_cap) -> bounded_explanation | forbidden
```

The authorizing `evaluate` path loads the current active bundle internally and
uses the caller's revision only as a stale-state guard; callers cannot select a
historical or shadow bundle. `preview` results use a disjoint type and key/
channel that the grant issuer never accepts.

Parser/validator, reference model, production evaluator, post-evaluation
authentication wrapper, and active-revision watcher are separate supervised
children. The policy-administration and activation service is a different
unprivileged protection domain with a different supervisor and no evaluation-
result authentication facet. An evaluator crash returns `indeterminate`; the
caller cannot retry past the original evidence deadlines. Admission is fair
per realm, and the most expensive request cannot monopolize all evaluator
workers.

## Failure and security analysis

| Hazard | Required response |
| --- | --- |
| Stale/mixed inputs | Pin all revisions and reject incoherent snapshot |
| `not_applicable` or exception mapped to allow | Type system and grant API accept only authenticated explicit permit |
| Combining-order ambiguity | One small specified forbid-overrides semantics |
| Parser/evaluator differential | Canonical form, reference model, differential/property/fuzz testing |
| Maliciously expensive policy | Static cost checks plus runtime work budget and deadline |
| Decision replay | Bind exact request/resource generation/input epochs and short expiry |
| Policy rollback/model skew | Protected activation high-water and atomic bundle/schema publication |
| Explanation side channel | Separate authorization, redaction, query budget, audit |
| PDP compromise | No resource or policy-write authority; issuer intersects with fixed envelope |

## Verification and evaluation plan

- Prove or exhaustively test default deny, forbid override, determinism,
  termination/work bounds, type safety, decision/request binding, and monotonic
  attenuation of maximum lifetime.
- Differentially generate well-typed and ill-typed policies/entities/requests
  between formal/reference and production implementations.
- Fuzz text/binary parsers, canonicalization, Unicode, duplicate members,
  numbers, entity graphs, extensions, and error paths.
- Mutation-test every policy rule and combining branch; require tests to detect
  behavior changes.
- Inject stale relations, conflicting/missing attributes, expired sessions,
  clock/epoch rollback, model skew, timeout, worker crash, and unsupported
  obligations.
- Measure p50/p99/worst evaluation steps, memory, explanation size, admission
  fairness, and shadow divergence by action class.

## Staged implementation

1. Specify a deliberately small typed language and executable reference
   semantics.
2. Implement canonical requests and an interpreter with hard work bounds.
3. Add signed immutable bundles, schema validation, activation epochs, and
   shadow evaluation.
4. Add production evaluator plus differential/property/fuzz harness.
5. Integrate obligations and the grant issuer only after effect-side support is
   explicit.

## Supported decisions and open questions

Supported: pure snapshot evaluation; explicit four outcomes; forbid overrides;
no I/O/effects; immutable atomic policy activation; only explicit permit can
reach issuance.

Open: language choice, formalization tool, schema evolution, permitted
extensions, maximum work, explanation policy, obligation vocabulary, and
policy-authoring/threshold governance.

## Connections

- [Relationship authority](relationship-authority.md)
- [Attribute authorities](attribute-authorities.md)
- [Grant compiler and issuer](grant-compiler-and-issuer.md)
- [Revocation and epoch service](revocation-and-epoch-service.md)
- [Main authentication and authorization synthesis](../authentication-and-authorization-across-the-five-layer-architecture.md)

## Sources

- [Cedar](../../30-sources/cutler-et-al-2024-cedar.md)
- [Verification-guided development of Cedar](../../30-sources/disselkoen-et-al-2024-verification-guided-cedar.md)
- [XACML 3.0](../../30-sources/oasis-2017-xacml-3-0.md)
- [NIST SP 800-162](../../30-sources/hu-et-al-2014-attribute-based-access-control.md)
- [Zero Trust Architecture](../../30-sources/rose-et-al-2020-zero-trust-architecture.md)
