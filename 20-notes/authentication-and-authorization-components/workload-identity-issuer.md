---
title: "Workload identity issuer"
kind: note
created: "2026-09-04"
maturity: developing
tags:
  - authentication
  - identity
  - spiffe
  - workload-identity
aliases:
  - "Workload credential issuer"
---

# Workload identity issuer

The recommended component is an **incarnation-aware local workload-attestation
and short-lived credential service**. The kernel atomically identifies the
calling protection domain and generation; the issuer resolves that immutable
fact through versioned registration policy, creates or selects a non-exportable
key, and streams a complete snapshot of narrowly scoped credentials and trust
bundles. A PID, registered actor name, path, UID, or network address is never
accepted as identity on its own.

This is component 4 of the [authentication and authorization service
set](README.md). It authenticates workload provenance to relying parties; it
does not assign roles or authorize application effects.

## Question, scope, and operational standard

> How can a newly started or restarted workload prove which declared service
> incarnation it is without static shared secrets, name/PID reuse, exported
> private keys, or an issuer that can reach every protected resource?

The service is acceptable only when:

- the local endpoint receives an unforgeable caller-domain, generation, launch
  digest, and boot epoch from Layer 2 in the same admission step as the request;
- registration policy is immutable by revision and maps only approved
  incarnation evidence to an identity within the issuer's trust domain;
- identity names and registration facts do not imply roles or resource
  authority;
- each private key is non-exportable by default and usable only through an
  audience/purpose-limited key facet;
- credentials are short-lived, overlap safely during rotation, bind one exact
  identity, and are removed from complete snapshots when no longer authorized;
- multiple eligible identities require explicit caller selection for sensitive
  operations;
- stale registry, bundle, attestation, or boot state cannot be replayed after
  rollback, restart, clone, or migration; and
- signer outage, rotation storms, and malformed requests are bounded and never
  cause fallback to static global credentials.

## Evidence and synthesis

The [SPIFFE Workload
API](../../30-sources/spiffe-project-2026-workload-api.md) provides the closest
operational model: a local endpoint identifies a caller out of band, returns
X.509- or JWT-based SVIDs, streams trust bundles, and treats each update as a
complete snapshot. It explicitly leaves caller attestation and application
authorization to the implementation. Its interoperability form can expose an
unencrypted PKCS#8 key, which Atom should replace with a protected handle where
both ends are native.

The stable [X.509-SVID
specification](../../30-sources/spiffe-project-2026-x509-svid.md) supplies the
normative compatibility checks: exactly one URI SAN/SPIFFE ID, distinct leaf
and signing-certificate constraints, RFC 5280 path validation, and additional
SPIFFE leaf validation. It authenticates a name under a trust bundle; it does
not assign a role or resource permission.

[RATS](../../30-sources/birkholz-et-al-2023-rats-architecture.md) supports
separating evidence production, appraisal, and the relying party's decision.
[TPM 2.0](../../30-sources/trusted-computing-group-2026-tpm-2-0-library.md) and
[DICE](../../30-sources/trusted-computing-group-2024-dice-hardware-requirements.md)
provide alternative hardware-root profiles for protected keys, measurements,
and compound identity, but neither converts a measurement into application
permission.

The Atom-specific kernel-incarnation binding and handle-based native profile
are proposals. They require an exact target and conformance tests.

## Authority boundary

The issuer holds a receive-only local endpoint, authentic caller facts, a
read-only registration snapshot, narrow CA signing or key-service facets,
trust-bundle publication, credential lifecycle state, and audit append.

It must not hold human credentials, root CA raw keys, registration-policy edit
rights, arbitrary workload-name allocation, resource capabilities, application
data, or unrestricted network/filesystem access. Signers are partitioned by
trust domain and identity namespace so compromise is not universal.

## Objects and registration model

```text
WorkloadIncarnation {
    domain_id,
    domain_generation,
    executable_or_manifest_digest,
    supervisor_lineage_digest,
    node_id_and_boot_epoch,
}

RegistrationBinding {
    binding_id,
    parent_or_node_scope,
    selector_predicate,
    workload_identity,
    allowed_credential_profiles,
    attestation_requirement,
    policy_revision,
    validity_and_revocation_epoch,
}

CredentialSnapshot {
    incarnation,
    sequence,
    svid_versions,
    opaque_key_handles,
    trust_bundle_revision,
    expiry_and_next_refresh_window,
}
```

Selectors are typed kernel facts or signed manifest facts. Mutable labels,
environment strings, actor-registered names, and filesystem paths are weak
hints unless bound into the authenticated launch record. Policy defines a
strength lattice and the minimum evidence for each identity.

## Issuance and rotation protocol

```text
attach -> snapshot_incarnation -> resolve_binding -> optional_attestation
       -> create_key_handle -> issue -> publish_complete_snapshot
       -> overlap_rotate -> redact_or_expire -> destroy_retired_key
```

