---
title: "The Early History of Smalltalk"
kind: source
created: "2026-09-04"
authors:
  - "Alan C. Kay"
published: "1993-03"
citation_key: "kay-1993-early-history-smalltalk"
container: "ACM SIGPLAN Notices 28(3), HOPL-II"
edition: null
isbn: null
doi: "10.1145/155360.155364"
url: "https://doi.org/10.1145/155360.155364"
accessed: "2026-09-04"
tags:
  - history-of-computing
  - human-computer-interaction
  - object-oriented-programming
  - smalltalk
aliases:
  - "Smalltalk early history"
---

# The Early History of Smalltalk

## Reference

Alan C. Kay. “[The Early History of
Smalltalk](https://doi.org/10.1145/155360.155364).” *ACM SIGPLAN Notices*
28(3), HOPL-II, pages 69–95, March 1993. A checked HTML transcription is
available from [WorryDream](https://worrydream.com/EarlyHistoryOfSmalltalk/).

## Contribution

Kay reconstructs the influences, design principles, implementations, user
interface work, educational experiments, and community decisions behind early
Smalltalk. It is both a primary participant account and a retrospective
history with unusually explicit attribution and negative evidence.

## Method

The paper combines documentary recollection, technical description, code and
interface examples, project chronology, and lessons drawn from educational
use. As a first-person history written roughly two decades later, it should be
cross-checked against contemporaneous papers for priority and implementation
detail.

## Findings

- Kay identifies durable external principles: everything is an object,
  objects communicate through messages, and objects retain their own memory.
  Particular class and implementation mechanisms changed around those ideas.
- The interface goal was deliberately rotated from access to functionality
  toward an environment in which people learn by doing. Exploration,
  modelessness, familiar presentation, and a path from action through images
  to symbols were central.
- Smalltalk became the Alto's live working environment, with draggable
  windows, structured and WYSIWYG editing, multimedia components, painting,
  music, browsing, debugging, files, printing, and networking.
- Kay reports that Smalltalk-76 integrated many functions now split between an
  OS, toolkit, development environment, and applications in roughly fifty
  classes. This is a historical scale report, not an independent complexity
  benchmark.
- The live-system demonstration in which scrolling behavior was changed while
  the environment kept running illustrates causal connection between visible
  behavior and editable code.
- Kay states that interface elements predated the Smalltalk effort and credits
  Dan Ingalls, Adele Goldberg, Ted Kaehler, Ron Baecker, Diana Merry, David
  Smith, and others. The evidence does not support “Kay invented the GUI.”
- The educational record was mixed: a minority of children took naturally to
  the medium, many needed substantial help, and inheritance and curriculum
  design remained difficult.

## Relevance

The paper connects Kay's conceptual vision to actual Smalltalk components and
supplies essential attribution and failure evidence. It also warns Atom OS
against treating universal malleability as automatically learnable: the
architecture must be paired with progressive tools, explanations, and studies
of real users.

## Limits

The work is retrospective and authored by a central participant. Counts,
anecdotes, and priority statements require contextual corroboration. Early
Smalltalk messaging and processes must not be equated with BEAM's isolated
heaps, asynchronous signals, or modern protection domains.

## Derived work

- [Alan Kay's Smalltalk visual interface and the modern desktop](../20-notes/alan-kay-smalltalk-visual-interface-and-modern-desktop.md)
- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
