---
title: "Typed commands, queries, events, and protocol contracts: internal services"
kind: map
created: "2026-09-09"
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
  - directory-index
aliases: []
---

# Typed commands, queries, events, and protocol contracts: internal services

## Purpose

Give decoding, operation outcomes, read frontiers and event histories independent
contracts.

This directory decomposes [Typed commands, queries, events, and protocol contracts](../typed-commands-queries-events-and-protocol-contracts.md)
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

- [Bounded envelope decoding and critical extensions](bounded-envelope-decoding-and-critical-extensions.md) — How does an untrusted message become one unambiguous typed application request?
- [Operation identity and honest outcome ledgers](operation-identity-and-honest-outcome-ledgers.md) — What can a caller safely conclude after a timeout, duplicate request or lost response?
- [Query frontiers, redaction, and continuation tokens](query-frontiers-redaction-and-continuation-tokens.md) — How does a query expose freshness without accidentally granting write authority or leaking another scope?
- [Event publication and behavioral history contracts](event-publication-and-behavioral-history-contracts.md) — When does a message represent an authoritative fact, and what must a compatible consumer preserve?

## Maintaining this index

Inventory every direct child and update the parent report, component index and
relevant map when a responsibility changes. Keep counts needs-based: split only
where distinct state, trust or completion obligations justify it. Preserve
unexecuted tests and unresolved choices as such.

Continue through the [application topic map](../../../10-maps/applications-and-domain-services.md)
and [open inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md);
neither literature coverage nor this decomposition closes architectural
qualification.
