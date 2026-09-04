---
title: "Federation gateway"
kind: note
created: "2026-09-04"
maturity: developing
tags:
  - federation
  - oauth
  - security
  - workload-identity
aliases:
  - "External identity gateway"
  - "Remote trust gateway"
---

# Federation gateway

The recommended component is a **one-way, explicitly configured trust and
protocol termination boundary**. It parses and validates remote certificates,
tokens, proofs, and bundles in confined workers; preserves issuer, subject,
current actor, audience, request, and assurance provenance; then asks the local
PDP and grant issuer for one new operation-specific local capability. It never
deserializes a kernel capability or trusts network location.

This is component 15 of the [authentication and authorization service
set](README.md).

## Question, scope, and operational standard

> How can Atom interoperate across trust domains and OAuth/OIDC/SPIFFE systems
without forwarding broad tokens, merging trust bundles, losing delegation
semantics, accepting bearer replay, or letting hostile parsers and peers reach
the local capability namespace?

Acceptance requires:

- every relationship is directional and pins peer trust domain/issuer,
  endpoints, profile, algorithms, key sources, audience/resource namespace,
  mapping policy, bundle sequence, and revocation/freshness requirements;
- remote input selects no arbitrary algorithm, key URL, parser, issuer, local
  namespace, or network destination;
- validation binds exact token/type, issuer, audience, subject/current actor,
  time, nonce/state, request/method/resource/body digest, and proof key;
- bearer-only credentials are rejected for sensitive operations; accepted
  proofs are still policy evidence, not permission;
- exchanged/delegated output is narrower and target-specific, preserves actor
  provenance, and cannot outlive or outscope its inputs or gateway envelope;
- foreign bundles never merge with the local trust bundle and relationship
  deletion/rotation has a measured propagation bound;
- parsers, discovery, metadata retrieval, certificate validation, replay state,
  and crypto have strict size/depth/time/network/tenant budgets; and
- peer, PDP, RATS, bundle, replay-store, or gateway failure produces typed
  restricted behavior, never location-based or bearer fallback.

## Evidence and synthesis

[OAuth Security
BCP](../../30-sources/lodderstedt-et-al-2025-oauth-security-bcp.md) requires
modern flow protections, exact redirect matching, PKCE, audience restriction,
and sender constraint while deprecating dangerous legacy flows. [Formal OIDC
analysis](../../30-sources/fett-et-al-2017-openid-connect-security.md) shows
why issuer/endpoint/flow/nonce/origin composition and malicious identity
providers matter.

[OAuth token
exchange](../../30-sources/jones-et-al-2020-oauth-token-exchange.md) supplies
subject versus actor and delegation versus impersonation semantics but leaves
the trust model and output security to profiles. [Mutual TLS](../../30-sources/campbell-et-al-2020-oauth-mutual-tls.md)
and [DPoP](../../30-sources/fett-et-al-2023-dpop.md) bind tokens to a key at the
resource protocol while exposing certificate/proxy, URI, nonce, replay, and
body-binding limits. [JWT BCP](../../30-sources/sheffer-et-al-2020-jwt-best-practices.md)
requires algorithm pinning, issuer/audience validation, explicit typing, and
defenses against cross-JWT confusion and attacker-controlled key URLs/IDs.

[SPIFFE federation](../../30-sources/spiffe-project-2026-federation.md)
provides a current first-party precedent for explicit one-way trust-domain
relationships, separate bundles, overlap during key rotation, normal-interval
retry, and removal propagation. It authenticates workloads; it does not decide
Atom authorization.

## Authority boundary

The gateway holds a bounded network endpoint, explicit peer relationships,
read-only bundle/issuer snapshots, allowed credential/algorithm profiles,
nonce/replay state, outbound client-key facets, and narrow request channels to
RATS, attribute, PDP, grant, revocation, and audit services.

It holds no root issuer key, arbitrary internal capability or namespace,
policy-edit right, transitive trust, long-lived bearer-token store, open-proxy
egress, or ability to serialize/import kernel handles. Each peer/profile runs
in a separate protection and resource domain where practical.

A separately protected federation-relationship administration and activation
guard validates signatures, separated approvals, epoch monotonicity, and
namespace/envelope constraints, then publishes a read-only active snapshot to
the gateway. The guard holds no network endpoint, token parser, remote client
key, or local grant channel.

