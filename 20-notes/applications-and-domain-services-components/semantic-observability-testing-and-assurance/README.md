---
title: "Semantic observability, testing, and assurance: internal services"
kind: map
created: "2026-09-09"
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
  - directory-index
aliases: []
---

# Semantic observability, testing, and assurance: internal services

## Purpose

Separate user-outcome measurement, disclosure-limited telemetry, executable oracles
and implementation fault evidence.

This directory decomposes [Semantic observability, testing, and assurance](../semantic-observability-testing-and-assurance.md)
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

- [Semantic indicators and outcome populations](semantic-indicators-and-outcome-populations.md) — Which observations distinguish a responsive application from one that actually completed correct work?
- [Telemetry redaction and evidence-channel separation](telemetry-redaction-and-evidence-channel-separation.md) — How can operators diagnose failures without treating diagnostics as authority or exposing domain secrets?
- [Executable domain models and history shrinking](executable-domain-models-and-history-shrinking.md) — What oracle can detect incorrect histories rather than merely compare implementation outputs with themselves?
- [Fault campaigns and model-to-implementation evidence](fault-campaigns-and-model-to-implementation-evidence.md) — How will a plausible architecture be tested against failures its abstract model cannot represent?

## Maintaining this index

Inventory every direct child and update the parent report, component index and
relevant map when a responsibility changes. Keep counts needs-based: split only
where distinct state, trust or completion obligations justify it. Preserve
unexecuted tests and unresolved choices as such.

Continue through the [application topic map](../../../10-maps/applications-and-domain-services.md)
and [open inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md);
neither literature coverage nor this decomposition closes architectural
qualification.
