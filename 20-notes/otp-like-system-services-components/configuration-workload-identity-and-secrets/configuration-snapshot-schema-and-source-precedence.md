---
title: "Configuration snapshot schema and source precedence"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Configuration snapshot schema and source precedence

This study decomposes [Configuration, workload identity, and secrets](../configuration-workload-identity-and-secrets.md).

Research question: How can a complete configuration be reproducible without embedding secrets or mutable operational state?

## Research basis and status

Immutable configuration and versioned delivery make revisions inspectable, but
neither establishes simultaneous service activation. [1](../../../30-sources/dolstra-et-al-2008-nixos.md) [2](../../../30-sources/envoy-project-2026-xds-protocol.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The snapshot builder owns source digests, precedence rules, schema identity, typed
values and configuration size limits. Credential material belongs to a separate
broker. Mutable workflow progress and authoritative domain data are not
configuration inputs.

### Admission, transitions and completion

Capture source revisions, validate types and dependency references, canonicalize
values and compute the candidate digest. Retain a complete immutable snapshot rather
than mutating fields in place. Unknown required fields fail; optional extensions
need explicit forwarding semantics. Secret-valued fields resolve only to scoped
opaque references.

### Failure and adversarial behavior

Conflicting precedence, cyclic imports and expansion bombs must fail before
candidate publication. A digest authenticates equality only after trusted provenance
is established. Signed stale configuration remains a rollback risk when no protected
high-water or external witness exists.

### Alternatives and unresolved tradeoffs

Delta distribution reduces bandwidth but requires a known base and
resynchronization. Full snapshots cost transfer bytes while simplifying recovery.
Choose the wire profile independently of the immutable semantic model and keep
schema downgrade rules explicit.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Shuffle input source ordering and verify declared precedence alone determines the digest.
- Inject a secret value into an ordinary field and ensure validation/redaction prevents publication and diagnostic leakage.

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

1. [NixOS](../../../30-sources/dolstra-et-al-2008-nixos.md).
2. [xDS protocol](../../../30-sources/envoy-project-2026-xds-protocol.md).
