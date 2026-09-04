---
title: "Authentication and authorization across the five-layer architecture"
kind: note
created: "2026-09-04"
maturity: developing
tags:
  - authentication
  - authorization
  - capabilities
  - distributed-systems
  - operating-systems
  - security
  - systems-architecture
aliases:
  - "Atom OS security architecture"
  - "System-wide authentication and authorization"
---

# Authentication and authorization across the five-layer architecture

## Conclusion

Atom OS should use a **two-plane security architecture** rather than put login
logic in the kernel or rely on a global logged-in user:

1. An unprivileged **identity and policy control plane** verifies evidence,
   establishes sessions, evaluates policy, and decides what authority may be
   issued.
2. A **capability data plane** carries and enforces already bounded authority
   at the resource boundary.

The end-to-end chain is:

```text
evidence -> authenticated principal -> session -> policy decision
         -> attenuated grant -> local capability -> mediated effect
```

No arrow is implicit. Authentication proves control of a credential under a
particular ceremony; attestation supplies evidence about a platform or
workload; policy decides what that evidence means; a grant records that
decision; a capability makes the permitted operation possible. A principal
name, PID, role, filesystem path, device measurement, certificate, network
location, or successful login is not itself authority.

This gives the five layers distinct responsibilities:

- hardware supplies protection, key, measurement, entropy, DMA, and trusted-
  interaction roots;
- the minimal kernel enforces typed capabilities, object generations,
  budgets, and revocation boundaries;
- the managed runtime preserves authority explicitly across actors without
  treating PIDs or supervision as permission;
- OTP-like services implement authentication, policy, session, attestation,
  grant, recovery, and audit mechanisms as separately confined services; and
- applications and the CLI request and consume narrow operation-scoped
  authority as ordinary unprivileged clients.

“Unauthenticated” must not mean “the authorization check was skipped.” A
pre-authentication domain represents an explicit anonymous principal and
receives only deliberately public or bootstrap capabilities, such as bounded
help, login, recovery, shutdown, and network-configuration entry points.
Sensitive objects are structurally unreachable until an authorized issuer
derives a capability from its own predeclared envelope.

This is a proposed architecture supported by literature and standards. It is
not yet an implementation result, a proof about Atom OS, or evidence that a
particular authenticator, policy engine, hardware root, or user interface is
secure in the eventual system.

## Research question and operational standard

The practical question is not whether the system can claim to be “the most
secure possible.” No design maximizes assurance, availability, recoverability,
privacy, usability, cost, legacy compatibility, and disconnected operation at
the same time. The answer must instead be evaluated against a concrete
operational standard:

- every protected effect has a named policy-enforcement boundary;
- every grant is created by monotonic derivation from an audited root of
  authority;
- anonymous code has no path to non-public objects;
- every accepted request is bound to an authenticated subject, current actor,
  action, exact object generation, audience, policy revision, validity window,
  revocation lineage, and resource budget;
- missing, stale, contradictory, or unverifiable evidence produces a typed
  non-permit result;
- delegation cannot amplify rights, duration, budget, audience, or
  delegation depth;
- policy change, revocation, logout, failure, and reboot have explicit
  semantics for new and already admitted work;
- authentication and recovery work cannot exhaust the rest of the system; and
- each security claim names its hardware, firmware, kernel, compiler, runtime,
  policy, cryptographic, time, network, and operational assumptions.

The design should be rejected or revised if testing finds a protected effect
without mediation, an authority path not rooted in the boot manifest, a PID or
name usable as authority, a stale policy decision that can expose newly
protected data, an unbounded unauthenticated workload, a recovery path broader
than its declared purpose, or a service that can silently combine policy edit,
credential verification, arbitrary grant issuance, audit deletion, and
recovery powers.

## Threat model

The architecture should contain or bound:

- a malicious or compromised application, shell command, BEAM actor, runtime
  domain, native extension, driver, network peer, and ordinary authenticated
  user;
- stolen bearer material, replayed assertions, compromised synchronized
  credential providers, weak account recovery, and coerced or confused users;
- UI spoofing, fake login prompts, clickjacking-like composition, full-screen
  capture, and credential prompts generated by applications;
- confused-deputy requests in which a less privileged caller induces a more
  privileged service to misuse its ambient authority;
- mutable-name and authorization time-of-check/time-of-use races;
- stale policy or relationship replicas, rollback, partitions, clock failure,
  and token replay across nodes;
- resource-exhaustion attacks against pre-authentication parsing, public
  endpoints, secure attention, cryptography, policy evaluation, audit, and
  revocation;
- service crash, restart, partial completion, failover, and delayed or lost
  revocation messages;
- boot or update rollback, dishonest attestation evidence, and compromised
  supply-chain components within explicitly named trust assumptions; and
- recovery, break-glass, debug, update, and audit interfaces becoming shadow
  superuser mechanisms.

A compromised kernel or hardware root remains catastrophic for guarantees it
enforces. A compromised identity, policy, or grant service is also serious,
but its possible damage should remain bounded by its kernel-issued capability
envelope. Side channels, coercion, malicious hardware below the selected root,
and an authorized reader deliberately disclosing plaintext are not solved by
ordinary access control; high-confidentiality profiles need additional static
partitioning or information-flow controls.

## Keep the security facts separate

| Fact | Question answered | Must not be treated as |
| --- | --- | --- |
| Authentication evidence | Did a claimant prove control of an accepted authenticator in this ceremony? | Permission, benign intent, civil identity, device health, or current session validity |
| Principal | Which durable or pseudonymous identity did the verifier bind to that evidence? | A process, a credential, a role, or a capability |
| Attestation result | What did an appraiser conclude about supplied platform/workload evidence under a named policy and freshness bound? | Authentication or direct authorization |
| Session | Which principal, assurance, device/workload context, proof-of-possession key, and expiry are currently bound together? | A global bag of the principal's possible rights |
| Policy decision | Should a specific subject and actor perform this action on this exact resource under this versioned context? | A durable capability or proof that the effect occurred |
| Grant | What narrowly bounded authority did an issuer encode from that decision? | A mutable role name or an ambient login state |
| Capability | What operation can this holder actually invoke on this object at the enforcement boundary? | Human identity or policy meaning |
| Ownership | Who controls lifecycle or policy for a resource? | Liveness, memory ownership, or unconditional access |
| Budget | Who pays for CPU, memory, queue, crypto, I/O, and revocation work? | Permission to access the resource |
| Completion | What state transition did the protected operation actually reach? | Authentication, authorization, cancellation, or successful intent |
| Audit evidence | What did an observer record, in what order, with what integrity assumptions? | Proof that the recorded claim was true or that nothing was omitted |

This separation carries forward the archive's existing rule that identity,
authority, ownership, accounting, liveness, and completion are independent
dimensions.

## The two planes

```text
                         IDENTITY AND POLICY CONTROL PLANE

  evidence ---> verifier ---> principal/session ---> policy decision
      |               |               |                    |
      |               |               |                    v
      |               |               +-----------> bounded grant issuer
      |               |                                    |
      |               +---- audit references               |
      +---- not authority                                  v

  ========================================================================

                            CAPABILITY DATA PLANE

  local capability ---> policy enforcement point ---> admitted operation
          |                         |                          |
          +---- object generation -+---- lifecycle/budget ----+
```

The control plane may be distributed and policy-rich, but it remains outside
the privileged kernel. The data plane is small: the kernel and resource
servers only need to recognize protected object identity, typed rights,
generation and revocation state, the caller's local capability, admission
state, and charged resource envelope.

The grant issuer is a security compiler. It translates a versioned policy
decision into a local capability or remote proof, but it cannot create more
authority than its own kernel capability permits. This bounds even an
incorrect policy rule or compromised issuer. Conversely, a capability can be
technically valid yet inappropriate under current policy; short leases,
generation fencing, revocation, and exact resource binding bound that gap.

## Mandatory request path

Every protected operation should follow the same logical path even when safe
fast paths collapse several steps:

1. The caller presents a routing name or existing capability. A name only
   locates an object; it does not authorize use.
2. The policy enforcement point identifies the `subject` that originated the
   request and the `actor` currently exercising authority.
3. It identifies the typed `action`, exact resource object and generation, and
   expected resource version.
4. It checks whether the session's authentication assurance, age, device or
   workload posture, and proof-of-possession binding satisfy the action's
   admission profile.
5. If assurance is missing or stale, it returns `unauthenticated` or
   `step_up_required`, not a generic denial.
6. The policy service evaluates a complete, typed, versioned query against
   authoritative relationship and attribute snapshots.
7. A permit result describes the narrow rights, lifetime, budget, audience,
   object generation, obligations, and delegation depth that may be issued.
8. A separately confined issuer derives a local capability or creates a
   short-lived sender-constrained remote grant within its own envelope.
9. The resource server validates and consumes the grant against the current
   object generation and expected version in the same transaction that admits
   the effect.
10. The admitted operation follows the resource's reserve, prepare, publish,
    close, drain, quiesce, sanitize, and retire-or-quarantine lifecycle.
11. The service returns a typed completion result. Timeout, cancellation,
    revocation, and nonexecution remain distinct.
12. Audit records the decision and observed outcome without storing raw
    credentials, keys, secrets, or unnecessary personal data.

