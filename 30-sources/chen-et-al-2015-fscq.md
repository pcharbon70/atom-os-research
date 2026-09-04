---
title: "Using Crash Hoare Logic for certifying the FSCQ file system"
kind: source
created: "2026-09-04"
authors:
  - "Haogang Chen"
  - "Daniel Ziegler"
  - "Tej Chajed"
  - "Adam Chlipala"
  - "M. Frans Kaashoek"
  - "Nickolai Zeldovich"
published: "2015-10-04"
citation_key: "chen-et-al-2015-fscq"
container: "Proceedings of the 25th Symposium on Operating Systems Principles"
edition: "SOSP '15, pages 18–37"
isbn: "978-1-4503-3834-9"
doi: "10.1145/2815400.2815402"
url: "https://doi.org/10.1145/2815400.2815402"
accessed: "2026-09-04"
tags:
  - crash-consistency
  - file-systems
  - formal-verification
  - recovery
  - storage
aliases:
  - "FSCQ paper"
  - "Crash Hoare Logic paper"
---

# Using Crash Hoare Logic for certifying the FSCQ file system

## Reference

Haogang Chen, Daniel Ziegler, Tej Chajed, Adam Chlipala, M. Frans Kaashoek,
and Nickolai Zeldovich. “[Using Crash Hoare Logic for Certifying the FSCQ File
System](https://pdos.csail.mit.edu/6.828/2018/readings/fscq-sosp15.pdf).”
*Proceedings of the 25th Symposium on Operating Systems Principles (SOSP
'15)*, pages 18–37, 2015. DOI
[10.1145/2815400.2815402](https://doi.org/10.1145/2815400.2815402).

## Research question or contribution

FSCQ asks how an implementation can be proved correct not only from one normal
precondition to one normal postcondition, but after a crash at any intermediate
write and after additional crashes during recovery. The paper introduces Crash
Hoare Logic (CHL), proves a write-ahead log, and builds a file system whose
machine-checked specification includes crash behavior.

## Method

The authors embed CHL in Coq, specify asynchronous disk writes and recovery
semantics, implement and prove the FscqLog transactional layer and a subset of
POSIX, extract a Haskell implementation, run it through FUSE, and evaluate
correctness tests and performance. The proof checker validates the mechanized
proof, while the compiler, extracted runtime, Haskell/FUSE glue, Linux, and
hardware remain in the end-to-end trusted base.

## Findings

- Ordinary pre/post specifications omit the states visible when execution
  stops between writes. CHL adds a crash condition and a recovery procedure,
  and its execution model allows recovery itself to crash and restart.
- The certified log converts asynchronous disk writes into an all-or-nothing
  transaction abstraction. Recovery checks a durable commit record, repeats
  committed updates, discards uncommitted log content, and is designed to be
  idempotent.
- Logical address spaces let higher layers reason about disjoint storage
  regions and reuse the log's atomicity theorem instead of reopening every
  low-level crash interleaving.
- Distinguishing normal completion from recovered completion permits stronger
  postconditions: a normally completed operation took effect, while a crashed
  operation may recover to either the prior or committed state according to
  the proven boundary.
- The system was usable for a teaching-file-system feature set, but its
  synchronous design was slower than ext4 with synchronous data journaling in
  the reported build workload. Proofs and specifications required substantially
  more effort than implementation.

## Relevance

Atom OS durable services should specify a crash condition for every persistence
step rather than documenting only the happy-path state machine. The first
storage profile can expose append, barrier, atomic sector or record, and
checkpoint-publication assumptions explicitly; build one small WAL over that
profile; and make replay, undo, checkpoint selection, and result-ledger cleanup
idempotent under repeated failure.

FSCQ also informs update and audit components. A release switch or audit chain
head is safe only if its publication record has a defined recovered state after
each torn or reordered write. This does not require adopting FSCQ as the Atom
OS file system, but it does require the same style of normal, crash, and
recovery contract plus fault injection at every persistence boundary.

## Limits

FSCQ proves a particular file-system subset under its formal disk model. It
lacks multiprocessor support and deferred durability in the described version,
and the running system includes unverified extraction and host components. The
proof does not establish behavior for flash translation layers, lying device
caches, media loss, malicious storage, distributed transactions, or application
effects outside the logged store. Atom OS must validate its target-specific
storage contract and cannot infer that a formally similar design is correct.

## Derived work

- [Durable state, transactions, and outcome recovery](../20-notes/otp-like-system-services-components/durable-state-transactions-and-outcome-recovery.md)
- [Release, update, rollback, and state migration](../20-notes/otp-like-system-services-components/release-update-rollback-and-state-migration.md)
- [Observability, audit, alarms, and operator control](../20-notes/otp-like-system-services-components/observability-audit-alarms-and-operator-control.md)
- [OTP-like system-services contract inquiry](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
