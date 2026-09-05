---
title: "Fault Tolerance via Idempotence"
kind: source
created: "2026-09-05"
authors:
  - "Ganesan Ramalingam"
  - "Kapil Vaswani"
published: 2013
citation_key: "ramalingam-vaswani-2013-fault-tolerance-via-idempotence"
container: "Proceedings of POPL 2013"
edition: null
isbn: "978-1-4503-1832-7"
doi: "10.1145/2429069.2429100"
url: "https://www.microsoft.com/en-us/research/publication/fault-tolerance-via-idempotence/"
accessed: "2026-09-05"
tags:
  - distributed-systems
  - fault-tolerance
  - idempotency
aliases:
  - "Failfree idempotence"
---

# Fault Tolerance via Idempotence

## Reference

Ganesan Ramalingam and Kapil Vaswani. “[Fault Tolerance via
Idempotence](https://www.microsoft.com/en-us/research/publication/fault-tolerance-via-idempotence/).”
*Proceedings of the 40th ACM SIGPLAN-SIGACT Symposium on Principles of
Programming Languages*, 2013, pages 249–262.

## Research question or contribution

The paper formalizes the relationship among process failure, duplicate
requests, local transactions, and idempotent application behavior, then
introduces language support for failure-tolerant composition.

## Method

The authors define a core language and the criterion of failfree idempotence,
construct an idempotence monad and extensions including compensation, and
report F# and C# implementations used for Azure applications.

## Findings

- Retry converts lost responses and process failures into duplicate work;
  correctness therefore needs durable duplicate semantics, not hope that a
  request ran once.
- Idempotent composition can recover useful workflow behavior without a
  central distributed transaction under the paper's storage model.
- Logical failure and compensation still need explicit application semantics.

## Relevance

Layer 5 commands and effects should carry stable operation IDs and retain
machine-readable outcomes. Idempotency is a semantic contract over results and
state, not merely an HTTP verb or deduplicating transport.

## Limits

The formal language assumes particular local transaction and partition
semantics. Low overhead in the authors' Azure examples does not transfer, and
nonparticipating physical or remote effects remain outside the guarantee.

## Derived work

- [Workflows, process managers, timers, and compensation](../20-notes/applications-and-domain-services-components/workflows-process-managers-timers-and-compensation.md)
- [External effects, ports, adapters, and reconciliation](../20-notes/applications-and-domain-services-components/external-effects-ports-adapters-and-reconciliation.md)
