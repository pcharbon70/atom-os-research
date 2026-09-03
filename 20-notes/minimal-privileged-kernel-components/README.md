---
title: "Minimal privileged kernel components"
kind: map
created: "2026-09-03"
tags:
  - archive-navigation
  - capabilities
  - directory-index
  - microkernels
  - operating-systems
aliases:
  - "Minimal-kernel component notes"
---

# Minimal privileged kernel components (`minimal-privileged-kernel-components`)

## Purpose

This directory collects the detailed implementation research for the eleven
components numbered 0 through 10 in the [minimal privileged kernel
layer](../minimal-privileged-kernel-layer.md).

## What belongs here

Put component-level architecture syntheses here when they develop one part of
the capability-microkernel boundary in enough detail to require its own
evidence, object model, state machine, failure analysis, implementation path,
and verification plan. Keep the integrated kernel contract and broader
operating-system syntheses in the parent notes directory.

## Index

### Subdirectories

- None yet.

### Documents

- [0. Bootstrap and root-authority handoff](bootstrap-and-root-authority-handoff.md) —
  turns validated boot facts and a declarative manifest into an auditable
  initial authority graph, then irreversibly seals temporary bootstrap power.
- [1. Typed object storage and explicit memory](typed-object-storage-and-explicit-memory.md) —
  makes every privileged object caller-backed, quota-charged, typed, and
  physically reusable only after its complete effect ledger has drained.
- [2. Capability spaces and authority](capability-spaces-and-authority.md) —
  develops typed, attenuable authority, bounded logical closure, incremental
  physical revocation, and lineage-preserving object creation.
- [3. Protection domains, threads, and address spaces](protection-domains-threads-and-address-spaces.md) —
  makes a protection domain the fixed admission and coordinated SMP stop
  boundary without confusing it with an actor, service, or recovery policy.
- [4. Bounded invocation and transport](bounded-invocation-and-transport.md) —
  gives protected calls, cancellation, replies, notifications, and shared
  queues explicit finite state, funding, terminal outcomes, and lifetimes.
- [5. Scheduling contexts and temporal authority](scheduling-contexts-and-temporal-authority.md) —
  represents CPU time as conserved capability-mediated budget and keeps an
  independently funded recovery path outside each supervised failure scope.
- [6. Memory mappings and architecture-resource bindings](memory-mappings-and-architecture-resource-bindings.md) —
  composes frames, virtual mappings, IRQs, timers, IOMMU state, DMA queues, and
  reset authority through generation-safe, completion-aware binding objects.
- [7. Fault capture and containment](fault-capture-and-containment.md) —
  normalizes faults into bounded typed evidence and separately authorizes
  repair, observation, thread termination, and domain-fatal escalation.
- [8. Failure boundaries and recovery topology](failure-boundaries-and-recovery-topology.md) —
  keeps recovery policy outside the failed component, precommits independent
  authority and reserves, and makes external-effect reconciliation explicit.
- [9. Teardown, revocation, and safe reclamation](teardown-revocation-and-safe-reclamation.md) —
  separates constant-work logical closure from charged traversal, hardware
  quiescence, quarantine, sanitization, and generation-safe reuse.
- [10. Observability and crash evidence](observability-and-crash-evidence.md) —
  provides capability-scoped bounded telemetry and an independently reserved
  higher-level evidence layout that enriches the architecture layer's one
  sealed terminal record without turning tracing into ambient authority.

## Maintaining this index

Inventory every direct component note, preserve the 0-through-10 numbering,
and update the parent notes index and minimal-kernel map whenever a component
is added, renamed, moved, archived, or superseded.
