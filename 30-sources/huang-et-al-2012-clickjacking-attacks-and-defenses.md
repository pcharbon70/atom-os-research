---
title: "Clickjacking: Attacks and Defenses"
kind: source
created: "2026-09-04"
authors:
  - "Lin-Shung Huang"
  - "Alexander Moshchuk"
  - "Helen J. Wang"
  - "Stuart Schechter"
  - "Collin Jackson"
published: "2012-08"
citation_key: "huang-et-al-2012-clickjacking-attacks-and-defenses"
container: "21st USENIX Security Symposium"
edition: null
isbn: "978-1-931971-95-9"
doi: null
url: "https://www.usenix.org/conference/usenixsecurity12/technical-sessions/presentation/huang"
accessed: "2026-09-04"
tags:
  - clickjacking
  - context-integrity
  - trusted-interaction
  - usable-security
aliases:
  - "InContext clickjacking defense"
---

# Clickjacking: Attacks and Defenses

## Reference

Lin-Shung Huang, Alexander Moshchuk, Helen J. Wang, Stuart Schechter, and
Collin Jackson. “[Clickjacking: Attacks and
Defenses](https://www.usenix.org/conference/usenixsecurity12/technical-sessions/presentation/huang).”
*21st USENIX Security Symposium*, pages 413–428, August 2012. The [open
paper](https://www.usenix.org/system/files/conference/usenixsecurity12/sec12-final39.pdf)
was read.

## Contribution

The paper characterizes UI-redressing attacks as failures of context
integrity, constructs new attacks, evaluates existing defenses, and proposes
InContext: browser or OS enforcement that a user saw the intended sensitive
element in its required visual context and acted within an appropriate timing
window.

## Method

The authors implement attack variants and defenses and run Mechanical Turk
studies totaling 2,064 participants. Reported attack success rates range from
43% to 98% under the studied conditions; the proposed defense substantially
reduces attacks for which redressing adds advantage over ordinary social
engineering.

## Findings

- Correct routing to a genuine target does not prove user intent when an
  attacker can obscure, move, time, or contextually misrepresent that target.
- Sensitive interaction needs integrity of visibility, geometry, timing, and
  target identity, not only focus ownership.
- Application-provided frame-busting and presentation heuristics leave gaps;
  the party that composes final pixels is best positioned to enforce context.
- Context protection mitigates UI redressing but cannot eliminate persuasion,
  confusing semantics, or all social engineering.

## Relevance

Atom OS input-derived authority must be bound to a compositor-observed surface
generation and trusted semantic target, with stability and visibility checks
for sensitive grants. A stale, occluded, transformed, or replaced surface must
not receive a capability minted for an earlier view.

## Limits

The experiments concern web clickjacking and visual pointing. Parameters do
not directly transfer to touch, keyboard, voice, switch access, or immersive
interfaces. Atom OS will need modality-specific context-integrity tests rather
than assuming a minimum visible-pixel rule is universal.

## Derived work

- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
