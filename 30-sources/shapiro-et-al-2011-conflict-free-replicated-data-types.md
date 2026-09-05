---
title: "Conflict-Free Replicated Data Types"
kind: source
created: "2026-09-04"
authors:
  - "Marc Shapiro"
  - "Nuno Preguiça"
  - "Carlos Baquero"
  - "Marek Zawirski"
published: "2011-10"
citation_key: "shapiro-et-al-2011-conflict-free-replicated-data-types"
container: "13th International Symposium on Stabilization, Safety, and Security of Distributed Systems (SSS 2011), LNCS 6976"
edition: null
isbn: null
doi: "10.1007/978-3-642-24550-3_29"
url: "https://doi.org/10.1007/978-3-642-24550-3_29"
accessed: "2026-09-04"
tags:
  - collaboration
  - consistency
  - crdt
  - distributed-systems
aliases:
  - "CRDTs"
---

# Conflict-Free Replicated Data Types

## Reference

Marc Shapiro, Nuno Preguiça, Carlos Baquero, and Marek Zawirski.
“[Conflict-Free Replicated Data
Types](https://doi.org/10.1007/978-3-642-24550-3_29).” *SSS 2011*, LNCS
6976, pages 386–400, October 2011. The [author
copy](https://perso.lip6.fr/Marc.Shapiro/papers/2011/CRDTs_SSS-2011.pdf) was
read.

## Contribution

The paper formalizes strong eventual consistency and gives sufficient
conditions under which state-based and operation-based replicated data types
converge without synchronous coordination among replicas.

## Method

The authors define formal models and convergence conditions, distinguish two
replication approaches, and present representative CRDT constructions. The
result concerns convergence under its delivery and algebra assumptions rather
than general application correctness.

## Findings

- State-based replicas converge when their states form an appropriate
  monotonic join structure and exchanged states are eventually delivered.
- Operation-based replicas converge under reliable causal delivery and
  commutativity conditions for concurrent operations.
- Replicas can accept updates without remote synchronization for types that
  satisfy the required algebra.
- Convergence does not itself establish authorization, invariant preservation,
  intention preservation, bounded metadata, confidentiality, or safe external
  effects.

## Relevance

Atom OS may offer CRDT-backed project object profiles, but every object and
edge must name its merge algebra. Capability grants, revocation, unique
ownership, provider selection, and irreversible effects require separately
fenced protocols.

## Limits

The paper's failure and delivery assumptions must be stated per deployment.
The formal result is not a universal merge procedure and does not choose user-
appropriate conflict semantics or schema-evolution behavior.

## Derived work

- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
