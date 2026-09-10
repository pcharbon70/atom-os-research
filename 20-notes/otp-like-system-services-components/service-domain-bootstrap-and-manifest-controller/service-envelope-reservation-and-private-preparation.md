---
title: "Service-envelope reservation and private preparation"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Service-envelope reservation and private preparation

This study decomposes [Service-domain bootstrap and manifest controller](../service-domain-bootstrap-and-manifest-controller.md).

Research question: How are resources and authority reserved without making preparation a second root of privilege?

## Research basis and status

Capability attenuation constrains delegated authority; Anvil motivates explicit
version-sensitive controller steps, not a resource-transaction theorem. [1](../../../30-sources/miller-et-al-2003-capability-myths.md) [2](../../../30-sources/sun-et-al-2024-anvil.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The preparation service owns an attempt ledger, provisional capability descendants
and reservations for domains, endpoints, memory and recovery work. The independent
boot holder owns the ceiling and replacement facet; reservation policy stays outside
privileged enforcement.

### Admission, transitions and completion

Validate the plan against the actual delegation envelope, atomically reserve scarce
resources, then construct private recipients. Each adapter request binds attempt,
recipient incarnation and input digest. Installation receipts must identify the
recipient, granted rights and lower-layer generation; a declared capability name is
insufficient.

### Failure and adversarial behavior

Crash between reservation and installation leaves recoverable attempt-owned
obligations. Cleanup must not revoke a shared dependency or reclaim memory before
its lower-layer quiescence proof. Uncertain DMA or storage effects become
quarantined obligations with an accountable custodian.

### Alternatives and unresolved tradeoffs

Central reservation simplifies conservation but risks a hot control service.
Distributed reservation requires a separate commit/recovery protocol and cannot be
justified merely by actor isolation. Recovery reserve must remain spendable when
ordinary admission is exhausted.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Crash after every reservation and installation acknowledgement; sum live, returned and quarantined resources against the original grant.
- Forge a recipient generation and request rights exceeding its parent; publication must remain unavailable.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Application lifecycle and dependency orchestration](../application-lifecycle-and-dependency-orchestration/README.md) — coordinates readiness, publication and drain.
- [Naming, registry, and local discovery](../naming-registry-and-local-discovery/README.md) — publishes current bindings and watch revisions.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [Capability myths demolished](../../../30-sources/miller-et-al-2003-capability-myths.md).
2. [Anvil](../../../30-sources/sun-et-al-2024-anvil.md).
