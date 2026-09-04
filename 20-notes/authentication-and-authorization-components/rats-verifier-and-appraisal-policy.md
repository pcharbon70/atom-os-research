---
title: "RATS Verifier and Appraisal Policy"
kind: note
created: "2026-09-04"
maturity: developing
tags:
  - attestation
  - rats
  - security
  - trusted-computing
  - verification
aliases:
  - "Attestation verifier"
  - "Evidence appraisal service"
---

# RATS Verifier and Appraisal Policy

The recommended design is **not one omnipotent attestation daemon**. A hot-path
verifier consumes bounded evidence, endorsements, reference values, freshness
state, and an immutable evidence-appraisal policy. A separately authorized
policy-owner facet stages and threshold-activates those inputs. The verifier
emits a privacy-minimized `AttestationResult`; a relying party and the policy
decision point independently decide whether that result justifies a grant.

This is component 5 of the [authentication and authorization service
set](README.md).

## Question, scope, and operational standard

> How can Atom turn heterogeneous, attacker-controlled attestation bytes into a
> trustworthy, fresh, provenance-preserving appraisal without treating a known
> measurement as identity or permission?

Acceptance requires:

- evidence, endorsements, reference values, evidence-appraisal policy, and
  relying-party policy remain separately named and versioned artifacts;
- each accepted profile pins wrapper, encoding, algorithms, claim vocabulary,
  maximum bytes/depth/submodules, freshness method, and composite binding;
- untrusted parsing happens in confined, replaceable domains with strict CPU,
  memory, recursion, decompression, and deadline budgets;
- the verifier pins one immutable input snapshot and returns `pass`, `fail`, or
  `indeterminate` with policy/input digests and provenance;
- unknown measurements, claims, algorithms, missing freshness, or unavailable
  endorsements never become approval by default;
- results disclose only claims required by the named relying party and expire
  within the evidence/freshness validity window;
- learning a “known good” reference value from submitted evidence is
  impossible; and
- verifier, policy-owner, root, or clock compromise is included in the threat
  and recovery model rather than hidden behind a signature.

## Evidence and synthesis

[RFC 9334](../../30-sources/birkholz-et-al-2023-rats-architecture.md)
separates Attester, Verifier, Relying Party, Evidence, Endorsements, Reference
Values, Appraisal Policy for Evidence, and Appraisal Policy for Attestation
Results. That separation is the architectural baseline. [Entity Attestation
Token](../../30-sources/lundblade-et-al-2025-entity-attestation-token.md)
provides a profileable CWT/JWT claims container with nonce and submodule
support; it deliberately supplies no universal mandatory claim set or
authorization semantics.

[RATS Conceptual Message
Wrapper](../../30-sources/birkholz-et-al-2026-rats-conceptual-message-wrapper.md)
distinguishes conceptual message types across encodings and supports recursive
collections while leaving authenticity/confidentiality protection to the
surrounding profile; optional nesting limits and recursive input motivate
Atom's own hard depth, item-count, and byte-size bounds. [TPM
2.0](../../30-sources/trusted-computing-group-2026-tpm-2-0-library.md) and
[DICE](../../30-sources/trusted-computing-group-2024-dice-hardware-requirements.md)
are hardware-root profiles; neither ensures the event log is truthful or the
measured runtime remains uncompromised.

The normalized claim model and update protocol below are Atom synthesis.

## Authority and ownership split

The verifier holds bounded evidence input, nonce/replay state, trust anchors,
read-only signed policy/reference/endorsement snapshots, isolated format
handlers, a result-signing facet, and audit append.

It holds no application/resource capability, workload identity issuance,
policy-edit right, remediation authority, or arbitrary raw-evidence disclosure.
The policy owner may stage signed reference values, endorsements, and evidence
policies but cannot run an unreviewed parser or authorize an application
operation. A separately confined policy/reference activation guard validates
approvals and publishes one immutable active snapshot; it has no evidence-
appraisal or result-signing facet. High-impact activation requires separated/
threshold approval.

## Input and result objects

```text
EvidenceEnvelope {
    conceptual_message_type,
    profile_and_encoding,
    bounded_bytes_or_handle,
    attester_and_channel_binding,
    freshness_challenge,
    collection_depth_and_count,
}

AppraisalSnapshot {
    trust_anchor_revision,
    reference_value_set_digest,
    endorsement_set_digest,
    evidence_policy_digest,
    algorithm_profile,
    activation_epoch,
}

AttestationResult {
    result_id,
    attester_handle,
    outcome,
    authority_tagged_claims,
    policy_and_input_digests,
    freshness_and_strength,
    privacy_profile,
    issued_and_expiry,
    verifier_generation,
}
```

Normalized claims retain issuer and evidence provenance; two identically named
claims from different roots never collapse. The result identifies failed,
unknown, unsupported, stale, malformed, or unavailable reason classes without
leaking unnecessary measurements to ordinary callers.

## Appraisal protocol

```mermaid
flowchart LR
  challenge --> receive
  receive --> classify
  classify --> parse_confined
  parse_confined --> validate_origin
  validate_origin --> freshness
  freshness --> pin_snapshot
  pin_snapshot --> appraise
  appraise --> minimized_result
  minimized_result --> relying_party_policy
```

