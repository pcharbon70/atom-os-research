---
title: "Application manifest, composition, and authority envelope: internal services"
kind: map
created: "2026-09-09"
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
  - directory-index
aliases: []
---

# Application manifest, composition, and authority envelope: internal services

## Purpose

Separate declarative application requirements from recipient-specific authority
installation and semantic readiness.

This directory decomposes [Application manifest, composition, and authority envelope](../application-manifest-composition-and-authority-envelope.md)
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

- [Manifest contract graph and dependency classes](manifest-contract-graph-and-dependency-classes.md) — Which application requirements must be closed before a generation can be composed?
- [Recipient-bound composition and installer retirement](recipient-bound-composition-and-installer-retirement.md) — How can composition wire the whole application without retaining the union of its powers?
- [Configuration snapshots and secret lease bindings](configuration-snapshots-and-secret-lease-bindings.md) — What configuration can be retained durably without retaining live authority or secret values?
- [Semantic readiness and degraded lifecycle evidence](semantic-readiness-and-degraded-lifecycle-evidence.md) — When is an application ready to accept responsibility rather than merely running?

## Maintaining this index

Inventory every direct child and update the parent report, component index and
relevant map when a responsibility changes. Keep counts needs-based: split only
where distinct state, trust or completion obligations justify it. Preserve
unexecuted tests and unresolved choices as such.

Continue through the [application topic map](../../../10-maps/applications-and-domain-services.md)
and [open inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md);
neither literature coverage nor this decomposition closes architectural
qualification.
