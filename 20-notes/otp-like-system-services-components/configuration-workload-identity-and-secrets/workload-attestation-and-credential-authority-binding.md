---
title: "Workload attestation and credential-authority binding"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Workload attestation and credential-authority binding

This study decomposes [Configuration, workload identity, and secrets](../configuration-workload-identity-and-secrets.md).

Research question: How does the broker identify its caller without trusting a self-declared service name?

## Research basis and status

SPIFFE relies on endpoint-side caller attribution; identity material does not itself
authorize resource operations. [1](../../../30-sources/spiffe-project-2026-workload-api.md) [2](../../../30-sources/miller-et-al-2003-capability-myths.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The credential broker owns the mapping from protected caller evidence to workload
identity, issuer policy and trust-domain scope. Kernel/runtime generations, artifact
identity and lifecycle receipts are inputs from named trusted owners. A request's
display name or business tenant label cannot replace them.

### Admission, transitions and completion

Bind the local protected channel to the actual caller incarnation, verify
eligibility and attenuate requested credential scope. Keep authentication, issuer
authorization and application authorization separate. A key handle additionally
binds operation, recipient and lifetime so forwarding a reference does not silently
widen use.

### Failure and adversarial behavior

PID reuse, forged manifest metadata and stale attestation can issue credentials to
the wrong process. Recheck lifecycle validity at issuance and renewal. Broker
compromise is a high-value failure: isolate issuer authority and preserve
independent replacement outside its own domain.

### Alternatives and unresolved tradeoffs

Exportable credentials ease interoperability; non-exportable handles reduce copying
but require a native cryptographic adapter. SPIFFE's standard byte-returning profile
is not automatically compatible with that adapter. Exact attestation evidence and
root trust remain unselected.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Reuse a numeric process identifier after destruction; the successor cannot renew its predecessor's lease.
- Submit a different tenant or service label through the same channel and verify issuer policy uses authenticated context, not payload designation.

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
