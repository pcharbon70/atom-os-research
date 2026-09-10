---
title: "Device inventory, reset domains, and driver admission"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Device inventory, reset domains, and driver admission

This study decomposes [Device-service policy and management](../device-service-policy-and-management.md).

Research question: Which hardware resources can actually be managed and reset independently?

## Research basis and status

sDDF separates driver and virtualizer responsibilities; capability confinement
depends on the actual delegated hardware boundary. [1](../../../30-sources/heiser-et-al-2026-sddf-design.md) [2](../../../30-sources/miller-et-al-2003-capability-myths.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The inventory manager owns device incarnation, class profile, firmware identity,
reset coupling and approved driver artifact. Privileged mapping, interrupt and IOMMU
enforcement remain below this layer. Enumeration is evidence about hardware, not
permission to expose it.

### Admission, transitions and completion

Match a device to an explicit driver and containment profile. Reserve queues and
buffers, derive only required data-path facets and retain reset/replacement
authority outside the driver. Treat shared reset, power and DMA isolation scopes as
distinct relations rather than assuming one function is independent.

### Failure and adversarial behavior

A compromised driver cannot attest its own safe removal. Hot-unplug, firmware change
or reset-group expansion invalidates dependent sessions. Where hardware lacks
adequate containment, record a weaker trust profile or refuse multi-principal
sharing instead of advertising isolation.

### Alternatives and unresolved tradeoffs

One domain per device is intuitive but may misrepresent reset-coupled functions. One
domain per group reduces false independence at the cost of broader failure impact.
Driver selection and hardware capability evidence remain device-specific research
obligations, not QEMU fixtures.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Model two functions sharing reset but not an endpoint; admission must disclose and enforce the collateral recovery scope.
- Replace a device at the same bus address and ensure old sessions cannot bind to the new incarnation.

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
