---
title: "An Approach to Persistent Programming"
kind: source
created: "2026-09-04"
authors:
  - "Malcolm P. Atkinson"
  - "Peter J. Bailey"
  - "Kenneth J. Chisholm"
  - "W. Paul Cockshott"
  - "Ronald Morrison"
published: "1983"
citation_key: "atkinson-et-al-1983-persistent-programming"
container: "The Computer Journal 26(4)"
edition: null
isbn: null
doi: "10.1093/comjnl/26.4.360"
url: "https://doi.org/10.1093/comjnl/26.4.360"
accessed: "2026-09-04"
tags:
  - object-graphs
  - persistence
  - programming-languages
  - type-systems
aliases:
  - "Orthogonal persistence"
---

# An Approach to Persistent Programming

## Reference

Malcolm P. Atkinson, Peter J. Bailey, Kenneth J. Chisholm, W. Paul
Cockshott, and Ronald Morrison. “[An Approach to Persistent
Programming](https://doi.org/10.1093/comjnl/26.4.360).” *The Computer
Journal* 26(4), pages 360–365, 1983. The [archived author
copy](https://archive.cs.st-andrews.ac.uk/papers/download/ABC%2B83a.pdf) was
read.

## Contribution

The paper proposes persistence that is independent of data type and ordinary
program syntax. Values reachable transitively from explicit persistent roots
can survive executions while retaining type and structural relationships,
reducing manual conversion between programming-language and storage models.

## Method

The authors define design principles, work through language and type examples,
and describe a persistent-heap approach. It is a foundational language and
storage proposal, not a security model, crash-consistency proof, collaborative
system, or user-interface study.

## Findings

- Persistence can be orthogonal to type: the same values and relations need not
  be recoded into a separate file model merely to outlive one execution.
- Reachability from explicit roots naturally defines a persistent transitive
  closure.
- Type information must persist with data if future programs are to interpret
  the graph safely.
- Data unused by one execution can remain available to other programs and
  later versions, supporting continuity beyond one application invocation.

## Relevance

The rooted graph is a useful precedent for an Atom OS project. Atom OS must
strengthen it with explicit schemas, versioned identities, transactions,
authority, revocation, quotas, and export, and must not persist raw actor PIDs
or live kernel capability selectors.

## Limits

Reachability-based persistence can retain too much data and authority if used
without policy. The paper does not address untrusted principals, distributed
replicas, schema migration, deletion, garbage-collection evidence, or
crash-safe durable outcomes.

## Derived work

- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
