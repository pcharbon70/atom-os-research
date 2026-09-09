---
title: "Invariants, transactions, and concurrency policy: internal services"
kind: map
created: "2026-09-09"
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
  - directory-index
aliases: []
---

# Invariants, transactions, and concurrency policy: internal services

## Purpose

Choose the synchronization mechanism from complete domain properties, not from the
presence of actors.

This directory decomposes [Invariants, transactions, and concurrency policy](../invariants-transactions-and-concurrency-policy.md)
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

- [Invariant catalog and coordination selection](invariant-catalog-and-coordination-selection.md) — Which properties actually require coordination, and which can survive independent decisions?
- [Aggregate commit bundles and revision validation](aggregate-commit-bundles-and-revision-validation.md) — What must commit together for one accepted domain transition to be recoverable?
- [Escrow rights conservation and transfer](escrow-rights-conservation-and-transfer.md) — When can a replica spend scarce quantity offline without exceeding the global bound?
- [Cross-aggregate coordination and visible intermediate states](cross-aggregate-coordination-and-visible-intermediate-states.md) — How should a domain choose between a true atomic transaction and a long-running workflow?

## Maintaining this index

Inventory every direct child and update the parent report, component index and
relevant map when a responsibility changes. Keep counts needs-based: split only
where distinct state, trust or completion obligations justify it. Preserve
unexecuted tests and unresolved choices as such.

Continue through the [application topic map](../../../10-maps/applications-and-domain-services.md)
and [open inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md);
neither literature coverage nor this decomposition closes architectural
qualification.
