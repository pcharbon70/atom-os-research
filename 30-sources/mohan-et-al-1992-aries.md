---
title: "ARIES: A transaction recovery method supporting fine-granularity locking and partial rollbacks using write-ahead logging"
kind: source
created: "2026-09-03"
authors:
  - "C. Mohan"
  - "Don Haderle"
  - "Bruce Lindsay"
  - "Hamid Pirahesh"
  - "Peter Schwarz"
published: 1992
citation_key: "mohan-et-al-1992-aries"
container: "ACM Transactions on Database Systems 17(1), 94–162"
edition: null
isbn: null
doi: "10.1145/128765.128770"
url: "https://research.ibm.com/publications/aries-a-transaction-recovery-method-supporting-fine-granularity-locking-and-partial-rollbacks-using-write-ahead-logging"
accessed: "2026-09-03"
tags:
  - persistence
  - recovery
  - transactions
  - write-ahead-logging
aliases:
  - "ARIES"
---

# ARIES: A transaction recovery method supporting fine-granularity locking and partial rollbacks using write-ahead logging

## Reference

C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh, and Peter Schwarz.
“[ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking
and Partial Rollbacks Using Write-Ahead
Logging](https://research.ibm.com/publications/aries-a-transaction-recovery-method-supporting-fine-granularity-locking-and-partial-rollbacks-using-write-ahead-logging).”
*ACM Transactions on Database Systems* 17(1), pages 94–162, 1992. DOI
[10.1145/128765.128770](https://doi.org/10.1145/128765.128770). An
[open paper copy](https://www.cs.cmu.edu/~15849g/readings/mohan92.pdf) was
also consulted.

## Research question or contribution

How can a write-ahead-logged transaction system support fine-grained locking,
steal/no-force buffer management, partial rollback, and repeatable crash
recovery without quiescing ordinary execution for checkpoints?

## Method

The paper develops logging and recovery invariants, compares them with earlier
System R and shadow-page approaches, and describes use across several database,
file, persistent-object, and transaction-oriented systems. ARIES combines page
log-sequence numbers, fuzzy checkpoints, analysis, history-repeating redo, and
logged undo through compensation log records.

## Findings

- A write-ahead rule must make the log durable before a dependent data page can
  reach durable storage, and transaction commit must have an explicit durable
  point.
- Per-page log-sequence numbers make recovery able to determine whether a
  logged update is already reflected in a page.
- Restart first analyzes state, then repeats history from the required redo
  point while page log-sequence numbers skip updates already reflected in a
  page, and finally undoes loser transactions. Compensation log records make
  undo itself restartable after a second crash.
- Fuzzy checkpoints can bound recovery scanning without stopping normal
  updates, but they enlarge the implementation and proof surface.
- Durable recovery is a protocol over storage ordering, metadata, and
  idempotence; restarting the actor that issued a write is not sufficient.

## Relevance

The Atom OS storage service should expose an explicit accepted/committed state,
durable operation identifiers, checksummed generations, and crash injection at
each ordering boundary. A simple first implementation can use append-only redo
and immutable checkpoints; it should adopt ARIES-class undo machinery only if
fine-grained concurrent mutation and partial rollback justify that complexity.

## Limits

ARIES is an industrial database recovery method, not a ready-made filesystem,
actor checkpoint format, or transaction across arbitrary network and device
effects. Its assumptions depend on the storage system's actual atomic-write,
flush, and ordering behavior. A correct implementation is substantial and can
be inappropriate for an early single-writer store.

## Derived work

- [OTP-like system services layer](../20-notes/otp-like-system-services-layer.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
- [OTP-like system-services contract inquiry](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
- [2026-09-03 OTP-like system-services deep dive](../50-journal/2026-09-03-otp-like-system-services-deep-dive.md)
