---
title: "Interrupt and timer binding lifetimes"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Interrupt and timer binding lifetimes

What lifetime object connects an authorized consumer to asynchronous architecture events?

## Research basis and status

Capability-mediated interrupts and bounded event mechanisms provide precedents, but cancellation completion must be composed explicitly. [1](../../../30-sources/sel4-foundation-2026-reference-manual.md), [2](../../../30-sources/mckenney-slingwine-1998-read-copy-update.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../memory-mappings-and-architecture-resource-bindings.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

An IRQBinding is one accounted aggregate over the lower fabric's source, route and delivery views. A timer binding separately names a deadline operation, target notification, clock era and cancellation epoch. A timer is not assumed to own a unique hardware interrupt unless the selected profile says so.

### Admission, transitions and completion

Authorize the source and destination before route installation, then publish the binding's generation after lower-layer setup completes. Closure denies new binding effects and requests masking, cancellation or rerouting using the applicable backend. Retain the target and event records until pending or in-service deliveries are drained or safely rejected by exact generation checks.

### Failure and adversarial behavior

Masking future interrupts does not prove an already delivered handler has returned. Canceling a software timer queue entry does not invalidate an already queued notification. Reassigning a source while an old event still names reusable storage can corrupt a replacement even when no new device interrupt is generated.

### Alternatives and unresolved tradeoffs

A single aggregate simplifies IRQ ownership, while lower architecture views remain necessary for hardware programming. Timer multiplexing reduces privileged resources but makes cancellation and clock-conversion identity more important. Their teardown nodes must remain distinct even when they share one hardware vector.

## Verification obligations

Race deadline expiry with cancel and notification close; deliver a stale interrupt after rebinding; delay in-service completion. Require exact old/new attribution and retention until all applicable nodes join the reaper's completion graph.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Effect ledger and dependency graph](../teardown-revocation-and-safe-reclamation/effect-ledger-and-dependency-graph.md) — Every admitted binding contributes its completion obligations.
- [Lease takeover and operation adoption](../failure-boundaries-and-recovery-topology/lease-takeover-and-operation-adoption.md) — Takeover must preserve valid old-operation evidence.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [seL4 reference manual, version 16.0.0](../../../30-sources/sel4-foundation-2026-reference-manual.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Read-copy update: Using execution history to solve concurrency problems](../../../30-sources/mckenney-slingwine-1998-read-copy-update.md) — comparative evidence; its methods and limits are recorded in the source note.
