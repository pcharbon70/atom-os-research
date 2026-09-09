---
title: "Offline collaboration, replication, and conflict semantics: internal services"
kind: map
created: "2026-09-09"
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
  - directory-index
aliases: []
---

# Offline collaboration, replication, and conflict semantics: internal services

## Purpose

Separate convergent content, authority admission, scarce rights, schema meaning and
safe history collection.

This directory decomposes [Offline collaboration, replication, and conflict semantics](../offline-collaboration-replication-and-conflict-semantics.md)
into 5 separately reviewable research responsibilities. These are service
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

- [Replicated-type specifications and intent preservation](replicated-type-specifications-and-intent-preservation.md) — Which concurrent edits should be equivalent, and which must remain visible conflicts?
- [Offline grants, provenance, and reconnect admission](offline-grants-provenance-and-reconnect-admission.md) — What authority does a disconnected device have, and what can revocation mean while it is absent?
- [Offline scarce rights and online effect gates](offline-scarce-rights-and-online-effect-gates.md) — Which offline changes can commit scarce resources, and which must remain proposals?
- [Schema lenses and concurrent semantic translation](schema-lenses-and-concurrent-semantic-translation.md) — Can old and new offline clients collaborate without silently changing the meaning of edits?
- [Causal frontiers, tombstones, and peer retirement](causal-frontiers-tombstones-and-peer-retirement.md) — When can collaborative history be collected without resurrecting deleted content?

## Maintaining this index

Inventory every direct child and update the parent report, component index and
relevant map when a responsibility changes. Keep counts needs-based: split only
where distinct state, trust or completion obligations justify it. Preserve
unexecuted tests and unresolved choices as such.

Continue through the [application topic map](../../../10-maps/applications-and-domain-services.md)
and [open inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md);
neither literature coverage nor this decomposition closes architectural
qualification.
