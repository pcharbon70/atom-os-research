---
title: "The Transaction Concept: Virtues and Limitations"
kind: source
created: "2026-09-05"
authors:
  - "Jim Gray"
published: 1981
citation_key: "gray-1981-transaction-concept"
container: "Proceedings of VLDB 1981"
edition: null
isbn: null
doi: null
url: "https://sigmod.org/publications/dblp/db/conf/vldb/Gray81.html"
accessed: "2026-09-05"
tags:
  - concurrency-control
  - database-systems
  - transactions
aliases:
  - "Transaction virtues and limitations"
---

# The Transaction Concept: Virtues and Limitations

## Reference

Jim Gray. “[The Transaction Concept: Virtues and
Limitations](https://sigmod.org/publications/dblp/db/conf/vldb/Gray81.html).”
*Proceedings of the 7th International Conference on Very Large Data Bases*,
1981, pages 144–154.

## Research question or contribution

Gray explains the transaction abstraction as a recoverable, consistency-
preserving state transformation and examines where flat transactions become
awkward for nested, distributed, or long-lived work.

## Method

The paper synthesizes database system concepts and limitations known at the
time. It is conceptual systems work rather than a modern workload evaluation.

## Findings

- Atomicity, consistency, isolation, and durability separate incomplete work
  from committed state.
- Concurrency control and recovery are related but distinct responsibilities.
- Long-lived and distributed activities strain conventional flat transaction
  boundaries and motivate nested or workflow-like alternatives.

## Relevance

Layer 5 should define each invariant and smallest atomic boundary; Layer 4 can
supply the transactional mechanism. Cross-aggregate and external work must
surface intermediate and uncertain states rather than pretend one unlimited
transaction exists.

## Limits

The paper predates current replicated databases and actor systems. It does not
select a storage engine or prove that a given domain model has complete
invariants.

## Derived work

- [Invariants, transactions, and concurrency policy](../20-notes/applications-and-domain-services-components/invariants-transactions-and-concurrency-policy.md)
- [Durable state, journals, snapshots, and projections](../20-notes/applications-and-domain-services-components/durable-state-journals-snapshots-and-projections.md)
