---
title: "Durable domain identity, aggregate actors, and lifecycle: internal services"
kind: map
created: "2026-09-09"
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
  - directory-index
aliases: []
---

# Durable domain identity, aggregate actors, and lifecycle: internal services

## Purpose

Separate durable entity lifetime, recoverable activation, serialized decisions and
retirement.

This directory decomposes [Durable domain identity, aggregate actors, and lifecycle](../durable-domain-identity-aggregate-actors-and-lifecycle.md)
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

- [Domain-reference resolution and lifecycle generations](domain-reference-resolution-and-lifecycle-generations.md) — How does a domain reference survive runtime replacement without reviving a deleted entity?
- [Activation recovery and writer fencing](activation-recovery-and-writer-fencing.md) — What must an aggregate recover before its activation is allowed to write?
- [Aggregate turns and asynchronous continuations](aggregate-turns-and-asynchronous-continuations.md) — How can an aggregate remain responsive without letting reentrant work invalidate its decision?
- [Passivation, tombstones, and retained responsibility](passivation-tombstones-and-retained-responsibility.md) — When may an aggregate release memory or destroy state without losing ownership of unresolved work?

## Maintaining this index

Inventory every direct child and update the parent report, component index and
relevant map when a responsibility changes. Keep counts needs-based: split only
where distinct state, trust or completion obligations justify it. Preserve
unexecuted tests and unresolved choices as such.

Continue through the [application topic map](../../../10-maps/applications-and-domain-services.md)
and [open inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md);
neither literature coverage nor this decomposition closes architectural
qualification.
