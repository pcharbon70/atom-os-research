---
title: "Life beyond Distributed Transactions: An Apostate's Opinion"
kind: source
created: "2026-09-05"
authors:
  - "Pat Helland"
published: 2007
citation_key: "helland-2007-life-beyond-distributed-transactions"
container: "CIDR 2007"
edition: null
isbn: null
doi: null
url: "https://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf"
accessed: "2026-09-05"
tags:
  - distributed-systems
  - messaging
  - transactions
aliases:
  - "Life beyond distributed transactions"
---

# Life beyond Distributed Transactions: An Apostate's Opinion

## Reference

Pat Helland. “[Life beyond Distributed Transactions: An Apostate's
Opinion](https://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf).” *CIDR 2007*.

## Research question or contribution

Helland argues that highly scalable systems cannot assume one transaction
spans arbitrary entities and instead must advance entity-local state through
messages, stable identities, and application-visible uncertainty.

## Method

This is a position paper synthesizing production architecture experience. It
develops a conceptual model and examples rather than a formal proof or
controlled evaluation.

## Findings

- Entity boundaries can delimit serializable local work while cross-entity
  coordination proceeds through messages.
- Stable identity, message history, idempotency, and explicit uncertainty are
  central once one global transaction is unavailable.
- Application semantics must account for work that is pending, duplicated, or
  only eventually known.

## Relevance

The paper supports aggregate-local transactions and explicit Layer 5 process
managers. Atom OS should not mistake actor messaging for atomic distributed
business work or hide ambiguous completion behind a synchronous-looking API.

## Limits

The author explicitly narrows the argument and does not solve high
availability, capability security, consensus, or every consistency need. It
is influential reasoning, not evidence that all aggregates should be remote
entities or that distributed transactions are never justified.

## Derived work

- [Invariants, transactions, and concurrency policy](../20-notes/applications-and-domain-services-components/invariants-transactions-and-concurrency-policy.md)
- [Workflows, process managers, timers, and compensation](../20-notes/applications-and-domain-services-components/workflows-process-managers-timers-and-compensation.md)
- [External effects, ports, adapters, and reconciliation](../20-notes/applications-and-domain-services-components/external-effects-ports-adapters-and-reconciliation.md)
