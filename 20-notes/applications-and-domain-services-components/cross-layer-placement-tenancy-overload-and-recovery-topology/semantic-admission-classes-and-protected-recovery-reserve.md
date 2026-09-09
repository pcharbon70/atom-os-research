---
title: "Semantic admission classes and protected recovery reserve"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Semantic admission classes and protected recovery reserve

This study decomposes [Cross-layer placement, tenancy, overload, and recovery topology](../cross-layer-placement-tenancy-overload-and-recovery-topology.md).

Research question: Which work may be rejected under overload without abandoning an accepted obligation?

## Research basis and status

SEDA exposes staged queues and admission control; its evaluation also documents missed latency targets and initially unbounded queues. [1](../../../30-sources/welsh-et-al-2001-seda.md).

DAGOR propagates admission priorities through request paths; its empirical policy is neither a hard resource ceiling nor universal fairness. [2](../../../30-sources/zhou-et-al-2018-dagor.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own command importance, useful deadlines and degraded-mode semantics. Layer 4
enforces admission and reserve allocation; kernel and runtime limits remain
authoritative. Distinguish new speculative work, new interactive requests, accepted
invariant work and safety or reconciliation activity.

### Admission, transitions and completion

Estimate and reserve bounded completion cost before accepting responsibility,
including durable metadata, outbox capacity and teardown. Propagate authenticated
admission class through child requests. If capacity is insufficient, return
pre-admission refusal or an explicitly bounded queued mode. After acceptance, finish
or preserve a queryable pending owner; ordinary load cannot consume the reserve
needed to reconcile it.

### Failure and adversarial behavior

A high-priority header supplied by the caller can steal recovery capacity. Retry
chains can amplify downstream load and restart can reset naïve counters. Queue delay
alone cannot bound memory or device work. Degraded modes must state freshness and
functionality instead of silently dropping accepted requests.

### Alternatives and unresolved tradeoffs

Feedback controllers adapt to load but are not hard ceilings or universal fairness
proofs. Static limits are simpler but may waste capacity. Combine measurable
semantic admission with enforced budgets and an independent recovery path; qualify
fairness and latency per workload.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Flood speculative requests while pending effects require reconciliation; recovery progresses within its admitted reserve.
- Restart clients and services during retry exhaustion; budget lineage and priority authorization must not reset.

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

1. [SEDA](../../../30-sources/welsh-et-al-2001-seda.md).
2. [DAGOR](../../../30-sources/zhou-et-al-2018-dagor.md).
