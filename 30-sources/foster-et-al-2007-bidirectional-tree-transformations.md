---
title: "Combinators for Bidirectional Tree Transformations: A Linguistic Approach to the View-Update Problem"
kind: source
created: "2026-09-04"
authors:
  - "J. Nathan Foster"
  - "Michael B. Greenwald"
  - "Jonathan T. Moore"
  - "Benjamin C. Pierce"
  - "Alan Schmitt"
published: "2007-05"
citation_key: "foster-et-al-2007-bidirectional-tree-transformations"
container: "ACM Transactions on Programming Languages and Systems 29(3)"
edition: null
isbn: null
doi: "10.1145/1232420.1232424"
url: "https://doi.org/10.1145/1232420.1232424"
accessed: "2026-09-04"
tags:
  - bidirectional-transformations
  - consistency
  - lenses
  - views
aliases:
  - "Tree lenses"
---

# Combinators for Bidirectional Tree Transformations: A Linguistic Approach to the View-Update Problem

## Reference

J. Nathan Foster, Michael B. Greenwald, Jonathan T. Moore, Benjamin C.
Pierce, and Alan Schmitt. “[Combinators for Bidirectional Tree
Transformations: A Linguistic Approach to the View-Update
Problem](https://doi.org/10.1145/1232420.1232424).” *ACM Transactions on
Programming Languages and Systems* 29(3), Article 17, May 2007. The [author
manuscript](https://www.cis.upenn.edu/~bcpierce/papers/newlenses-popl.pdf)
was read.

## Contribution

The paper develops *lenses*: paired transformations that extract a view from a
source and reconcile an updated view back into a source. A type discipline and
combinator language make useful round-trip laws explicit for tree-structured
data and address a central version of the view-update problem.

## Method

The authors define formal semantics and well-behavedness laws, construct a
language of compositional lens combinators, prove properties, implement the
approach in the Harmony synchronizer, and work through tree-transformation
examples.

## Findings

- A forward projection is not enough to support editing through a view; an
  explicit backward reconciliation policy is required.
- Round-trip laws can rule out important classes of silent divergence between
  source and view.
- Complementary information not present in a view must be preserved or
  supplied deliberately when propagating changes backward.
- Some transformations are ambiguous or lossy, so no generic inverse can
  preserve intent without additional policy.
- Combinators can localize consistency reasoning, but concurrency,
  authorization, external effects, and human conflict resolution remain
  outside the core model.

## Relevance

Lenses provide a precise foundation for Atom OS editable alternate views. A
view provider should declare whether it is read-only, command-producing, or a
law-checked bidirectional adapter; it must never infer write authority from the
existence of a projection.

## Limits

The paper concerns tree transformations, not arbitrary actor protocols or
concurrent distributed editing. Its laws establish transformation coherence,
not domain invariant preservation, user intent, access control, or exactly-once
effects. Those checks remain at the model command boundary.

## Derived work

- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
