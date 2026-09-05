---
title: "A Conflict-Free Replicated JSON Datatype"
kind: source
created: "2026-09-04"
authors:
  - "Martin Kleppmann"
  - "Alastair R. Beresford"
published: "2017-10"
citation_key: "kleppmann-beresford-2017-conflict-free-json"
container: "IEEE Transactions on Parallel and Distributed Systems 28(10)"
edition: null
isbn: null
doi: "10.1109/TPDS.2017.2697382"
url: "https://doi.org/10.1109/TPDS.2017.2697382"
accessed: "2026-09-04"
tags:
  - collaboration
  - crdt
  - json
  - local-first
aliases:
  - "CRDT JSON"
---

# A Conflict-Free Replicated JSON Datatype

## Reference

Martin Kleppmann and Alastair R. Beresford. “[A Conflict-Free Replicated JSON
Datatype](https://doi.org/10.1109/TPDS.2017.2697382).” *IEEE Transactions on
Parallel and Distributed Systems* 28(10), pages 2733–2746, October 2017. The
[author copy](https://www.cl.cam.ac.uk/~arb33/papers/KleppmannBeresford-CRDT-JSON-TPDS2017.pdf)
was read.

## Contribution

The paper defines a replicated nested map/list/register data type intended to
converge without losing concurrent user input. It analyzes operation semantics
for structured JSON-like documents and contrasts them with simple last-writer
resolution.

## Method

The authors formalize operations and concurrency, state convergence arguments,
and work through examples including concurrent deletion and update. The paper
does not report a production-scale performance evaluation.

## Findings

- Structured CRDTs can retain concurrent updates that a last-writer policy
  would discard.
- Global invariants such as uniqueness generally require serialization or a
  specialized coordination scheme.
- Delete/update concurrency can resurrect or reposition data in ways that
  conflict with an implicit application schema.
- Move, undo, schema evolution, metadata reclamation, and practical
  performance remain nontrivial.

## Relevance

Atom OS may use a nested replicated type for selected project records, but
must version the merge algebra, validate domain invariants, and surface
semantic conflicts. Provider bindings, authority, revocation, and irreversible
commands remain fenced rather than merged.

## Limits

JSON structure is not a general actor-state or semantic-intent model. Eventual
delivery and replica assumptions must be made explicit, and convergence does
not imply authorization, confidentiality, or user satisfaction.

## Derived work

- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
