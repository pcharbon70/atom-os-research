---
title: "Achieving Convergence, Causality Preservation, and Intention Preservation in Real-Time Cooperative Editing Systems"
kind: source
created: "2026-09-04"
authors:
  - "Chengzheng Sun"
  - "Xiaohua Jia"
  - "Yanchun Zhang"
  - "Yun Yang"
  - "David Chen"
published: "1998-03"
citation_key: "sun-et-al-1998-cooperative-editing-consistency"
container: "ACM Transactions on Computer-Human Interaction 5(1)"
edition: null
isbn: null
doi: "10.1145/274444.274447"
url: "https://doi.org/10.1145/274444.274447"
accessed: "2026-09-04"
tags:
  - collaboration
  - consistency
  - operational-transformation
  - user-intent
aliases:
  - "Cooperative editing consistency model"
---

# Achieving Convergence, Causality Preservation, and Intention Preservation in Real-Time Cooperative Editing Systems

## Reference

Chengzheng Sun, Xiaohua Jia, Yanchun Zhang, Yun Yang, and David Chen.
“[Achieving Convergence, Causality Preservation, and Intention Preservation in
Real-Time Cooperative Editing
Systems](https://doi.org/10.1145/274444.274447).” *ACM Transactions on
Computer-Human Interaction* 5(1), pages 63–108, March 1998. The [author
copy](https://www.cs.cityu.edu.hk/~jia/research/reduce98.pdf) was read.

## Contribution

The paper separates three cooperative-editing properties—replica convergence,
preservation of causal order, and preservation of an operation's intended
effect—and proposes operational-transformation control and string-operation
algorithms intended to satisfy them together.

## Method

The authors define a consistency model, derive transformation algorithms,
analyze properties, and implement an Internet-based collaborative editing
prototype. The algorithms and intention definition are tied to their operation
model and do not cover arbitrary domain actors.

## Findings

- Equal final replica state is not enough if causally dependent operations were
  reordered or a user's intended edit changed meaning.
- Concurrent operations require an explicit transformation or conflict policy
  relative to the state in which each was authored.
- Reversible inclusion and exclusion transformations can support the studied
  string operations under the control algorithm.
- “Intention” is formalized within an operation model; it is not a general
  psychological or domain-semantic guarantee.

## Relevance

Atom OS must report convergence, causality, domain validity, authority, and
human conflict as separate properties. A project service must not hide a
meaningful conflict merely because replicas have converged.

## Limits

The results do not establish capability authorization, confidentiality,
offline revocation, actor-state merging, schema migration, or exactly-once
external effects. Operational-transformation results should not be generalized
to every project object type.

## Derived work

- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