This path is the system's reference monitor at architectural scale. The
reference-monitor argument comes from the [Anderson security-kernel
study](../30-sources/anderson-1972-computer-security-technology-planning-study.md),
while complete mediation, least privilege, economy of mechanism, and fail-safe
defaults come from [Saltzer and
Schroeder](../30-sources/saltzer-schroeder-1975-protection-information.md).
Atom OS still has to show that all relevant effect paths actually traverse the
mechanism.

## Placement across the five layers

| Layer | Security responsibilities | Deliberately excluded |
| --- | --- | --- |
| 1. Hardware and architecture support | Privilege separation, page/PMP protection, IOMMU confinement, interrupt ownership, entropy, protected key operations, measured/verified boot support, anti-rollback state where available, unforgeable secure-attention or physical-presence event | Password, WebAuthn, CTAP, certificate, token, CBOR/JSON, role, consent, or recovery-policy parsing |
| 2. Minimal privileged kernel | Typed capability enforcement, object identity and generation, domain isolation, explicit transfer, budgets, revocation anchors, admitted-operation state, exclusive trusted-path handoff | User database, civil identity, roles, policy language, OAuth, X.509 validation, UI content, audit-retention policy |
| 3. Managed actor runtime | Opaque capability handles, explicit authority transfer, launch manifests, subject/actor propagation, actor budgets, isolation of native trust boundaries | PID-as-permission, supervisor inheritance of child authority, serialization of kernel capabilities, credential collection |
| 4. OTP-like system services | Authenticators, identity and credential inventory, sessions, workload identity, attestation appraisal, policy, relationship/attribute authorities, bounded grant issue, keys, revocation, audit, recovery, federation gateway | One omnipotent IAM daemon or policy bypass on service failure |
| 5. Applications and domain services | Typed resources/actions, policy-enforcement points, trusted-path requests, least-authority command actors, domain-specific obligations and completion evidence | Collecting OS credentials, interpreting raw PCRs, minting trusted identity, assigning own roles, assuming “local” is trusted |

### Layer 1 — hardware and architecture support

Layer 1 should provide mechanisms on which stronger claims can be based:

- privilege rings or modes and memory protection for kernel, service, driver,
  runtime, and application domains;
- IOMMU or equivalent DMA confinement so a device cannot bypass CPU page
  protection;
- isolated entropy and key-generation primitives, monotonically advancing or
  rollback-resistant state where the target supports it, and protected key use
  so callers receive sign/decrypt/derive results rather than raw key bytes;
- verified boot for deciding which signed image may run, measured boot for
  recording what ran, and protected event logs needed for later appraisal;
- an unforgeable secure-attention or physical-presence event and a way to hand
  exclusive display/input authority to a trusted domain; and
- hardware identities or compound device identifiers usable as evidence for a
  device-specific key hierarchy.

The [TPM 2.0 Library](../30-sources/trusted-computing-group-2026-tpm-2-0-library.md)
is the full-featured profile; [DICE hardware
requirements](../30-sources/trusted-computing-group-2024-dice-hardware-requirements.md)
are an embedded profile. A TPM quote, DICE compound identity, boot
measurement, or signed image is evidence, not permission. The layer exposes
narrow semantic operations and protected handles; complex TPM, CTAP, X.509,
CBOR, and policy parsers stay outside privilege.

CHERI-like tagged capabilities can strengthen native memory safety and
compartmentalization. The [Morello proof
work](../30-sources/bauereiss-et-al-2022-verified-morello-security.md) is
valuable evidence about a particular architecture model, not proof about Atom
OS and not a replacement for authentication or policy.

### Layer 2 — minimal privileged kernel

Every protected kernel object is named by an unforgeable, typed capability.
Rights should distinguish at least:

- invoke or use;
- receive or accept;
- delegate or grant;
- manage or reconfigure;
- revoke descendants;
- destroy or retire; and
- allocate or charge a resource budget.

Rights, duration, audience, object set, resource budget, and delegation depth
can only narrow during derivation. A local capability selector is an index
into a protected capability table, never a serializable bearer value.

The kernel maintains object generations, revocation anchors or derivation
provenance, bounded queues, resource charges, and explicit admitted-operation
records. A generation change prevents an old grant for a destroyed object from
authorizing a new object that reuses the same name or storage. Revocation-tree
walks are charged, bounded, interruptible, and resumable so an attacker cannot
turn delegation structure into unbounded privileged work.

The boot loader installs a versioned, checked manifest that creates initial
domains and the minimum authority graph. Bootstrap authority is then shed or
sealed. There is no UID 0, ambient superuser, “same machine means trusted,” or
kernel escape hatch for support. [Lampson's protection
model](../30-sources/lampson-1971-protection.md), the [confused-deputy
analysis](../30-sources/hardy-1988-confused-deputy.md), and systems such as
[KeyKOS](../30-sources/hardy-1990-keykos-architecture.md),
[EROS](../30-sources/shapiro-et-al-1999-eros.md), and
[Capsicum](../30-sources/watson-et-al-2010-capsicum.md) support this direction.
They do not establish the security of Atom OS's future object model.

Secure-attention kernel code should only validate the unforgeable event,
freeze or revoke competing display/input leases, and transfer exclusive
authority to an isolated trusted-interaction service. It should not implement
credential ceremonies or user-facing policy.

### Layer 3 — managed actor runtime

BEAM processes remain cheap language actors, not automatic hardware security
principals. PIDs, registered names, links, monitors, supervisor ancestry,
mailbox metadata, and trace context are routing, lifecycle, or observation
facts. None grants access.

Each protected runtime domain receives a checked launch manifest containing
only opaque, non-serializable capability handles and resource budgets. Spawn,
link, restart, or hot-code replacement does not implicitly inherit the
runtime, parent, or supervisor's authority. Capability transfer is a typed
kernel-mediated operation that requires both sender delegation authority and
receiver slot/admission authority. Ordinary BEAM term construction,
serialization, persistence, distribution, or logging cannot forge or export
the handle.

Messages carry separate provenance fields when needed:

```text
subject = principal on whose behalf the operation originated
actor   = current workload/domain exercising authority
chain   = bounded, integrity-protected delegation history
```

Those fields inform policy and audit but do not authorize a receive or effect.
The capability attached to the operation does. Services must validate that
the subject/actor/audience binding in a grant matches the actual IPC peer and
resource endpoint to prevent a confused deputy from replaying another
caller's grant.

Native extensions, JIT helpers, decoders, crypto, network stacks, and drivers
belong in separately confined domains when they cross trust boundaries. One
runtime should not host mutually distrustful tenants unless its isolation is
independently proved. Runtime supervision can restore availability; it cannot
retroactively authorize work or repair a leaked secret.

### Layer 4 — OTP-like security services

The control plane should be decomposed by authority, not gathered into a
single identity daemon:

| Service | Holds | Does not hold |
| --- | --- | --- |
| [Trusted-interaction broker](authentication-and-authorization-components/trusted-interaction-broker.md) | Exclusive trusted display/input lease, ceremony state, request-bound challenge channel | Arbitrary resource capabilities, policy-edit rights, raw long-term keys |
| [Credential registrar and inventory](authentication-and-authorization-components/credential-registrar-and-inventory.md) | Principal-to-authenticator bindings, assurance metadata, lifecycle status | General application authority or hidden credential removal |
| [Authentication verifier](authentication-and-authorization-components/authentication-verifier.md) | Protocol-specific verification envelopes, replay state, rate limits | Policy-edit or arbitrary capability-minting authority |
| [Session service](authentication-and-authorization-components/session-service.md) | Session anchors, assurance/age, proof-of-possession binding, generation, expiry | The principal's complete possible authority |
| [Workload identity issuer](authentication-and-authorization-components/workload-identity-issuer.md) | Manifest/domain evidence and narrowly scoped workload credentials | Human credentials, roles inferred from names, application data |
| [RATS Verifier and Appraisal Policy owner](authentication-and-authorization-components/rats-verifier-and-appraisal-policy.md) | Evidence appraisal, endorsements, reference values, freshness policy | Direct resource capabilities or application policy |
| [Relationship authority](authentication-and-authorization-components/relationship-authority.md) | Versioned ownership, membership, sharing, and revocation facts | Authentication secrets or arbitrary effect authority |
| [Attribute authorities](authentication-and-authorization-components/attribute-authorities.md) | Signed, typed, short-lived claims with provenance | Self-asserted values or policy decisions |
| [Policy decision point](authentication-and-authorization-components/policy-decision-point.md) | Pure evaluation over versioned inputs | Side effects, credentials, kernel authority, or mutable lookup during evaluation |
| [Grant compiler/issuer](authentication-and-authorization-components/grant-compiler-and-issuer.md) | A bounded capability envelope and one decision-to-grant transformation | Policy-edit, credential, recovery, audit-deletion, or unlimited minting authority |
| [Revocation and epoch service](authentication-and-authorization-components/revocation-and-epoch-service.md) | Session/object/relation epochs, ordered invalidations, freshness watermarks | Secret disclosure or silent recovery activation |
| [Key and secret service](authentication-and-authorization-components/key-and-secret-service.md) | Non-exportable key handles, sealed objects, explicit sign/decrypt/derive facets | Policy bypass, debugging access, raw-key export by default |
| [Audit and witness services](authentication-and-authorization-components/audit-and-witness-services.md) | Append-only event admission, forward-integrity state, external commitments | Credential secrets, policy bypass, unilateral log deletion |
| [Recovery coordinator](authentication-and-authorization-components/recovery-coordinator.md) | Predeclared recovery workflow and narrowly scoped recovery envelopes | Ordinary administrator session or universal read authority |
| [Update/release service](authentication-and-authorization-components/update-and-release-service.md) | Threshold verification, freshness and rollback policy for signed artifacts | Identity-root, audit-root, or recovery-root keys |
| [Federation gateway](authentication-and-authorization-components/federation-gateway.md) | Remote protocol parsing, issuer/audience/PoP validation, local capability derivation within its envelope | Deserializing a kernel capability or trusting network location |

