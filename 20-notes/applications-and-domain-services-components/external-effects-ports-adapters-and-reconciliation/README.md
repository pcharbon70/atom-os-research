---
title: "External effects, ports, adapters, and reconciliation: internal services"
kind: map
created: "2026-09-09"
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
  - directory-index
aliases: []
---

# External effects, ports, adapters, and reconciliation: internal services

## Purpose

Make endpoint participation, intent publication, constrained authority and ambiguous
effect repair explicit.

This directory decomposes [External effects, ports, adapters, and reconciliation](../external-effects-ports-adapters-and-reconciliation.md)
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

- [Semantic port profiles and endpoint qualification](semantic-port-profiles-and-endpoint-qualification.md) — Which completion guarantees can a particular external endpoint honestly support?
- [Outbox, inbox coupling, and deduplication retention](outbox-inbox-coupling-and-deduplication-retention.md) — How do committed domain changes cross a message boundary without losing or duplicating accepted intent?
- [Intent-bound grants and compromised-adapter containment](intent-bound-grants-and-compromised-adapter-containment.md) — What prevents a compromised adapter from using its legitimate access for a different effect?
- [Effect reconciliation and unqueryable repair](effect-reconciliation-and-unqueryable-repair.md) — How can the system preserve useful truth when no component knows whether an effect happened?

## Maintaining this index

Inventory every direct child and update the parent report, component index and
relevant map when a responsibility changes. Keep counts needs-based: split only
where distinct state, trust or completion obligations justify it. Preserve
unexecuted tests and unresolved choices as such.

Continue through the [application topic map](../../../10-maps/applications-and-domain-services.md)
and [open inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md);
neither literature coverage nor this decomposition closes architectural
qualification.
