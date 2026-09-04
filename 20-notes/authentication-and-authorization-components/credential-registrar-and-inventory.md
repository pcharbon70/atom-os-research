---
title: "Credential registrar and inventory"
kind: note
created: "2026-09-04"
maturity: developing
tags:
  - authentication
  - credential-management
  - identity
  - passkeys
  - security
aliases:
  - "Authenticator registry"
  - "Credential inventory service"
---

# Credential registrar and inventory

The recommended component is an **authoritative, append-oriented binding
ledger** for principals and authenticators. Enrollment is a multi-party
transaction requiring an already justified account context, trusted human
intent, a fresh registrar challenge, verifier-confirmed proof, and an atomic
commit. Removal is visible and leaves a rollback-resistant tombstone.

This is component 1 of the [authentication and authorization service
set](README.md). It records which evidence a verifier may accept; it does not
verify a login, create a session, recover an account, or confer application
authority.

## Question, scope, and operational standard

> How can Atom add, inspect, rotate, suspend, and remove authenticators without
> letting registrar compromise, enrollment races, synchronization, recovery,
> or snapshot rollback become an impersonation path?

The component is acceptable only when:

- every binding names a stable principal, relying-party/audience, unique
  credential, algorithm, assurance facts, provenance, and lifecycle revision;
- high-assurance enrollment requires both verifier evidence and a request-bound
  trusted-interaction receipt;
- the registrar never receives authenticator private keys, raw activation
  secrets, plaintext recovery codes, or data-recovery keys;
- replacement creates a new record and preserves the old record's history;
- removal and compromise produce durable tombstones that survive restart and
  old-snapshot restoration;
- inventories expose all active, pending, synchronized, suspended, and recently
  removed authenticators in a comprehensible form;
- stale or unknown authenticator metadata cannot increase assurance; and
- concurrent retries are idempotent and cannot bind a response to another
  subject, request, relying party, or credential.

## Evidence and synthesis

[NIST SP
800-63B-4](../../30-sources/temoshok-et-al-2025-authentication-and-authenticator-management.md)
requires lifecycle records, multiple binding options, notifications, and
assurance-aware authenticator management. [WebAuthn Level
3](../../30-sources/w3c-2026-webauthn-level-3.md) specifies credential IDs,
public keys, relying-party binding, user handles, authenticator flags, backup
eligibility/state, and counter signals. [CTAP
2.2](../../30-sources/fido-alliance-2025-ctap-2-2.md) specifies authenticator
credential-management and PIN/UV operations.

[Formal FIDO2
analysis](../../30-sources/guan-et-al-2022-formal-analysis-fido2.md) shows why
registration and authentication must be modeled as a composed ceremony with
parallel-session and rebinding threats. The empirical [passkey abusability
study](../../30-sources/daffalla-et-al-2025-passkey-abusability.md) shows that
inventory, synchronization, naming, and removal can be exploitable in
interpersonal threat models even when signatures are correct. The [FIDO
Metadata Service](../../30-sources/fido-alliance-2026-metadata-service.md)
supplies signed authenticator characteristics and security status, but vendor
metadata remains an input whose provenance and freshness must be visible.

Atom's ledger, transaction, and tombstone design are proposals. None of these
sources proves crash consistency or rollback resistance for Atom storage.

## Authority boundary

The registrar front service holds scoped read authority over credential-
binding records, append-only proposal authority for pending records, read-only
metadata trust roots, one-time enrollment challenge state, and audit append.
It may request proof from the verifier and intent from the trusted-interaction
broker.

Only a separately confined credential-ledger commit guard can change an active
binding. That guard exposes no arbitrary row-write API: its activation
transition atomically verifies and consumes an unforgeable, audience-bound,
one-shot verifier record, a target-principal/request-bound authorization record
for the initiator, and, for human credentials, a receipt from the trusted-
interaction broker. For add/replace, the record is a one-shot grant produced
inside a fixed credential-management issuer envelope from an authenticated PDP
permit whose evidence includes the current subject session. Recovery instead
requires a typed recovery-coordinator result naming the target and maximum
resulting assurance. The commit guard is the policy-enforcement point that
consumes this record. The evidence/decision/grant issuers cannot write the
ledger, and the registrar cannot forge their records.

