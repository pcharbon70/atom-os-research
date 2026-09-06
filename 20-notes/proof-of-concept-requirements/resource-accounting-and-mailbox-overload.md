---
title: "Resource accounting and mailbox overload"
kind: note
created: "2026-09-06"
maturity: developing
tags:
  - operating-systems
  - proof-of-concept
  - requirements
aliases: []
---

# Resource accounting and mailbox overload

Requirement R11, M2–M4. Every admitted allocation and outstanding operation needs an owner, an account and a finite failure path. “Bounded heaps” is not a complete memory guarantee.

## Evidence and incompatible promises

The [OTP runtime limits documentation](../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md) explains that heap limits are checked at collection and that off-heap messages and shared binaries need separate attention. Ordinary send behavior cannot be replaced silently with a new successful-delivery or backpressure contract.

The [seL4 object-memory model](../../30-sources/sel4-foundation-2026-reference-manual.md) provides a precedent for explicit backing resources. Atom still needs its own complete kernel/runtime ledger and rules for transient allocations.

Finite memory, an actor that never receives, unlimited accepted sends and indefinite survival cannot all be guaranteed. Choose and document the overload outcome. This is a logical constraint, not an optimization that a faster queue can remove.

## Proposed two-level ledger

At the kernel boundary, account physical pages, page tables, domain/thread slots, capability slots, endpoint request/reply records, timers, fault records, console buffers and cleanup metadata. Each category has a hard capacity and a designated payer.

Inside the runtime, account private heaps, collector destination/work space, mailbox bodies and headers, copied messages in transit, shared binary backing, sub-binary retention, atoms, code/literals, actor records, links/monitors/aliases, timers, adapter continuations and allocator slack.

Separate physical backing from logical attribution to avoid counting the same shared page as multiple physical allocations. A quota may conservatively charge each consumer, but report that policy distinctly. Track committed, reserved, free and quarantined resources and show conservation at state transitions.

Reserve completion and error-reporting capacity before admitting an operation. The child cannot consume the outer recovery domain's pages, CPU or replacement slots. A diagnostic path that allocates from an already exhausted general pool is not reliable fault reporting.

## Mailbox admission policy

For the initial profile, define a finite message-size limit, per-process and per-runtime mailbox ceilings, and a deterministic action when reservation fails. Candidate actions include failing the sender under an explicit resource exception, terminating the receiver under a documented limit policy, or using an application-level credit protocol before ordinary sends.

Select one policy and mark any intentional deviation from upstream behavior in the compatibility manifest. Do not return apparent success while discarding an otherwise admitted local message. Do not block the only runtime scheduler waiting for a nonreceiving actor to free space.

Preserve the ordinary send return value where that behavior is claimed. Application-level acknowledged or credit-controlled delivery is a separate protocol, not an implicit change to the language operator.

Global resources deserve independent limits: distinct atom creation, repeated failed loads, retained code and shared binaries can exhaust the runtime while individual heaps look small. Reject unsupported dynamic atom/code behavior explicitly if the initial profile cannot bound it safely.

## Acceptance and next exploration

Run exhaustion tests for each ledger category, not only pages. Include simultaneous failures: a full mailbox during GC reservation, a full call pool during child death, and a full diagnostic ring while recovery replaces a service.

Use tiny configured capacities to force boundary paths. Verify that denied admission leaves no partial authority or ownership changes and that a completed failure releases the correct reservations. After each restart, compare ledgers against a baseline and explain bounded retained or quarantined objects.

The CLI's mem command should report actual categories and reservations, not a single allocator number labeled total memory. Pair ps and services with generation-aware domain and actor counts.

The next artifact is a machine-readable capacity/payer table and reservation-conservation tests. Numerical capacities remain test-profile choices until measured; the suggested 128 actors is an input, not an established supported maximum.

## Connections

[GC](private-heaps-and-tracing-garbage-collection.md), [IPC](capabilities-syscalls-and-bounded-ipc.md), [cleanup](domain-lifecycle-and-safe-reclamation.md) and [recovery](supervision-and-independent-recovery.md) must use the same ledger.
