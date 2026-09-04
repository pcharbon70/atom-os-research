---
title: "2026-09-04 authentication and authorization deep dive"
kind: journal
created: "2026-09-04"
tags:
  - authentication
  - authorization
  - capabilities
  - research-session
  - security
aliases:
  - "Authentication and authorization research session"
---

# 2026-09-04 authentication and authorization deep dive

## Observations

The research question began with preventing unauthenticated access and
providing authorization across the five-layer Atom OS architecture. The search
quickly showed that a login subsystem alone would leave the important problems
unsolved: secure interaction, credential lifecycle, workload and node identity,
attestation, policy semantics, capability enforcement, distributed freshness,
revocation, storage unlock, recovery, audit, update, and denial of service form
one end-to-end authority lifecycle.

The main synthesis is a two-plane architecture:

```text
identity/evidence/policy control plane -> bounded grant
bounded grant -> kernel/local capability data plane -> mediated effect
```

Authentication creates evidence, not authority. Attestation creates appraised
evidence, not authority. Policy authorizes one typed request. The grant issuer
can derive only authority already inside its kernel envelope, and the resource
server validates the exact object generation and request in the same admission
transaction as the effect.

An explicit anonymous principal is a critical result. The pre-authentication
environment is a confined application domain with only deliberately public or
bootstrap capabilities and finite CPU, memory, queue, cryptographic, UI, and
audit budgets. “No session” is never a reason to skip policy.

Cross-review identified two easy-to-miss boundaries. First, credential
recovery, encrypted-data-key recovery, and destructive reprovisioning are
different powers; any escrow is decryption authority. Second, a distributed
grant is not safe merely because its signature verifies: issue, lineage/audit
registration, replay/idempotency consumption, effect commit, issuer fencing,
policy activation, and revocation watermarks require crash and partition
semantics.

## Environment

- Repository: `/home/ducky/code/atom-os-research`
- Repository revision at the final research check: `bff2082`
- Research date: 2026-09-04
- Host used for archive checks: Linux 6.8.0-51-generic, x86-64
- Validation runtime: Python 3.12.12
- Subject architecture: five layers documented in [BEAM, ERTS, and OTP
  principles for a new operating
  system](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md)
- Work type: literature and standards review plus architectural synthesis
- Hardware or simulator target: none selected
- Atom OS implementation, benchmark, or fault-injection run: none
- External material: scientific papers, standards, official project
  specifications, government guidance, and selected empirical security studies

## Evidence

### Search and selection method

The search covered foundational access-control theory, capability systems,
reference monitors and formal assurance; human authenticator assurance and
lifecycle; WebAuthn/FIDO protocol composition; trusted UI and spoofing;
workload identity; measured boot, TPM, DICE, remote attestation and EAT;
policy-language semantics and verification; relationship consistency;
delegated credentials; OAuth sender constraints; audit integrity; secure
updates; and information-flow boundaries.

Primary papers, normative standards, official project specifications, and
government publications were preferred. Each substantively used work received
a source note with bibliographic metadata, claims, relevance, and limitations.
Architecture decisions were accepted only after the relevant slot had direct
evidence or was explicitly labeled an Atom-specific proposal.

Three independent review lanes examined capability/kernel placement,
human/trusted-path/recovery design, and distributed policy/revocation/audit
failure modes. Their challenges were reconciled into the synthesis rather than
reported as source evidence.

### Current source revisions checked

- NIST SP 800-63B-4, *Digital Identity Guidelines: Authentication and
  Authenticator Management*, final July/August 2025 publication.
- W3C *Web Authentication: Level 3*, Recommendation dated 2026-08-25. Earlier
  draft status would have been stale by the research date.
- FIDO Alliance CTAP 2.2 Proposed Standard dated 2025-07-14.
- Trusted Computing Group TPM 2.0 Library Specification, version 185, current
  March 2026 publication set.
- Trusted Computing Group DICE Hardware Requirements 1.0 revision 0.91,
  published 2024-08-08.
- RFC 9334 RATS architecture, RFC 9711 EAT, RFC 9700 OAuth 2.0 Security BCP,
  and RFC 9449 DPoP.
- The archive's pinned SPIFFE Workload API revision for workload identity
  semantics.

### Evidence families

