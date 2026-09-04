---
title: "Key and secret service"
kind: note
created: "2026-09-04"
maturity: developing
tags:
  - cryptography
  - key-management
  - secrets
  - security
aliases:
  - "Cryptographic key broker"
  - "Secret lease service"
---

# Key and secret service

The recommended component is a **capability-native cryptographic broker whose
default object is a non-exportable, purpose-bound operation handle—not key
bytes**. Key custody, dynamic-secret adapters, lease scheduling, and recovery
ceremonies are separated so one plugin or logged-in token session is not a
universal signing/decryption oracle.

This is component 11 of the [authentication and authorization service
set](README.md).

## Question, scope, and operational standard

> How can Atom generate, use, rotate, revoke, recover, and destroy keys and
secrets while preventing raw material from escaping through messages, heaps,
traces, dumps, backups, broad HSM sessions, plugins, or confused-deputy calls?

Acceptance requires:

- every key object has immutable purpose, algorithm/profile, allowed
  operations, audience, owner, generation, export/wrap policy, hardware
  binding, lifecycle, validity/cryptoperiod, and protected metadata;
- callers receive separate capabilities for sign, verify, decrypt, derive,
  unwrap, attest, rotate, or destroy—never an ambient “use token” session;
- private/root keys are non-exportable by default, and any import/export/wrap
  route is independently authorized, typed, audited, and tested;
- requests bind caller incarnation, object generation, purpose, algorithm,
  canonical input digest, context, deadline, quota, and idempotency where
  needed;
- originator use can stop before historical recipient/verification use, so
  rotation does not erase the ability to verify or decrypt retained data;
- copied bearer secrets are treated as irretrievable after disclosure and only
  bounded by lease/rotation/backend revocation;
- metadata, key versions, leases, destruction tombstones, and recovery shares
  resist rollback; and
- crypto/HSM queues, renewals, revocations, and plugin failures are bounded and
  isolated.

## Evidence and synthesis

[NIST SP 800-57 Part 1
Rev. 5](../../30-sources/barker-2020-key-management.md) distinguishes key types,
uses, lifecycle states, cryptoperiods, metadata, inventory, compromise,
recovery, and destruction. Its central implication is that a signing key, data-
encryption key, authentication key, and wrapping key are different powers.

[PKCS #11
3.2](../../30-sources/oasis-2026-pkcs11-3-2.md) supplies typed token/session
objects, handles, attributes, mechanisms, and sensitive/extractable controls.
The [PKCS #11 usage
guide](../../30-sources/oasis-2025-pkcs11-usage-guide-3-2.md) exposes an
important limit: a logged-in Cryptoki session generally does not provide Atom-
style per-object least authority, and OS/application compromise can steal
activation input or misuse operations. Atom therefore uses a narrow broker,
not the full token API as a kernel ABI.

[TPM 2.0](../../30-sources/trusted-computing-group-2026-tpm-2-0-library.md)
provides protected objects, policy-gated operations, sealing, quotes, and NV/
counter primitives. Hardware protection does not choose good policy, prevent
all side channels, ensure fair scheduling, or make backup/recovery safe.

[Vault's secrets and lease
model](../../30-sources/hashicorp-2026-vault-secrets-and-leases.md) provides an
operational comparison for returned TTLs, renewal, revocation lineage, dynamic
credentials, and the crucial limit that a copied static secret is not recalled
merely because a broker later marks a nominal lease revoked. These are product
semantics and engineering lessons, not evidence that Vault's host/plugin trust
model should be imported into Atom.

## Authority and process split

Separate facets or protection domains own:

- key-object metadata and lifecycle transactions;
- hardware/software crypto operations;
- dynamic secret backend adapters;
- lease/renew/revoke scheduling;
- audit receipt emission; and
- threshold recovery-share ceremonies.

No adapter can enumerate or use every key. No client inherits a global HSM
login. The service has no policy/grant administration or application data
capability. Root and issuer keys are available only through operation-specific
handles constrained to canonical payload types.

## Objects and facets

```text
KeyObject {
    key_id_and_generation,
    owner_and_security_realm,
    purpose_and_allowed_operations,
    algorithm_parameters_and_profile,
    origin_and_entropy_provenance,
    hardware_or_software_binding,
    sensitive_extractable_wrap_backup_policy,
    activation_originator_recipient_periods,
    lifecycle_and_compromise_state,
    metadata_revision_and_audit_refs,
}

KeyFacet {
    parent_key,
    operation,
    caller_or_audience,
    input_schema_and_context,
    use_rate_count_and_time_budget,
    expiry_and_revocation_anchor,
}

SecretLease {
    lease_id_and_parent,
    holder_and_purpose,
    version_or_backend_ref,
    issued_expiry_and_max_ttl,
    renewable,
    backend_revocation_state,
}
```

`sign(release_metadata)` and `sign(arbitrary_bytes)` are different facets.
Decryption accepts an authenticated envelope and policy context, not arbitrary
ciphertext, to limit oracle use. Public verification material may be exportable
under a separate read facet.

## Key and lease lifecycles

```text
preactive/imported -> active_originator -> rotate_prepublished
                   -> recipient_or_verify_only -> retired
                   -> compromised -> disabled -> destroyed+tombstone
```

