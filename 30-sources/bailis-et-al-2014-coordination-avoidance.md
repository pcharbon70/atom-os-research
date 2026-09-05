---
title: "Coordination Avoidance in Database Systems"
kind: source
created: "2026-09-05"
authors:
  - "Peter Bailis"
  - "Alan Fekete"
  - "Michael J. Franklin"
  - "Ali Ghodsi"
  - "Joseph M. Hellerstein"
  - "Ion Stoica"
published: 2014
citation_key: "bailis-et-al-2014-coordination-avoidance"
container: "Proceedings of the VLDB Endowment 8(3)"
edition: null
isbn: null
doi: "10.14778/2735508.2735509"
url: "https://www.vldb.org/pvldb/vol8/p185-bailis.pdf"
accessed: "2026-09-05"
tags:
  - consistency
  - coordination
  - database-systems
  - invariants
aliases:
  - "Invariant confluence"
---

# Coordination Avoidance in Database Systems

## Reference

Peter Bailis, Alan Fekete, Michael J. Franklin, Ali Ghodsi, Joseph M.
Hellerstein, and Ion Stoica. “[Coordination Avoidance in Database
Systems](https://www.vldb.org/pvldb/vol8/p185-bailis.pdf).” *Proceedings of the
VLDB Endowment* 8, no. 3, 2014.

## Research question or contribution

The paper asks exactly when a database can execute transactions without
coordination while preserving declared application invariants and develops
the criterion of invariant confluence.

## Method

The authors formalize invariant confluence relative to transactions, valid
states, and merge, prove necessity and sufficiency in their model, analyze
common invariants, and evaluate a prototype on several workloads.

## Findings

- Coordination freedom is conditional on both the invariant and the merge/
  transaction design; it is not a property of a datatype name alone.
- Some constraints admit coordination-free designs, while uniqueness and
  other scarce-claim invariants commonly require coordination or reformulation.
- The prototype reported a 25-fold improvement for TPC-C New-Order at 200
  servers, but that result belongs to its system, workload, and hardware.

## Relevance

Atom OS should default to conservative local serializability for non-mergeable
invariants and permit coordination-free collaboration only after an explicit
invariant-confluence argument or executable check for the declared model.

## Limits

Incomplete invariants make the analysis unsound for the real domain. The
formal and performance results do not transfer automatically to actors,
external effects, authorization, or Atom OS targets.

## Derived work

- [Invariants, transactions, and concurrency policy](../20-notes/applications-and-domain-services-components/invariants-transactions-and-concurrency-policy.md)
- [Offline collaboration, replication, and conflict semantics](../20-notes/applications-and-domain-services-components/offline-collaboration-replication-and-conflict-semantics.md)
- [2026-09-05 applications deep dive](../50-journal/2026-09-05-applications-and-domain-services-deep-dive.md)
