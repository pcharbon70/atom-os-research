---
title: "Decentralized ETS Counters for Better Scalability"
kind: source
created: "2026-09-09"
authors:
  - "Kjell Winblad"
published: "2021-08-03"
citation_key: "winblad-2021-decentralized-ets-counters"
container: "Erlang/OTP Blog"
edition: null
isbn: null
doi: null
url: "https://www.erlang.org/blog/scalable-ets-counters/"
accessed: "2026-09-09"
tags:
  - beam
  - managed-runtime
  - concurrency
aliases: []
---

# Decentralized ETS Counters for Better Scalability

## Reference

Kjell Winblad. [Decentralized ETS Counters for Better Scalability](https://www.erlang.org/blog/scalable-ets-counters/). Erlang/OTP Blog.
Published 2021-08-03.
Accessed 2026-09-09.

## Research question or contribution

When does distributing runtime counters improve performance, and what does observation cost?

## Method

Read the first-party article's benchmark setup, counter representation, snapshot steps and conclusions. The historical configuration is not asserted to be a current default.

## Findings

Scheduler-striped counters reduce update contention. Coherent observation swaps the array, waits for thread progress, sums the old array and carries its value forward. Exact size/memory reads become expensive. Reported tests used 64 hardware threads and a nondefault lock-count build.

## Relevance

Separate diagnostic estimates from hard quota admission. Atom OS can explore local credits bounded by an authoritative parent reservation, but cannot enforce a hard limit by independently summing changing telemetry shards. Counter-array retirement belongs to the same charged progress model as other shared metadata.

## Limits

The measurements are workload/configuration-specific, not a prediction for this runtime. No benchmark was reproduced; graphs were not used to infer a numerical speedup. The article does not prove a hierarchical resource ledger.

## Derived work

- [Service study](../20-notes/managed-actor-runtime-components/resource-accounting-and-overload-control/hierarchical-reservations-and-ledger-reconciliation.md).
- [Managed-runtime map](../10-maps/managed-actor-runtime.md).
- [Introducing research session](../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md).
