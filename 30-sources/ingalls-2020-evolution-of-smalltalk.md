---
title: "The Evolution of Smalltalk: From Smalltalk-72 through Squeak"
kind: source
created: "2026-09-04"
authors:
  - "Daniel Ingalls"
published: "2020-06"
citation_key: "ingalls-2020-evolution-of-smalltalk"
container: "Proceedings of the ACM on Programming Languages 4 (HOPL), Article 85"
edition: null
isbn: null
doi: "10.1145/3386335"
url: "https://doi.org/10.1145/3386335"
accessed: "2026-09-04"
tags:
  - history-of-computing
  - live-programming
  - smalltalk
  - virtual-machines
aliases:
  - "Evolution of Smalltalk"
---

# The Evolution of Smalltalk: From Smalltalk-72 through Squeak

## Reference

Daniel Ingalls. “[The Evolution of Smalltalk: From Smalltalk-72 through
Squeak](https://doi.org/10.1145/3386335).” *Proceedings of the ACM on
Programming Languages* 4 (HOPL), Article 85, June 2020. A [corrected author
copy](https://worrydream.com/refs/Ingalls_2020_-_The_Evolution_of_Smalltalk.pdf)
was reviewed.

## Contribution

Ingalls gives a technical history of the Smalltalk systems and separates “a
Smalltalk”—a complete live personal-computing environment—from the language
alone. The paper documents object memory, snapshots, BitBlt, projects, tools,
live evolution, MVC attribution, and implementation trade-offs.

## Method

The article is a participant history built from implementations, surviving
artifacts, demonstrations, and design recollection. Its technical details are
strong primary evidence; broad outcome claims remain retrospective.

## Findings

- A Smalltalk combines immediate response, message-sending objects, persistent
  whole-work-state images, managed storage, and user-defined objects in one
  compact environment.
- Ingalls describes his redesign and generalization of BitBlt into one
  rectangular bitmap operation beneath text, lines, scrolling, menus, sprites,
  and dragged windows. Kay's history identifies Diana Merry's earlier operator
  as the starting point, so the lineage should credit both Merry and Ingalls.
- Smalltalk-74 supported scheduled events, independent windows, live class and
  method redefinition, and recovery from file-backed state.
- Smalltalk-76 Projects saved scheduler, window-list, and change-tracking
  objects to provide task workspaces inside the shared environment. They were
  not protection domains.
- Browsers and a debugger were implemented in Smalltalk, operated on the
  running system, and could themselves be inspected and changed.
- Instance enumeration, `become:`, message-not-understood handling, and an
  emergency evaluator supported live schema evolution and repair, while also
  exposing the fragility of a shared mutable environment.
- Ingalls attributes MVC to Trygve Reenskaug and its Smalltalk implementation
  to Adele Goldberg, Jim Althoff, and others.

## Relevance

The source supplies both the attractive and hazardous sides of liveness. Atom
OS can seek a semantic continuum between running objects and visual tools
without recreating a single shared failure and authority domain. Projects can
be rebuilt as capability graphs of supervised actors; live changes can be
transactional, scoped, and reversible.

## Limits

This is a long retrospective by a principal implementer. The historical image
model, memory size, performance envelope, and trusted-user assumptions do not
transfer directly to a contemporary distributed operating system.

## Derived work

- [Alan Kay's Smalltalk visual interface and the modern desktop](../20-notes/alan-kay-smalltalk-visual-interface-and-modern-desktop.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
