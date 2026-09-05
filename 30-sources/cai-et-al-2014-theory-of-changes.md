---
title: "A Theory of Changes for Higher-Order Languages: Incrementalizing Lambda-Calculi by Static Differentiation"
kind: source
created: "2026-09-04"
authors:
  - "Yufei Cai"
  - "Paolo G. Giarrusso"
  - "Tillmann Rendel"
  - "Klaus Ostermann"
published: "2014-06-09"
citation_key: "cai-et-al-2014-theory-of-changes"
container: "Proceedings of the 35th ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI '14)"
edition: null
isbn: "978-1-4503-2784-8"
doi: "10.1145/2594291.2594304"
url: "https://doi.org/10.1145/2594291.2594304"
accessed: "2026-09-04"
tags:
  - incremental-computation
  - programming-languages
  - semantics
  - views
aliases:
  - "Incremental lambda calculus"
---

# A Theory of Changes for Higher-Order Languages: Incrementalizing Lambda-Calculi by Static Differentiation

## Reference

Yufei Cai, Paolo G. Giarrusso, Tillmann Rendel, and Klaus Ostermann. “[A
Theory of Changes for Higher-Order Languages: Incrementalizing Lambda-Calculi
by Static Differentiation](https://doi.org/10.1145/2594291.2594304).”
*Proceedings of PLDI '14*, pages 145–155, June 2014. The [author
copy](https://inc-lc.github.io/resources/pldi14-ilc-author-final.pdf) was read.

## Contribution

The paper derives incremental programs that map input changes to output
changes rather than recomputing the original function. It supplies a general
change interface for base types, a static transformation supporting higher-
order functions, and a mechanized correctness result for a family of typed
lambda calculi.

## Method

The transformation is formalized and proved correct in Agda under specified
primitive-change interfaces. A Scala implementation and case study show
orders-of-magnitude improvement for one nontrivial workload.

## Findings

- Incremental updates are meaningful only relative to an old input, old output,
  and defined change representation.
- Static derivation can preserve the meaning of a computation under the stated
  interfaces while avoiding complete recomputation.
- Performance depends on the function, change structure, maintained base
  state, and ordinary optimization.
- A correct incremental function does not supply message ordering, gap
  recovery, authorization, persistence, or bounded state retention.

## Relevance

Atom OS semantic views may use derived incremental maintenance, but each delta
must name its exact base revision. A receiver that misses, reorders, or rejects
a delta requests a complete bounded snapshot instead of guessing a base.

## Limits

The formal language and case study do not directly model asynchronous actors,
distributed replicas, UI event streams, cyclic graphs, or external effects.
Incrementalization is an optimization beneath the semantic snapshot contract,
not the contract itself.

## Derived work

- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