The [component research index](authentication-and-authorization-components/README.md)
develops each row as a separate evidence-backed implementation report. The
reports use the same review frame—authority boundary, typed objects, protocol
and supervision, failure and compromise behavior, verification, and staged
implementation—so their contracts can be checked together rather than treated
as sixteen independent daemons.

No service should combine policy editing, identity proofing, evidence
verification, arbitrary grant issuance, revocation override, update signing,
audit deletion, and recovery. High-impact credential, policy, trust-root,
recovery, and release changes require separated roles and, for high-assurance
profiles, threshold approval.

Supervisors restart these services under declared policies. If a verifier,
policy service, revocation authority, trusted clock, or grant issuer is
unavailable, the default response is a typed failure or restricted mode—not a
fall-through allow.

### Layer 5 — applications, CLI, and domain services

Applications define typed resource and action schemas, place policy-
enforcement points at actual effect boundaries, request authentication or
step-up, and consume narrow grants. They do not collect OS credentials,
interpret raw PCRs, mint trusted identity, assign their own administrative
roles, or treat a route, endpoint name, localhost address, process ancestry,
or successful TLS handshake as authorization.

The CLI is an unprivileged presentation and orchestration application:

- the pre-login CLI holds only public help, bounded authentication, recovery,
  shutdown, and network-bootstrap entry capabilities;
- an authenticated shell receives a session namespace and launch authority,
  not every right the user might obtain;
- each command runs as a fresh actor or domain with declared input facets,
  output/reply authority, target-object capabilities, deadline, memory/CPU/I/O
  budget, and optional one-shot grant;
- pipelines transfer explicitly typed streams and capabilities rather than
  inheriting a global ambient user authority; and
- administrative elevation creates a separate short-lived session after an
  operation-bound trusted-path step-up. It never mutates the shell or command
  into root.

## Human authentication architecture

### Assurance profiles

The baseline should follow the intent of [NIST SP
800-63B-4](../30-sources/temoshok-et-al-2025-authentication-and-authenticator-management.md)
without pretending that NIST's federation and identity-proofing ecosystem is
the OS architecture itself:

| Operation profile | Atom OS recommendation |
| --- | --- |
| Public/bootstrap | Explicit anonymous principal, no reusable credential, narrow capabilities and strict budgets |
| Ordinary low-risk local use | AAL2-like session, preferably phishing-resistant public-key authentication, with device/workload context according to deployment policy |
| Important data or remote access | Phishing-resistant multi-factor public-key authentication with replay resistance, user presence and verification, and sender/session binding |
| Administration, recovery, release signing, trust-root or policy-root change | AAL3-like non-exportable hardware key, explicit intent, operation-bound step-up, and where appropriate a second administrator or threshold |

[WebAuthn Level
3](../30-sources/w3c-2026-webauthn-level-3.md) and [CTAP
2.2](../30-sources/fido-alliance-2025-ctap-2-2.md) are strong bases for
public-key authenticators. Native OS login is not automatically WebAuthn: a
browser origin and a native trusted-path ceremony are different protocol
contexts. Atom OS needs a formally specified, domain-separated local relying-
party profile whose challenge binds at least:

```text
protocol/version, local relying-party ID, boot epoch, requester domain,
target principal, exact proposed action/grant, required assurance,
expiry, nonce, trusted-interaction transcript digest
```

User presence or user verification does not mean that an authenticator
understood or displayed the transaction. Atom OS therefore needs one canonical
request encoding. Its digest is atomically rendered by the trusted OS surface,
placed in the native/WebAuthn challenge, signed, and checked by the final
policy-enforcement point. For the highest-value actions, the deployment
profile must state whether the protected OS display is the transaction-
authorization boundary or require an authenticator or independent approval
channel that can itself display and verify the transaction.

The [formal FIDO2
analysis](../30-sources/guan-et-al-2022-formal-analysis-fido2.md) is a warning
that individually analyzed subprotocols can fail when composed or run in
parallel. Atom OS must model its precise WebAuthn/CTAP/native-client composition
and test concurrent ceremonies, PIN or user-verification state, credential
management, and downgrade paths.

### Enrollment, inventory, removal, and recovery

Authentication is a lifecycle, not a login screen:

```text
invite/provision -> trusted enrollment -> active -> rotated
                 -> suspended -> removed -> recovery-reviewed
```

Every principal should have a visible authenticator inventory with type,
assurance, creation time, last use, origin/provider, sync or export status,
and recovery implications. Important accounts should bind at least two
independent authenticators. Binding, replacement, removal, and recovery are
high-risk policy actions requiring current strong authentication or the
separate recovery workflow, plus independent notification over an already
registered channel.

Syncable passkeys are useful and phishing resistant, but their effective
assurance includes the sync provider's account recovery and endpoint security.
They should not satisfy the highest non-exportable hardware-key profile. The
[passkey abusability
study](../30-sources/daffalla-et-al-2025-passkey-abusability.md) reinforces the
need to analyze enrollment, sharing, export, and recovery rather than evaluate
only the cryptographic assertion.

Biometrics and PINs activate an authenticator locally. Applications, shell
commands, logs, and ordinary runtime messages must never receive them.
Passwords may exist only for compatibility or carefully bounded recovery. If
enabled, they are entered exclusively through the trusted path, checked
against length and breached/block lists, rate-limited, stored with salted
adaptive hashing and an independently protected pepper where used, and never
accepted by arbitrary applications.

“Hardware protected” and “non-exportable” cannot be inferred from a successful
assertion alone. An authenticator-trust service maintains accepted attestation
roots, AAGUID/model and certification policy, metadata/status and firmware
revocation, cache freshness, and offline behavior. It records WebAuthn backup-
eligibility and backup-state signals and lowers assurance or rejects a
credential whose state conflicts with the requested profile. Signature
counters are useful signals, not a sole clone detector.

Authenticator selection is downgrade resistant: the verifier, not the client,
chooses the acceptable method set for the requested action. Timeout, missing
hardware, network failure, or parser failure cannot silently reveal a weaker
password or recovery path. Binding a new credential requires secure attention,
fresh high-assurance authentication or the explicit recovery workflow, proof
of possession of the new key, independent notification, and risk-based
termination of existing sessions. Password and recovery authentication carry
an explicit lower assurance ceiling.

PIN and biometric handling has three different trust boundaries:

- an authenticator with integrated verification keeps the secret and matching
  operation on the authenticator;
- a platform authenticator makes the trusted platform verifier part of the
  ceremony; and
- a client-entered CTAP PIN makes the trusted broker and input path part of the
  secret-handling trusted computing base even when the CTAP transport protects
  it cryptographically.

The last two paths require no tracing or dumps, immediate zeroization, scoped
and short-lived `pinUvAuthToken` handling, correct retry-state treatment, and
no cached user-verification result reused across a step-up ceremony.

### Trusted interaction

An application-drawn login window cannot be authoritative. A hardware/kernel
secure-attention event freezes or revokes competing input and display leases
and transfers exclusive authority to a small isolated trusted-interaction
service with reserved CPU and memory. The protected surface displays:

- the OS identity and current boot/trust status;
- the requesting actor and authenticated subject, if any;
- the exact action, resource, destination, scope, and duration;
- whether the ceremony is login, consent, step-up, enrollment, removal,
  recovery, or break-glass; and
- the effect of approval and a safe cancellation path.

The authenticator response is bound to that request. A secure-attention key is
necessary but not sufficient: the system must also prohibit reusable device
credentials in spoofable application surfaces. In the [Operating System
Framed study](../30-sources/bravo-lillo-et-al-2012-operating-system-framed.md),
even strong visual treatments did not eliminate spoofing; [Nitpicker's secure
GUI](../30-sources/feske-helmuth-2005-nitpicker.md) shows how trusted labeling,
focus, input, and display can be separated into a small service. Atom OS needs
its own usability and red-team evidence.

Trusted interaction is bound to a physical seat and an authenticated
destination: display, input devices, terminal, requesting domain incarnation,
and boot epoch. Requester labels come from verified system state, never caller-
supplied strings. Remote and headless flows authenticate the destination node
and protected transport before soliciting user proof.

Accessibility services, input methods, screen readers, Bluetooth keyboards,
remote KVM, remote desktop, screen sharing, and capture tools are part of the
trusted-path decision, not invisible exceptions. Each supported variant needs
a documented authority graph and assurance ceiling. A high-assurance ceremony
fails closed when the platform cannot establish trusted input, output, focus,
and destination integrity.

### Session state

Use an explicit state machine:

