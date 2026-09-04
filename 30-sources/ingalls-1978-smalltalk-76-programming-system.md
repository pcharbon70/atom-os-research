---
title: "The Smalltalk-76 Programming System: Design and Implementation"
kind: source
created: "2026-09-04"
authors:
  - "Daniel H. H. Ingalls"
published: 1978
citation_key: "ingalls-1978-smalltalk-76-programming-system"
container: "Proceedings of POPL '78"
edition: null
isbn: null
doi: "10.1145/512760.512762"
url: "https://doi.org/10.1145/512760.512762"
accessed: "2026-09-04"
tags:
  - live-programming
  - object-oriented-programming
  - smalltalk
  - user-interface
aliases:
  - "Smalltalk-76 design and implementation"
---

# The Smalltalk-76 Programming System: Design and Implementation

## Reference

Daniel H. H. Ingalls. “[The Smalltalk-76 Programming System: Design and
Implementation](https://doi.org/10.1145/512760.512762).” *Proceedings of the
5th ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages*,
pages 9–16, 1978. An [author-curated
scan](https://smalltalkzoo.thechm.org/papers/The%20Smalltalk-76%20Programming%20System.PDF)
was used for the full text.

## Contribution

Ingalls describes the language, virtual machine, storage, display, and
interface principles of the running Smalltalk-76 system. The paper supplies
contemporaneous implementation evidence for the claim that user-visible tools
and ordinary objects inhabited the same communicative framework.

## Method

The paper presents the design and implementation, including examples of
classes, messages, windows, editing, and system construction. It demonstrates
mechanisms but does not provide controlled usability or reliability results.

## Findings

- Smalltalk is organized as communicating objects and gives one person
  creative control over numbers, text, sound, and images.
- Text editing, debugging, filing, and graphics are facilities of the running
  Smalltalk system rather than opaque external tools.
- Under the “reactive principle,” system components should remain visibly
  alive: an object can present itself and offer simple means for meaningful
  alteration.
- `Object` provides default inspection and alteration behavior. `Window`
  establishes a uniform interaction protocol while subclasses attach text,
  drawing, font, clock, or other domain semantics.
- Window behavior includes activation, fronting, input routing, moving,
  resizing, printing, and closing; content-specific windows reuse those common
  operations while supplying their own editing behavior.
- Ingalls warns that the specific visual appearance is not the main result.
  The transferable principle is that interface parts are participating objects
  in the same message system.

## Relevance

This source distinguishes Kay's aspiration from an implemented architecture.
For Atom OS, it motivates a common semantic protocol by which models, views,
tools, and inspectors remain causally connected, while leaving room to replace
the historical widgets and single-address-space assumptions.

## Limits

Smalltalk-76 ran in a trusted research environment. Its communicative
uniformity is not evidence of multi-principal isolation, bounded resource use,
or independent UI-process restart. The paper explicitly cautions against
canonizing one interface presentation.

## Derived work

- [Alan Kay's Smalltalk visual interface and the modern desktop](../20-notes/alan-kay-smalltalk-visual-interface-and-modern-desktop.md)
- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
