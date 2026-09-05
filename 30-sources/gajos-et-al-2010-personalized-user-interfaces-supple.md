---
title: "Automatically Generating Personalized User Interfaces with SUPPLE"
kind: source
created: "2026-09-04"
authors:
  - "Krzysztof Z. Gajos"
  - "Daniel S. Weld"
  - "Jacob O. Wobbrock"
published: "2010-08"
citation_key: "gajos-et-al-2010-personalized-user-interfaces-supple"
container: "Artificial Intelligence 174(12-13)"
edition: null
isbn: null
doi: "10.1016/j.artint.2010.05.005"
url: "https://doi.org/10.1016/j.artint.2010.05.005"
accessed: "2026-09-04"
tags:
  - accessibility
  - adaptive-ui
  - model-based-ui
  - personalization
aliases:
  - "SUPPLE personalized UI generation"
---

# Automatically Generating Personalized User Interfaces with SUPPLE

## Reference

Krzysztof Z. Gajos, Daniel S. Weld, and Jacob O. Wobbrock. “[Automatically
Generating Personalized User Interfaces with
SUPPLE](https://doi.org/10.1016/j.artint.2010.05.005).” *Artificial
Intelligence* 174(12–13), pages 910–950, August 2010. The [author
copy](https://faculty.washington.edu/wobbrock/pubs/aij-10.pdf) was read.

## Contribution

SUPPLE represents an interface independently of a concrete widget layout and
formulates rendering for a user, device, task distribution, and abilities as
an optimization problem. It demonstrates run-time generation and adaptation,
including ability-based alternatives for people with motor impairments.

## Method

The paper formalizes the generation problem, analyzes the search space,
implements optimizers and several cost functions, measures solution time, and
reports comparative user studies. For a specified class of cost functions,
many exact solutions complete in under a second; the worst reported case is
over a minute. The participant studies compare generated alternatives with
manufacturer defaults for particular tasks and motor abilities.

## Findings

- A declarative functional specification can support several concrete
  interfaces without making any one layout authoritative.
- User traces, task frequency, device constraints, preferences, and measured
  ability can change the selected representation.
- Automatic alternatives improved speed, accuracy, and satisfaction for the
  studied users with motor impairments relative to defaults.
- Generation is computationally feasible in the studied space, but stability,
  predictability, and human designer overrides remain important.
- Optimization criteria embody policy and can produce poor results when the
  model, cost function, or context estimate is wrong.

## Relevance

SUPPLE is experimental support for deriving multiple accessible presentations
from shared action and data semantics. Atom OS should borrow the separation
between semantic task model and renderer, not place an optimizer in the
trusted path or promise that automatic adaptation replaces designed views.

## Limits

The system's task and widget model is narrower than a general dynamic medium.
The studies do not establish long-term learnability, cross-view semantic
equivalence, capability safety, recovery behavior, or suitability for
latency-critical whole-desktop generation.

## Derived work

- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
