---
title: "Authentication verifier"
kind: note
created: "2026-09-04"
maturity: developing
tags:
  - authentication
  - credentials
  - fido2
  - security
  - webauthn
aliases:
  - "Credential verifier service"
---

# Authentication verifier

The recommended component is a **set of protocol-confined verifier workers
behind one small evidence interface**. Each worker owns fresh challenges,
bounded parsing, protocol validation, atomic replay state, and persistent
throttling for one registered profile. Successful verification returns a
short-lived, one-use `AuthenticationEvidence` capability—not a session and not
permission to touch a resource.

This is component 2 of the [authentication and authorization service
set](README.md).

## Question, scope, and operational standard

> How can Atom verify human or recovery authenticators without placing complex
> protocol parsers, password work factors, transport quirks, or reusable
> authentication assertions inside the kernel or grant issuer?

Acceptance requires:

- every attempt begins with a fresh challenge bound to subject, verifier,
  purpose, audience, caller incarnation, request digest, boot epoch, and
  deadline;
- a response finalizes the challenge exactly once whether it succeeds or fails;
- the selected verifier profile pins canonical parsing, allowed algorithms,
  origin/RP rules, user-presence/verification requirements, and credential
  lifecycle revision;
- verification evidence records what was actually established and never claims
  more assurance than the credential and ceremony support;
- evidence is opaque, non-bearer, audience-specific, short-lived, and atomically
  consumed by the session service or named coordinator;
- parser failure, metadata outage, clock uncertainty, replay-store failure, or
  unsupported extension returns a typed non-success;
- expensive cryptography and password hashing are admission-controlled and
  bounded per principal/source before they can exhaust the system; and
- restart cannot reset throttling, resurrect challenges, or convert an
  incomplete attempt into success.

## Evidence and synthesis

[WebAuthn Level
3](../../30-sources/w3c-2026-webauthn-level-3.md) provides the relying-party
validation algorithm and distinguishes user presence, user verification,
backup state, and counter signals. [CTAP
2.2](../../30-sources/fido-alliance-2025-ctap-2-2.md) defines the client-to-
authenticator transport and PIN/UV permission model. [Guan et
al.](../../30-sources/guan-et-al-2022-formal-analysis-fido2.md) demonstrate why
parallel ceremonies, client/authenticator composition, and rebinding must be
modeled rather than assuming the standards compose automatically.

[NIST SP
800-63B-4](../../30-sources/temoshok-et-al-2025-authentication-and-authenticator-management.md)
separates replay resistance, phishing resistance, authentication intent,
verifier compromise, throttling, and authenticator assurance. [RFC
9106](../../30-sources/biryukov-et-al-2021-argon2.md) supplies a current
memory-hard password primitive and also exposes the verifier-side denial-of-
service cost.

Atom's typed evidence, challenge finalization, and worker isolation are
architectural proposals. Passing protocol conformance does not prove native
trusted-path composition or authorization correctness.

## Authority boundary

The front service holds challenge/replay records, read-only access to active
credential revisions, rate-limit state, and narrowly scoped endpoints to
protocol workers and authenticators. A password worker may read only its
opaque verifier record; a FIDO worker may read only the selected public key and
profile.

It cannot add/remove credentials, create or elevate sessions, recover a
principal, edit policy, mint resource grants, or use the authenticated
principal's resources. Complex CBOR, COSE, JSON, certificate, vendor, and
compatibility parsers run in distinct unprivileged Layer-4 parser domains whose
memory, authority, IPC identity, and CPU/message/deadline limits Layer 2
enforces.

## Challenge and evidence objects

```text
AuthenticationChallenge {
    challenge_id_and_random_value,
    subject_hint_or_discoverable_mode,
    verifier_profile_and_audience,
    purpose_and_request_digest,
    intended_recipient_domain_and_generation,
    explicit_delegatee,
    seat_and_channel_binding,
    proof_key_binding,
    credential_set_revision,
    required_assurance_vector,
    issued_at_monotonic,
    deadline,
    boot_epoch,
}

AuthenticationEvidence {
    evidence_id,
    subject,
    credential_id_and_revision,
    verifier_profile_and_audience,
    purpose_and_request_digest,
    authentication_time,
    user_presence,
    user_verification,
    phishing_and_replay_resistance,
    hardware_and_exportability_facts,
    risk_signals,
    assurance_ceiling,
    expires_at,
    boot_epoch,
    intended_recipient_domain_and_generation,
    explicit_delegatee,
    seat_and_channel_binding,
    proof_key_binding,
    single_consumer_service,
}
```

Layer 2 supplies the authenticated caller domain and generation when the
challenge is created; the caller does not serialize that fact. The intended
session recipient, explicit delegatee, seat/channel, proof key, audience,
purpose, and request digest survive unchanged into the evidence so the session
service can compare them with its own authenticated IPC peer and proof rather
than accepting a new caller-provided binding.

Risk signals—counter regression, newly backed-up status, unfamiliar transport,
or metadata warning—remain facts. The verifier neither invents a risk policy
nor silently upgrades a credential because a field is absent.

## State machine and atomicity

```text
issued -> parsing -> validating -> verified -> consumed
   |         |           |            \-> expired
   |         |           \-> failed
   |         \-> failed
   \-> cancelled | expired
```

