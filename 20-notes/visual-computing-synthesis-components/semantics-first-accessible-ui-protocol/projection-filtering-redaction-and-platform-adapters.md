---
title: "Projection filtering, redaction, and platform adapters"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - accessibility
  - privacy
  - semantic-ui
aliases: []
---

# Projection filtering, redaction, and platform adapters

This study decomposes [Semantics-first accessible UI protocol](../semantics-first-accessible-ui-protocol.md).

Research question: How can one semantic authority produce structurally
different visual, assistive, automation, and remote projections without
leaking excluded meaning?

## Research basis and status

Core-AAM documents platform-specific mappings; AccessKit implements adapters
and explicitly calls them best effort. Chromium caches renderer semantics in a
more trusted process for platform exposure. SUPPLE shows useful adaptive
generation within a bounded model and population.
[1](../../../30-sources/w3c-2026-core-accessibility-api-mappings-1-2.md)
[2](../../../30-sources/accesskit-project-2026-architecture-and-engineering.md)
[3](../../../30-sources/chromium-project-2026-multiprocess-graphics-and-accessibility.md)
[4](../../../30-sources/gajos-et-al-2010-personalized-user-interfaces-supple.md)

Cross-platform equivalence and noninterference remain unproved.

## Development

### Owned state and trust boundary

The projection service owns a consumer-specific disclosure policy, semantic
profile, retained filtered graph, and adapter generation. Platform adapters
own only ephemeral handles and event translation. They do not gain unfiltered
model access merely because the platform accessibility API is trusted locally.

### Admission, transitions, and completion

Filter a complete source revision into a self-consistent subgraph before
adapter mapping. Remove or rewrite relations, counts, indices, geometry,
labels, timing channels, and action descriptors that reveal excluded nodes.
Adapter loss or vocabulary mismatch reports degradation and resynchronizes from
the filtered authority.

### Failure and adversarial behavior

Redacted siblings can leak through positions, live-region events, focus jumps,
or response time. Platform callbacks may be reentrant or request stale node
handles. Stable filtered identities, padding/batching where justified, strict
callback bounds, and current-generation checks constrain the boundary.

### Alternatives and unresolved tradeoffs

Filtering after platform mapping is easy but loses semantic context needed for
safe redaction. One universal tree avoids adapter differences but mismatches
platform conventions. Pre-mapping semantic filtering plus measured adapter
conformance is preferred; acceptable structural leakage needs a threat profile.

## Verification obligations

- Attempt to infer redacted objects through sibling counts, order, relations,
  geometry, events, focus, timing, and error messages.
- Compare essential task reachability through AT-SPI, UIA, visual, remote, and
  debug adapters despite differing tree shapes.
- Crash and restart adapters during updates; stale platform handles must never
  address a new semantic node.

## Connections

- [Internal-service index](README.md) — adapter boundary.
- [Observational equivalence](../plural-representations-and-cross-view-consistency/observational-equivalence-task-outcomes-and-conformance.md) — task-level comparison.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — source manifest.

## Sources

1. [Core-AAM 1.2](../../../30-sources/w3c-2026-core-accessibility-api-mappings-1-2.md).
2. [AccessKit architecture](../../../30-sources/accesskit-project-2026-architecture-and-engineering.md).
3. [Chromium UI process architecture](../../../30-sources/chromium-project-2026-multiprocess-graphics-and-accessibility.md).
4. [SUPPLE](../../../30-sources/gajos-et-al-2010-personalized-user-interfaces-supple.md).
