---
title: "The Dexter Hypertext Reference Model"
kind: source
created: "2026-09-04"
authors:
  - "Frank Halasz"
  - "Mayer Schwartz"
published: "1994-02"
citation_key: "halasz-schwartz-1994-dexter-hypertext-reference-model"
container: "Communications of the ACM 37(2)"
edition: null
isbn: null
doi: "10.1145/175235.175237"
url: "https://doi.org/10.1145/175235.175237"
accessed: "2026-09-04"
tags:
  - hypermedia
  - model-view-separation
  - persistence
  - reference-models
aliases:
  - "Dexter model"
---

# The Dexter Hypertext Reference Model

## Reference

Frank Halasz and Mayer Schwartz. “[The Dexter Hypertext Reference
Model](https://doi.org/10.1145/175235.175237).” *Communications of the ACM*
37(2), pages 30–39, February 1994. The [reference-model
draft](https://media.inhatc.ac.kr/papers/hypermedia/Dexter90.pdf) was checked.

## Contribution

Dexter separates a persistent storage layer of components and links, a
run-time layer of presentation and interaction instantiations, and
within-component media content. Anchors and presentation specifications mediate
between stable stored identity and particular run-time presentations.

## Method

The model was developed through workshops comparing established hypertext
systems, then expressed as a common conceptual and formal reference framework.
It classifies and relates system responsibilities; it does not benchmark a
single implementation or define a security and recovery protocol.

## Findings

- Durable hypermedia structure and transient presentation are distinct layers.
- Stable component identifiers permit run-time instantiations and links to be
  reconstructed without making a displayed object the stored truth.
- Anchoring is an explicit interface problem between media internals and
  cross-component structure.
- Presentation specifications can travel with a component without requiring
  one permanent renderer instance.

## Relevance

Dexter supplies a strong precedent for separating Atom OS project/model state,
semantic anchors, view specifications, and disposable renderer/surface state.
The same split helps a model outlive a desktop process while several providers
offer different views.

## Limits

The reference model predates capability systems, modern accessibility APIs,
GPU composition, actor supervision, and offline multi-writer replication. Its
layers do not by themselves guarantee stable anchors across arbitrary schema
change or safe recovery after ambiguous effects.

## Derived work

- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
