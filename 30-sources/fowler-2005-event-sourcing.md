---
title: "Event Sourcing"
kind: source
created: "2026-09-05"
authors:
  - "Martin Fowler"
published: "2005-12-12"
citation_key: "fowler-2005-event-sourcing"
container: "martinfowler.com"
edition: null
isbn: null
doi: null
url: "https://www.martinfowler.com/eaaDev/EventSourcing.html"
accessed: "2026-09-05"
tags:
  - event-sourcing
  - practitioner-literature
  - software-architecture
aliases:
  - "Fowler event sourcing article"
---

# Event Sourcing

## Reference

Martin Fowler. “[Event Sourcing](https://www.martinfowler.com/eaaDev/EventSourcing.html).”
12 December 2005.

## Research question or contribution

The article describes an application pattern in which a sequence of events is
the authoritative record and current state is reconstructed by replay.

## Method

This is practitioner design writing with worked examples, not peer-reviewed
empirical research. The page itself describes the material as an old, unedited
draft; it was used for the historical pattern definition and then checked
against later empirical evidence.

## Findings

- Replay can rebuild state and new projections, support temporal queries, and
  aid diagnosis.
- External systems and nondeterministic queries require special treatment so
  replay does not repeat real-world effects or rewrite what was known then.
- Correctness depends on retaining interpretable history and separating event
  application from effect execution.

## Relevance

The article gives useful vocabulary for journals and projections. The Atom OS
recommendation is qualified by the later empirical finding that event
evolution, projection rebuild, privacy, tooling, and expertise are substantial
costs.

## Limits

It is not maintained as a formal pattern specification, benchmark, or proof.
Its examples do not define capability security, distributed outcomes, erasure,
or rolling schema compatibility.

## Derived work

- [Durable state, journals, snapshots, and projections](../20-notes/applications-and-domain-services-components/durable-state-journals-snapshots-and-projections.md)