```text
preauth -> challenged -> authenticated -> policy_evaluated
        -> capabilities_installed -> active -> step_up_pending
        -> locked | suspended -> reauthentication
        -> closing -> revoked_or_expired -> drained
```

Every failure before `capabilities_installed` denies authority. A session is a
revocable anchor binding principal, authenticator assurance and age, boot
epoch, local domain, proof-of-possession key, device/workload result references,
and expiry. It is not a global set of user permissions. Locking the screen
revokes interactive-input authority and may retain a separately classified
background lease; logout closes the session generation and descendants.

Authentication always mints a fresh session anchor; a pre-authentication
handle is never upgraded in place. Step-up creates a short-lived child session
or one-operation grant instead of raising the parent's assurance. Generic
long-lived refresh tokens are avoided. A federation profile that requires one
must sender-constrain it, rotate it on use, and detect reuse. Users receive a
visible inventory of concurrent sessions and can terminate each lineage.

Lock, suspend, hibernate, VM snapshot, restore, and migration are explicit
transitions. They increment a resume or instance epoch, suspend or destroy
sensitive descendant grants, clear cached verification material, reseal
high-value keys, and require reauthentication according to operation risk.
A restored snapshot or cloned runtime receives a fresh instance key and boot
identity and cannot resurrect sessions, one-shot approvals, replay state, or
retry counters.

Offline login can be offered only as an explicit deployment profile. Cached
verification material must be sealed to an accepted boot state, bound to a
local principal and device, rollback protected, tightly rate-limited, and
time- or counter-bounded. It may issue only a reduced offline authority set.
Administrator, trust-root, and high-value secret operations fail closed when
fresh policy, revocation, or time evidence is unavailable.

Pre-boot storage unlock is a separate trust boundary. Full-disk or volume keys
should be sealed to an accepted boot state plus an appropriate user or recovery
factor, with rollback-resistant anti-hammering. Firmware or boot-loader UI is
not automatically the Atom trusted path, and unlocking storage does not
automatically establish an OS login session. A product that offers single
sign-on passes a one-shot cryptographic proof into the measured OS ceremony,
never the password or PIN itself.

Persistent throttling must survive reboot without giving a remote attacker an
easy permanent lockout weapon. Prefer authenticator-enforced retry limits and
rollback-resistant per-credential state, combined with source/global budgets,
progressive delays, owner-visible status, and a physically gated recovery
budget distinct from ordinary login attempts.

## Machine, workload, and node authentication

### Keep boot, identity, attestation, and authorization distinct

```text
verified boot  = which signed image was allowed to execute
measured boot  = what components were measured during launch
attestation    = what evidence a verifier appraised under a named policy
authentication = which key/workload/device proved possession
authorization = what this actor may do now to this exact resource
```

A workload identity is derived from kernel-unforgeable domain incarnation,
signed launch manifest and release measurement, parent provenance, device or
node identity, and boot nonce—not from PID, UID, path, mutable filename,
DNS name, or self-asserted labels. A restart creates a new incarnation; policy
may recognize continuity without treating the old live authority as reusable.

The [SPIFFE Workload API](../30-sources/spiffe-project-2026-workload-api.md)
provides useful patterns for local workload attestation and short-lived
credentials. SPIFFE-like IDs should be opaque trust-domain names, not encoded
roles. Inside a node, authenticated kernel IPC and local capability handles are
preferred. Across nodes, use short-lived X.509 workload credentials and mutual
TLS. Bearer JWT credentials are compatibility-only and require exact audience,
short expiry, replay defense, and conversion through the local gateway.

### Attestation appraisal

The [RATS architecture](../30-sources/birkholz-et-al-2023-rats-architecture.md)
separates Attester, Verifier, Endorser, Reference Value Provider, Appraisal
Policy owner, and Relying Party. Preserve that separation. A confined Verifier
consumes TPM/DICE evidence, endorsements, reference values, event logs,
freshness, and a versioned appraisal policy; it emits a privacy-minimized,
short-lived result in an [EAT-like
format](../30-sources/lundblade-et-al-2025-entity-attestation-token.md).

Applications never parse raw evidence or equate one PCR value with trust.
Policy decides whether the attestation result is relevant to one requested
action. Results bind to verifier, appraisal-policy version, evidence and boot
epoch, workload or device identity, freshness, intended relying party, and
declared limitations. Unknown measurements, missing event-log evidence,
stale endorsements, rollback, and failed freshness yield `indeterminate` or
`unavailable`, not permit.

Node admission is a staged protocol: authenticate the provisioning authority,
appraise the node, assign it a trust-domain identity, install narrow bootstrap
authority, fetch current policy and revocation watermarks, then enable
application workloads. Compromise or removal increments a node/trust-domain
epoch and stops new admissions before background cleanup.

## Authorization model

### Combine policy models without confusing them with enforcement

No single conventional model covers the whole system:

- **ReBAC** expresses ownership, membership, tenancy, sharing, and delegation
  relationships;
- **RBAC** is an administrative convenience for job functions, quorum, and
  separation of duty;
- **ABAC** contributes authoritative, typed, short-lived context such as
  device posture, session assurance, purpose, time window, network exposure,
  and resource classification; and
- **capabilities** carry the resulting bounded authority to the enforcement
  boundary.

Roles and attributes do not travel as ambient magic. Each comes from a named
authority with schema, validity, provenance, revision, and revocation rules.
Self-asserted attributes are input data, not trusted policy facts.

A Cedar-like policy language is a useful control-plane model because it can
combine principal, action, resource, context, roles, groups, and relationships
while remaining analyzable. The [Cedar
paper](../30-sources/cutler-et-al-2024-cedar.md) and [verification-guided
development work](../30-sources/disselkoen-et-al-2024-verification-guided-cedar.md)
support pure semantics, explicit validation, mechanized properties, and
differential testing. Atom OS's evaluator should be:

- pure, deterministic, total, typed, side-effect free, and bounded;
- default-deny with explicit forbid-overrides semantics;
- evaluated against one immutable policy/relationship/attribute snapshot;
- closed to unknown actions, entity types, fields, algorithms, and extensions;
- incapable of fetching mutable network state during evaluation; and
- versioned so every decision and grant names the exact model and data
  revisions used.

The [Harrison-Ruzzo-Ullman
result](../30-sources/harrison-et-al-1976-protection-in-operating-systems.md)
warns that unrestricted protection-state transition systems make general
right-leakage safety undecidable. Atom OS should deliberately restrict its
authority algebra and policy language instead of promising a universal safety
analyzer.

### Authorization query

The canonical query should carry all security-relevant context explicitly:

```text
request_id, idempotency_key
subject_principal, current_actor_domain, bounded_delegation_chain
authentication_evidence_ref, assurance, authentication_time
session_id, session_generation, proof_of_possession_key
attestation_result_ref and freshness where required
action, exact_resource_id, resource_generation, expected_version
policy_model_id, minimum_relationship_revision
bounded_attributes {value, authority, validity, revision}
requested_rights, lifetime, delegation_depth, resource_budget
purpose/consent context and obligations where policy requires them
```

The policy service returns one typed outcome:

```text
permit | deny | unauthenticated | step_up_required | indeterminate
conflict | revoked | expired | unavailable
```

These outcomes are operationally different. `deny` means sufficiently fresh
policy rejected the request. `unauthenticated` means the required subject
evidence is absent. `step_up_required` identifies a stronger ceremony.
`indeterminate` means inputs conflict or cannot safely be interpreted.
`conflict` means the resource version changed. `unavailable` represents a
dependency or freshness failure. Clients must not retry them all as if they
were transient network errors.

### Structured grant

A permit is not a Boolean. It authorizes an issuer to create a grant containing:

```text
grant_id, decision_id, request_digest
subject, actor, audience, action
exact object_id and object_generation
rights, obligations, resource budget
policy model/revision and relationship revision
attribute digest and attestation-result digest
boot, node, session, object, and revocation epochs
not_before, expiry, maximum clock uncertainty
proof-of-possession key or local IPC peer binding
delegation depth and permitted attenuation axes
issuer identity and authenticated integrity protection
```

The issuer derives a local capability no broader than both this grant and its
own capability envelope. A remote issuer creates a short-lived sender-
constrained proof. Grants are not hidden global ACL entries and cannot be
enlarged by changing a role name or moving a resource pathname.

### Eliminate authorization TOCTOU

The resource's policy-enforcement point validates and consumes the grant in
the same transaction that admits the effect. It compares the exact object
generation, expected content/version, session and revocation generations,
request digest, audience, actor, deadline, and budget. If a pathname or name
now resolves to another object, or content/policy changed beyond the permitted
revision, it returns `conflict` and requires a fresh decision.

Long-running operations retain an admitted-operation record with the granted
envelope and lifecycle policy. They do not continuously reinterpret every
policy edit, but revocation policy specifies whether they finish, stop at a
safe point, compensate, quarantine output, or require manual recovery. This
avoids both a meaningless “check once forever” rule and an impossible promise
to undo effects already committed externally.

### Delegation and impersonation

Delegation is explicit attenuation:

```text
child rights        subset of parent rights
child resources     subset of parent resources
child lifetime      no longer than parent lifetime
child budget        no greater than remaining parent budget
child audience      no broader than parent audience
child depth         strictly decreases
child obligations   preserve or strengthen mandatory obligations
```

