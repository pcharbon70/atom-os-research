---
title: "A Cookbook for Using the Model-View-Controller User Interface Paradigm in Smalltalk-80"
kind: source
created: "2026-09-04"
authors:
  - "Glenn E. Krasner"
  - "Stephen T. Pope"
published: 1988
citation_key: "krasner-pope-1988-mvc-smalltalk-80"
container: "Journal of Object-Oriented Programming 1(3)"
edition: null
isbn: null
doi: "10.5555/50757.50759"
url: "https://mvc.givan.se/papers/A_Cookbook_for_Using_the_Model-View-Controller_User_Interface_Paradigm_in_Smalltalk-80.pdf"
accessed: "2026-09-04"
tags:
  - model-view-controller
  - smalltalk
  - user-interface-toolkit
aliases:
  - "Smalltalk-80 MVC Cookbook"
---

# A Cookbook for Using the Model-View-Controller User Interface Paradigm in Smalltalk-80

## Reference

Glenn E. Krasner and Stephen T. Pope. “[A Cookbook for Using the
Model-View-Controller User Interface Paradigm in
Smalltalk-80](https://mvc.givan.se/papers/A_Cookbook_for_Using_the_Model-View-Controller_User_Interface_Paradigm_in_Smalltalk-80.pdf).”
*Journal of Object-Oriented Programming* 1(3), pages 26–49, August/September
1988.

## Contribution

The article documents the mature Smalltalk-80 MVC implementation, including
dependency notification, view composition, controller policies, concrete UI
components, and the construction of standard tools.

## Method

This is a practitioner design guide organized around framework classes,
message flow, examples, and reusable idioms. It explains architecture and
experience but does not compare usability or performance experimentally.

## Findings

- MVC factors domain state, its display, and user interaction. One model may
  have several view/controller pairs, while the model does not directly depend
  on their concrete classes.
- Models broadcast change notifications to dependents so multiple views can
  refresh without embedding presentation logic in domain objects.
- A superview/subview hierarchy provides spatial transforms, clipping, and
  composition.
- Abstract model, view, and controller classes support concrete text, list,
  menu, form, switch, and scheduled-view components.
- Browsers and debuggers are compositions of several cooperating MVC triples,
  rather than indivisible application windows.
- Editors cover text, files, bitmaps, graphs, maps, spreadsheets, animation,
  and other domain-specific representations.
- Strict pluggability produced practical tensions, including class growth and
  movement of some interaction choices into parameterized models.

## Relevance

This source provides a concrete component vocabulary for reconstructible Atom
OS visual services: semantic models, multiple views, input policies,
dependency/change streams, nested layout, and reusable editors. The historical
global object graph should be replaced by versioned actor identities and
failure-aware subscriptions.

## Limits

The article documents one Smalltalk-80 framework, not Kay's whole design and
not a universal definition of MVC. It assumes a shared image and synchronous
message environment, leaving process isolation, asynchronous failure, access
control, and compositor restart unspecified.

## Derived work

- [Alan Kay's Smalltalk visual interface and the modern desktop](../20-notes/alan-kay-smalltalk-visual-interface-and-modern-desktop.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