- [Reference monitor, protection, and capability
  sources](../10-maps/authentication-and-authorization.md#architecture-and-authority)
  support complete mediation, explicit authority, monotonic attenuation, and a
  small kernel mechanism, while warning that unrestricted right-leakage safety
  is undecidable.
- [Human authentication and trusted-interaction
  sources](../10-maps/authentication-and-authorization.md#human-authentication-and-trusted-interaction)
  support phishing-resistant public-key authentication, strong lifecycle
  management, protocol-composition analysis, and an OS-owned trusted path;
  they do not prove a future Atom UI or native login profile.
- [Workload, attestation, and hardware-root
  sources](../10-maps/authentication-and-authorization.md#workloads-devices-and-boot-evidence)
  support role separation and evidence appraisal but explicitly leave
  authorization to the relying party.
- [Policy and distributed-system
  sources](../10-maps/authentication-and-authorization.md#distribution-delegation-and-consistency)
  support typed analyzable policy, attenuation, sender constraints, and causal
  relationship revisions; Atom's combination and failure semantics remain a
  proposal.
- [Audit, update, and formal-assurance
  sources](../10-maps/authentication-and-authorization.md#recovery-audit-update-and-assurance)
  show how to narrow integrity and proof claims and expose their assumptions.

### Resulting artifacts

- [Main authentication and authorization synthesis](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
  is the durable synthesis.
- [Authentication and authorization map](../10-maps/authentication-and-authorization.md) is the
  conceptual route through the evidence.
- [Open system-wide security contract inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
  retains the unresolved decisions and falsifiers.

### Evidence boundary

No Atom OS code, hardware, firmware, authenticator, trusted display/input path,
TPM/DICE integration, policy engine, capability grant compiler, distributed
relation store, recovery process, audit witness, or update flow was built or
tested in this session. The work is an evidence-backed architecture proposal,
not a demonstration of confidentiality, integrity, availability, usability,
formal correctness, or standards conformance.

### Archive verification

From the repository root, `python3 validate_archive.py` passed after the
connected bundle and all source-index entries were installed: 242 completed
documents, 13 directories, 1,885 local links, and 163 source notes were
checked. This is structural validation of frontmatter, indexes, filenames,
local links, and source identifiers; it is not semantic, protocol, security,
hardware, or citation-content validation.

## Source manifest

This is the authoritative session-level provenance list. “Newly introduced”
means that the source note first entered the archive during this deep dive;
“reused” means that an existing source note substantively informed the work.

### Newly introduced sources

#### Protection, capabilities, and assurance boundaries

- [Anderson, Computer Security Technology Planning Study](../30-sources/anderson-1972-computer-security-technology-planning-study.md) — supplied the reference-monitor and security-kernel criteria.
- [Lampson, Protection](../30-sources/lampson-1971-protection.md) — supplied the domain, object, right, and access-matrix model.
- [Hardy, The Confused Deputy](../30-sources/hardy-1988-confused-deputy.md) — motivated designation coupled to explicit authority.
- [Harrison, Ruzzo, and Ullman, Protection in Operating Systems](../30-sources/harrison-et-al-1976-protection-in-operating-systems.md) — bounded general safety claims for unrestricted protection systems.
- [Hardy, The KeyKOS Architecture](../30-sources/hardy-1990-keykos-architecture.md) — supplied a pure capability-system precedent.
- [Bauereiss et al., Verified Security for Morello](../30-sources/bauereiss-et-al-2022-verified-morello-security.md) — bounded claims about capability-enhanced hardware.

#### Human authentication and trusted interaction

- [Temoshok et al., NIST SP 800-63B-4](../30-sources/temoshok-et-al-2025-authentication-and-authenticator-management.md) — supplied current authentication-assurance and authenticator-lifecycle requirements.
- [W3C, Web Authentication Level 3](../30-sources/w3c-2026-webauthn-level-3.md) — supplied the public-key relying-party ceremony and authenticator data model.
- [FIDO Alliance, CTAP 2.2](../30-sources/fido-alliance-2025-ctap-2-2.md) — supplied client-to-authenticator, PIN/UV, and credential-management semantics.
- [Guan et al., A Formal Analysis of the FIDO2 Protocols](../30-sources/guan-et-al-2022-formal-analysis-fido2.md) — exposed protocol-composition and concurrent-session risks.
- [Bravo-Lillo et al., Operating System Framed](../30-sources/bravo-lillo-et-al-2012-operating-system-framed.md) — supplied empirical evidence about credential-prompt spoofing.
- [Feske and Helmuth, A Nitpicker's Guide to a Minimal-complexity Secure GUI](../30-sources/feske-helmuth-2005-nitpicker.md) — supplied a small trusted-input/output architecture.
- [Daffalla et al., The Abusability of Passkeys](../30-sources/daffalla-et-al-2025-passkey-abusability.md) — broadened passkey analysis to enrollment, sharing, synchronization, and recovery.

#### Workload identity, attestation, and hardware roots

- [Birkholz et al., RATS Architecture](../30-sources/birkholz-et-al-2023-rats-architecture.md) — separated attestation evidence, verification, appraisal, and relying-party policy.
- [Lundblade et al., Entity Attestation Token](../30-sources/lundblade-et-al-2025-entity-attestation-token.md) — supplied a versioned attestation claims container.
- [Trusted Computing Group, TPM 2.0 Library version 185](../30-sources/trusted-computing-group-2026-tpm-2-0-library.md) — supplied the full protected-key and measured-boot hardware profile.
- [Trusted Computing Group, DICE Hardware Requirements](../30-sources/trusted-computing-group-2024-dice-hardware-requirements.md) — supplied the constrained-device compound-identity profile.

#### Policy, delegation, distribution, and federation

- [Rose et al., Zero Trust Architecture](../30-sources/rose-et-al-2020-zero-trust-architecture.md) — separated policy decision, administration, and enforcement without trusting location.
- [Cutler et al., Cedar](../30-sources/cutler-et-al-2024-cedar.md) — supplied a typed, expressive, analyzable policy-language model.
- [Disselkoen et al., Verification-guided Development of Cedar Authorization](../30-sources/disselkoen-et-al-2024-verification-guided-cedar.md) — supplied mechanized properties and differential production testing.
- [Birgisson et al., Macaroons](../30-sources/birgisson-et-al-2014-macaroons.md) — supplied monotonic caveat attenuation and its delegation trade-offs.
- [Pang et al., Zanzibar](../30-sources/pang-et-al-2019-zanzibar.md) — supplied relationship authorization and causal consistency tokens.
- [Lodderstedt et al., OAuth 2.0 Security BCP](../30-sources/lodderstedt-et-al-2025-oauth-security-bcp.md) — supplied current external-federation security requirements.
- [Fett et al., DPoP](../30-sources/fett-et-al-2023-dpop.md) — supplied application-layer sender constraint and its replay/body-binding limits.

### Reused sources

- [Saltzer and Schroeder, The Protection of Information in Computer Systems](../30-sources/saltzer-schroeder-1975-protection-information.md) — supplied fail-safe defaults, complete mediation, least privilege, and separation of privilege.
- [Miller, Yee, and Shapiro, Capability Myths Demolished](../30-sources/miller-et-al-2003-capability-myths.md) — clarified capability authority, confinement, revocation, and confused-deputy properties.
- [Shapiro et al., EROS](../30-sources/shapiro-et-al-1999-eros.md) — supplied a persistent pure-capability system precedent.
- [Watson et al., Capsicum](../30-sources/watson-et-al-2010-capsicum.md) — supplied a pragmatic capability-mode and descriptor-rights precedent.
- [Klein et al., Comprehensive Formal Verification of an OS Microkernel](../30-sources/klein-et-al-2014-comprehensive-sel4-verification.md) — supplied proof structure and explicit assumption boundaries.
- [Murray et al., seL4 Information-flow Enforcement](../30-sources/murray-et-al-2013-sel4-information-flow.md) — supplied a stronger confidentiality boundary beyond access control.
- [Rushby, Design and Verification of Secure Systems](../30-sources/rushby-1981-design-verification-secure-systems.md) — supplied separation-kernel and proof-decomposition discipline.
- [SPIFFE Project, Workload API](../30-sources/spiffe-project-2026-workload-api.md) — supplied short-lived workload identity and trust-bundle delivery semantics.
- [Schneier and Kelsey, Secure Audit Logs](../30-sources/schneier-kelsey-1999-secure-audit-logs.md) — supplied forward-integrity audit mechanisms and their limits.
- [Samuel et al., The Update Framework](../30-sources/samuel-et-al-2010-tuf.md) — supplied role-separated update trust, freshness, threshold, and rollback defenses.

## Threads

- Which deployment profile should be first: single-owner embedded,
  interactive multi-user, headless institutional, disconnected/resilient, or
  high-confidentiality?
- What is the exact typed capability algebra, revocation anchor, object
  generation, admitted-operation, and budget contract?
- What canonical request encoding and local relying-party separation make a
  native FIDO2 ceremony safe?
- Which trusted input/output paths are possible on the first board, including
  accessibility, remote administration, suspend, and storage unlock?
- Which policy rules are monotonic enough for bounded-stale evaluation, and
  what are the causal and revocation service-level objectives for every action
  class?
- Does encrypted-data recovery use no escrow, owner-held wrapped keys, or a
  declared threshold custodian, and how is destructive reset distinguished?
- Which data classes require information-flow enforcement in addition to
  capability access control?

## Follow-ups

- Build the executable authority graph and lifecycle state machines before a
  user-facing login prototype.
- Select one deployment profile and board and write its complete trust and
  hardware-assumption inventory.
- Prototype the single-node anonymous-to-session-to-command capability path
  with no UID 0 compatibility shortcut.
- Specify and model the native authenticator ceremony, enrollment, downgrade,
  lock/resume, logout, pre-boot handoff, and recovery flows.
- Implement a small reference policy semantics and grant compiler and plan
  differential, property, parser-fuzz, crash, partition, replay, revocation,
  UI-spoofing, and recovery tests.
- Record all implementation commands, versions, outputs, failures, and
  artifacts in later journal entries.
