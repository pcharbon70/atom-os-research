---
title: "Class virtualization, queue credits, and buffer custody"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Class virtualization, queue credits, and buffer custody

This study decomposes [Device-service policy and management](../device-service-policy-and-management.md).

Research question: How can untrusted clients share I/O without forging descriptors or duplicating buffer ownership?

## Research basis and status

sDDF uses selectively shared ownership queues; queue-based modularity still needs
explicit resource and overload contracts. [1](../../../30-sources/heiser-et-al-2026-sddf-design.md) [2](../../../30-sources/welsh-et-al-2001-seda.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The virtualizer owns per-client sessions, operation permissions, descriptor credits,
payload ownership and scheduling policy. The driver owns hardware issue mechanics.
Metadata and payload mappings expose only the regions needed by each participant.

### Admission, transitions and completion

Validate lengths, operation classes, buffer bounds and device/session generations
before ownership transfer. Charge descriptor and byte capacity independently. Return
credits only when the resource is genuinely released, not merely when dequeued for
processing. Cross-principal reuse requires sanitization and relabel evidence.

### Failure and adversarial behavior

Forged completion, duplicate return and stale reset-generation traffic must not free
current buffers. A full return path can deadlock reclamation unless its capacity is
reserved. Client failure leaves tracked custody; it does not permit reuse while DMA
remains possible.

### Alternatives and unresolved tradeoffs

Zero-copy reduces transfer cost but increases shared-memory protocol trust. Copying
into broker-owned buffers may simplify small control operations. Choose by measured
cost, confidentiality and ownership proof rather than requiring one mechanism for
every device class.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Exhaust request and return rings independently and verify forward progress or bounded rejection without overwriting ownership.
- Replay a return descriptor after buffer reuse; no second credit or current-generation release may occur.

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
2. [SEDA](../../../30-sources/welsh-et-al-2001-seda.md).
