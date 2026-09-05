---
title: "Functional Reactive Animation"
kind: source
created: "2026-09-04"
authors:
  - "Conal Elliott"
  - "Paul Hudak"
published: "1997"
citation_key: "elliott-hudak-1997-functional-reactive-animation"
container: "Proceedings of the Second ACM SIGPLAN International Conference on Functional Programming (ICFP '97)"
edition: null
isbn: null
doi: "10.1145/258948.258973"
url: "https://doi.org/10.1145/258948.258973"
accessed: "2026-09-04"
tags:
  - declarative-ui
  - functional-reactive-programming
  - interaction
  - semantics
aliases:
  - "Fran"
---

# Functional Reactive Animation

## Reference

Conal Elliott and Paul Hudak. “[Functional Reactive
Animation](https://doi.org/10.1145/258948.258973).” *Proceedings of ICFP
'97*, pages 263–273, 1997. An [archived author
copy](https://users.cs.northwestern.edu/~robby/courses/395-495-2009-winter/fran.pdf)
was read.

## Contribution

The paper introduces Fran, a typed compositional model in which behaviors are
time-varying values and events are first-class occurrences carrying data.
Interactive multimedia is expressed declaratively in terms of what changes
over time rather than as imperative repaint and input-handler procedures.

## Method

Elliott and Hudak define a denotational semantics, including a domain for time,
derive polymorphic behavior and event operators, describe interval-analysis
event detection, implement the model in Hugs, and present animation and
physical-simulation examples. The examples demonstrate expressive and
semantic feasibility; they are not a modern latency, memory, accessibility, or
fault-recovery evaluation.

## Findings

- Images, sounds, geometry, and ordinary values can share a common typed model
  of time-varying behavior while retaining media-specific operations.
- Events and behavior switching are compositional, which separates the
  semantic relationship among values from manual frame-update sequencing.
- A formal, implementation-independent meaning can guide execution strategy
  and reasoning about reactive presentation.
- Implicit continuous time and general event detection create substantial
  implementation challenges; the elegant semantic model is not itself a
  resource bound.

## Relevance

Fran supports a narrow Atom OS conclusion: disposable presentation should be a
declarative projection of versioned meaning, and input events should be typed
data rather than callbacks with ambient authority. It does not imply that the
durable actor graph should be an FRP network or that effects can be rolled back
by recomputing a view.

## Limits

The model predates GPU compositors, platform accessibility APIs, mutually
distrustful clients, actor supervision, and distributed replicas. Continuous
semantics can also hide operational work unless an implementation supplies
explicit scheduling, backpressure, sampling, and memory bounds.

## Derived work

- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
