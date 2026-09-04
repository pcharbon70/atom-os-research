---
title: "Authentication and authorization"
kind: map
created: "2026-09-04"
tags:
  - authentication
  - authorization
  - capabilities
  - security
  - systems-architecture
aliases:
  - "Atom OS security map"
---

# Authentication and authorization

## Scope

This map connects the proposed end-to-end security architecture for human,
machine, workload, service, node, and recovery principals. It follows evidence
from authentication through policy and capability issuance to effect
mediation, revocation, audit, and recovery across all five Atom OS layers.

Authentication, attestation, authorization, capability possession, ownership,
accounting, and effect completion are deliberately separate facts. The map is
about how they compose without introducing an ambient root identity or an
unauthenticated bypass.

## Start here

- [Main authentication and authorization synthesis](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
  is the main synthesis. It proposes an unprivileged identity/policy control
  plane and a kernel-enforced capability data plane, then specifies human and
  workload authentication, grant contracts, revocation, recovery, audit, and
  evaluation.
- [Component implementation deep dives](../20-notes/authentication-and-authorization-components/README.md)
  develop each of the sixteen proposed OTP-like security services as an
  explicit authority boundary, typed protocol, supervised state machine,
  failure contract, verification target, and staged implementation.
- [Open system-wide security contract inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
  keeps the unresolved profile, protocol, policy, consistency, hardware,
  recovery, and assurance choices falsifiable.
- [2026-09-04 research journal](../50-journal/2026-09-04-authentication-and-authorization-deep-dive.md)
  records the research method, evidence families, current source revisions,
  and explicit absence of implementation evidence.
- [2026-09-04 component research journal](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
  records the expanded scientific, standards, and engineering search, exact
  source provenance, cross-service conclusions, falsifiers, and remaining
  evidence gaps.

## Component implementation deep dives

The control plane is decomposed into sixteen separately confined services,
numbered 0 through 15. Each report preserves one invariant: these services may
interpret evidence and policy, but only a bounded capability accepted at the
actual effect boundary authorizes local execution.

### Human authentication and session continuity

- [0. Trusted-interaction broker](../20-notes/authentication-and-authorization-components/trusted-interaction-broker.md) —
  develops secure attention, exclusive input/display leasing, canonical
  request rendering, one-shot confirmation, and explicit abort behavior.
- [1. Credential registrar and inventory](../20-notes/authentication-and-authorization-components/credential-registrar-and-inventory.md) —
  develops transactional enrollment and an auditable, visible authenticator
  lifecycle whose tombstones resist rollback and hidden reactivation.
- [2. Authentication verifier](../20-notes/authentication-and-authorization-components/authentication-verifier.md) —
  confines protocol parsing, challenge verification, password compatibility,
  replay defense, throttling, and bounded evidence production.
- [3. Session service](../20-notes/authentication-and-authorization-components/session-service.md) —
  models authenticated continuity as a proof-of-possession-capable,
  generation-bound context rather than ambient user authority.

### Workload evidence and policy inputs

- [4. Workload identity issuer](../20-notes/authentication-and-authorization-components/workload-identity-issuer.md) —
  derives short-lived credentials from kernel-authenticated incarnations and
  versioned registration policy without inferring roles from names.
- [5. RATS Verifier and Appraisal Policy](../20-notes/authentication-and-authorization-components/rats-verifier-and-appraisal-policy.md) —
  separates evidence parsing, endorsement and reference-value selection,
  appraisal, and the relying party's eventual authorization decision.
- [6. Relationship authority](../20-notes/authentication-and-authorization-components/relationship-authority.md) —
  provides a versioned, causally queryable ownership and sharing graph with
  immutable models, tombstones, and bounded traversal.
- [7. Attribute authorities](../20-notes/authentication-and-authorization-components/attribute-authorities.md) —
  issues scoped, typed, provenance-carrying, short-lived claims while
  preserving privacy and excluding self-asserted policy inputs.

### Decision, grant, and revocation

- [8. Policy decision point](../20-notes/authentication-and-authorization-components/policy-decision-point.md) —
  develops a pure, deterministic, resource-bounded evaluator over immutable
  policy and evidence snapshots with typed non-permit outcomes.
- [9. Grant compiler and issuer](../20-notes/authentication-and-authorization-components/grant-compiler-and-issuer.md) —
  compiles one authenticated permit into attenuated local authority or a
  sender-constrained remote grant inside a fixed issuer envelope.
- [10. Revocation and epoch service](../20-notes/authentication-and-authorization-components/revocation-and-epoch-service.md) —
  distinguishes committed, distributed, enforced, quiesced, and sanitized
  revocation and binds authority to rollback-resistant epochs.

### Secrets, evidence, recovery, and release

- [11. Key and secret service](../20-notes/authentication-and-authorization-components/key-and-secret-service.md) —
  exposes non-exportable, purpose-specific cryptographic facets with explicit
  lease, rotation, compromise, destruction, and recovery behavior.
- [12. Audit and witness services](../20-notes/authentication-and-authorization-components/audit-and-witness-services.md) —
  composes bounded durable admission, forward integrity, Merkle commitments,
  independent witnesses, and declared loss semantics.
- [13. Recovery coordinator](../20-notes/authentication-and-authorization-components/recovery-coordinator.md) —
  separates credential, data-key, platform, break-glass, and destructive-reset
  recovery into predeclared threshold workflows and one-shot authority.
- [14. Update and release service](../20-notes/authentication-and-authorization-components/update-and-release-service.md) —
  combines role-separated metadata, supply-chain provenance, applicability,
  trial activation, independent health, and rollback protection.

### External federation boundary

- [15. Federation gateway](../20-notes/authentication-and-authorization-components/federation-gateway.md) —
  confines remote token and certificate parsing, preserves subject/actor
  provenance, and terminates federation in a fresh local authorization
  decision rather than importing bearer authority.

## Trails

### Architecture and authority

- [BEAM, ERTS, and OTP principles for a new operating
  system](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md)
  defines the five layers and the boundary between a privileged substrate,
  managed actors, policy services, and applications.
- [Anderson's security-kernel
  study](../30-sources/anderson-1972-computer-security-technology-planning-study.md)
  motivates complete, tamper-resistant, analyzable mediation.
- [Saltzer and Schroeder's protection
  principles](../30-sources/saltzer-schroeder-1975-protection-information.md)
  frame fail-safe defaults, complete mediation, least privilege, separation of
  privilege, and economy of mechanism.
- [Lampson's protection
  model](../30-sources/lampson-1971-protection.md) separates domains, objects,
  rights, and the access matrix; [Harrison, Ruzzo, and
  Ullman](../30-sources/harrison-et-al-1976-protection-in-operating-systems.md)
  show why unrestricted protection-state safety is not generally decidable.
- [The confused deputy](../30-sources/hardy-1988-confused-deputy.md),
  [KeyKOS](../30-sources/hardy-1990-keykos-architecture.md),
  [EROS](../30-sources/shapiro-et-al-1999-eros.md), and
  [Capsicum](../30-sources/watson-et-al-2010-capsicum.md) lead to explicit,
  attenuated authority rather than ambient identity-based privilege.

### Human authentication and trusted interaction

- [NIST SP 800-63B-4](../30-sources/temoshok-et-al-2025-authentication-and-authenticator-management.md)
  supplies current assurance and authenticator-lifecycle requirements.
- [WebAuthn Level 3](../30-sources/w3c-2026-webauthn-level-3.md) and
  [CTAP 2.2](../30-sources/fido-alliance-2025-ctap-2-2.md) provide the public-
  key authenticator baseline; [formal FIDO2
  analysis](../30-sources/guan-et-al-2022-formal-analysis-fido2.md) warns that
  protocol composition and parallel ceremonies still need proof and testing.
- [Operating System
  Framed](../30-sources/bravo-lillo-et-al-2012-operating-system-framed.md) shows
  that visual security framing does not eliminate spoofing, while
  [Nitpicker](../30-sources/feske-helmuth-2005-nitpicker.md) provides a small
  secure-GUI architecture to study.
- [The passkey abusability
  study](../30-sources/daffalla-et-al-2025-passkey-abusability.md) keeps
  enrollment, sharing, synchronization, and recovery inside the threat model.

### Workloads, devices, and boot evidence

- [The SPIFFE Workload
  API](../30-sources/spiffe-project-2026-workload-api.md) informs short-lived,
  attested workload credentials without turning an identity name into a role.
- [RATS](../30-sources/birkholz-et-al-2023-rats-architecture.md) separates
  evidence, verification, appraisal, endorsement, reference values, and the
  relying party; [EAT](../30-sources/lundblade-et-al-2025-entity-attestation-token.md)
  provides a claims container rather than an authorization decision.
- [TPM 2.0](../30-sources/trusted-computing-group-2026-tpm-2-0-library.md) is the
  full hardware-root profile and
  [DICE](../30-sources/trusted-computing-group-2024-dice-hardware-requirements.md)
  is the constrained-device profile.
- [Verified Morello
  security](../30-sources/bauereiss-et-al-2022-verified-morello-security.md)
  constrains claims about hardware capabilities: memory-authority protection
  is defense in depth, not authentication or end-to-end authorization.

### Policy and local enforcement

- [Cedar](../30-sources/cutler-et-al-2024-cedar.md) provides a model for typed,
  pure, default-deny policy across roles, attributes, and relationships.
- [Verification-guided Cedar
  development](../30-sources/disselkoen-et-al-2024-verification-guided-cedar.md)
  supports mechanized semantics plus differential randomized testing of the
  production evaluator.
- [The minimal privileged kernel
  layer](../20-notes/minimal-privileged-kernel-layer.md) owns typed local
  capabilities, object generations, budgets, admission, and revocation
  anchors; policy meaning remains outside privilege.
- [The managed actor runtime
  layer](../20-notes/managed-actor-runtime-layer.md) must preserve opaque
  handles and separate subject, actor, routing identity, and supervision.

### Distribution, delegation, and consistency

- [NIST zero trust](../30-sources/rose-et-al-2020-zero-trust-architecture.md)
  motivates explicit policy decision, administration, and enforcement without
  trusting network location.
- [Macaroons](../30-sources/birgisson-et-al-2014-macaroons.md) provide an
  optional caveated-delegation model, but Atom needs proof-of-possession,
  resource-generation, budget, and revocation bindings.
- [Zanzibar](../30-sources/pang-et-al-2019-zanzibar.md) supplies causal
  relationship revisions for avoiding stale “new enemy” authorization.
- [OAuth 2.0 Security BCP](../30-sources/lodderstedt-et-al-2025-oauth-security-bcp.md)
  and [DPoP](../30-sources/fett-et-al-2023-dpop.md) constrain external
  federation. Remote proof terminates at a gateway and becomes a new local
  capability; a kernel capability never becomes a network bearer token.

### Recovery, audit, update, and assurance

- [Secure audit
  logs](../30-sources/schneier-kelsey-1999-secure-audit-logs.md) support
  forward-integrity chains and independent witnesses while leaving
  completeness and truthfulness as explicit assumptions.
- [TUF](../30-sources/samuel-et-al-2010-tuf.md) supports role-separated update
  keys, threshold signatures, freshness, and rollback resistance.
- [Comprehensive seL4
  verification](../30-sources/klein-et-al-2014-comprehensive-sel4-verification.md),
  [seL4 information-flow
  enforcement](../30-sources/murray-et-al-2013-sel4-information-flow.md), and
  [Rushby's secure-system
  decomposition](../30-sources/rushby-1981-design-verification-secure-systems.md)
  provide proof and assumption disciplines. Their results do not transfer to
  an unimplemented Atom OS composition.

## Open questions

- [What contract should system-wide authentication and authorization
  provide?](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
  asks which first deployment profile, capability algebra, native-login
  ceremony, hardware root, policy schema, consistency bounds, recovery design,
  and assurance evidence the implementation will commit to.
- The first target must choose between interactive, embedded, institutional,
  disconnected, and high-confidentiality profiles; presenting their union as
  one implementable policy would conceal incompatible assumptions.
- Pre-boot data-key recovery, trusted input/output hardware, authorization
  policy activation, distributed revocation service levels, and information-
  flow requirements remain design decisions rather than settled evidence.
