---
title: "Provider registration, negotiation, and representation contracts"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - multimodal-interaction
  - semantic-ui
  - visual-computing
aliases: []
---

# Provider registration, negotiation, and representation contracts

This study decomposes [Plural representations and cross-view consistency](../plural-representations-and-cross-view-consistency.md).

Research question: How can independently implemented visual, textual,
programmatic, voice, assistive, and remote providers declare what they preserve
and what authority they require?

## Research basis and status

CAMELEON separates task/domain, abstract, concrete, and final presentation.
SUPPLE evaluates model-driven adaptation, while AccessKit demonstrates one
cross-platform semantic core with multiple adapters and explicit best-effort
limits. [1](../../../30-sources/calvary-et-al-2003-multi-target-user-interface-framework.md)
[2](../../../30-sources/gajos-et-al-2010-personalized-user-interfaces-supple.md)
[3](../../../30-sources/accesskit-project-2026-architecture-and-engineering.md)

The Atom provider contract and registry are not implemented.

## Development

### Owned state and trust boundary

An offer declares provider identity and digest, accepted object/schema and
semantic profiles, representation class, required observations/actions,
editable fields, loss model, resource profile, locale/modality support,
fallback behavior, and conformance evidence. Registry presence grants no
project access.

### Admission, transitions, and completion

Negotiation intersects project type, user needs, device/modality, policy,
protocol versions, and resource ceilings. Binding derives only the declared
facets and records a generation. Replacement or uninstallation withdraws the
binding while durable model/project truth remains interpretable through
fallback semantics.

### Failure and adversarial behavior

Providers can overclaim equivalence, hide lossy transforms, request excessive
authority, squat on generic roles, or make data hostage. Independent
conformance, explicit loss descriptors, human-readable authority diffs,
generation fencing, and export requirements limit the risk.

### Alternatives and unresolved tradeoffs

One canonical toolkit improves consistency but excludes new modalities and
media. Completely ad hoc providers destroy interoperability. A versioned
semantic core plus negotiated extensions and task profiles is preferred; trust
ranking and evidence freshness remain open.

## Verification obligations

- Admit two independent providers for one object type; replace and uninstall
  each without data loss or authority residue.
- Lie about protocol, resource, modality, and round-trip support; conformance
  must detect unsupported claims before destructive editing.
- Compare granted facets with declared requirements and attempt hidden
  capability return or cross-project reuse.

## Connections

- [Internal-service index](README.md) — plural-view decomposition.
- [Project provider binding](../user-owned-project-graph-and-composition/provider-discovery-binding-and-schema-negotiation.md) — durable attachment.
- [Semantic vocabulary](../semantics-first-accessible-ui-protocol/semantic-vocabulary-identity-and-localization.md) — negotiated core.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — provenance.

## Sources

1. [CAMELEON framework](../../../30-sources/calvary-et-al-2003-multi-target-user-interface-framework.md).
2. [SUPPLE](../../../30-sources/gajos-et-al-2010-personalized-user-interfaces-supple.md).
3. [AccessKit architecture](../../../30-sources/accesskit-project-2026-architecture-and-engineering.md).
