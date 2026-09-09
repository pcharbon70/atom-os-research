---
title: "Extension points, plugins, and live-tooling confinement: internal services"
kind: map
created: "2026-09-09"
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
  - directory-index
aliases: []
---

# Extension points, plugins, and live-tooling confinement: internal services

## Purpose

Distinguish extension admission, proposal validation, live-tool powers and
generation retirement.

This directory decomposes [Extension points, plugins, and live-tooling confinement](../extension-points-plugins-and-live-tooling-confinement.md)
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

- [Extension descriptors and risk-selected hosts](extension-descriptors-and-risk-selected-hosts.md) — Which execution boundary is justified for a particular extension?
- [Extension invocation and domain-proposal validation](extension-invocation-and-domain-proposal-validation.md) — How can extensions influence behavior without becoming aggregate writers?
- [Live-tool facets and staged change authority](live-tool-facets-and-staged-change-authority.md) — How can inspection and live programming coexist without a universal debugger capability?
- [Extension state, update, revocation, and uninstall](extension-state-update-revocation-and-uninstall.md) — What survives an extension replacement, and what does revocation actually stop?

## Maintaining this index

Inventory every direct child and update the parent report, component index and
relevant map when a responsibility changes. Keep counts needs-based: split only
where distinct state, trust or completion obligations justify it. Preserve
unexecuted tests and unresolved choices as such.

Continue through the [application topic map](../../../10-maps/applications-and-domain-services.md)
and [open inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md);
neither literature coverage nor this decomposition closes architectural
qualification.
