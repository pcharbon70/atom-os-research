---
title: "Potluck: Dynamic Documents as Personal Software"
kind: source
created: "2026-09-04"
authors:
  - "Geoffrey Litt"
  - "Max Schoening"
  - "Paul Shen"
  - "Paul Sonnentag"
published: "2022-10"
citation_key: "litt-et-al-2022-potluck-dynamic-documents"
container: "LIVE 2022 Workshop at SPLASH and Ink & Switch research essay"
edition: null
isbn: null
doi: null
url: "https://www.inkandswitch.com/potluck/"
accessed: "2026-09-04"
tags:
  - dynamic-documents
  - end-user-programming
  - live-programming
  - personal-software
aliases:
  - "Potluck"
---

# Potluck: Dynamic Documents as Personal Software

## Reference

Geoffrey Litt, Max Schoening, Paul Shen, and Paul Sonnentag. “[Potluck:
Dynamic Documents as Personal Software](https://www.inkandswitch.com/potluck/).”
Ink & Switch research essay and LIVE 2022 Workshop contribution, October 2022.

## Contribution

Potluck explores *gradual enrichment*: beginning with unconstrained text,
adding user-defined searches that recognize structure, computing over those
results, and projecting dynamic annotations and widgets back onto the text.
The artifact remains useful at each stage rather than requiring a complete
application schema before the user can begin.

## Method

The team built interactive examples for recipes, workouts, agendas, chores,
expenses, and similar personal tasks. Its findings come from sustained design
use by the team and informal sessions with roughly a dozen participants,
mostly programmers familiar with JavaScript.

## Findings

- Free-form text is an effective permissive source of truth for small personal
  tools and preserves ordinary editing, copy, history, and portability.
- Separating computational annotations from source text avoids circular
  feedback and lets the underlying material remain inspectable.
- Search, computation, and presentation can compose incrementally, but tools
  become difficult to understand as rule sets grow.
- Immediate, predictable feedback helps users learn a limited parser even when
  the input initially appears informal.
- Text is not an adequate universal view: rich spatial data and visualization
  require other representations.
- JavaScript enabled rapid experiments but excluded most non-programmers from
  sophisticated authorship; discoverability and debuggability remain open.

## Relevance

Potluck supplies a concrete design pattern for Atom OS project tools: durable
source objects, separately derived semantics and annotations, explicit
user-triggered writes, reusable recognizers, and plural views. It also provides
negative evidence against one universal graphical or textual representation.

## Limits

The evaluation is small and informal, the prototype is not a secure
multi-principal operating environment, and text edits do not cover arbitrary
stateful actors or external effects. Its “OS woven through Potluck” conclusion
is a research vision, not demonstrated architecture.

## Derived work

- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
