---
title: "Authentication and authorization components"
kind: map
created: "2026-09-04"
tags:
  - authentication
  - authorization
  - archive-navigation
  - directory-index
  - security
aliases:
  - "Authentication and authorization service notes"
---

# Authentication and authorization components (`authentication-and-authorization-components`)

## Purpose

This directory collects the detailed implementation research for the sixteen
OTP-like security services proposed in [authentication and authorization
across the five-layer architecture](../authentication-and-authorization-across-the-five-layer-architecture.md).

## What belongs here

Put component-level architecture syntheses here when they develop one
authentication, identity, policy, grant, revocation, secret, audit, recovery,
update, or federation service in enough detail to require its own evidence,
authority boundary, objects, state machine, failure analysis, and verification
plan. Keep the integrated cross-layer security model and other broad operating-
system syntheses in the parent notes directory.

## Index

### Subdirectories

- None yet.

### Documents

- [0. Trusted-interaction broker](trusted-interaction-broker.md) — develops a
  secure-attention-mediated, request-bound, one-shot human confirmation path
  with explicit abort and overload semantics.
- [1. Credential registrar and inventory](credential-registrar-and-inventory.md) —
  develops an auditable principal-to-authenticator binding ledger with
  transactional enrollment, visible lifecycle, and rollback-resistant
  tombstones.
- [2. Authentication verifier](authentication-verifier.md) — confines protocol
  parsing, challenge validation, password compatibility, replay state, and
  throttling behind one-use typed authentication evidence.
- [3. Session service](session-service.md) — models authentication continuity as
  a generation-bound, proof-of-possession-capable context that never carries
  ambient resource authority.
- [4. Workload identity issuer](workload-identity-issuer.md) — derives short-
  lived workload credentials from kernel-authenticated incarnations and
  versioned registration policy without exporting broad signing authority.
- [5. RATS Verifier and Appraisal Policy](rats-verifier-and-appraisal-policy.md) —
  separates bounded evidence parsing, reference values, endorsements, evidence
  appraisal, and relying-party authorization.
- [6. Relationship authority](relationship-authority.md) — develops a versioned,
  causally queryable ownership and sharing graph with immutable models,
  tombstones, and bounded traversal.
- [7. Attribute authorities](attribute-authorities.md) — defines scoped issuers
  of typed, provenance-carrying, privacy-aware, short-lived claims rather than
  a universal attribute oracle.
- [8. Policy decision point](policy-decision-point.md) — develops a pure,
  deterministic, resource-bounded evaluator over immutable policy and evidence
  snapshots with typed non-permit outcomes.
- [9. Grant compiler and issuer](grant-compiler-and-issuer.md) — compiles one
  authenticated permit into an attenuated local capability or sender-
  constrained remote grant inside a fixed issuer envelope.
- [10. Revocation and epoch service](revocation-and-epoch-service.md) — makes
  committed, distributed, enforced, quiesced, and sanitized revocation stages
  explicit and binds authority to rollback-resistant epochs.
- [11. Key and secret service](key-and-secret-service.md) — exposes non-
  exportable, per-purpose cryptographic operation facets, protected metadata,
  leases, rotation, compromise, destruction, and recovery boundaries.
- [12. Audit and witness services](audit-and-witness-services.md) — composes
  bounded durable admission, forward integrity, Merkle commitments, independent
  witnesses, and declared loss behavior without claiming event truth.
- [13. Recovery coordinator](recovery-coordinator.md) — separates credential,
  data-key, platform, break-glass, and destructive-reset recovery into
  predeclared threshold workflows with one-shot authority.
- [14. Update and release service](update-and-release-service.md) — combines
  role-separated metadata, supply-chain provenance, target applicability,
  trial activation, independent health, and anti-rollback state.
- [15. Federation gateway](federation-gateway.md) — confines remote token and
  certificate parsing, preserves subject/actor provenance, and terminates
  federation in a fresh local authorization decision.

## Maintaining this index

Inventory every direct component note, preserve the 0-through-15 numbering,
and update the parent notes index and authentication-and-authorization map
whenever a component is added, renamed, moved, archived, or superseded.
