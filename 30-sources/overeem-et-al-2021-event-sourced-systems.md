---
title: "An Empirical Characterization of Event Sourced Systems and Their Schema Evolution: Lessons from Industry"
kind: source
created: "2026-09-05"
authors:
  - "Michiel Overeem"
  - "Marten Spoor"
  - "Slinger Jansen"
  - "Sjaak Brinkkemper"
published: 2021
citation_key: "overeem-et-al-2021-event-sourced-systems"
container: "Journal of Systems and Software 178"
edition: null
isbn: null
doi: "10.1016/j.jss.2021.110970"
url: "https://doi.org/10.1016/j.jss.2021.110970"
accessed: "2026-09-05"
tags:
  - event-sourcing
  - empirical-software-engineering
  - schema-evolution
aliases:
  - "Event sourcing lessons from industry"
---

# An Empirical Characterization of Event Sourced Systems and Their Schema Evolution: Lessons from Industry

## Reference

Michiel Overeem, Marten Spoor, Slinger Jansen, and Sjaak Brinkkemper. “[An
Empirical Characterization of Event Sourced Systems and Their Schema Evolution:
Lessons from Industry](https://doi.org/10.1016/j.jss.2021.110970).” *Journal of
Systems and Software* 178, 2021, article 110970.

## Research question or contribution

The study characterizes why practitioners use event sourcing, which
architectural patterns accompany it, which difficulties they encounter, and
how they evolve event schemas.

## Method

The authors use constructivist grounded theory based on 25 engineers and 19
event-sourced systems.

## Findings

- Participants reported audit/history and flexibility benefits but also event
  evolution, steep learning, tooling, projection rebuild, and privacy
  challenges.
- Observed evolution tactics included versioned events, weak schemas,
  upcasting, in-place transformation, and copy-and-transform.
- Event sourcing often interacts with CQRS and event-driven architecture but
  the patterns are not identical requirements.

## Relevance

Atom OS should make event sourcing an opt-in domain policy, never the universal
Layer 5 store. A selected context must own versioning, replay fixtures,
projection rebuild, retention, and privacy/erasure policy explicitly.

## Limits

The evidence is qualitative and self-reported, with a modest sample. It does
not establish causal performance or reliability benefits, a universal event
model, or Atom OS suitability.

## Derived work

- [Durable state, journals, snapshots, and projections](../20-notes/applications-and-domain-services-components/durable-state-journals-snapshots-and-projections.md)
- [Application evolution, schema compatibility, and migration](../20-notes/applications-and-domain-services-components/application-evolution-schema-compatibility-and-migration.md)
- [2026-09-05 applications deep dive](../50-journal/2026-09-05-applications-and-domain-services-deep-dive.md)