It holds no active-binding mutation facet, resource capability, session root,
verifier signing authority, authenticator private key, recovery envelope, or
hidden delete function. A compromised registrar can propose records, disclose
inventory within its read scope, and deny service, but cannot activate a
binding without independently protected evidence. Compromise of a ledger
commit guard remains an impersonation root inside that guard's realm, so guard
and ledger authority are partitioned by tenant/security realm and high-impact
transitions require separated approval.

Separate tenants or security realms use separate ledgers and administrative
capabilities. Listing credentials is itself authorized because identifiers,
device types, and last-use data are sensitive.

## Record model

```text
CredentialBinding {
    binding_id,
    subject_id,
    credential_id,
    verifier_profile_and_audience,
    public_key_or_opaque_verifier_ref,
    algorithm,
    authenticator_type_and_transports,
    user_presence_and_verification_capability,
    phishing_resistance,
    hardware_protection_and_exportability,
    backup_eligibility_and_state,
    attestation_and_aaguid_refs,
    metadata_version_and_status,
    sign_count_signal,
    created_and_last_used_revisions,
    lifecycle_state_and_reason,
    provenance_and_audit_refs,
}
```

Subject handles are opaque and non-identifying. Notification destinations are
stored under a different protection label so inventory readers do not
automatically obtain recovery channels.

`sign_count` is a risk signal, not proof of cloning: authenticators can race,
malfunction, or not implement a useful counter. Backup eligibility is stable;
backup state can change. Synced and device-bound credentials therefore remain
distinct assurance facts rather than one `passkey` boolean.

## Lifecycle and enrollment transaction

```text
pending -> active -> suspended -> active
                  \-> compromised -> tombstoned
                  \-> expired -----> tombstoned
                  \-> removed -----> tombstoned
```

Enrollment proceeds as follows:

1. Authenticate the initiator at the policy-required assurance and bind the
   operation to the target principal.
2. Obtain a one-shot authorization record naming the initiator, target
   principal, add/replace/recover operation, maximum assurance, and exact
   request digest, plus a trusted-interaction receipt for a human ceremony.
3. Create a fresh, single-use challenge and pending record with an idempotency
   key and deadline.
4. Have the authentication verifier validate the complete response and
   attestation/metadata policy against the pending record.
5. Ask the separately confined commit guard to atomically validate the
   initiator-authorization, new-credential-verification, and trusted-intent
   issuers; commit the binding; consume all one-shot records; append the
   lifecycle event; and enqueue notification.
6. For replacement, require a successful test authentication with the new
   credential before retiring the old one unless an emergency policy says
   otherwise.

A crash before commit leaves only an expired pending record. A retry with the
same idempotency key returns the same result. A crash after commit cannot hide
the new credential from inventory or notification. Removal is another
transaction; it never deletes the historical identifier.

## Metadata and attestation policy

Metadata updates are signed, versioned, rollback-checked snapshots. A status
such as compromised authenticator or user-verification bypass can reduce
assurance, suspend new use, or trigger review. Network or metadata outage does
not silently upgrade an unknown device.

Attestation can reveal model/vendor identity and enable tracking. Deployment
profiles must state whether they require direct, enterprise, anonymized, or no
attestation and what privacy cost follows. Certification is not proof that a
synchronized provider, client platform, or account-recovery path is secure.

## OTP-like service and supervision contract

```text
begin_binding(subject, profile, idempotency, deadline)
  -> {ok, pending_ref, challenge} | typed_error
commit_binding(pending_ref, initiator_authorization, verifier_evidence,
               interaction_receipt_or_headless_recovery_evidence)
  -> {ok, binding_revision} | typed_error
change_state(binding_ref, expected_revision, transition, authorization)
  -> {ok, new_revision} | {error, conflict | forbidden | stale}
inventory(subject, cursor, disclosure_cap)
  -> bounded_page
```

