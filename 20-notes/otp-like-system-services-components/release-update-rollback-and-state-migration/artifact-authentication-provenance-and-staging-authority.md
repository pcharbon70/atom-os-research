---
title: "Artifact authentication, provenance, and staging authority"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Artifact authentication, provenance, and staging authority

This study decomposes [Release, update, rollback, and state migration](../release-update-rollback-and-state-migration.md).

Research question: What must be verified before signed bytes are eligible for deployment?

## Research basis and status

TUF authenticates delivered targets; in-toto constrains signed supply-chain steps
and artifact relationships, not software correctness. [1](../../../30-sources/tuf-project-2026-specification-1-0-36.md) [2](../../../30-sources/torres-arias-et-al-2019-in-toto.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The verifier owns trusted metadata roles, accepted security high-water state,
artifact digests, provenance policy and inactive staging references. The rollout
controller separately owns activation authority. Builders and attesting
functionaries remain explicit trusted parties.

### Admission, transitions and completion

Bound downloads, delegation traversal and archive expansion. Verify metadata
freshness and consistent digests, then validate the approved provenance layout and
signer requirements. Bind the accepted result to exact bytes and policy revision.
Staging produces an immutable candidate, never permission to activate it.

### Failure and adversarial behavior

A valid signature from a compromised authorized builder can still describe malicious
output. Provenance inspections themselves may execute code and therefore need
confinement and explicit authority. Restoring old trusted metadata requires
rollback-resistant evidence; absence of reliable freshness must be disclosed.

### Alternatives and unresolved tradeoffs

Release signatures alone are simpler but omit build-path evidence. Reproducible
rebuilding provides a different check and does not replace authorization. Choose the
exact attestation and verifier profile separately; neither cited framework supplies
safe runtime migration.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Substitute a build product while retaining valid target metadata for another digest; staging must fail.
- Present complete signatures from unauthorized functionaries, then a valid old release below the protected security floor; reject both.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Application lifecycle and dependency orchestration](../application-lifecycle-and-dependency-orchestration/README.md) — coordinates readiness, publication and drain.
- [Durable state, transactions, and outcome recovery](../durable-state-transactions-and-outcome-recovery/README.md) — retains committed state and retry-result responsibility.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [TUF specification 1.0.36](../../../30-sources/tuf-project-2026-specification-1-0-36.md).
2. [in-toto](../../../30-sources/torres-arias-et-al-2019-in-toto.md).
