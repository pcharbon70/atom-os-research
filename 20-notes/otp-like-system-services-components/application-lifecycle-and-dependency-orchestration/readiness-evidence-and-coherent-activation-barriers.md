---
title: "Readiness evidence and coherent activation barriers"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Readiness evidence and coherent activation barriers

This study decomposes [Application lifecycle and dependency orchestration](../application-lifecycle-and-dependency-orchestration.md).

Research question: When may prepared services become discoverable as one usable generation?

## Research basis and status

An atomic profile selector does not atomically apply live effects; configuration ACK
is weaker than actual adoption. [1](../../../30-sources/dolstra-et-al-2008-nixos.md) [2](../../../30-sources/envoy-project-2026-xds-protocol.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The gate owns predicates over recovered state, dependency revisions, endpoint
bindings, active configuration, identity generation and resource reservation.
Individual services supply claims; protected owners supply the independent receipts
required by the selected assurance profile.

### Admission, transitions and completion

Collect evidence against a frozen plan and reject stale contributors. Prepare an
immutable registry table, then conditionally select it. Where semantic coherence
spans independently scheduled consumers, require an activation barrier and
generation checks on requests; otherwise explicitly permit mixed versions.

### Failure and adversarial behavior

A healthy process with the wrong credentials or state frontier is not Ready. A
provider may change after a consumer probe succeeds; revalidate at publication and
use. A lost commit reply is reconciled against the authoritative root, not treated
as failed activation.

### Alternatives and unresolved tradeoffs

Deep readiness probes detect integration defects but may introduce circular
dependencies and expensive work. Prefer small declarative predicates tied to proof
points. A continuous health check is not a permanent readiness certificate or
authority grant.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Change a dependency and configuration revision between probe and publish; stale evidence must not satisfy the gate.
- Publish while one participant has not adopted the shared generation; mismatched operations must fence or remain blocked.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Service-domain bootstrap and manifest controller](../service-domain-bootstrap-and-manifest-controller/README.md) — reconciles desired service generations within the boot envelope.
- [Release, update, rollback, and state migration](../release-update-rollback-and-state-migration/README.md) — coordinates code/state transitions and retention.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [NixOS](../../../30-sources/dolstra-et-al-2008-nixos.md).
2. [xDS protocol](../../../30-sources/envoy-project-2026-xds-protocol.md).
