---
title: "Business-tenant bindings and realm reassignment"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Business-tenant bindings and realm reassignment

This study decomposes [Cross-layer placement, tenancy, overload, and recovery topology](../cross-layer-placement-tenancy-overload-and-recovery-topology.md).

Research question: How does a domain partition retain identity while its authenticated security binding changes?

## Research basis and status

The SaaS concern model spans data, customization, placement and performance; one tenant label is not physical isolation. [1](../../../30-sources/krebs-et-al-2012-multi-tenant-saas.md).

The archived WASI design principles favor explicit imports and resource handles; correct host enforcement is still assumed. [2](../../../30-sources/wasi-project-2026-design-principles.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own the business-tenant designation and its domain lifecycle. Layer 4 owns
authenticated realm identity, binding generation, policy, grants and account scopes.
A TenantApplicationBinding relates them explicitly; neither a caller-supplied string
nor equality of names establishes this relationship.

### Admission, transitions and completion

Require one current binding on each admitted operation and derive store, projection,
adapter, backup and diagnostic scopes from it. During reassignment, fence old
admission, classify accepted work and migrate or rebind only under dedicated
authority. DomainRef remains stable unless the business entity itself changes
lifecycle.

### Failure and adversarial behavior

A stale cache key can disclose data under a new tenant binding. A backup restore can
revive old realm credentials if metadata is treated as a live grant. Many-to-many
historical mappings need exact generation lookup, not a global current-tenant
variable or default process identity.

### Alternatives and unresolved tradeoffs

Separate stores, keys and domains offer stronger isolation for selected profiles but
increase operating cost. Logical namespaces can serve mutually trusted workloads
only with actual scope enforcement. Reassignment is not a simple tag update because
accepted effects and retained outcomes carry old provenance.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Reassign one business tenant while commands, projections and backups are active; stale bindings fail at each sink.
- Present a matching tenant name with an unauthenticated or wrong-generation realm binding; refuse before admission and avoid data disclosure.

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
2. [WASI Design Principles](../../../30-sources/wasi-project-2026-design-principles.md).