## Relationship and request objects

```text
FederationRelationship {
    relationship_id_and_direction,
    local_realm_and_peer_trust_domain,
    issuer_and_endpoint_allowlist,
    credential_token_and_algorithm_profile,
    peer_bundle_revision_and_keys,
    local_namespace_mapping,
    allowed_resource_action_envelope,
    proof_freshness_and_replay_policy,
    policy_revision_and_revocation_epoch,
}

RemoteEvidence {
    relationship,
    issuer,
    subject,
    current_actor_and_bounded_actor_chain,
    audience_resource_scope,
    assurance_and_authentication_time,
    token_type_and_digest,
    proof_key_thumbprint,
    request_method_uri_body_digest_nonce,
    issue_not_before_expiry,
    bundle_and_revocation_revisions,
}
```

Names are mapped into a dedicated foreign namespace; a peer's `admin`, UID,
path, role, or SPIFFE path never collides with a local principal or role. Trust
is not transitive unless another independently reviewed directional
relationship explicitly says so.

## Inbound protocol

```mermaid
flowchart LR
  bounded_accept --> relationship_select
  relationship_select --> confined_parse
  confined_parse --> issuer_type_algorithm_validate
  issuer_type_algorithm_validate --> audience_time_nonce_validate
  audience_time_nonce_validate --> proof_and_replay_validate
  proof_and_replay_validate --> optional_attestation
  optional_attestation --> local_policy
  local_policy --> local_grant
  local_grant --> effect_admission
  effect_admission --> audit_outcome
```

Relationship selection happens from the local endpoint/configuration, not from
an untrusted `iss`, `jku`, `x5u`, or discovery URL alone. Remote key retrieval
uses fixed schemes/hosts, byte/time limits, certificate policy, cache revision,
and rollback protection. Explicit token types and mutually exclusive validation
rules prevent one JWT class from being accepted as another.

The target verifies PoP at the actual authenticated transport/request boundary.
If TLS terminates at a proxy, the propagation of client-certificate facts is a
separately authenticated internal protocol, not an HTTP header convention.
DPoP method/URI binding is supplemented by Atom's canonical body/operation
digest when the effect depends on a body.

## Outbound and exchange protocol

Outbound code selects one peer relationship and exact foreign resource/
audience. It obtains a short-lived local workload credential and proof-key
facet; it never forwards the user's broad session or internal capability.

Token exchange retains subject and current actor. Delegation is the default;
impersonation requires an explicit policy and audit reason. Requested resource,
audience, and scope are intersected rather than combined. Input/output
revocation linkage is not assumed: the gateway records lineage and binds the
local/remote expiry and epochs explicitly.

## Bundle lifecycle and partition behavior

```text
configured -> fetched -> validated -> active
           -> overlap_rotate -> active_new -> old_removed
           -> relationship_removed -> bundle_redacted -> expired
```

New verification keys appear for multiple refresh intervals before use; old
keys remain only for the declared overlap. Bundles for different trust domains
remain separate. Removing a relationship removes the authoritative validator
snapshot and advances its epoch; consumers acknowledge redaction.

During bundle/peer/PDP/RATS outage, no new high-risk gateway session or local
grant is created. Already issued grants remain only within their own explicit
expiry/watermark. Retries use bounded exponential backoff/jitter and per-peer
circuit budgets rather than aggressive synchronized polling.

## OTP-like protocol and supervision

```text
accept(endpoint, expected_active_relationship_revision, bounded_request,
       deadline)
  -> local_result | typed_protocol_error
validate(expected_active_relationship_revision, credential, request_binding)
  -> remote_evidence_handle | typed_error
exchange(local_context, expected_active_relationship_revision,
         foreign_target, deadline)
  -> outbound_grant_handle | typed_error
```

The gateway selects the active relationship snapshot internally; the supplied
revision is only a stale-state guard and never caller-provided policy. The
separate activation guard—not this API—owns `activate_relationship(config,
approvals, expected_epoch)`.

Network framing, JSON/JWT, CBOR/COSE, X.509, discovery/metadata, DPoP, and each
compatibility profile are distinct supervised workers. A crash drops the
request and nonce; it does not reuse a partial response. Replay and revocation
paths have reserved storage/compute. Per-peer fairness prevents one federation
from starving local security. The relationship activation guard has a separate
supervisor and cannot inherit a worker's network or parsing authority.

