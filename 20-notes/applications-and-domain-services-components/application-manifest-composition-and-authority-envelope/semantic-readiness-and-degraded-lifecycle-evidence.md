---
title: "Semantic readiness and degraded lifecycle evidence"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Semantic readiness and degraded lifecycle evidence

This study decomposes [Application manifest, composition, and authority envelope](../application-manifest-composition-and-authority-envelope.md).

Research question: When is an application ready to accept responsibility rather than merely running?

## Research basis and status

TOSCA separates typed requirements, graph resolution and lifecycle actions; a graph does not establish authority or truthful readiness. [1](../../../30-sources/oasis-2025-tosca-2.md).

Crash-only design puts authoritative state outside replaceable components; restarting cannot repair every corruption or ambiguous effect. [2](../../../30-sources/candea-fox-2003-crash-only-software.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own readiness predicates over recovered aggregate frontiers, outcome lookup,
compatible workflow definitions, dependency generations and available semantic
modes. Layer 4 owns lifecycle orchestration, hard reserves and route publication.
Application liveness is a separate observation from permission to accept a
particular command class.

### Admission, transitions and completion

Recover state and accepted responsibilities in a private generation. Evaluate
no-effect checks against exact dependency bindings. Return an evidence digest,
validity conditions and a mode such as full, read-only, repair-only or unavailable.
Any dependency transition recomputes affected predicates. Publication is requested
only when Layer 4 can enforce the resulting admission profile.

### Failure and adversarial behavior

An always-green health endpoint can publish a writer before deduplication records
load. A synthetic payment used as a readiness probe can itself create an effect.
Dependency loss after publication must close new affected work while retaining
pending operations for reconciliation; a supervisor restart must not reset this
obligation.

### Alternatives and unresolved tradeoffs

A single Boolean readiness flag works only for applications with one inseparable
service mode. Richer predicates cost more to maintain but expose useful read-only
and repair paths. Degradation must be domain-approved; silently returning stale
results is not recovery.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Start with valid aggregate state but missing outcome metadata; writes must remain closed.
- Remove an effect dependency after admission; prove the pending operation remains queryable while new effectful work is rejected.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Business-tenant bindings and realm reassignment](../cross-layer-placement-tenancy-overload-and-recovery-topology/business-tenant-bindings-and-realm-reassignment.md) — a cross-component contract this service must preserve.
- [Workflow-generation handoff and publication fences](../application-evolution-schema-compatibility-and-migration/workflow-generation-handoff-and-publication-fences.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [TOSCA 2.0](../../../30-sources/oasis-2025-tosca-2.md).
2. [Crash-only software](../../../30-sources/candea-fox-2003-crash-only-software.md).
