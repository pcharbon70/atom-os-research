---
title: "Manifest contract graph and dependency classes"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Manifest contract graph and dependency classes

This study decomposes [Application manifest, composition, and authority envelope](../application-manifest-composition-and-authority-envelope.md).

Research question: Which application requirements must be closed before a generation can be composed?

## Research basis and status

TOSCA separates typed requirements, graph resolution and lifecycle actions; a graph does not establish authority or truthful readiness. [1](../../../30-sources/oasis-2025-tosca-2.md).

NixOS separates immutable configuration generations from mutable activation effects; selecting an old generation does not undo domain state. [2](../../../30-sources/dolstra-et-al-2008-nixos.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own an immutable graph of context IDs, artifact digests, provided and required
ports, schema profiles, dependency classes and resource requests. A graph edge
states whether a dependency is needed during preparation, continuing service, effect
dispatch or optional enhancement. Names designate candidates; they carry no
authority.

### Admission, transitions and completion

Normalize and bound the document before interpretation. Check unique IDs, version
intersections, mandatory imports, cycles among actual ordering edges and declared
degraded alternatives. Produce a graph digest and unresolved obligations for the
Layer 4 resolver. A successful graph check is permission to request preparation, not
to publish routes or invoke a device. Record the resolved provider generations
separately so replacing a provider invalidates only dependent evidence.

### Failure and adversarial behavior

A malicious manifest can force excessive nesting, combinatorial version search or a
readiness cycle. Bound nodes, alternatives and traversal work. Reject an unresolved
mandatory port instead of quietly binding a global default. A cycle of optional
discovery references need not be a startup cycle; the edge semantics decide.

### Alternatives and unresolved tradeoffs

A flat ordered startup list is cheaper for a closed application but obscures
continuing dependencies. A general cloud orchestration language adds unnecessary
interpretation and extension authority. Research a small typed profile, not a
universal deployment language.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Construct graphs with optional discovery cycles and mandatory readiness cycles; accept only the former when no hidden ordering remains.
- Change one provider generation after validation; dependent readiness evidence must become stale without broadening any import.

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
2. [NixOS](../../../30-sources/dolstra-et-al-2008-nixos.md).
