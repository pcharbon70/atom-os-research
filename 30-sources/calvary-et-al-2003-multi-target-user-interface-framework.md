---
title: "A Unifying Reference Framework for Multi-Target User Interfaces"
kind: source
created: "2026-09-04"
authors:
  - "Gaëlle Calvary"
  - "Joëlle Coutaz"
  - "David Thevenin"
  - "Quentin Limbourg"
  - "Laurent Bouillon"
  - "Jean Vanderdonckt"
published: "2003-06"
citation_key: "calvary-et-al-2003-multi-target-user-interface-framework"
container: "Interacting with Computers 15(3)"
edition: null
isbn: null
doi: "10.1016/S0953-5438(03)00010-9"
url: "https://doi.org/10.1016/S0953-5438(03)00010-9"
accessed: "2026-09-04"
tags:
  - adaptive-ui
  - model-based-ui
  - multimodal-interaction
  - user-interface
aliases:
  - "CAMELEON reference framework"
---

# A Unifying Reference Framework for Multi-Target User Interfaces

## Reference

Gaëlle Calvary, Joëlle Coutaz, David Thevenin, Quentin Limbourg, Laurent
Bouillon, and Jean Vanderdonckt. “[A Unifying Reference Framework for
Multi-Target User
Interfaces](https://doi.org/10.1016/S0953-5438(03)00010-9).” *Interacting
with Computers* 15(3), pages 289–308, June 2003. The [author
copy](https://iihm.imag.fr/publs/2003/Calvary-IwC2003.pdf) was checked.

## Contribution

The CAMELEON framework classifies user-interface development and run-time
adaptation across task/domain models, abstract user interfaces, concrete user
interfaces, and final interfaces. It defines context through user, platform,
and environment and distinguishes transformations, mappings, and the points at
which context change is handled.

## Method

The paper synthesizes prior model-based and multi-target UI work into a common
reference vocabulary and applies the framework to classify systems. It is a
conceptual framework rather than an implementation benchmark or controlled
user study.

## Findings

- Device-independent intent and domain concepts can be separated from
  modality-specific interaction and final rendering.
- Adaptation can occur at several abstraction levels and at design time,
  installation, session start, or run time; those choices have different
  continuity and implementation costs.
- Reverse translation and preservation of design rationale are as important
  as forward generation when a user edits a concrete representation.
- “Plasticity” is not merely rescaling pixels: user, platform, and physical
  environment can require different interaction techniques.

## Relevance

The framework helps Atom OS split durable domain actors, semantic interaction
records, concrete renderer plans, and transient surfaces. It also provides a
taxonomy for deciding whether a change belongs in the model, semantic view,
renderer, or user preference service.

## Limits

The framework does not prescribe a consistency algorithm, authority model,
distributed state protocol, resource budget, or failure recovery mechanism.
Atom OS needs those operational contracts rather than treating model
transformations as inherently safe or reversible.

## Derived work

- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
