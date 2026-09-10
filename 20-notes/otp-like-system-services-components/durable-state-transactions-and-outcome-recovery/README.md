---
title: "Durable state, transactions, and outcome recovery: internal services"
kind: map
created: "2026-09-10"
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Durable state, transactions, and outcome recovery: internal services

## Purpose

Separate the storage fault contract, transactional log, recoverable checkpoint and
durable retry-result lifetime.

This directory decomposes [Durable state, transactions, and outcome recovery](../durable-state-transactions-and-outcome-recovery.md).
These are logical responsibilities, not a requirement for one process per study.

## What belongs here

Keep owned state, authority, transition evidence, failure cases, alternatives
and unexecuted verification obligations here. This is full-system Layer 4
architecture research, not a PoC, QEMU profile or implementation plan. Layers
2–3 supply enforcement and managed execution; Layer 5 supplies domain meaning.
The [session manifest](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) records provenance.

## Index

### Subdirectories

- None yet.

### Documents

- [Durability profile and storage failure boundary](durability-profile-and-storage-failure-boundary.md) — Which failures does a successful persistence acknowledgement actually survive?
- [Transaction-log framing and commit publication](transaction-log-framing-and-commit-publication.md) — How can recovery distinguish a committed transaction from a plausible but incomplete log tail?
- [Checkpoint replay and retention frontiers](checkpoint-replay-and-retention-frontiers.md) — When can log history be reclaimed without invalidating recovery, readers or promised outcomes?
- [Operation-result ledger, retry rendezvous, and expiry](operation-result-ledger-retry-rendezvous-and-expiry.md) — How can duplicate suppression remain bounded without executing an old operation again?

## Maintaining this index

Inventory every direct child. Keep the parent report, component index, topic
map and inquiry connected when responsibilities change. Decompose according
to distinct state, authority and completion needs, not a fixed document quota.
Writing these studies does not validate their proposed guarantees.
