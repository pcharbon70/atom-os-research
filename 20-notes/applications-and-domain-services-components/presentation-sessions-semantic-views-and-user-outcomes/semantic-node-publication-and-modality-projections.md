---
title: "Semantic-node publication and modality projections"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Semantic-node publication and modality projections

This study decomposes [Presentation sessions, semantic views, and user outcomes](../presentation-sessions-semantic-views-and-user-outcomes.md).

Research question: What common semantics should different views preserve without requiring identical trees?

## Research basis and status

WAI-ARIA defines semantic roles, states and relationships; vocabulary conformance alone does not establish usable or authorized interaction. [1](../../../30-sources/w3c-2023-wai-aria-1-2.md).

The early Elm paper demonstrates asynchronous view composition, not durable application outcomes or protected presentation. [2](../../../30-sources/czaplicki-chong-2013-asynchronous-frp-guis.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own stable logical object references, permitted properties, semantic roles and
states, available action descriptions and source frontiers. A visual tree,
accessibility tree, voice summary and text view are projections, not copies of the
domain's authority. Redaction happens before data crosses into a presentation that
lacks read permission.

### Admission, transitions and completion

Build a bounded semantic publication under the caller's current read profile. Map
logical relationships and actions to each modality while preserving permitted
meaning. Localized labels and grouping can differ; action identity and resulting
domain postconditions cannot. Large collections expose explicit virtualized windows
and completeness rather than implying unseen nodes do not exist.

### Failure and adversarial behavior

A renderer may lie about displayed content even when the model is correct. Trusted
confirmation for consequential work must bind the exact action and relevant facts
through a protected path. Accessibility output can leak hidden fields if generated
from an unrestricted model instead of an authorized semantic projection.

### Alternatives and unresolved tradeoffs

A universal literal tree simplifies adapters but often fits one modality poorly.
Independent widget-owned models offer flexibility at the cost of divergent truth.
Research semantic equivalence at the action and outcome level, with
modality-specific usability evidence.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Execute equivalent permitted actions through visual and nonvisual adapters and compare domain outcomes.
- Request hidden and off-screen relationships with a restricted facet; unpublished sensitive properties must remain absent.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Operation identity and honest outcome ledgers](../typed-commands-queries-events-and-protocol-contracts/operation-identity-and-honest-outcome-ledgers.md) — a cross-component contract this service must preserve.
- [Effect reconciliation and unqueryable repair](../external-effects-ports-adapters-and-reconciliation/effect-reconciliation-and-unqueryable-repair.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [WAI-ARIA 1.2](../../../30-sources/w3c-2023-wai-aria-1-2.md).
2. [Asynchronous FRP](../../../30-sources/czaplicki-chong-2013-asynchronous-frp-guis.md).
