---
title: "Durable state, journals, snapshots, and projections: internal services"
kind: map
created: "2026-09-09"
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
  - directory-index
aliases: []
---

# Durable state, journals, snapshots, and projections: internal services

## Purpose

Separate authoritative persistence choice, deterministic history, checkpoint
promotion, derived views and retention.

This directory decomposes [Durable state, journals, snapshots, and projections](../durable-state-journals-snapshots-and-projections.md)
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

- [Authoritative state profiles and persistence boundaries](authoritative-state-profiles-and-persistence-boundaries.md) — Which stored representation is authoritative for each domain object?
- [Deterministic event reducers and replay firewalls](deterministic-event-reducers-and-replay-firewalls.md) — How can history reconstruct truth without repeating real-world actions?
- [Snapshot validation and authority promotion](snapshot-validation-and-authority-promotion.md) — When is a checkpoint a disposable cache, and when has pruning made it authoritative?
- [Projection checkpoints, rebuild, and publication](projection-checkpoints-rebuild-and-publication.md) — How can a derived view be rebuilt and switched without claiming false freshness?
- [Retention, erasure, and recovery dependency closure](retention-erasure-and-recovery-dependency-closure.md) — What must remain reachable before history, outcomes or private data can be collected?

## Maintaining this index

Inventory every direct child and update the parent report, component index and
relevant map when a responsibility changes. Keep counts needs-based: split only
where distinct state, trust or completion obligations justify it. Preserve
unexecuted tests and unresolved choices as such.

Continue through the [application topic map](../../../10-maps/applications-and-domain-services.md)
and [open inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md);
neither literature coverage nor this decomposition closes architectural
qualification.
