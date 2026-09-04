---
title: "2026-09-04 authentication and authorization components deep dive"
kind: journal
created: "2026-09-04"
tags:
  - authentication
  - authorization
  - literature-review
  - research-method
  - security
aliases:
  - "Authentication and authorization service component research session"
---

# 2026-09-04 authentication and authorization components deep dive

## Observations

This session expanded all sixteen proposed OTP-like services in the
[authentication and authorization synthesis](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
into detailed reports under the [authentication and authorization components
directory](../20-notes/authentication-and-authorization-components/README.md).

The shared result is not an identity daemon. It is a compartmentalized control
plane whose services can authenticate, appraise, record, decide, translate,
revoke, witness, or recover only their own artifact. Local effects remain
authorized by Layer-2 capabilities and accepted by the resource-owning
enforcement point.

The strongest cross-service invariant is:

```text
effective authority =
    kernel parent-capability envelope
  ∩ issuer envelope
  ∩ authenticated PDP permit
  ∩ current policy/relationship/attribute/session/epoch state
  ∩ resource-local enforcement constraints
```

Authentication, interaction confirmation, session continuity, workload
identity, and attestation are evidence—not authority. Relationship and
attribute services produce versioned facts. The PDP produces a pure decision.
Only the grant issuer derives an attenuated capability, and it can derive no
power outside a parent capability installed before the request. The resource
checks the exact object generation, request, epochs, proof, budget, and
obligations when admitting the effect.

OTP supervision remains valuable for fault isolation and recovery, but restart
never authorizes an operation or converts incomplete work into success. Each
report defines terminal/indeterminate states, durable idempotency where needed,
resource bounds, reserved control paths, and restart invalidation.

## Environment

- Repository: `/home/ducky/code/atom-os-research`
- Research date: 2026-09-04
- Host time zone: America/Toronto
- Activity: scientific-paper, standards, official-project documentation, and
  first-party engineering-documentation review; cross-source architecture
  synthesis; archive editing
- Subject: sixteen Layer-4 security services and their Layer-1/2/3/5 contracts
- Hardware or simulator target: none selected
- Atom kernel, runtime, authenticator, policy engine, or security service
  implemented: none
- Benchmarks, user studies, formal proofs, or fault injection performed: none
- Local artifacts: sixteen component reports, thirty-one new source notes, one
  component directory index, navigation/inquiry updates, and this evidence
  record

## Evidence

### Research question and operational standard

For every proposed service, the research asked:

> What is the smallest unprivileged service boundary that preserves the
> relevant authentication or authorization evidence, cannot amplify authority,
> remains bounded under hostile input and overload, and exposes crash,
> partition, replay, rollback, and recovery outcomes precisely enough to test?

A component recommendation was retained only when its report:

- identifies what the service holds and explicitly must not hold;
- places non-bypassable mechanisms in Layer 2 while keeping rich policy and
  parsers in replaceable Layer-4 protection domains;
- defines typed objects, generations, immutable revisions, state transitions,
  linearization or evidence points, and one-shot/idempotency behavior;
- distinguishes identity, evidence, session, decision, grant, admission,
  completion, revocation progress, and audit evidence;
- specifies queue, CPU, memory, storage, crypto, traversal, parser, deadline,
  and tenant bounds where hostile traffic enters;
- gives explicit behavior for crash, restart, partition, stale state, rollback,
  clone, replay, compromise, and overload;
- records what sources demonstrated versus Atom-specific synthesis;
- includes verification, fault-injection, measurement, and staged-
  implementation work that could falsify the proposal; and
- remains `maturity: developing` because no Atom implementation was tested.

### Search and selection method

The integrated parent note supplied the sixteen-service decomposition. Three
independent evidence lanes examined:

1. trusted interaction, credential lifecycle, authentication, sessions, and
   recovery;
2. workload identity, attestation, protected keys, updates, and federation;
3. relationships, attributes, policy evaluation, grant issuance, revocation,
   audit, and distributed failure.

Searches covered peer-reviewed systems/security/HCI research, IETF/W3C/OASIS/
FIDO standards, NIST guidance, and current first-party Android, SPIFFE, TUF,
and Uptane documentation. Search snippets were discovery only. Claims retained
in reports were checked against the primary paper or normative/official text.
Current living specifications were pinned by version, immutable revision, or
access date. Secondary blogs were screened for operational leads but not used
when stronger primary evidence was available.

### Component reports

#### Human evidence and continuity

- [Trusted-interaction broker](../20-notes/authentication-and-authorization-components/trusted-interaction-broker.md)
- [Credential registrar and inventory](../20-notes/authentication-and-authorization-components/credential-registrar-and-inventory.md)
- [Authentication verifier](../20-notes/authentication-and-authorization-components/authentication-verifier.md)
- [Session service](../20-notes/authentication-and-authorization-components/session-service.md)

#### Machine identity and appraised evidence

- [Workload identity issuer](../20-notes/authentication-and-authorization-components/workload-identity-issuer.md)
- [RATS Verifier and Appraisal Policy](../20-notes/authentication-and-authorization-components/rats-verifier-and-appraisal-policy.md)

#### Policy facts, decisions, grants, and revocation

- [Relationship authority](../20-notes/authentication-and-authorization-components/relationship-authority.md)
- [Attribute authorities](../20-notes/authentication-and-authorization-components/attribute-authorities.md)
- [Policy decision point](../20-notes/authentication-and-authorization-components/policy-decision-point.md)
- [Grant compiler and issuer](../20-notes/authentication-and-authorization-components/grant-compiler-and-issuer.md)
- [Revocation and epoch service](../20-notes/authentication-and-authorization-components/revocation-and-epoch-service.md)

#### Protected operations and trust maintenance

- [Key and secret service](../20-notes/authentication-and-authorization-components/key-and-secret-service.md)
- [Audit and witness services](../20-notes/authentication-and-authorization-components/audit-and-witness-services.md)
- [Recovery coordinator](../20-notes/authentication-and-authorization-components/recovery-coordinator.md)
- [Update and release service](../20-notes/authentication-and-authorization-components/update-and-release-service.md)
- [Federation gateway](../20-notes/authentication-and-authorization-components/federation-gateway.md)

### Strongest cross-component conclusions

1. **Process separation needs protection-domain separation.** Mutually
   distrustful security services cannot rely only on actors inside one
   compromised managed runtime. Layer 2 must isolate domains and authenticate
   IPC peers; Layer 4 owns replaceable policy.
2. **Human confirmation is request-bound evidence.** A protected path first
   renders a canonical typed request, then arms input; interruption aborts. A
   one-use receipt cannot become a general user credential.
3. **Enrollment is an authorization transaction.** Binding a credential needs
   existing evidence, trusted intent, a fresh verifier challenge, atomic
   commit, visible inventory, independent notification, and durable tombstone.
4. **Sessions remember authentication, not permissions.** Assurance can only
   decrease with time or transitions. Step-up creates a separate purpose-bound
   context; lock, suspend, snapshot, logout, and reboot each have explicit
   epoch behavior.
5. **Workload names and measurements do not grant roles.** Kernel-authenticated
   incarnation facts select versioned registration/appraisal policy; short-
   lived credentials and attestation results remain policy input.
6. **Policy evaluation is a pure snapshot function.** Every external lookup is
   completed and versioned first. Only explicit permit proceeds; missing,
   unsupported, no-applicable-rule, timeout, and error never fall through.
7. **Grant issuance is mechanically attenuating.** Every output dimension is
   a subset of a held parent, static issuer envelope, decision, and current
   epochs. Durable reservation precedes release where lineage, quotas, or one-
   shot use matter.
8. **Revocation is a progress vector.** Authority committed, invalidation
   distributed, admission blocked, work quiesced, state sanitized, and lineage
   retired are different facts. Offline authority cannot promise immediate
   global revocation or exact global quotas.
9. **Non-exportable keys still need least-authority operations.** A broad HSM/
   PKCS login can be a crypto oracle. Key purpose, input schema, audience,
   lifecycle, quota, metadata, and recovery remain protected per object.
10. **Tamper evidence has a narrow claim.** Forward chains and witnessed Merkle
    roots can expose later rewriting, truncation, and equivocation; they cannot
    prove a producer told the truth or emitted every required event.
11. **Recovery powers are not interchangeable.** Replacing an authenticator,
    decrypting retained data, booting recovery firmware, invoking break-glass,
    and destroying all state need different roots, quorums, results, and
    disclosure.
12. **Update authorization ends before installation safety.** Role-separated
    metadata and supply-chain provenance establish eligible bytes; target
    compatibility, quiescence, migration, trial activation, independent health,
    and recovery establish whether this node should commit them.
13. **Federation terminates at a local decision.** Foreign tokens, certificates,
    bundles, subjects, and actors live in separate directional namespaces. A
    gateway validates them and requests a fresh local capability; it never
    imports a serialized kernel right.

### Evidence gaps and falsifiers

The principal unresolved items are the first deployment profile and board;
native RP/verifier naming; trusted attention/display/input/accessibility paths;
credential and recovery assurance; policy language and formal model; relation
store and adversarial-replica assumptions; capability ABI; revocation SLAs;
monotonic time/state; key hardware and algorithms; witness topology/privacy;
update/migration/health protocol; and federation namespace/profile.

The baseline is falsified by any implementation that:

- runs mutually distrustful service roots in one unisolated runtime;
- treats login, role/name, an SVID, certificate, attestation result, or network
  location as direct resource permission;
- resumes a half-finished security ceremony after supervisor restart;
- maps missing/stale/error/timeout to allow or lets a service exceed its fixed
  authority envelope;
- releases a grant before required lineage/idempotency/audit state is durable;
- accepts an old object generation, boot/session epoch, policy model, bundle,
  key, credential, or recovery code after rollback or clone;
- reports revocation complete before the stated enforcement/quiescence stage;
- exports native private keys into ordinary BEAM terms or gives a client a
  broadly logged-in cryptographic token;
- silently drops critical audit events, calls a signed log complete/truthful,
  or calls an unavailable revocation/recovery operation successful;
- lets one recovery path bind credentials, decrypt data, alter firmware roots,
  and mint general administrator authority; or
- installs correctly signed but incompatible/unprovenanced software or converts
  a foreign bearer token directly into a kernel capability.

### Evidence boundary

No Atom OS code, trusted UI, authenticator, hardware root, workload issuer,
RATS profile, relation store, attribute issuer, policy language, grant compiler,
revocation stream, key broker, audit witness, recovery ceremony, updater, or
federation gateway was implemented or run. No cited experiment was reproduced,
and no external system's proof or certification transfers to Atom. The reports
are evidence-backed architectural hypotheses and test programs.

## Source manifest

### Newly introduced sources

#### Human interaction, credential lifecycle, sessions, and recovery

- [User interaction design for secure systems](../30-sources/yee-2002-user-interaction-design-secure-systems.md) — explicit authority/intent and authentic-party interaction principles.
- [Android Protected Confirmation](../30-sources/android-project-2026-protected-confirmation.md) — current protected rendering/input, message-bound confirmation, and abort precedent.
- [FIDO Metadata Service](../30-sources/fido-alliance-2026-metadata-service.md) — signed authenticator characteristics, trust anchors, status, refresh, and multi-device limits.
- [Argon2](../30-sources/biryukov-et-al-2021-argon2.md) — memory-hard password compatibility and verifier-side resource trade-offs.
- [Formal security analysis of OpenID Connect](../30-sources/fett-et-al-2017-openid-connect-security.md) — issuer/flow/session composition, attacks, and proof-bounded guidance.
- [Secrets, lies, and account recovery](../30-sources/bonneau-et-al-2015-secrets-lies-account-recovery.md) — empirical weakness and memorability limits of personal-knowledge recovery.
- [Platform firmware resiliency](../30-sources/regenscheid-2018-platform-firmware-resiliency.md) — independently rooted platform protection, detection, and recovery.

#### Relationships, attributes, policy, grants, and revocation

- [The NIST RBAC model](../30-sources/sandhu-et-al-2000-nist-rbac-model.md) — role/session/hierarchy/constraint and separation-of-duty model.
- [NIST SP 800-162](../30-sources/hu-et-al-2014-attribute-based-access-control.md) — authoritative ABAC sources, timeliness, interoperability, and privacy.
- [XACML 3.0](../30-sources/oasis-2017-xacml-3-0.md) — PAP/PIP/PDP/PEP split, four outcomes, combining, and obligations.
- [OAuth token exchange](../30-sources/jones-et-al-2020-oauth-token-exchange.md) — subject/actor, delegation/impersonation, and target-specific exchange boundaries.
- [OAuth mutual TLS](../30-sources/campbell-et-al-2020-oauth-mutual-tls.md) — client authentication, certificate-bound tokens, and resource-side PoP validation.
- [OAuth token revocation](../30-sources/lodderstedt-et-al-2013-oauth-token-revocation.md) — related-grant invalidation, propagation delay, and unavailable semantics.
- [OAuth token introspection](../30-sources/richer-2015-oauth-token-introspection.md) — authorized active-state checks and cache-created revocation windows.
- [Security Event Token](../30-sources/hunt-et-al-2018-security-event-token.md) — authenticated security-event facts, issuer/audience, deduplication, and ordering limits.

#### Attestation, keys, audit, update, and federation

- [The X.509 SPIFFE Verifiable Identity Document](../30-sources/spiffe-project-2026-x509-svid.md) — exact URI identity, leaf/signing, key-usage, path-validation, and bundle constraints for the X.509 compatibility profile.
- [RATS Conceptual Message Wrapper](../30-sources/birkholz-et-al-2026-rats-conceptual-message-wrapper.md) — explicit conceptual-message typing, collections, protection, and parser bounds.
- [NIST key-management guidance](../30-sources/barker-2020-key-management.md) — key-type, lifecycle, metadata, compromise, recovery, and destruction distinctions.
- [PKCS #11 3.2](../30-sources/oasis-2026-pkcs11-3-2.md) — token objects, handles, attributes, mechanisms, and operation interface precedent.
- [PKCS #11 usage guide](../30-sources/oasis-2025-pkcs11-usage-guide-3-2.md) — session/login breadth, object access, host trust, and concurrency limits.
- [Efficient tamper-evident logging](../30-sources/crosby-wallach-2009-tamper-evident-logging.md) — logarithmic inclusion/consistency proof construction and measured prototype.
- [Certificate Transparency v2](../30-sources/laurie-et-al-2021-certificate-transparency-v2.md) — Merkle log, signed heads, monitor/auditor, and split-view boundaries.
- [Signed syslog messages](../30-sources/kelsey-et-al-2010-signed-syslog-messages.md) — producer sessions, sequencing, gap detection, replay, and collector flooding.
- [NIST log-management guidance](../30-sources/kent-souppaya-2006-log-management.md) — tiered collection, buffering, redundancy, retention, confidentiality, and capacity.
- [in-toto](../30-sources/torres-arias-et-al-2019-in-toto.md) — signed supply-chain steps, artifacts, layout, and compromise analysis.
- [Uptane 2.1.0](../30-sources/uptane-community-2023-standard-2-1-0.md) — target inventory, dual repositories, embedded update threats, and applicability.
- [TUF specification 1.0.36](../30-sources/tuf-project-2026-specification-1-0-36.md) — current role/threshold, root rotation, metadata workflow, and client bounds.
- [Firmware update architecture](../30-sources/moran-et-al-2021-firmware-update-architecture.md) — signer/operator/consumer/boot-verifier separation and recovery.
- [Firmware manifest information model](../30-sources/moran-et-al-2022-firmware-manifest-information-model.md) — authenticated target compatibility, sequence, dependencies, type, size, and location.
- [JWT best current practices](../30-sources/sheffer-et-al-2020-jwt-best-practices.md) — algorithm/type/issuer/audience validation and indirect-input attacks.
- [SPIFFE federation](../30-sources/spiffe-project-2026-federation.md) — directional trust relationships, separate bundles, rotation, retry, and removal.

### Reused sources

#### Human authentication and sessions

- [Operating System Framed](../30-sources/bravo-lillo-et-al-2012-operating-system-framed.md) — empirical limits of visually strengthened OS credential prompts.
- [Nitpicker](../30-sources/feske-helmuth-2005-nitpicker.md) — minimal trusted compositor, input routing, labels, and client quotas.
- [NIST SP 800-63B-4](../30-sources/temoshok-et-al-2025-authentication-and-authenticator-management.md) — current assurance, authenticator lifecycle, sessions, throttling, and recovery.
- [WebAuthn Level 3](../30-sources/w3c-2026-webauthn-level-3.md) — public-key ceremony and credential-record validation.
- [CTAP 2.2](../30-sources/fido-alliance-2025-ctap-2-2.md) — client-authenticator, PIN/UV, credential management, and version negotiation.
- [Formal FIDO2 analysis](../30-sources/guan-et-al-2022-formal-analysis-fido2.md) — composed ceremony, rebinding, and concurrent-session assumptions.
- [Passkey abusability](../30-sources/daffalla-et-al-2025-passkey-abusability.md) — enrollment, inventory, synchronization, removal, and interpersonal abuse.
- [OAuth Security BCP](../30-sources/lodderstedt-et-al-2025-oauth-security-bcp.md) — modern flow, audience, refresh, and sender-constraint requirements.
- [DPoP](../30-sources/fett-et-al-2023-dpop.md) — request/key/token proof binding and replay/body/canonicalization limits.

#### Machine identity, attestation, policy, and capabilities

- [SPIFFE Workload API](../30-sources/spiffe-project-2026-workload-api.md) — local caller identification requirement, short-lived identity, complete snapshots, and bundles.
- [RATS architecture](../30-sources/birkholz-et-al-2023-rats-architecture.md) — evidence/verifier/appraisal/result/relying-party separation.
- [Entity Attestation Token](../30-sources/lundblade-et-al-2025-entity-attestation-token.md) — profileable attestation claims, nonce, boot, and submodule vocabulary.
- [TPM 2.0 Library](../30-sources/trusted-computing-group-2026-tpm-2-0-library.md) — protected objects, policies, measurements, quotes, and monotonic state mechanisms.
- [DICE hardware requirements](../30-sources/trusted-computing-group-2024-dice-hardware-requirements.md) — constrained compound-device identity and measured derivation root.
- [Zanzibar](../30-sources/pang-et-al-2019-zanzibar.md) — relation tuples, causal consistency tokens, caching, and overload isolation.
- [Chubby](../30-sources/burrows-2006-chubby.md) — replicated metadata, generations, cache invalidation, leases, and fencing lessons.
- [Raft](../30-sources/ongaro-ousterhout-2014-raft.md) — crash-fault committed ordering and configuration-change evidence.
- [Cedar](../30-sources/cutler-et-al-2024-cedar.md) — typed pure authorization semantics, schemas, and forbid override.
- [Verification-guided Cedar](../30-sources/disselkoen-et-al-2024-verification-guided-cedar.md) — executable model, differential testing, and production defects found.
- [Zero Trust Architecture](../30-sources/rose-et-al-2020-zero-trust-architecture.md) — decision/enforcement separation and rejection of location trust.
- [Capability Myths Demolished](../30-sources/miller-et-al-2003-capability-myths.md) — designation, attenuation, confinement, confused deputies, and revocation.
- [seL4 reference manual](../30-sources/sel4-foundation-2026-reference-manual.md) — capability spaces, mint/copy, derivation/revoke, and reply authority.
- [Macaroons](../30-sources/birgisson-et-al-2014-macaroons.md) — caveated monotonic attenuation and bearer/root-secret limits.

#### Audit, persistence, and update

- [Vault secrets, leases, and security model](../30-sources/hashicorp-2026-vault-secrets-and-leases.md) — dynamic credential TTL, renewal, revocation lineage, copied-secret limits, and backend threat-model boundaries.
- [Secure audit logs](../30-sources/schneier-kelsey-1999-secure-audit-logs.md) — forward-integrity chains, key evolution, commitments, and claim limits.
- [ARIES](../30-sources/mohan-et-al-1992-aries.md) — write-ahead intent/commit/recovery discipline and its database boundary.
- [The Update Framework paper](../30-sources/samuel-et-al-2010-tuf.md) — role-separated update trust, freshness, consistency, threshold, and rollback defenses.
- [NixOS](../30-sources/dolstra-et-al-2008-nixos.md) — immutable generations and atomic profile switching with mutable-state limits.

## Threads

- The [system-wide security contract inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
  retains the unresolved deployment profile, capability algebra, trusted-path,
  policy, consistency, hardware-root, recovery, audit, update, and federation
  decisions.
- A later inquiry should choose the first single-node profile and turn these
  sixteen reports into one executable authority graph and protocol model.
- Source candidates deliberately not used should stay out of this manifest
  until a future claim actually depends on them.

## Follow-ups

- Select one board/deployment profile and write its complete trust, privilege,
  secure-input/output, entropy, storage, time, TPM/DICE, and recovery inventory.
- Formalize the grant lattice, service envelopes, state machines, request
  encoding, epoch algebra, and resource-side admission transaction.
- Build a minimal anonymous → trusted interaction → verifier → session → PDP →
  local capability → effect path with no root/UID shortcut.
- Add model checking, reference/production differential tests, parser fuzzing,
  power-cut/crash/partition/replay/rollback/clone fault injection, UI studies,
  and compromise-containment reviews as implementation evidence.
- Record commands, versions, outputs, hardware/simulator facts, failures, and
  artifacts in later journal entries; do not promote these reports to stable
  based on prose completeness.
