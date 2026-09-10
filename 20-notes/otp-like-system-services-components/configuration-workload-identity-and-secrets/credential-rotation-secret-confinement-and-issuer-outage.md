---
title: "Credential rotation, secret confinement, and issuer outage"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Credential rotation, secret confinement, and issuer outage

This study decomposes [Configuration, workload identity, and secrets](../configuration-workload-identity-and-secrets.md).

Research question: What remains valid when credentials rotate or issuance becomes unavailable?

## Research basis and status

SPIFFE streams complete credential/trust snapshots; revocation cannot recall copied
bearer bytes or undo prior effects. [1](../../../30-sources/spiffe-project-2026-workload-api.md) [2](../../../30-sources/miller-et-al-2003-capability-myths.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The rotation service owns current/next credential generations, trust bundles,
renewal deadlines and adoption receipts. The broker owns protected secret buffers or
key handles. Established transport sessions retain separate authentication and
revalidation state.

### Admission, transitions and completion

Stage new material, establish permitted replacement sessions, observe adoption, then
drain old sessions according to policy. Removed trust entries must stop authorizing
new validation. Jitter renewal within a bounded lead window. Declare whether
existing sessions continue, reauthenticate or close at expiry and trust change.

### Failure and adversarial behavior

An issuer outage enters jeopardy before credentials expire. No silent lifetime
extension is permitted. Exported bytes may survive in tracing heaps, binaries or
crash data; zeroizing the original buffer is not comprehensive erasure. Handle-only
secrecy is a distinct profile with explicit interoperability limits.

### Alternatives and unresolved tradeoffs

Short leases reduce stale authority but increase issuer dependence. Offline
emergency authority must be predeclared, narrowly scoped and auditable rather than
becoming permanent fallback. Protected time, revocation freshness and allowed
degraded operations remain qualification decisions.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Rotate while the consumer is stalled, then remove a trust bundle; test both new validation and existing-session policy.
- Scan permitted diagnostic outputs and controlled crash captures for secret material, including copied managed terms.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Network endpoint and protocol services](../network-endpoint-and-protocol-services/README.md) — separates transport session state from application outcomes.
- [Release, update, rollback, and state migration](../release-update-rollback-and-state-migration/README.md) — coordinates code/state transitions and retention.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [SPIFFE Workload API](../../../30-sources/spiffe-project-2026-workload-api.md).
2. [Capability myths demolished](../../../30-sources/miller-et-al-2003-capability-myths.md).