Rotation publishes the new verification/decryption relationship before ending
old originator use. Destruction records an irreversible tombstone and verifies
backend/device state; inability to confirm becomes `destruction_uncertain`, not
success.

Secret leases follow:

```text
issued -> active -> renewed | expired | revoke_requested
revoke_requested -> backend_confirmed | revocation_uncertain
```

The returned TTL is authoritative. A static secret stored in a KV-like backend
is not made recallable by attaching a nominal lease after it has been copied.

## Operation protocol and BEAM boundary

```text
create(profile, purpose, owner, approvals) -> key_facets | typed_error
operate(facet, canonical_input, context, idempotency, deadline)
  -> bounded_output_or_receipt | typed_error
rotate(key_ref, plan, approvals) -> generation_and_progress
destroy(key_ref, approvals, expected_generation) -> confirmed | uncertain
lease(secret_profile, holder, purpose, ttl) -> lease_handle | typed_error
```

Raw secret material never becomes an Erlang term in the native profile.
Conventional NIFs execute inside the VM address space, so the high-assurance
profile forbids NIFs that handle raw secrets. Crypto libraries, HSM/TPM
adapters, drivers, compatibility export, and any native implementation run as
ports or external services in separately confined unprivileged domains. Trace,
crash-dump, inspect, serialize, copy, compare, and log operations on opaque
handles are nonrevealing.

The runtime cannot guarantee zeroization of arbitrary copied immutable terms;
therefore “zeroize later” is not a substitute for never importing a key into
the managed heap.

## Failure, compromise, and overload analysis

| Hazard | Required handling |
| --- | --- |
| Broad signing/decryption oracle | Per-purpose input schema, audience, operation facet, quotas |
| Raw key copied to heap/dump | Non-exportable handles and confined native adapter |
| Shared HSM login amplifies client | Broker mediates each object/use; never delegate logged-in global session |
| Metadata/key rollback | Authenticated sealed metadata plus protected high-water and tombstones |
| Split-brain rotation | One authoritative generation transaction and overlap state |
| Backend revoke fails | `revocation_uncertain`; expire credentials and restrict dependent actions |
| Lease/renew storm | Bounded leases, randomized renewal, batch revoke, fair queues, reserved control lane |
| Crypto queue contention | Per-principal rate/work budgets and priority for revoke/lock/recovery |
| Plugin compromise | One backend/namespace per domain; no universal key enumeration |
| Recovery share concentration | Independent custodians, threshold, sealed shares, rehearsed replacement |

## Verification and evaluation plan

- Run algorithm/TPM/PKCS conformance vectors and an exhaustive negative matrix
  of every operation against every facet, purpose, state, and caller.
- Attempt export through plaintext, wrap, backup, migration, error, debug,
  trace, heap, crash dump, swap, audit, and plugin interfaces.
- Power-cut at generation, metadata seal, activation, prepublication, originator
  stop, recipient drain, revoke, destroy, and tombstone commits; roll snapshots
  backward.
- Test type/algorithm/context confusion and malformed inputs in confined crypto
  workers; differential-test parsers and signatures.
- Exercise cryptoperiod overlap and prove new signing/encryption stops while
  required historical verify/decrypt remains.
- Saturate HSM/TPM queues, lease creation/renewal/revocation, and one tenant;
  measure fairness, cancellation, deadlines, and reserved emergency capacity.
- Perform a threshold recovery drill and verify recovered authentication/
  signing keys follow replacement rules while data-key recovery is explicitly
  recorded as decryption authority.

## Staged implementation

1. Software-backed opaque handles with per-operation facets and no export.
2. Protected metadata/lifecycle journal, rotation, destruction tombstones, and
   audit.
3. One TPM/HSM adapter with queue budgets and conformance tests.
4. Dynamic secret leases with honest backend-revocation status.
5. Threshold recovery and additional crypto profiles only after governance and
   target side-channel assumptions are documented.

## Supported decisions and open questions

Supported: purpose-specific non-exportable handles; no global crypto session;
metadata protected like keys; explicit lifecycle; copied secrets cannot be
recalled; recovery powers differ by key type.

Open: first hardware/FIPS profile, algorithms and post-quantum agility, BEAM-
safe buffer discipline, entropy health, HSM scheduling, sealed-store crash
protocol, backup format, and recovery governance.

## Connections

- [Workload identity issuer](workload-identity-issuer.md)
- [RATS Verifier and Appraisal Policy](rats-verifier-and-appraisal-policy.md)
- [Grant compiler and issuer](grant-compiler-and-issuer.md)
- [Recovery coordinator](recovery-coordinator.md)
- [Update and release service](update-and-release-service.md)

## Sources

- [NIST key-management guidance](../../30-sources/barker-2020-key-management.md)
- [PKCS #11 3.2](../../30-sources/oasis-2026-pkcs11-3-2.md)
- [PKCS #11 3.2 usage guide](../../30-sources/oasis-2025-pkcs11-usage-guide-3-2.md)
- [TPM 2.0 Library](../../30-sources/trusted-computing-group-2026-tpm-2-0-library.md)
- [Vault secrets, leases, and security model](../../30-sources/hashicorp-2026-vault-secrets-and-leases.md)
