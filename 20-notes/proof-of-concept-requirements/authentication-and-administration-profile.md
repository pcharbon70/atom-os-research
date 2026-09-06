---
title: "Authentication and administration profile"
kind: note
created: "2026-09-06"
maturity: developing
tags:
  - capability-roadmap
  - proof-of-concept
  - requirements
aliases: []
---

# Authentication and administration profile

Requirement R18, after M4. Select the deployment threat model before introducing login, remote administration or untrusted tenants. Static demo capabilities are useful bootstrap authority, not authentication evidence.

## Evidence and applicability

[NIST's authentication guidance](../../30-sources/temoshok-et-al-2025-authentication-and-authenticator-management.md) covers authenticators, enrollment and lifecycle for digital identity systems. It is not a specification for local kernel capabilities or proof of isolation between hostile BEAM actors.

[NIST's entropy-source guidance](../../30-sources/turan-et-al-2018-entropy-source-requirements.md) requires source characterization and health assessment. Statistical tests or hashing cannot manufacture unpredictability from a known input.

Use those sources to structure requirements, then qualify actual libraries, devices and administrative paths. No authenticator scheme, secure-channel implementation or entropy device was selected in this session.

## Proposed deployment profiles

Keep three profiles distinct:

- Trusted local development: a host operator controls the serial connection, boot images and emulator. No human-login or hostile-host claim.
- Remote administration: authenticated operators receive narrowly scoped management capabilities over a qualified secure channel.
- Untrusted tenancy: separate principals receive enforced memory, CPU, namespace and device authority boundaries, with explicit denial-of-service and side-channel exclusions.

The first PoC uses the first profile. Do not expose its unauthenticated serial command interface as a remote management service accidentally.

Authentication establishes which identity is present. Authorization decides which operations that identity may perform, and capability checks enforce those decisions at the service/kernel boundaries. Trace this chain for restart, image installation, key enrollment and diagnostic access.

A login inside one shared runtime cannot by itself establish hostile-tenant memory isolation. Assign adversarial tenants to an appropriate protection boundary and state which runtime/kernel components remain trusted.

## Trusted interaction, keys and revocation

Define enrollment and recovery channels, operator confirmation, credential storage, key rotation, failed-attempt policy and audit retention. Prevent untrusted service output from impersonating a trusted authentication prompt or management confirmation.

Inventory entropy requirements for keys, nonces and session identifiers. A virtual entropy source may depend on the trusted host; document it. A clock, deterministic seed or device identifier is not a production key source. If qualified entropy is unavailable, fail the dependent security operation explicitly.

Snapshot and rollback can repeat random-generator state or session epochs. Test restoration and cloning, not only ordinary reboot. Cryptographic algorithm choice cannot compensate for repeated keys/nonces caused by a lifecycle error.

Specify how revoked authority stops new operations, what happens to admitted effects, and how recovery avoids resurrecting old credentials or capabilities. Credentials and authorization policy need version/freshness handling if persistent rollback is possible.

## Acceptance and next exploration

Choose one post-M4 profile and draw the end-to-end identity/authority graph. For every sensitive CLI action, identify the trusted input path, authenticated principal, policy decision, capability grant and enforcing component.

Test impersonation, replay, stale sessions, privilege escalation, credential loss, revoked users, recovery into an old policy and resource exhaustion of authentication services. Verify that diagnostics omit secrets and that failed authentication cannot consume the recovery reserve.

The next artifact is a deployment-specific threat model with enrollment, entropy and revocation test plans. Static grants suffice for the local demonstration only; no remote-administration or untrusted-tenancy security claim has passed.

## Connections

[CLI placement](serial-console-and-minimal-cli.md), [capabilities](capabilities-syscalls-and-bounded-ipc.md), [network sessions](networking-and-remote-actor-boundaries.md) and [updates](updates-and-recovery-root-survival.md) carry the resulting authority.