The caller must possess a separate delegate right, and the receiver must
accept the capability into an appropriate slot. Forwarding data is not the
same as forwarding authority.

Services act **on behalf of** a subject while retaining their own actor
identity. Impersonation that erases the actor is prohibited in normal paths.
A narrowly defined recovery or support workflow may impersonate only when
policy explicitly authorizes it, the trusted UI displays it, and independent
audit records both identities.

## Distributed authorization and federation

Kernel capabilities never cross a node boundary. A confined gateway
terminates remote proof, validates it, and derives a new local capability from
its own bounded envelope. The gateway checks:

- mutually authenticated channel or accepted federation protocol;
- issuer and trust-domain policy;
- exact audience and endpoint identity;
- holder or client proof-of-possession;
- nonce, replay cache, validity, and maximum clock uncertainty;
- boot/node/session/policy/revocation epochs and required watermarks;
- subject, actor, delegation chain, and target-resource binding; and
- permitted algorithm/profile versions with no silent downgrade.

[NIST's zero-trust architecture](../30-sources/rose-et-al-2020-zero-trust-architecture.md)
supports separating policy decision, administration, and enforcement and not
trusting network location. Atom OS should adopt those principles without
making a central policy engine an all-powerful runtime dependency.

### OAuth and sender-constrained tokens

OAuth belongs only at HTTP and external federation edges. Follow [RFC
9700](../30-sources/lodderstedt-et-al-2025-oauth-security-bcp.md): authorization
code plus PKCE, exact redirect matching, no implicit or resource-owner
password grant, audience-restricted access tokens, mix-up defenses, and sender
constraints. Translate a validated access token into a local capability; do
not expose OAuth semantics inside the kernel.

[DPoP](../30-sources/fett-et-al-2023-dpop.md) is useful where mutual TLS is
impractical, but it only demonstrates possession of a key associated with an
application-layer request. It does not authenticate the user, decide policy,
or bind the request body. Atom's profile must add exact issuer, audience,
subject, actor, method, URI, request digest where needed, nonce/replay, session,
and resource bindings.

[Macaroons](../30-sources/birgisson-et-al-2014-macaroons.md) offer useful
monotonic caveat-based attenuation for delegated or partly disconnected
workflows. If supported, Atom's profile must require holder binding, exact
audience, resource generation, action, expiry, request digest, depth, budget,
and revocation caveats. A bearer macaroon is not the default local authority
format.

### Relationship consistency

Distributed relationship authorization has a “new enemy” problem: a replica
may see new content but not the revocation that should hide it. A
[Zanzibar-like](../30-sources/pang-et-al-2019-zanzibar.md) relation service
should return opaque causal revision tokens. Content and authorization updates
are coupled so a read that observes content revision `C` must evaluate against
at least the associated authorization revision `A`.

Authorization cache keys include the complete security context: subject,
actor, action, exact resource and generation, assurance, session and
attestation references, attributes, policy and relation revisions, purpose,
audience, obligations, and epochs. Positive cache lifetime is no longer than
the minimum of credential expiry, attribute validity, policy lease,
relationship freshness, revocation service-level objective, and resource
generation lifetime. Unknown or omitted fields miss the cache rather than
wildcard-match.

Policy activation is atomic across schema, policy, relationship snapshot, and
required attribute contracts. Every enforcement point carries a minimum
accepted model, relation, issuer-key, and revocation revision, protected
against rollback across reboot and failover. A tightening change states
whether it fences existing grants immediately or only future renewal.
Unsupported obligations fail closed.

Bounded-stale evaluation is safe only for explicitly monotonic low-risk rules.
Negation, exclusion, newly added `forbid` rules, separation of duty, quotas,
and decisions based on the absence of a relationship require a causally
complete snapshot; an incomplete replica cannot prove absence.

### Partitions and clock failure

During a control-plane partition:

- do not issue a new grant, change policy, change membership, delegate,
  disclose a secret, run a destructive command, or elevate privilege from a
  stale allow;
- already admitted work continues only within its existing lease, budget, and
  cancellation contract;
- only explicitly classified low-risk idempotent reads may use a bounded-stale
  decision whose maximum age and causal revision remain acceptable; and
- recovery uses separately preprovisioned authority and is never activated
  merely because the ordinary policy service failed.

If trustworthy time or revocation watermarks are unavailable after reboot,
reject grants whose safety depends on them and enter a named restricted mode.
Availability policy must be declared per action class. “Fail secure” is not a
single universal behavior: for a medical alarm or reactor shutdown, the safe
physical action may be different from denying a data read, but it must still
be preauthorized and narrowly represented.

An authority namespace has one linearizable or epoch-fenced grant issuer, or
pre-partition issuers receive disjoint, non-overlapping rights and consumptive
budgets. Two partitioned issuers must not double-spend a delegation count,
quota, one-shot approval, or resource budget. Self-contained offline tokens
cannot safely enforce a global consumptive quota and are not used for one.

Issuer signing keys and trust bundles carry epochs and minimum accepted
versions. Rotation has bounded overlap; emergency rejection is explicit; a
partitioned verifier cannot extend an expired trust epoch. A restored or
cloned issuer receives a fresh boot/instance identity so duplicated state
cannot yield two apparently valid issuers or replay databases.

The authoritative replay consumer for a remote grant atomically records the
nonce or `jti`, idempotency key, request digest, and admitted effect. Replicas
use linearizable coordination, deterministic request affinity, or disjoint
nonce spaces. If replay state is unavailable, privileged or non-idempotent
requests fail closed. DPoP's normal proof does not supply these application
semantics.

Grant registration, durable audit-outbox admission, and release of a token or
capability form one crash-consistent protocol: an externally visible grant
must not escape before its lineage and required audit evidence are durable.
At the resource, nonce/idempotency consumption is atomic with the effect where
possible. Exactly-once effects on an external actuator are impossible without
downstream protocol support, so integrations require idempotency,
reconciliation, and explicit uncertainty outcomes.

## Revocation, logout, and authority expiry

Revocation is a lifecycle, not deletion of a handle and not retroactive undo:

```text
requested -> authoritative-committed -> distributed -> enforced
          -> in-flight-quiesced -> sanitized -> retired | quarantined
```

Use complementary mechanisms:

| Mechanism | Best use | Limitation |
| --- | --- | --- |
| Derivation-tree traversal | Selective local descendant revocation | Work is proportional to graph shape and must be charged/resumable |
| Revocation proxy or anchor | Many facets sharing one revocation point | Extra indirection and anchor availability |
| Object generation | Fast fencing after destroy/recreate or broad object revocation | Coarse; does not undo admitted work |
| Session/node/policy epoch | Fast rejection of an entire stale class | Coarse invalidation and coordination cost |
| Short-lived lease | Bounds disconnected and remote exposure | Exposure lasts until expiry; renewal adds availability dependency |
| Online status/watermark check | Critical current-state decision | Availability, latency, privacy, and DoS costs |
| Ordered invalidation stream | Efficient distributed propagation | Partitions and lag require explicit stale behavior |

The kernel rejects new admissions after the relevant generation or anchor is
closed. Resource servers then follow declared in-flight semantics: complete a
safe atomic operation, stop at a safe point, compensate if the operation is
designed to be compensable, quarantine unpublished output, or escalate manual
recovery. Cancellation is a request, not proof of nonexecution; timeout is not
nonexecution; revoked authority cannot erase plaintext already disclosed or
undo a message delivered to an external system.

Logout closes the session anchor, increments its generation, rejects new
admission, drives descendant grants through close and drain, destroys session
key handles, revokes trusted input/output leases, and sanitizes sensitive UI,
IPC, and reusable buffer state. Background tasks survive only if they were
launched under a separately visible background principal and lease.

Global instantaneous revocation cannot coexist with offline acceptance of
self-contained tokens. Every action class therefore declares a maximum stale-
authority window and whether online checking is mandatory. That bound becomes
an assurance metric and test target.

Each consumer of a revocation stream tracks signed per-authority sequence
numbers, acknowledges an enforced watermark, detects gaps, and supports
replay/resynchronization. While a required gap exists, it cannot issue or admit
sensitive authority. Status reports distinguish authoritative commitment,
distribution, enforcement at named consumers, in-flight quiescence, and
sanitization; they never say simply “revoked” before the requested scope is
reached. Revocation cascades from parent credential or token through exchanged
tokens, local capabilities, and admitted-operation records, and no child's
expiry can exceed its parent.

## Recovery and break-glass

Recovery authenticates a distinct recovery principal and grants only recovery
operations. It does not silently become a normal administrator. High-impact
recovery should combine physical presence, a hardware-bound recovery
authenticator, and another independent offline factor or institutional 2-of-N
quorum. Recovery and update roots, instructions, and minimal services live
outside the ordinary service failure domain.

A recovery workflow should be explicit:

1. enter a named restricted recovery state through physical/trusted attention;
2. authenticate recovery principals and verify quorum;
3. display the exact target, scope, consequences, and credentials affected;
4. issue a one-shot, short-lived, nondelegable recovery capability;
5. perform only the approved repair or credential reset;
6. revoke affected sessions, authenticators, workload keys, and grants;
7. rotate derived keys and increment relevant generations/epochs;
8. notify the owner and independent operators through preexisting channels;
9. require normal strong re-enrollment before full access; and
10. preserve independent audit evidence and conduct incident review.

Credential recovery, encrypted-data recovery, and destructive reprovisioning
are different authorities:

- **credential recovery** restores the ability to establish a low-assurance
  identity session;
- **data-key recovery** decrypts existing protected data through an explicitly
  chosen escrow, wrapped recovery key, or threshold-custody design; and
- **factory reset/reprovisioning** establishes a new owner while irreversibly
  discarding prior data.

Losing an authenticator does not magically reconstruct a data key. Any escrow
or threshold share is decryption authority and must be modeled, protected,
audited, and disclosed as such; otherwise “no backdoor” would be misleading.

A recovered session starts at reduced assurance. It cannot immediately bind a
highest-assurance authenticator, remove surviving authenticators, decrypt or
export high-value data, change trust roots, disable notification, or erase
audit. Those transitions need an existing strong factor, an independent
quorum, or a reviewed cooling-off period. Notify every surviving authenticator
and registered channel and provide a cancellation/escalation path.

Offline recovery codes are high entropy, verifier-hashed, single-use,
rate-limited, independently stored, and replaced after use. Email, SMS,
knowledge questions, or two factors controlled by one synchronized account or
device do not form an independent high-impact recovery quorum. Threshold
custodians need explicit enrollment, replacement, revocation, and resharing
procedures and cannot approve their own privilege elevation.

A break-glass grant is predeclared, one-shot or very short-lived,
resource/action scoped, nondelegable, threshold-approved where appropriate,
and non-disableably audited. It cannot read ordinary secrets unless the exact
emergency action requires that access. There is no manufacturer master
password, hidden support principal, universal recovery token, or policy-engine
failure bypass.

Break-glass approval binds to a fresh challenge, boot and recovery epoch,
exact action and resource, quorum, and a rollback-resistant one-shot counter.
Rollback or audit-witness failure cannot make an emergency grant reusable.

## Keys and secrets

Boot authorization, workload identity, authentication, policy signing,
release signing, audit witnessing, storage encryption, and recovery use
separate keys and derivation domains. Key services return narrow
sign/decrypt/derive or seal/unseal handles rather than raw bytes where
possible. Callers cannot request a generic signing operation when the intended
use can be encoded as a typed protocol operation.

Secrets must not appear in configuration files, BEAM terms, actor mailboxes,
traces, crash dumps, command history, telemetry, audit records, swap,
uninitialized memory, or reusable DMA/network buffers. Secret-bearing domains
need reserved memory budgets, explicit zeroization/sanitization, dump and trace
exclusion, and output declassification rules. Debug authority is distinct from
secret, recovery, and policy authority.

## Audit and accountability

Audit at least:

- authentication success, failure, lockout, and evidence-policy version;
- authenticator enrollment, binding, removal, rotation, and recovery;
- principal, role, relationship, attribute, policy, and trust-root changes;
- grant issue, attenuation, transfer, consumption, expiry, and revocation;
- denied high-risk requests, step-up, trusted-path use, and consent;
- break-glass, recovery, update, release, and rollback decisions;
- security-service failure, partition, clock uncertainty, stale watermark, and
  restricted-mode transitions; and
- effect admission, completion state, compensation, quarantine, and residual
  uncertainty.

Events bind boot epoch, monotonic sequence, request and decision IDs,
subject/actor, evidence references, action, exact object generation, policy and
relationship revisions, grant digest, enforcement point, declared intent,
observed outcome, and uncertainty. Store references or privacy-preserving
digests instead of raw credentials, biometrics, tokens, secrets, or excessive
personal data.

Use forward-secure chaining and periodic commitments to an independent witness
following the direction of [Schneier and
Kelsey](../30-sources/schneier-kelsey-1999-secure-audit-logs.md). Separate
admission from export so a remote outage cannot silently erase events; reserve
audit resources and define overload behavior for each event class. Audit
integrity cannot prove that compromised code reported truthfully or completely,
so sequence gaps, witness divergence, loss, and unavailable exporters are
first-class alarms.

Audit uses a reserved bounded local spool and per-operation outage policy.
Critical actions normally stop when required local evidence cannot be
admitted. A preauthorized life/safety recovery path may continue only with
sealed local evidence and an explicit loss/uncertainty marker. Rate-limit
attacker-triggered denial details while retaining aggregate counters.
Per-producer boot and sequence chains, witness acknowledgements, gap detection,
and split-view alarms do not depend on wall-clock ordering.

## Resource, graph, and batch hardening

Resource creation atomically establishes object identity and generation,
initial policy-relevant metadata, ownership/relationship state, and initial
capabilities. Delete/recreate, rename, parent movement, snapshot restore, and
generation wraparound cannot resurrect a prior grant. Decisions bind every
policy-relevant metadata version, not only content bytes.

Authorization graph APIs are themselves protected resources. `check`, `list`,
expand, and diagnostic queries can leak object existence, group membership,
tenant relationships, and organizational structure. Queries are tenant scoped,
recursion/cycle/fan-out bounded and budgeted, and use non-enumerating error
behavior where confidentiality requires it.

A batch grant names an immutable collection snapshot or enumerates and binds
every subeffect. It cannot authorize items added after the decision. The API
declares atomic, partial-commit, retry, compensation, and per-item result
semantics so a grant cannot be replayed against the unfinished remainder or a
different collection.

Gateways are sharded by trust domain and resource class where possible, with
separate derivation envelopes. Every hop exchanges and downscopes authority;
it never forwards the original user bearer credential as service authority.
The final target still validates the local grant. A macaroon verifier uses
per-target keys or a reviewed public-key attenuation design so ordinary
verification authority is not also universal minting authority; caveat
encoding is canonical and unknown caveats fail closed.

## Secure updates and policy evolution

Security fails if an attacker can roll back the kernel, authenticator parser,
policy, trust bundle, reference values, or recovery code. Use role-separated,
threshold-signed metadata with freshness, version, expiry, rollback, and
freeze protections, following the architectural lessons from
[TUF](../30-sources/samuel-et-al-2010-tuf.md). Targets bind their compatible
boot manifests, policy schemas, capability ABI profiles, migration code, and
expected measurements.

Update staging is unprivileged; only a narrow boot-selection mechanism commits
the next candidate. Activation creates a new boot/policy epoch, performs health
and migration checks, and either commits or returns to a known-safe image under
an audited rollback policy. A rollback may restore software while retaining
monotonic revocation and credential-compromise state; restoring an old disk
snapshot must not resurrect revoked authority.

## Availability and unauthenticated denial of service

Pre-authentication code is exposed by definition. It runs in a constrained
domain with:

- a minimal parser and protocol surface;
- fixed request, queue, memory, CPU, crypto, UI, and log budgets;
- per-source and global rate limits plus progressive backoff;
- proof-of-work or admission tickets only where their equity and accessibility
  costs are understood;
- no secret-dependent detailed error messages;
- reserved capacity for local secure attention and recovery; and
- separate overload signals so an attacker cannot force an authorization
  bypass by exhausting the verifier.

Costly certificate, attestation, password-hash, and signature work is admitted
only after cheap syntactic and replay checks. Parsers operate in isolated,
restartable domains. Authentication failure, policy unavailability, audit
pressure, and revocation backlog never broaden authority.

## Worked CLI flow

Consider an authenticated user asking the CLI to replace a protected network
policy:

1. The shell parses syntax without privilege and resolves the target through
   its namespace capability.
2. It sends a typed request naming the exact policy object, generation,
   expected version, proposed content digest, and idempotency key.
3. The endpoint declares that the action requires fresh hardware-backed
   step-up and two-person approval.
4. The trusted-interaction service acquires exclusive input/display authority,
   displays the request and digest, and runs a domain-separated authenticator
   ceremony.
5. The session service binds the new evidence to this request without
   expanding the shell's ambient authority.
6. The policy service evaluates subject, command actor, relationship/role,
   device/workload appraisal, current policy and relation revisions, target
   generation, purpose, and quorum state.
7. The grant compiler creates a one-shot capability for `replace-version` on
   only that object and expected version, with a small execution budget and
   short expiry.
8. A fresh command actor receives the input blob by read-only facet, the
   one-shot target capability, an audit reply endpoint, and nothing else.
9. The policy service validates generation, expected version, request digest,
   quorum, revocation state, and grant in the same transaction that publishes
   the new version.
10. The capability is consumed; audit records the decision, approvers,
    versions, digest, and completion. The command exits and its domain drains.

There is no `sudo`, root shell, reusable administrator token, inherited
ambient filesystem access, or opportunity to substitute another target after
approval.

## Failure matrix

| Condition | Required behavior |
| --- | --- |
| Missing authentication | `unauthenticated`; offer only the bounded trusted-path entry capability |
| Insufficient or old assurance | `step_up_required` naming the acceptable profile and exact request; do not mutate the existing session |
| Unknown principal, action, resource type, field, algorithm, or extension | Fail closed as `indeterminate` or `deny`; never infer a permissive default |
| Policy or relationship service unavailable | No new sensitive grant; existing leases follow their declared profile |
| Policy/content version mismatch | `conflict`; resolve exact object and reauthorize |
| Revocation committed during evaluation | Admission transaction observes the new generation and returns `revoked` |
| Revocation after admission | Follow operation-specific safe-point, compensation, quarantine, or completion contract |
| Authenticator or verifier crashes | No capability installation; restart in isolated domain with replay-safe ceremony state |
| Runtime actor restarts | New incarnation and launch manifest; no implicit inheritance of old handles |
| Clock rollback or excessive uncertainty | Reject time-dependent grants and enter restricted mode |
| Network partition | Deny new sensitive grants; permit only explicitly bounded low-risk stale reads or preauthorized safety actions |
| Audit exporter unavailable | Continue only within reserved local journal policy; alarm and deny actions whose audit obligation cannot be met |
| Local audit spool full | Stop critical actions; only a predeclared safety path may proceed with sealed loss evidence |
| Grant issued just before issuer crash | Do not release it until lineage and required audit-outbox admission are durable |
| Effect commits just before resource crash | Atomically consume nonce/idempotency state where local; otherwise report uncertainty and reconcile downstream |
| Split-brain grant issuers | Fence by authority epoch or consume disjoint preallocated envelopes; never double-spend quotas |
| Revocation stream gap | Stop sensitive issue/admission until authenticated replay or resynchronization reaches the required watermark |
| Non-monotonic rule on incomplete replica | Refuse evaluation; absence, forbids, separation-of-duty, and quota checks require a causally complete snapshot |
| Revocation traversal exceeds budget | Persist cursor and continue; affected anchor rejects new admissions throughout |
| Break-glass coordinator unavailable | Remain restricted; do not reinterpret normal failure as emergency authority |
| User cancels or command times out | Return cancellation/timeout separately; inspect effect completion rather than claiming nonexecution |

## Formal properties and assurance argument

The first implementation artifact should be an executable authority model, not
a login UI. At minimum, specify and model-check:

1. **Non-amplification:** every installed capability is within a boot root or
   a monotonic derivation of one.
2. **Complete mediation:** every protected state transition requires a valid
   capability at its resource boundary.
3. **No implicit anonymous authority:** pre-authentication domains can reach
   only manifest-declared public/bootstrap objects and bounded budgets.
4. **Designation with authority:** a request cannot substitute a different
   object, generation, action, actor, or audience after authorization.
5. **Session confinement:** authentication or step-up changes only a new
   session/grant lineage and never expands unrelated live domains.
6. **Revocation freshness:** after an anchor or generation becomes enforced,
   no new descendant admission succeeds; in-flight behavior matches the
   declared operation class.
7. **Policy determinism and termination:** one validated query and immutable
   snapshot produce one bounded result or explicit failure.
8. **Fail-safe degradation:** missing evidence, stale watermarks, unknown
   syntax, parser failure, service crash, and resource exhaustion cannot turn
   a non-permit state into permit.
9. **Budget conservation:** unauthenticated, delegated, policy, revocation,
   cryptographic, and audit work is always charged to an authorized finite
   budget.
10. **Lifecycle closure:** logout, domain death, revocation, and recovery
    eventually reach drained, sanitized, retired, or explicitly quarantined
    states without losing uncertainty evidence.

The [seL4 proof
literature](../30-sources/klein-et-al-2014-comprehensive-sel4-verification.md),
[information-flow work](../30-sources/murray-et-al-2013-sel4-information-flow.md),
and [Rushby's separation-kernel
analysis](../30-sources/rushby-1981-design-verification-secure-systems.md)
show useful proof structures and assumption discipline. They do not transfer
to Atom OS without refinement proofs from its specification through source,
compiler, binary, target architecture, boot configuration, and devices.

### Verification and test program

- Define executable state machines for bootstrap, enrollment, login, session,
  step-up, policy change, grant issue, delegation, revocation, logout, update,
  partition, recovery, and audit.
- Build a small reference policy semantics and grant compiler. Mechanize key
  properties and differentially test the production evaluator against it with
  randomized policies, entities, unknown fields, malformed schemas, and
  mutation testing.
- Property-test the kernel authority graph, generation reuse, revocation
  cursor, capability transfer, budget conservation, and actor/domain restart.
- Fuzz every untrusted parser: CTAP, WebAuthn client data, CBOR/COSE, X.509,
  ASN.1, TLS, OAuth, DPoP, EAT, event logs, policy/schema input, update metadata,
  CLI protocol, and audit transport.
- Fault-inject verifier/PDP/issuer/revocation/audit death, queue overflow,
  delayed messages, split-brain relation stores, disk exhaustion, interrupted
  update, boot rollback, clock rollback, stale trust bundles, and DMA teardown.
- Exercise token replay across replicas, missing cache-key fields, the
  Zanzibar new-enemy race, object-name reuse, request substitution, concurrent
  FIDO ceremonies, credential rebinding, and policy/model rollback.
- Conduct trusted-path usability and adversarial studies for spoofing,
  habituation, coercion, picture-in-picture, full-screen capture, ambiguous
  resource names, consent fatigue, recovery, and break-glass drills.
- Red-team the separation of policy editor, verifier, grant issuer, key
  service, audit operator, update signer, and recovery quorum.
- Publish an assurance manifest naming source revision, compiler, target ISA
  and board, kernel configuration, boot path, IOMMU/device state, hardware
  root, crypto profile, policy model, time assumptions, and excluded covert or
  timing channels for every result.

## Implementation program and exit criteria

### Stage 1 — model before mechanisms

Define the threat model, principal/evidence/session/query/grant schemas,
capability rights, authority algebra, boot manifest, lifecycle state machines,
and formal properties.

Exit only when model checking or exhaustive small-state exploration finds no
authority amplification, anonymous path to protected objects, post-revocation
new admission, or unbounded policy evaluation under the modeled assumptions.

### Stage 2 — single-node capability data plane

Implement manifest bootstrap, explicit anonymous domain, typed local
capabilities, generations, derivation/revocation anchors, protected transfer,
budgets, and admitted-operation records. Do not add a root UID compatibility
layer.

Exit only after hostile-domain tests demonstrate isolation, failed forgery,
safe object-name reuse, bounded revocation, correct teardown, and no sensitive
effect without a capability check.

### Stage 3 — human login and command confinement

Implement the trusted-interaction domain, native FIDO2 profile, credential
inventory, session anchors, command-scoped CLI launch, step-up, lock, logout,
and drain.

Exit only after protocol modeling, parser fuzzing, physical input/display
tests, concurrent-ceremony tests, spoofing studies, credential lifecycle tests,
and recovery exercises meet defined thresholds.

### Stage 4 — policy and security services

Implement typed pure policy, versioned relationship and attribute authorities,
bounded grant compiler, workload identity, key handles, revocation epochs,
and forward-integrity audit.

Exit only after differential policy testing, separation-of-duty tests,
confused-deputy attacks, cache-key mutation, policy rollback, service failure,
and audit-loss tests.

### Stage 5 — hardware roots, update, and recovery

Add measured boot, TPM profile and DICE fallback, RATS verification, Atom's EAT
profile, signed updates, rollback protection, threshold recovery, and
restricted boot modes.

Exit only after cross-reboot/replay/rollback testing, compromised-reference-
value exercises, key rotation, lost-authenticator recovery, update interruption,
and owner notification drills.

### Stage 6 — distributed authority

Add mTLS workload identity, remote gateways, causal relationship revisions,
sender-constrained grants, partition modes, ordered invalidations, federation,
and explicit maximum stale-authority windows.

Exit only after split-brain, replay, delayed revocation, clock failure,
cross-tenant, trust-domain rollover, issuer compromise, and new-enemy tests.

### Stage 7 — higher-assurance profiles

Add threshold administration, selected information-flow compartments, formal
refinement, a second architecture, CHERI experiments, extensive red-team and
usability work, and certification evidence where justified.

Exit criteria are profile-specific. No proof, certification, or hardware
result is generalized beyond the exact configuration and assumptions tested.

## Deployment profiles

One policy cannot safely cover every product. Specify profiles explicitly:

| Profile | Likely emphasis | Required differences |
| --- | --- | --- |
| Single-owner embedded | Physical presence, DICE/TPM-bound owner key, minimal remote surface, deterministic recovery | No fictitious multi-user root; signed provisioning and narrowly scoped maintenance |
| Interactive multi-user | Strong trusted UI, per-user sessions, isolated apps, credential inventory, lock/logout semantics | Clear subject versus actor, anti-spoofing tests, no shared ambient shell authority |
| Headless institutional | Hardware workload identity, remote administration, threshold roles, external audit witness | No screen-dependent recovery; strong node join/removal and policy consistency |
| Disconnected/high-resilience | Preprovisioned authority, short bounded offline leases, physical quorum, local audit | Explicit loss of instant revocation and federation freshness; reduced offline actions |
| High-confidentiality | Static partitions, non-exportable keys, narrow declassification, information-flow analysis | Lower compatibility and flexibility; stricter debug, DMA, storage, and output controls |

Each profile declares its roots, acceptable authenticators, assurance mapping,
offline behavior, revocation service-level objective, recovery quorum, audit
topology, hardware dependencies, and maximum authority exposure after
compromise.

## Rejected shortcuts

- **Put authentication in the kernel.** This expands privileged parsers,
  crypto policy, credential lifecycle, and UI state while still failing to
  express application policy.
- **Authenticate once and make the user root.** This creates ambient authority,
  confused deputies, long-lived compromise, and unauditable propagation.
- **Treat PIDs, UIDs, paths, node names, or signed binaries as permission.**
  They designate or describe actors; they do not carry bounded authority.
- **Use an ACL or role check only at lookup time.** Mutable names, policy
  changes, and object reuse create TOCTOU and stale-authority gaps.
- **Serialize local capabilities across the network.** This destroys the local
  protection boundary and turns an unforgeable handle into bearer data.
- **Let every app show a password or biometric prompt.** Users cannot reliably
  distinguish spoofed credential paths, and applications gain reusable
  secrets.
- **Make one IAM service omnipotent.** Compromise combines identity, policy,
  grant, revocation, audit, and recovery into an effective superuser.
- **Treat attestation as authorization.** Measurements need appraisal, and an
  appraisal still needs resource policy.
- **Assume short tokens provide instant revocation.** They only bound exposure
  by their remaining lifetime and verifier behavior.
- **Fail open when policy or audit is unavailable.** An attacker can convert
  denial of service into privilege; only named preauthorized safety actions
  may operate in degraded modes.
- **Create a vendor backdoor for recovery.** It is a universal credential and
  defeats the stated architecture.

## Material limitations and unresolved tradeoffs

- Stronger authenticators and trusted interaction can increase friction and
  denial-of-service opportunities; recovery can become less usable at exactly
  the moment it is needed.
- Central policy improves coherence but concentrates availability and
  compromise risk. Separating decision, grant issue, revocation, and resource
  enforcement plus bounded leases reduces but does not remove that risk.
- Short-lived credentials limit exposure but increase renewal and clock
  dependencies. Disconnected operation necessarily weakens revocation
  freshness.
- Hardware attestation provides valuable evidence while adding endorsement,
  reference-value, supply-chain, privacy, and hardware-availability
  dependencies.
- Capability security prevents unauthorized direct use and many confused-
  deputy failures; it cannot stop an authorized reader from disclosing learned
  data.
- A trusted path can make the requester and action clearer, but no UI removes
  coercion, habituation, or all spoofing.
- Native Atom OS login needs a new formal and usability analysis; conformance
  to WebAuthn or CTAP alone is insufficient.
- Existing seL4, CHERI, Cedar, FIDO, Zanzibar, TPM, and RATS results constrain
  the design but do not prove its composition.

The highest-priority unresolved choices are the initial deployment profile,
the first board's trusted display/input and TPM/DICE support, the exact
capability rights and revocation contract, the native-login relying-party
profile, policy/entity schemas, per-action consistency and stale-authority
bounds, recovery ownership and quorum, audit-witness topology, and which data
classes warrant information-flow enforcement.

## Connections

- [BEAM, ERTS, and OTP principles for a new operating
  system](beam-erts-and-otp-principles-for-a-new-operating-system.md) defines
  the five-layer architecture into which this security design fits.
- [Kernel hardware and architecture support
  layer](kernel-hardware-and-architecture-support-layer.md) owns the hardware
  roots and semantic privilege mechanisms used here.
- [Minimal privileged kernel layer](minimal-privileged-kernel-layer.md) defines
  the capability, domain, budget, completion, and revocation mechanisms on
  which the data plane depends.
- [Managed actor runtime layer](managed-actor-runtime-layer.md) defines actor,
  runtime-domain, message, scheduling, and native-code boundaries that must
  preserve explicit authority.
- [OTP-like system services layer](otp-like-system-services-layer.md) provides
  the unprivileged policy and lifecycle setting for the control-plane services.
- [Authentication and authorization map](../10-maps/authentication-and-authorization.md)
  provides a shorter route through the design and evidence.
- [Authentication and authorization component
  research](authentication-and-authorization-components/README.md) develops
  one detailed architecture, protocol, failure analysis, verification plan,
  and staged implementation path for each proposed layer-4 security service.
- [What contract should system-wide authentication and authorization
  provide?](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
  retains the open design decisions and falsification program.
- [2026-09-04 authentication and authorization deep
  dive](../50-journal/2026-09-04-authentication-and-authorization-deep-dive.md)
  records the research method, source families, and evidence limits.
- [2026-09-04 authentication and authorization components deep
  dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
  records the component-level search, exact source provenance, cross-service
  conclusions, falsifiers, and remaining evidence gaps.

## Sources

### Protection, capabilities, and assurance boundaries

- [Anderson, *Computer Security Technology Planning
  Study*](../30-sources/anderson-1972-computer-security-technology-planning-study.md)
- [Saltzer and Schroeder, *The Protection of Information in Computer
  Systems*](../30-sources/saltzer-schroeder-1975-protection-information.md)
- [Lampson, *Protection*](../30-sources/lampson-1971-protection.md)
- [Hardy, *The Confused
  Deputy*](../30-sources/hardy-1988-confused-deputy.md)
- [Harrison, Ruzzo, and Ullman, *Protection in Operating
  Systems*](../30-sources/harrison-et-al-1976-protection-in-operating-systems.md)
- [Hardy, *The KeyKOS
  Architecture*](../30-sources/hardy-1990-keykos-architecture.md)
- [Miller, Yee, and Shapiro, *Capability Myths
  Demolished*](../30-sources/miller-et-al-2003-capability-myths.md)
- [Shapiro et al., *EROS: A Fast Capability System*](../30-sources/shapiro-et-al-1999-eros.md)
- [Watson et al., *Capsicum*](../30-sources/watson-et-al-2010-capsicum.md)
- [Klein et al., *Comprehensive Formal Verification of an OS
  Microkernel*](../30-sources/klein-et-al-2014-comprehensive-sel4-verification.md)
- [Murray et al., *seL4: From General Purpose to a Proof of Information Flow
  Enforcement*](../30-sources/murray-et-al-2013-sel4-information-flow.md)
- [Rushby, *Design and Verification of Secure
  Systems*](../30-sources/rushby-1981-design-verification-secure-systems.md)
- [Bauereiss et al., *Verified Security for the Morello Capability-enhanced
  Prototype Arm Architecture*](../30-sources/bauereiss-et-al-2022-verified-morello-security.md)

### Human authentication and trusted interaction

- [Temoshok et al., *Digital Identity Guidelines: Authentication and
  Authenticator Management*](../30-sources/temoshok-et-al-2025-authentication-and-authenticator-management.md)
- [W3C, *Web Authentication: Level
  3*](../30-sources/w3c-2026-webauthn-level-3.md)
- [FIDO Alliance, *Client to Authenticator Protocol
  2.2*](../30-sources/fido-alliance-2025-ctap-2-2.md)
- [Guan et al., *A Formal Analysis of the FIDO2
  Protocols*](../30-sources/guan-et-al-2022-formal-analysis-fido2.md)
- [Bravo-Lillo et al., *Operating System
  Framed*](../30-sources/bravo-lillo-et-al-2012-operating-system-framed.md)
- [Feske and Helmuth, *A Nitpicker's Guide to a Minimal-complexity Secure
  GUI*](../30-sources/feske-helmuth-2005-nitpicker.md)
- [Daffalla et al., *The Abusability of
  Passkeys*](../30-sources/daffalla-et-al-2025-passkey-abusability.md)

### Workload identity, attestation, and hardware roots

- [SPIFFE Project, *SPIFFE Workload API*](../30-sources/spiffe-project-2026-workload-api.md)
- [Birkholz et al., *Remote ATtestation procedureS (RATS)
  Architecture*](../30-sources/birkholz-et-al-2023-rats-architecture.md)
- [Lundblade et al., *The Entity Attestation Token
  (EAT)*](../30-sources/lundblade-et-al-2025-entity-attestation-token.md)
- [Trusted Computing Group, *TPM 2.0 Library Specification,
  v185*](../30-sources/trusted-computing-group-2026-tpm-2-0-library.md)
- [Trusted Computing Group, *Hardware Requirements for a Device Identifier
  Composition Engine*](../30-sources/trusted-computing-group-2024-dice-hardware-requirements.md)

### Policy, delegation, distribution, and federation

- [Rose et al., *Zero Trust
  Architecture*](../30-sources/rose-et-al-2020-zero-trust-architecture.md)
- [Cutler et al., *Cedar: A New Language for Expressive, Fast, Safe, and
  Analyzable Authorization*](../30-sources/cutler-et-al-2024-cedar.md)
- [Disselkoen et al., *Verification-guided Development of Cedar
  Authorization*](../30-sources/disselkoen-et-al-2024-verification-guided-cedar.md)
- [Birgisson et al., *Macaroons*](../30-sources/birgisson-et-al-2014-macaroons.md)
- [Pang et al., *Zanzibar*](../30-sources/pang-et-al-2019-zanzibar.md)
- [Lodderstedt et al., *Best Current Practice for OAuth 2.0
  Security*](../30-sources/lodderstedt-et-al-2025-oauth-security-bcp.md)
- [Fett et al., *OAuth 2.0 Demonstrating Proof of
  Possession*](../30-sources/fett-et-al-2023-dpop.md)

### Audit and update

- [Schneier and Kelsey, *Secure Audit Logs to Support Computer
  Forensics*](../30-sources/schneier-kelsey-1999-secure-audit-logs.md)
- [Samuel et al., *Survivable Key Compromise in Software Update
  Systems*](../30-sources/samuel-et-al-2010-tuf.md)
