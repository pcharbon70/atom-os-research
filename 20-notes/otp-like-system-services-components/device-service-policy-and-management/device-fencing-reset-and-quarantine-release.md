---
title: "Device fencing, reset, and quarantine release"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Device fencing, reset, and quarantine release

This study decomposes [Device-service policy and management](../device-service-policy-and-management.md).

Research question: When is old device activity unable to corrupt a replacement's resources?

## Research basis and status

DMA confinement and capability revocation constrain access, but safe reset and
reclamation require separate platform evidence. [1](../../../30-sources/heiser-et-al-2026-sddf-design.md) [2](../../../30-sources/miller-et-al-2003-capability-myths.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The recovery manager owns admission closure, device fence, reset-group membership,
outstanding custody and quarantine records. The privileged layer supplies interrupt,
mapping and IOMMU invalidation proofs. The driver has no authority to bypass its own
containment.

### Admission, transitions and completion

Close software admission, fence old sessions, stop new DMA and settle interrupts and
queue activity according to the hardware profile. Reset the complete affected group,
reconcile outcomes and initialize a private successor. Publish only after both
service readiness and safe-resource-reuse evidence pass.

### Failure and adversarial behavior

A reset acknowledgement is not universally proof that all previously issued writes
or DMA disappeared. If quiescence cannot be established, retain buffers and
operations in quarantine and escalate. A replacement that reuses addresses too early
creates a stale-DMA attack surface despite fresh software IDs.

### Alternatives and unresolved tradeoffs

Function reset may be cheap but unsupported or shared; wider reset improves
containment at availability cost. Full reboot is a legitimate declared outer
boundary, not proof of external effect reversal. Exact recovery orders require
hardware-specific validation.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Delay a DMA write beyond software teardown; the buffer cannot enter the successor's pool before safe isolation proof.
- Fail the recovery manager during reset and ensure its successor preserves quarantine and accepted-operation identities.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Network endpoint and protocol services](../network-endpoint-and-protocol-services/README.md) — separates transport session state from application outcomes.
- [Supervision and recovery policy](../supervision-and-recovery-policy/README.md) — owns restart admission, quarantine and escalation.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [sDDF design](../../../30-sources/heiser-et-al-2026-sddf-design.md).
2. [Capability myths demolished](../../../30-sources/miller-et-al-2003-capability-myths.md).
