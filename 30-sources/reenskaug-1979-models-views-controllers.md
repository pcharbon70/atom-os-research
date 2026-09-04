---
title: "Models-Views-Controllers"
kind: source
created: "2026-09-04"
authors:
  - "Trygve Reenskaug"
published: "1979-12-10"
citation_key: "reenskaug-1979-models-views-controllers"
container: "Xerox PARC technical note"
edition: null
isbn: null
doi: "10.5281/zenodo.3676092"
url: "https://doi.org/10.5281/zenodo.3676092"
accessed: "2026-09-04"
tags:
  - human-computer-interaction
  - model-view-controller
  - smalltalk
aliases:
  - "Original MVC note"
---

# Models-Views-Controllers

## Reference

Trygve Reenskaug. “[Models-Views-Controllers](https://doi.org/10.5281/zenodo.3676092).”
Xerox PARC technical note, 10 December 1979. A [readable
copy](https://mvc.givan.se/papers/Models-Views-Controllers.pdf) was reviewed.

## Contribution

Reenskaug defines the three roles that became MVC in the context of Smalltalk:
a problem-domain model, a visual presentation, and a mediator between human
input and the system. The note is the primary attribution anchor for MVC.

## Method

This short design note states responsibilities and message relationships. It
does not evaluate an implementation or prescribe the later Smalltalk-80 class
hierarchy, much less later web-framework uses of the name.

## Findings

- The model represents knowledge and operations at one problem-domain level;
  it should not be shaped by display and input details.
- A view is a presentation or visual filter over the model. It asks questions
  in the model's own vocabulary.
- A controller connects the user and the system, arranges relevant views, and
  translates user output into messages to those views; a view can update the
  model. A view should not itself understand raw mouse and keyboard operation.
- A temporary editor can be inserted into an interaction when a presentation
  needs modification.
- The separation permits several views of one model and changes to presentation
  or interaction without redefining domain knowledge.

## Relevance

MVC helps explain some Smalltalk components but not Kay's complete vision. For
Atom OS it suggests separating durable semantic actor models, reconstructible
views, and seat/input mediation. Those roles should communicate through typed
actor protocols rather than share unrestricted object references.

## Limits

The note is conceptual and very brief. It does not define notification,
concurrency, persistence, security, failure recovery, or distribution. Modern
uses of “MVC” often assign different responsibilities and must not be projected
back onto this text.

## Derived work

- [Alan Kay's Smalltalk visual interface and the modern desktop](../20-notes/alan-kay-smalltalk-visual-interface-and-modern-desktop.md)
- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
