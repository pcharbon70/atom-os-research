---
title: "Mutatis Mutandis: Safe and Predictable Dynamic Software Updating"
kind: source
created: "2026-09-04"
authors:
  - "Gareth Stoyle"
  - "Michael Hicks"
  - "Gavin Bierman"
  - "Peter Sewell"
  - "Iulian Neamtiu"
published: "2005-01"
citation_key: "stoyle-et-al-2005-safe-predictable-dynamic-updating"
container: "Proceedings of POPL 2005 and ACM SIGPLAN Notices 40(1)"
edition: null
isbn: null
doi: "10.1145/1040305.1040321"
url: "https://doi.org/10.1145/1040305.1040321"
accessed: "2026-09-04"
tags:
  - dynamic-software-updating
  - live-programming
  - program-analysis
  - type-safety
aliases:
  - "Mutatis Mutandis"
  - "Proteus dynamic updating"
---

# Mutatis Mutandis: Safe and Predictable Dynamic Software Updating

## Reference

Gareth Stoyle, Michael Hicks, Gavin Bierman, Peter Sewell, and Iulian
Neamtiu. “[Mutatis Mutandis: Safe and Predictable Dynamic Software
Updating](https://doi.org/10.1145/1040305.1040321).” *Proceedings of POPL
2005* / *ACM SIGPLAN Notices* 40(1), pages 183–194, January 2005.

## Contribution

The paper presents Proteus, a core calculus for changing functions, named
types, and data in a running C-like program. It defines type-safe update
conditions and an updateability analysis that identifies program points where
future well-formed updates can be applied predictably.

## Method

The authors formalize the language and con-freeness property, prove relevant
type-safety results, implement a static analysis for C, and test it on several
established programs. The work addresses language-level safety, not complete
operational rollback or distributed effect consistency.

## Findings

- An update must account for code, type representation, and live data; swapping
  a function pointer is not a general state-evolution protocol.
- Explicit coercions and analysis can identify states in which a changing type
  is no longer concretely constrained by old code.
- Safe update points depend on the current program state and compatibility
  relation, so an arbitrary immediate commit is not always possible.
- Type correctness after an update does not guarantee application invariants,
  effect idempotence, availability, or successful rollback.

## Relevance

Atom OS live tools should stage a typed change, validate target generation and
migration, reach an explicit safe point, and publish one new generation. The
paper supports separating edit authority from commit authority and treating
state transformation as first-class rather than promising unrestricted
Smalltalk-style mutation.

## Limits

Proteus models C-like programs, not BEAM modules, supervised actor graphs,
capabilities, replicated projects, or GPU resources. Its guarantees must be
combined with Atom OS code-generation rules, effect journals, schema
compatibility, and recovery policy.

## Derived work

- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
