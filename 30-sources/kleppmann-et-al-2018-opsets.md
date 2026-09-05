---
title: "OpSets: Sequential Specifications for Replicated Datatypes"
kind: source
created: "2026-09-05"
authors:
  - "Martin Kleppmann"
  - "Victor B. F. Gomes"
  - "Dominic P. Mulligan"
  - "Alastair R. Beresford"
published: 2018
citation_key: "kleppmann-et-al-2018-opsets"
container: "arXiv"
edition: null
isbn: null
doi: null
url: "https://arxiv.org/abs/1805.04263"
accessed: "2026-09-05"
tags:
  - collaborative-editing
  - formal-specification
  - replicated-data
aliases:
  - "OpSets"
---

# OpSets: Sequential Specifications for Replicated Datatypes

## Reference

Martin Kleppmann, Victor B. F. Gomes, Dominic P. Mulligan, and Alastair R.
Beresford. “[OpSets: Sequential Specifications for Replicated
Datatypes](https://arxiv.org/abs/1805.04263).” arXiv:1805.04263, 2018.

## Research question or contribution

The work specifies replicated datatypes by interpreting an unordered set of
immutable operations in a deterministic sequence and uses the method to expose
subtle list-editing anomalies.

## Method

The authors give executable sequential specifications, compare replicated list
semantics, and mechanize key results in Isabelle/HOL.

## Findings

- Convergence alone allows several user-visible orders for concurrent list
  insertion, including surprising interleavings.
- A compact sequential interpretation can make intended replicated semantics
  easier to state and prove than an operational distributed algorithm.
- Formal datatype properties still depend on the chosen user-level
  specification.

## Relevance

Collaborative Layer 5 types should define intent-level sequential semantics and
test histories, not accept byte convergence as the complete product contract.
The operation set can also support deterministic replay and audit without
being confused with every domain event.

## Limits

This is a preprint focused on replicated datatypes. It does not solve
authorization, revocation, scarce resources, workflows, or external effects.

## Derived work

- [Offline collaboration, replication, and conflict semantics](../20-notes/applications-and-domain-services-components/offline-collaboration-replication-and-conflict-semantics.md)