The transition to `verified` consumes the challenge and records the replay
decision in the same durable transaction that publishes evidence. Any response
after `failed`, `cancelled`, or `expired` is a replay. A retry begins a new
challenge. The evidence consumer atomically consumes the handle with session
creation or the named one-shot operation.

For WebAuthn, validation includes ceremony type, exact challenge, trusted
origin/top-origin policy, RP ID hash, credential and subject mapping, UP/UV,
algorithm and signature, extensions, backup-state consistency, and counter
signal. Native login needs an Atom-specific verifier-name/RP-ID profile; simply
calling a browser API does not define it.

## Password compatibility profile

Passwords are optional compatibility authenticators, not the architecture's
preferred root. The trusted-interaction broker sends the password directly to
the password worker. The registrar stores an opaque salted Argon2id verifier
record with algorithm/version/parameters.

The worker:

- admits a bounded attempt before allocating the configured memory cost;
- uses a constant-behavior nonexistent-account path to limit enumeration;
- combines per-account, per-source, and global limits without allowing trivial
  lockout attacks;
- persists retry state and protects it against rollback;
- upgrades parameters only after successful verification; and
- zeroizes/cages working buffers as far as the runtime and target make
  meaningful, while documenting that BEAM copying/GC can defeat naive claims.

Password success is not phishing-resistant and cannot create an AAL3-like
session.

## OTP-like protocol and supervision

```text
challenge(profile, purpose, request_digest, recipient_proof_key, deadline)
  -> challenge | typed_error
respond(challenge_ref, bounded_response) -> evidence_handle | typed_failure
cancel(challenge_ref) -> ok | stale
```

The coordinator uses transient workers under a rest-for-one strategy only
where dependencies require it. Parser crashes invalidate their challenge
generation but do not restart the credential ledger or session service.
Backpressure is explicit; mailboxes never hold unbounded responses.

## Failure and abuse analysis

| Hazard | Required handling |
| --- | --- |
| Challenge replay or race | Atomic terminal state and one evidence publication |
| Origin/RP/account mix-up | Bind and validate all fields against the immutable challenge |
| UP confused with UV | Preserve separate flags and policy-required minimum |
| Algorithm/type confusion | Profile-pinned algorithms and explicit token/COSE types |
| Parser differential | Canonical encoding plus fuzzing and independent/reference differential tests |
| Credential removed during attempt | Pin revision and recheck active state at evidence publication/consumption |
| Password CPU/memory flood | Pre-crypto admission, bounded worker pool, quotas, cancellation |
| Retry rollback on reboot | Protected counter/epoch; fail restricted if unavailable |
| Verifier compromise | No registrar, session, policy, or resource authority; rotate verifier generation |

## Verification and evaluation plan

- Run W3C and FIDO conformance suites plus a negative test for every validation
  step and every typed failure.
- Coverage-fuzz CBOR, COSE, JSON, certificate chains, extensions, UTF-8, and
  response framing in isolated workers; compare independent decoders.
- Model parallel registration/authentication, subject rebinding, challenge
  consumption, credential removal, and session consumption.
- Race identical responses across CPUs and restart the verifier at each commit
  point; assert at most one evidence object.
- Test Argon2 vectors, parameter migration, nonexistent accounts, rollback,
  cancellation, memory pressure, fair admission, and distributed throttling.
- Inspect traces, heaps, crash dumps, logs, and audit events for activation
  secrets, responses, or freely replayable evidence.
- Measure p50/p99/worst latency and bounded resource use by profile under valid,
  malformed, and adversarial traffic.

## Staged implementation

1. Implement the evidence/challenge algebra and a deterministic fake verifier.
2. Add one hardware-backed public-key profile and replay/throttle persistence.
3. Integrate the trusted broker and session-service atomic consumption.
4. Add password compatibility in a separate budgeted domain.
5. Add further protocols only with a profile, conformance corpus, parser limits,
   downgrade rules, and compromise-recovery plan.

## Supported decisions and open questions

Supported: verification produces evidence only; one terminal response per
challenge; separate protocol domains; persistent throttling; public-key,
phishing-resistant authentication as preferred baseline.

Open: native verifier naming, credential-discovery privacy, exact algorithms,
hardware authenticator transports, retry policy, secure heap treatment in a
BEAM-compatible runtime, and whether the first profile supports passwords.

## Connections

- [Credential registrar and inventory](credential-registrar-and-inventory.md)
- [Trusted-interaction broker](trusted-interaction-broker.md)
- [Session service](session-service.md)
- [Policy decision point](policy-decision-point.md)
- [Main authentication and authorization synthesis](../authentication-and-authorization-across-the-five-layer-architecture.md)

## Sources

- [NIST SP 800-63B-4](../../30-sources/temoshok-et-al-2025-authentication-and-authenticator-management.md)
- [WebAuthn Level 3](../../30-sources/w3c-2026-webauthn-level-3.md)
- [CTAP 2.2](../../30-sources/fido-alliance-2025-ctap-2-2.md)
- [A formal analysis of the FIDO2 protocols](../../30-sources/guan-et-al-2022-formal-analysis-fido2.md)
- [Argon2](../../30-sources/biryukov-et-al-2021-argon2.md)
