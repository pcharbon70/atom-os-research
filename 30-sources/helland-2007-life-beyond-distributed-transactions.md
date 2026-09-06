---
title: "Life beyond Distributed Transactions: An Apostate's Opinion"
kind: source
created: "2026-09-05"
authors:
  - "Pat Helland"
published: 2007
citation_key: "helland-2007-life-beyond-distributed-transactions"
container: "3rd Biennial Conference on Innovative Data Systems Research (CIDR 2007)"
edition: null
isbn: null
doi: null
url: "https://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf"
accessed: "2026-09-05"
tags:
  - distributed-systems
  - fault-tolerance
  - messaging
  - transactions
aliases:
  - "Life beyond distributed transactions"
---

# Life beyond Distributed Transactions: An Apostate's Opinion

## Reference

Pat Helland. “[Life beyond Distributed Transactions: An Apostate's
Opinion](https://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf).” *3rd Biennial
Conference on Innovative Data Systems Research (CIDR)*, 2007.

## Research question or contribution

How should a highly scalable system structure entity state and message delivery
when one transaction cannot span arbitrary entities, including the ambiguity
between a receiver's committed effect and the sender's durable acknowledgement?

## Method

This position paper synthesizes production architecture experience into a
conceptual model of entity-local transactions, messages, retries, stable
identifiers, ordering metadata, and idempotence. It develops patterns and
examples rather than a formal proof or controlled evaluation.

## Findings

- Entity boundaries can delimit serializable local work while cross-entity
  coordination proceeds through messages.
- A receiver may commit an effect and crash before its acknowledgement becomes
  durable, so a retry can deliver the same substantive message again.
- Stable message identifiers and durable receiver history let a receiver
  recognize a duplicate and return the earlier result or apply an idempotent
  operation.
- Reordering, delayed duplicates, and work whose outcome is only eventually
  known are normal protocol states once a global transaction is unavailable.
- Application semantics must expose and resolve that uncertainty rather than
  hide it behind a synchronous-looking interface.

## Relevance

The paper supports aggregate-local transactions and explicit Layer 5 process
managers. Atom OS should not mistake actor messaging for atomic distributed
business work. Its fault-escalation channel should likewise qualify
at-least-once retention by durability domain, bind items to stable event and
boot/recovery generations, and require idempotent or deduplicated recovery
actions. The stronger boundary—claim exactly-once only when action and receipt
commit atomically in one durability domain—is Atom synthesis. Device resets and
other accepted-with-lost-completion operations can remain indeterminate, as
also illustrated by [recovering device drivers](swift-et-al-2004-recovering-device-drivers.md).

## Limits

The author deliberately narrows the argument. The paper does not solve high
availability, capability security, consensus, every consistency need, NMI-safe
kernel queuing, or hardware corruption. It is influential architectural
reasoning, not evidence that every aggregate should be remote or that
distributed transactions are never justified.

## Derived work

- [Invariants, transactions, and concurrency policy](../20-notes/applications-and-domain-services-components/invariants-transactions-and-concurrency-policy.md)
- [Workflows, process managers, timers, and compensation](../20-notes/applications-and-domain-services-components/workflows-process-managers-timers-and-compensation.md)
- [External effects, ports, adapters, and reconciliation](../20-notes/applications-and-domain-services-components/external-effects-ports-adapters-and-reconciliation.md)
- [Escalation channel](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/escalation-channel.md)