Attaching and reading caller facts must be atomic with endpoint admission so a
PID or domain cannot exit and be reused between inspection and issuance.
Issuance pins the registration, attestation, bundle, boot, and issuer epochs.

A workload leaf X.509-SVID contains exactly one workload identity in its URI
identity field and is restricted to leaf/end-entity usage; signing SVIDs follow
the separate CA profile and cannot authenticate a workload. A JWT-like
compatibility credential is explicitly audience-bound and short-lived. Native
local callers receive an opaque key-and-identity handle. A complete stream
snapshot replaces prior state; sequence gaps force resynchronization rather
than additive guessing.

Rotation begins before expiry with randomized renewal windows and overlap long
enough for bounded propagation. Removing a registration, terminating a domain,
changing its generation, or revoking an issuer causes a new complete snapshot
without the credential and advances the relevant epoch.

## OTP-like protocol and supervision

```text
attach(identity_stream_options, deadline) -> stream_ref | typed_error
select_identity(stream_ref, identity, audience) -> credential_handle | typed_error
current_bundle(trust_domain, minimum_revision) -> snapshot | stale | unavailable
```

The hot issuer, registry watcher, bundle publisher, and crypto adapter are
separate supervised children. Parser/attestation failures do not restart the
signer. After restart, the service rebuilds state from protected revisions and
emits a fresh complete snapshot; it never assumes clients retained the last
increment.

## Failure, compromise, and overload analysis

| Hazard | Required response |
| --- | --- |
| PID/name reuse or selector TOCTOU | Kernel-authenticated incarnation attached atomically to request |
| Multiple eligible identities | Explicit selection; no “first identity” for sensitive use |
| Registry/bundle rollback | Protected high-water revisions and boot epoch; restricted mode on uncertainty |
| Raw key leakage through BEAM heap/trace | Opaque handles, confined crypto adapter, redacted crash/audit paths |
| Issuer signing compromise | Namespace-limited intermediates, short TTL, epoch revoke, independent root/recovery |
| Stale stream after removal | Complete snapshots, sequence gaps, expiry, consumer acknowledgement |
| Rotation thundering herd | Randomized renewal, per-identity quotas, bounded queue, prepublication overlap |
| Signer outage | Existing credentials expire by contract; no static-key fallback |

## Verification and evaluation plan

- Race domain exit/reuse, actor restart, exec/hot-code transition, and identity
  request; assert the issued identity binds the observed incarnation.
- Run wrong-selector, wrong-node, wrong-boot, wrong-parent, and registry-rollback
  matrices for every identity profile.
- Validate exactly one workload identity, audience rules, end-entity key usage,
  chain/bundle revision, expiry, and algorithm profile with independent tools.
- Inspect heaps, messages, traces, dumps, swap, logs, and audit for raw private
  material; exercise wrap/export and error paths.
- Drop stream updates, reconnect, remove a binding, and rotate issuer/bundle
  keys; verify complete-snapshot redaction and bounded expiry.
- Saturate issuance and renewal by tenant; measure fairness, signer queueing,
  p99 renewal margin, and outage behavior.

## Staged implementation

1. Native local identity handles from kernel incarnation plus static signed
   registration snapshot.
2. Short-lived X.509 compatibility profile and complete snapshot streaming.
3. Protected key service, rotation, bundle high-water state, and revocation.
4. Optional RATS/TPM/DICE profiles after reference-value governance exists.
5. Federation only through the separate gateway.

## Supported decisions and open questions

Supported: out-of-band kernel caller identity; short-lived credentials; no role
in names; non-exportable native keys; full-snapshot streams; explicit
multi-identity choice.

Open: identity-name allocation, selector lattice, first trust domain, raw-key
compatibility, signer-compromise recovery, bundle anti-rollback, and live-
runtime freshness after boot attestation.

## Connections

- [RATS Verifier and Appraisal Policy](rats-verifier-and-appraisal-policy.md)
- [Key and secret service](key-and-secret-service.md)
- [Attribute authorities](attribute-authorities.md)
- [Federation gateway](federation-gateway.md)
- [Main authentication and authorization synthesis](../authentication-and-authorization-across-the-five-layer-architecture.md)

## Sources

- [SPIFFE Workload API](../../30-sources/spiffe-project-2026-workload-api.md)
- [X.509 SPIFFE Verifiable Identity Document](../../30-sources/spiffe-project-2026-x509-svid.md)
- [RATS architecture](../../30-sources/birkholz-et-al-2023-rats-architecture.md)
- [TPM 2.0 Library](../../30-sources/trusted-computing-group-2026-tpm-2-0-library.md)
- [DICE hardware requirements](../../30-sources/trusted-computing-group-2024-dice-hardware-requirements.md)
