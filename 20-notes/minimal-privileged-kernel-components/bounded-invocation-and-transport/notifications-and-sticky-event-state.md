---
title: "Notifications and sticky event state"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Notifications and sticky event state

How can a bounded wakeup primitive avoid both lost transitions and a false promise of event counting?

## Research basis and status

Notification-oriented IPC guidance separates synchronization from argument transfer. [1](../../../30-sources/heiser-2019-sel4-ipc-design.md), [2](../../../30-sources/sel4-foundation-2026-reference-manual.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../bounded-invocation-and-transport.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

A notification stores a bounded sticky bitset, generation, permitted producers and a finite waiter relation. Bits represent pending classes of work, not a count of occurrences or an authenticated transcript. The data source retains its own authoritative queue or condition.

### Admission, transitions and completion

Producers atomically OR permitted bits and arrange a wakeup under the notification's admission gate. A consumer atomically obtains and clears an observed set, then checks the underlying condition using its own synchronization protocol. Registering a waiter must serialize with signal publication so that a signal cannot disappear between checking state and sleeping.

### Failure and adversarial behavior

Two identical signals may coalesce legitimately. Software that interprets one bit as exactly one queued packet will lose work. Closing the object must prevent new waiter or producer admission while retaining already admitted signal effects; a stale generation must not wake a replacement service's waiter.

### Alternatives and unresolved tradeoffs

A counter supports quantity but needs overflow semantics and often duplicates a queue's state. Sticky bits keep the privileged object small, leaving event counts and payloads in explicit shared or private storage. Fanout requires separate bounded receiver state rather than an unbounded broadcast list.

## Verification obligations

Race signal, clear, waiter registration and close; send repeated signals while a consumer is suspended. Verify no missed persistent condition, explicit coalescing and bounded waiter storage. Demonstrate that consumers drain the real data source rather than assuming one wakeup per item.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Exclusive binding, donation and migration](../scheduling-contexts-and-temporal-authority/exclusive-binding-donation-and-migration.md) — Call acceptance and donation share a commit boundary.
- [Recipient fences and service publication](../failure-boundaries-and-recovery-topology/recipient-fences-and-service-publication.md) — Replacement must preserve old call outcomes.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [How to (and how not to) use seL4 IPC](../../../30-sources/heiser-2019-sel4-ipc-design.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [seL4 reference manual, version 16.0.0](../../../30-sources/sel4-foundation-2026-reference-manual.md) — comparative evidence; its methods and limits are recorded in the source note.
