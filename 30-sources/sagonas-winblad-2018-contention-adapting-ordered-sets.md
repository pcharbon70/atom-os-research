---
title: "A contention adapting approach to concurrent ordered sets"
kind: source
created: "2026-09-03"
authors:
  - "Konstantinos Sagonas"
  - "Kjell Winblad"
published: 2018
citation_key: "sagonas-winblad-2018-contention-adapting-sets"
container: "Journal of Parallel and Distributed Computing"
edition: "115, 1-19"
isbn: null
doi: "10.1016/j.jpdc.2017.11.007"
url: "https://doi.org/10.1016/j.jpdc.2017.11.007"
accessed: "2026-09-03"
tags:
  - concurrent-data-structures
  - erlang
  - ets
  - shared-state
aliases:
  - "Contention adapting search trees"
  - "CA trees"
---

# A contention adapting approach to concurrent ordered sets

## Reference

Konstantinos Sagonas and Kjell Winblad. “[A Contention Adapting Approach to
Concurrent Ordered Sets](https://doi.org/10.1016/j.jpdc.2017.11.007).”
*Journal of Parallel and Distributed Computing* 115, pages 1–19, 2018.

## Research question or contribution

The paper asks whether an ordered concurrent set can adapt its synchronization
granularity to observed contention while supporting single-key operations,
range queries, and bulk operations. It develops contention-adapting search
trees whose routing layer divides the key space among lock-protected base
structures that split or join according to collected contention statistics.

## Method

The authors specify the tree and adaptation operations, discuss linearizable
range operations, implement several base-node variants, and compare them with
contemporary concurrent ordered structures under basic, range-query, and
range-update workloads.

## Findings

- Fixed synchronization granularity is not optimal across sequential,
  disjoint-key, hot-key, and range-heavy workloads.
- Local contention statistics can drive splits and joins, retaining coarse
  structures when contention is low and exposing more parallelism when it is
  high.
- The reported CA-tree variants were competitive on basic operations and
  showed large gains in selected range workloads.
- Adaptation has costs: statistics, routing nodes, restructuring, memory
  reclamation, and base-node choices can lose to simpler structures on some
  workloads. No single configuration dominates universally.

## Relevance

The result supplies a strong implementation candidate for an ETS-compatible
`ordered_set` with write concurrency, but the public Atom OS contract should
name ordering, operation atomicity, traversal consistency, ownership, and
resource limits rather than “CA tree.” Bulk operations and adaptation must
yield in slices and charge deferred reclamation to the table account.

## Limits

The paper evaluates a data structure, not the complete ETS ownership, heir,
copy-in/out, match-specification, failure, or memory-accounting contract. Its
throughput results do not establish bounded operation latency or suitability
under runtime-domain memory pressure. Hash tables and simple trees remain
valid alternatives for other table kinds and workloads.

## Derived work

- [Resource accounting and overload control](../20-notes/managed-actor-runtime-components/resource-accounting-and-overload-control.md)
- [Managed actor runtime layer](../20-notes/managed-actor-runtime-layer.md)
- [2026-09-03 component research journal](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md)
