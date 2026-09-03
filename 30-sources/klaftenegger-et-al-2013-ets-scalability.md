---
title: "On the scalability of the Erlang Term Storage"
kind: source
created: "2026-09-03"
authors:
  - "David Klaftenegger"
  - "Konstantinos Sagonas"
  - "Kjell Winblad"
published: 2013
citation_key: "klaftenegger-et-al-2013-ets-scalability"
container: "12th ACM SIGPLAN Workshop on Erlang"
edition: "Erlang '13, 15-26"
isbn: null
doi: "10.1145/2505305.2505308"
url: "https://doi.org/10.1145/2505305.2505308"
accessed: "2026-09-03"
tags:
  - concurrent-data-structures
  - erlang
  - ets
  - scalability
aliases:
  - "ETS scalability study"
---

# On the scalability of the Erlang Term Storage

## Reference

David Klaftenegger, Konstantinos Sagonas, and Kjell Winblad. “[On the
Scalability of the Erlang Term
Storage](https://doi.org/10.1145/2505305.2505308).” *12th ACM SIGPLAN Workshop
on Erlang*, pages 15–26, 2013.

## Research question or contribution

The paper identifies synchronization and metadata bottlenecks in ETS and asks
how table types and concurrency options scale across cores and workloads.

## Method

The authors benchmark then-current ETS implementations under varied read/write
patterns and contention, inspect bottlenecks, and evaluate implementation
changes intended to improve parallelism.

## Findings

- “Shared table” is not one scalability profile: table type, key distribution,
  read/write ratio, and shared metadata determine contention.
- Global or frequently written table metadata can cap scaling even when data
  buckets are independently accessible.
- Distributed reader groups and finer bucket locking trade additional memory
  plus writer and uncontended overhead against parallel read/write throughput.

## Relevance

The study argues for workload-explicit table kinds and metrics in Atom OS,
separate accounting for metadata and deferred reclamation, and benchmarks that
include hot keys, disjoint ranges, traversal, resize, and owner death.

## Limits

The evaluated R16-era ETS implementation is not current OTP 29. Current CA
trees, decentralized counters, and allocator behavior differ. The work is
historical evidence about hidden shared-state bottlenecks, not a current
performance prediction or a table-semantics specification.

## Derived work

- [Resource accounting and overload control](../20-notes/managed-actor-runtime-components/resource-accounting-and-overload-control.md)
- [2026-09-03 component research journal](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md)
