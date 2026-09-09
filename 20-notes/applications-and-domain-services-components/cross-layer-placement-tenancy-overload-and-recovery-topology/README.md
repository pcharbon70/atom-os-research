---
title: "Cross-layer placement, tenancy, overload, and recovery topology: internal services"
kind: map
created: "2026-09-09"
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
  - directory-index
aliases: []
---

# Cross-layer placement, tenancy, overload, and recovery topology: internal services

## Purpose

Map semantic ownership onto enforceable trust, tenant, resource and recovery
boundaries.

This directory decomposes [Cross-layer placement, tenancy, overload, and recovery topology](../cross-layer-placement-tenancy-overload-and-recovery-topology.md)
into 4 separately reviewable research responsibilities. These are service
contracts, not a mandate for one actor, protected domain or deployable package
per document.

## What belongs here

Keep owned state, authority boundaries, transition and completion semantics,
failure cases, alternatives and falsifiers here. Primary findings remain in
source notes; the [session manifest](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md)
records exact provenance. This is full-system architecture research, not
implementation delivery or a proof-of-concept gate.

Layer 5 declares domain meaning and required evidence. Layer 4 supplies generic
policy and durability services; Layers 2–3 enforce protection, resources and
managed execution. Proposed guarantees remain conditional on those contracts.

## Index

### Subdirectories

- None yet.

### Documents

- [Placement contracts and independent boundary selection](placement-contracts-and-independent-boundary-selection.md) — Which application boundaries should coincide, and which should remain separate?
- [Business-tenant bindings and realm reassignment](business-tenant-bindings-and-realm-reassignment.md) — How does a domain partition retain identity while its authenticated security binding changes?
- [Semantic admission classes and protected recovery reserve](semantic-admission-classes-and-protected-recovery-reserve.md) — Which work may be rejected under overload without abandoning an accepted obligation?
- [Recovery topology and responsibility handoff](recovery-topology-and-responsibility-handoff.md) — Can each failed component be replaced without depending on itself for authority or outcome truth?

## Maintaining this index

Inventory every direct child and update the parent report, component index and
relevant map when a responsibility changes. Keep counts needs-based: split only
where distinct state, trust or completion obligations justify it. Preserve
unexecuted tests and unresolved choices as such.

Continue through the [application topic map](../../../10-maps/applications-and-domain-services.md)
and [open inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md);
neither literature coverage nor this decomposition closes architectural
qualification.
