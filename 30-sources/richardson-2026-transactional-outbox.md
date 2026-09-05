---
title: "Pattern: Transactional Outbox"
kind: source
created: "2026-09-05"
authors:
  - "Chris Richardson"
published: null
citation_key: "richardson-2026-transactional-outbox"
container: "Microservices.io"
edition: null
isbn: null
doi: null
url: "https://microservices.io/patterns/data/transactional-outbox"
accessed: "2026-09-05"
tags:
  - integration-events
  - practitioner-literature
  - transactional-outbox
aliases:
  - "Transactional outbox pattern"
---

# Pattern: Transactional Outbox

## Reference

Chris Richardson. “[Pattern: Transactional
Outbox](https://microservices.io/patterns/data/transactional-outbox).”
Microservices.io. Publication date not stated; accessed 5 September 2026.

## Research question or contribution

The article describes how an application can commit a business-state change
and a message-to-be-published in one local database transaction, then relay the
stored message separately.

## Method

This is a practitioner pattern description, not a formal paper or independent
evaluation. It was used for the operational outbox shape and its explicitly
stated duplicate-delivery limitation.

## Findings

- Writing state and outbox intent in one local transaction avoids the gap
  between committing domain state and attempting broker publication.
- A relay can crash after publishing but before recording progress, so it may
  publish the same record again.
- Consumers still need idempotency and ordering policy; the pattern does not
  create a distributed atomic transaction.

## Relevance

Layer 5 should distinguish committed domain events from exported integration
records, assign stable operation/event IDs, and define inbox behavior. Layer 4
can supply atomic storage and relay mechanics, but only the application knows
the event meaning and safe duplicate result.

## Limits

The page offers no peer-reviewed performance or correctness evaluation and
assumes a local transactional database. It does not resolve nonparticipating
external effects or prove global exactly-once delivery.

## Derived work

- [External effects, ports, adapters, and reconciliation](../20-notes/applications-and-domain-services-components/external-effects-ports-adapters-and-reconciliation.md)
- [Durable state, journals, snapshots, and projections](../20-notes/applications-and-domain-services-components/durable-state-journals-snapshots-and-projections.md)