The nonce or other freshness challenge binds the evidence to the intended
verifier, session, request, and deadline. Composite/layered evidence is accepted
only if the profile cryptographically binds subcomponents and defines whether
partial failure makes the whole appraisal fail or become indeterminate.

Caching keys include every evidence, endorsement, reference-value, policy,
algorithm-profile, verifier-generation, and freshness digest. Fresh nonces
usually make raw result caching inappropriate; stable subordinate validation
can be cached only within its signed validity and revocation epochs.

## Policy and reference-value lifecycle

```text
authored -> signed -> validated -> shadow-evaluated -> threshold-active
         -> superseded -> retained-for-audit -> retired
```

The separate activation guard publishes atomically: no request may mix old
reference values with new policy. Rollback protection stores the highest
activation epoch in protected state. Emergency removal can immediately cause
`indeterminate` or `fail`; adding a new approved measurement follows review and
shadow comparison rather than learning from a passing attester. The verifier
loads only the authenticated active snapshot internally.

## OTP-like protocol and supervision

```text
challenge(attester, profile, request_digest, deadline) -> nonce_handle
appraise(evidence, challenge, expected_active_snapshot_revision)
  -> result_handle | typed_error
preview(evidence, candidate_snapshot, work_budget)
  -> explicitly_non_authorizing_preview | typed_error
```

Each encoding/profile handler is a separately supervised worker with no
signing key or policy-write authority. A handler crash invalidates the request
and produces no result. The core verifier is deterministic over normalized
claims and the internally selected active snapshot; the caller's revision is
only a stale-state guard. Preview results use a disjoint type/key that relying
parties cannot accept. The activation guard is a different unprivileged domain
and supervisor. Queue admission happens before expensive crypto and
decompression.

## Failure and privacy analysis

| Hazard | Required handling |
| --- | --- |
| Evidence replay or nonce collision | Verifier-generated challenge, atomic replay state, adequate entropy |
| CBOR/JWT/certificate bomb | Profile-specific byte/depth/count limits and confined parsers |
| Unknown measurement/claim | Typed indeterminate unless policy explicitly defines safe treatment |
| Policy/reference rollback | Signed immutable snapshots and protected activation high-water |
| Unbound composite evidence | Reject unless profile proves composition and shared freshness |
| Runtime drift after boot | Short result lifetime plus runtime evidence/continuous controls where required |
| Privacy/linkability | Minimize result, pairwise handles, purpose/audience binding, protected raw evidence |
| Verifier/root compromise | Partition roots, transparent activation/audit, short results, recovery procedure |
| Endorsement outage | Cached signed data within validity or typed unavailable; never self-endorse |

## Verification and evaluation plan

- Use profile conformance corpora and known-good, known-bad, unknown, stale,
  partially valid, and revoked matrices.
- Coverage-fuzz wrappers, CBOR/COSE, JSON/JWT, X.509, event logs, submodules,
  duplicate claims, tags, algorithms, decompression, and nesting boundaries.
- Replay nonces and evidence across relying parties, request digests, boot
  epochs, and verifier generations; roll clocks and protected state backward.
- Differential-test production appraisal against a small reference model for a
  fixed snapshot; assert determinism and provenance preservation.
- Compromise/restart individual parser workers and saturate one attester;
  measure fairness, resource ceilings, deadline cancellation, and circuit
  breaking.
- Inspect results and logs for privacy-minimization violations and prove raw
  evidence is unavailable to ordinary applications.

## Staged implementation

1. A tiny synthetic evidence profile and immutable signed policy snapshots.
2. One TPM or DICE profile with isolated parser and freshness/replay tests.
3. Privacy-minimized result capabilities consumed by the PDP.
4. Threshold policy/reference activation, rollback state, and transparency.
5. Composite evidence only after binding and partial-failure semantics are
   modeled.

## Supported decisions and open questions

Supported: RATS role separation; typed profiles; bounded isolated parsing;
immutable evidence policy; results are evidence, never resource authority.

Open: first evidence/result profile, target hardware root, reference-value
governance, endorsement availability, verifier transparency, runtime freshness,
privacy requirements, and recovery after root/verifier compromise.

## Connections

- [Workload identity issuer](workload-identity-issuer.md)
- [Attribute authorities](attribute-authorities.md)
- [Policy decision point](policy-decision-point.md)
- [Key and secret service](key-and-secret-service.md)
- [Main authentication and authorization synthesis](../authentication-and-authorization-across-the-five-layer-architecture.md)

## Sources

- [RATS architecture](../../30-sources/birkholz-et-al-2023-rats-architecture.md)
- [Entity Attestation Token](../../30-sources/lundblade-et-al-2025-entity-attestation-token.md)
- [RATS Conceptual Message Wrapper](../../30-sources/birkholz-et-al-2026-rats-conceptual-message-wrapper.md)
- [TPM 2.0 Library](../../30-sources/trusted-computing-group-2026-tpm-2-0-library.md)
- [DICE hardware requirements](../../30-sources/trusted-computing-group-2024-dice-hardware-requirements.md)
