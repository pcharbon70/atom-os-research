---
title: "Accessible Rich Internet Applications (WAI-ARIA) 1.2"
kind: source
created: "2026-09-04"
authors:
  - "W3C Accessible Rich Internet Applications Working Group"
published: "2023-06-06"
citation_key: "w3c-2023-wai-aria-1-2"
container: "W3C Recommendation"
edition: "1.2"
isbn: null
doi: null
url: "https://www.w3.org/TR/2023/REC-wai-aria-1.2-20230606/"
accessed: "2026-09-04"
tags:
  - accessibility
  - semantics
  - standards
  - user-interface
aliases:
  - "WAI-ARIA 1.2"
---

# Accessible Rich Internet Applications (WAI-ARIA) 1.2

## Reference

W3C Accessible Rich Internet Applications Working Group. “[Accessible Rich
Internet Applications (WAI-ARIA)
1.2](https://www.w3.org/TR/2023/REC-wai-aria-1.2-20230606/).” W3C
Recommendation, 6 June 2023.

## Contribution

WAI-ARIA defines an ontology of UI roles, states, and properties so user agents
can expose structure and behavior to assistive technologies. It also defines
role taxonomy, inherited properties, supported states, ownership
relationships, widget constraints, and author and user-agent conformance
requirements.

## Method

This is a consensus standard with an implementation report, normative
requirements, examples, and explicit authoring and user-agent obligations. It
is not a controlled empirical study and its implementation evidence is tied to
web content and existing accessibility stacks.

## Findings

- Accessibility requires semantic information about structure and behavior;
  pixels and geometry alone are insufficient.
- Roles, names, values, states, properties, and relationships form a reusable
  vocabulary that user agents can map to platform accessibility APIs.
- A semantic role carries required context, owned elements, supported states,
  and expected interaction behavior; publishing a label alone is not
  conformance.
- Native semantics and author-supplied semantics can conflict, so precedence
  and validation rules are necessary.
- The ontology improves interoperability but does not define application data
  models, authorization for actions, durable identity, localization storage,
  or restart generations.

## Relevance

WAI-ARIA gives Atom OS a mature lower bound for a semantic UI record, but the
Atom protocol needs stronger identity, generation, authority, outcome, and
recovery fields. The standard supports deriving both visual and assistive
projections from one semantic source rather than reconstructing accessibility
from rendered pixels.

## Limits

ARIA can be applied incorrectly and cannot repair missing domain semantics.
Its vocabulary is intentionally web-oriented and extensibility must not become
an unreviewed central taxonomy for every Atom OS domain. Conformance to ARIA
also does not establish WCAG conformance or usable interaction.

## Derived work

- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
