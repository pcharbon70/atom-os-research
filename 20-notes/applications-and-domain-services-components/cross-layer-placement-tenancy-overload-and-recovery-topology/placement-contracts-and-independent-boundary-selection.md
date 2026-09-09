---
title: "Placement contracts and independent boundary selection"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Placement contracts and independent boundary selection

This study decomposes [Cross-layer placement, tenancy, overload, and recovery topology](../cross-layer-placement-tenancy-overload-and-recovery-topology.md).

Research question: Which application boundaries should coincide, and which should remain separate?

## Research basis and status

The SaaS concern model spans data, customization, placement and performance; one tenant label is not physical isolation. [1](../../../30-sources/krebs-et-al-2012-multi-tenant-saas.md).

Wedge demonstrates reduced-privilege compartments in Linux applications; it does not validate Atom OS isolation costs. [2](../../../30-sources/bittau-et-al-2008-wedge.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own a placement declaration mapping bounded contexts, aggregate actors, supervisors,
packages and protected domains. Layer 5 selects semantic and trust requirements;
Layer 4 admits placement; Layers 2–3 enforce protection and runtime accounting. A
business boundary is not automatically a security or restart boundary.

### Admission, transitions and completion

Inventory mutable state, secrets, native code, effect authority, independent
recovery needs and resource coupling. Co-locate only mutually trusted code whose
combined failure and authority scope is acceptable. Record explicit reasons for each
protection boundary and the lower contracts required to maintain it.

### Failure and adversarial behavior

One runtime per tenant may still combine distrustful plugins. One process per actor
may impose unacceptable memory and IPC cost without clarifying domain ownership.
Shared caches and broad recovery tools can defeat a carefully drawn diagram.
Placement review must include actual reachable authority, not only dependency
arrows.

### Alternatives and unresolved tradeoffs

Shared trusted actor domains preserve cheap communication. Separate domains provide
stronger enforceable containment at measurable cost. Decide granularity from threats
and workloads; the current literature cannot supply Atom OS footprint, latency or
density results.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Trace reachable secrets and effect facets across every proposed co-location boundary.
- Compare shared and isolated placements under runtime compromise and load, preserving identical semantic workload and declared assumptions.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Semantic readiness and degraded lifecycle evidence](../application-manifest-composition-and-authority-envelope/semantic-readiness-and-degraded-lifecycle-evidence.md) — a cross-component contract this service must preserve.
- [Intent-bound grants and compromised-adapter containment](../external-effects-ports-adapters-and-reconciliation/intent-bound-grants-and-compromised-adapter-containment.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [Multi-tenant SaaS concerns](../../../30-sources/krebs-et-al-2012-multi-tenant-saas.md).
2. [Wedge](../../../30-sources/bittau-et-al-2008-wedge.md).