## Failure and attack analysis

| Hazard | Required handling |
| --- | --- |
| Token forwarding/confused deputy | Exchange to exact next hop; subject/actor/request binding; no broad pass-through |
| Bearer theft/replay | PoP, nonce, short lifetime, replay store, target validation |
| Algorithm/type/cross-JWT confusion | Profile-pinned algorithms and explicit mutually exclusive token types |
| `jku` SSRF or `kid` injection | Local endpoint/key allowlist, noninterpreted key IDs, confined retrieval |
| Bundle merge/rollback | Per-domain snapshots, sequence/high-water, authenticated complete redaction |
| Accidental transitive trust | Directional explicit relationships only |
| TLS proxy spoof | Authenticated internal binding from trusted terminator; never raw header |
| Peer/gateway compromise | Local namespace/envelope partition, fresh PDP decision, short grant |
| Parser/crypto/replay DoS | Byte/depth/time quotas, early admission, per-peer fairness, circuit breaker |
| Partition | Typed unavailable/restricted; no fail-open; bounded extant leases |

## Verification and evaluation plan

- Build a full negative matrix for issuer, audience, subject, actor, type,
  algorithm, time, nonce, state, method, URI, body digest, proof key, bundle,
  resource, relationship direction, and local namespace.
- Run OAuth/OIDC/JWT/FIDO/certificate conformance where applicable and
  coverage-fuzz every parser, metadata retriever, and error path under limits.
- Test mix-up/malicious issuer, cross-JWT substitution, bearer replay, DPoP
  same-endpoint replay, URI normalization, certificate mismatch/rotation, TLS
  termination spoof, `jku` SSRF, and `kid` injection.
- Rotate/add/remove peer keys and relationships, drop updates, roll bundle state
  backward, split peers, and measure redaction/revocation exposure.
- Compromise a peer and gateway worker; prove it can reach only the mapped
  namespace and issuer envelope and cannot import/export kernel authority.
- Saturate connections, signatures, replay cache, PDP/RATS calls, and retries;
  measure per-peer fairness, latency, rejection cost, and local-service impact.

## Staged implementation

1. One fixed mutual-TLS workload peer with static pinned bundle and local PDP
   conversion.
2. Rotation, replay, revocation epoch, explicit one-way relationship lifecycle.
3. One OAuth authorization-code/PoP external profile with formal negative tests.
4. Token exchange preserving subject/actor and target-specific outbound grants.
5. Dynamic discovery or additional formats only after sandboxing, allowlisting,
   and rollback/compromise recovery are demonstrated.

## Supported decisions and open questions

Supported: federation terminates at a gateway; directional explicit trust;
separate bundles/namespaces; PoP plus fresh local policy; no remote kernel
capabilities; no location trust or bearer fallback.

Open: canonical foreign principal/actor model, first remote profile, namespace
mapping, bundle rollback anchor, revocation SLA, privacy/linkability policy,
trusted TLS termination, dynamic discovery, and partition behavior by action.

## Connections

- [Workload identity issuer](workload-identity-issuer.md)
- [RATS Verifier and Appraisal Policy](rats-verifier-and-appraisal-policy.md)
- [Policy decision point](policy-decision-point.md)
- [Grant compiler and issuer](grant-compiler-and-issuer.md)
- [Revocation and epoch service](revocation-and-epoch-service.md)

## Sources

- [OAuth 2.0 Security BCP](../../30-sources/lodderstedt-et-al-2025-oauth-security-bcp.md)
- [Formal OpenID Connect security analysis](../../30-sources/fett-et-al-2017-openid-connect-security.md)
- [OAuth token exchange](../../30-sources/jones-et-al-2020-oauth-token-exchange.md)
- [OAuth mutual TLS](../../30-sources/campbell-et-al-2020-oauth-mutual-tls.md)
- [DPoP](../../30-sources/fett-et-al-2023-dpop.md)
- [JWT best current practices](../../30-sources/sheffer-et-al-2020-jwt-best-practices.md)
- [SPIFFE federation](../../30-sources/spiffe-project-2026-federation.md)
