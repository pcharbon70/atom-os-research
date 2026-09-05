---
title: "Statecharts: A Visual Formalism for Complex Systems"
kind: source
created: "2026-09-05"
authors:
  - "David Harel"
published: 1987
citation_key: "harel-1987-statecharts"
container: "Science of Computer Programming 8(3)"
edition: null
isbn: null
doi: "10.1016/0167-6423(87)90035-9"
url: "https://doi.org/10.1016/0167-6423(87)90035-9"
accessed: "2026-09-05"
tags:
  - formal-modeling
  - state-machines
  - reactive-systems
aliases:
  - "Statecharts"
---

# Statecharts: A Visual Formalism for Complex Systems

## Reference

David Harel. “[Statecharts: A Visual Formalism for Complex
Systems](https://doi.org/10.1016/0167-6423(87)90035-9).” *Science of Computer
Programming* 8, no. 3, 1987, pages 231–274.

## Research question or contribution

Harel extends flat state-transition diagrams with hierarchy, orthogonality,
and communication so that complex reactive behavior can be modeled without an
unmanageable enumeration of states.

## Method

The paper defines the visual formalism and illustrates it on reactive-system
examples. It is foundational modeling work rather than an implementation
benchmark or a security proof.

## Findings

- Hierarchical states factor shared transitions and behavior.
- Orthogonal regions express concurrent state dimensions without flattening
  their Cartesian product in the diagram.
- Events, conditions, and transitions make lifecycle behavior explicit enough
  to analyze and communicate.

## Relevance

Aggregate lifecycles, application readiness, workflows, effects, migration,
and recovery should be specified as explicit state machines. Atom OS must pin
one operational semantics and test it; “drawn as a statechart” is not itself a
runtime guarantee.

## Limits

Statechart variants differ in event ordering and concurrency semantics. The
formalism does not supply persistence, authorization, crash recovery,
distributed consensus, or upgrade compatibility.

## Derived work

- [Durable domain identity, aggregate actors, and lifecycle](../20-notes/applications-and-domain-services-components/durable-domain-identity-aggregate-actors-and-lifecycle.md)
- [Workflows, process managers, timers, and compensation](../20-notes/applications-and-domain-services-components/workflows-process-managers-timers-and-compensation.md)
- [Semantic observability, testing, and assurance](../20-notes/applications-and-domain-services-components/semantic-observability-testing-and-assurance.md)