The worker handling untrusted formats, registrar front service, evidence
issuers, and credential-ledger commit guard occupy separate unprivileged
protection domains. The registrar's supervisor may restart parsers and
metadata refresh independently, but it neither supervises nor inherits the
guard's mutation facet. No component retries a commit without the original
idempotency key or reconstructs missing proof as success.

## Failure and abuse analysis

| Hazard | Defense and explicit residual risk |
| --- | --- |
| Rogue-key or subject misbinding | Bind target, initiator authorization/recovery result, RP, challenge, interaction receipt, and verifier response in one transaction |
| Concurrent duplicate enrollment | Per-subject serialization plus idempotency and unique credential constraints |
| Silent downgrade | Versioned profile and algorithm registry; unknown/stale metadata never raises assurance |
| Snapshot resurrection | Protected monotonic ledger epoch and durable tombstones; fail restricted if anti-rollback is unavailable |
| Synced passkey abuse | Show provider/backup state, require stronger policy for high-impact roles, make removal reachable |
| Inventory hiding or coercion | Complete bounded inventory, protected naming, independent notification, tested removal ceremony |
| Metadata compromise | Separate trust roots, signature/expiry/rollback validation, reversible assurance reduction |
| Registrar compromise | Proposal-only writes; separate evidence issuers and commit guard; realm partition and threshold approval for high-impact bindings |

## Verification and evaluation plan

- Run WebAuthn/CTAP conformance and negative vectors for challenge, origin, RP
  ID, user handle, algorithm, flags, signature, attestation, and extension
  handling.
- Schedule parallel enrollments, response substitution, duplicate credentials,
  add/remove races, and a compromised authenticator transport.
- Cut power at every journal and notification point; restore an older disk
  image and assert tombstoned credentials remain unusable.
- Test metadata signature, expiry, rollback, revoked-status, and unavailable
  states without assurance inflation.
- Inspect BEAM heaps, mailbox traces, crash dumps, logs, and audit payloads for
  secrets or public-key records copied outside intended boundaries.
- Conduct inventory/removal user studies under shared-device, coercive, and
  periodic-unlocked-access threat models.
- Measure pending-record bounds, per-subject fairness, commit latency, metadata
  fan-out, and notification backlog under enrollment floods.

## Staged implementation

1. Implement a local public-key binding ledger with durable revisions and
   tombstones.
2. Integrate one WebAuthn/CTAP profile through the verifier and trusted broker.
3. Add explicit inventory, notification, suspension, replacement, and audit.
4. Add metadata and synchronized-credential profiles only after privacy and
   rollback policies are decided.
5. Add institutional threshold enrollment as a separate profile.

## Supported decisions and open questions

Supported: append-oriented records; no private keys; transactional proof plus
intent; visible inventory; tombstones; assurance is a vector, not one scalar.

Open: native RP/verifier naming, initial device-owner bootstrap, identity-
proofing profiles, metadata-offline behavior, synced-credential assurance,
notification ownership, and the protected monotonic storage mechanism.

## Connections

- [Trusted-interaction broker](trusted-interaction-broker.md)
- [Authentication verifier](authentication-verifier.md)
- [Session service](session-service.md)
- [Recovery coordinator](recovery-coordinator.md)
- [Main authentication and authorization synthesis](../authentication-and-authorization-across-the-five-layer-architecture.md)

## Sources

- [NIST SP 800-63B-4](../../30-sources/temoshok-et-al-2025-authentication-and-authenticator-management.md)
- [WebAuthn Level 3](../../30-sources/w3c-2026-webauthn-level-3.md)
- [CTAP 2.2](../../30-sources/fido-alliance-2025-ctap-2-2.md)
- [A formal analysis of the FIDO2 protocols](../../30-sources/guan-et-al-2022-formal-analysis-fido2.md)
- [The abusability of passkeys](../../30-sources/daffalla-et-al-2025-passkey-abusability.md)
- [FIDO Metadata Service](../../30-sources/fido-alliance-2026-metadata-service.md)
