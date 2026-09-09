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

This directory collects the detailed architecture research for the eleven
components numbered 0 through 10 in the [minimal privileged kernel
layer](../minimal-privileged-kernel-layer.md).

All eleven components now have internal-service decompositions: 54 reports
across eleven component-named subdirectories. The parent reports remain the
integrated contracts. Documented coverage is not implementation or proof.

## What belongs here

Put component-level architecture syntheses here when they develop one part of
the capability-microkernel boundary in enough detail to require its own
evidence, object model, state machine, failure analysis, implementation path,
and verification plan. Keep the integrated kernel contract and broader
operating-system syntheses in the parent notes directory.

## Index

### Subdirectories

- [0. Bootstrap and root-authority handoff: internal services](bootstrap-and-root-authority-handoff/README.md) — 5 reports. Turn sealed machine facts and an authorized construction description into a private, audited authority graph, then permanently remove bootstrap admission.
- [1. Typed object storage and explicit memory: internal services](typed-object-storage-and-explicit-memory/README.md) — 5 reports. Give every privileged object explicit backing, accounting and lifetime, with allocator reuse dependent on completed teardown rather than capability count alone.
- [2. Capability spaces and authority: internal services](capability-spaces-and-authority/README.md) — 5 reports. Resolve current typed authority, fund its propagation and preserve effect-bearing lifetime dependencies through logical closure and eventual revocation.
- [3. Protection domains, threads and address spaces: internal services](protection-domains-threads-and-address-spaces/README.md) — 5 reports. Make domains exact execution-stop boundaries while keeping accounting, actors, service identity and recovery policy separate.
- [4. Bounded invocation and transport: internal services](bounded-invocation-and-transport/README.md) — 5 reports. Keep small protected calls, coalescing notifications and shared-buffer transport finite, explicitly funded and honest about accepted effects.
- [5. Scheduling contexts and temporal authority: internal services](scheduling-contexts-and-temporal-authority/README.md) — 5 reports. Conserve execution budget across binding and donation, separately fund causal work and recovery, and avoid confusing availability budgets with timing confidentiality.
- [6. Memory mappings and architecture-resource bindings: internal services](memory-mappings-and-architecture-resource-bindings/README.md) — 6 reports. Bind current authority to lower-layer mapping, interrupt and device effects while preserving exact generations and profile-specific completion evidence.
- [7. Fault capture and containment: internal services](fault-capture-and-containment/README.md) — 4 reports. Produce bounded fault evidence, route it independently and grant only the narrow repair or termination authority justified by the fault contract.
- [8. Failure boundaries and recovery topology: internal services](failure-boundaries-and-recovery-topology/README.md) — 5 reports. Keep recovery authority and resources outside the failed scope, fence replacement managers, and leave application-state recovery policy unprivileged.
- [9. Teardown, revocation and safe reclamation: internal services](teardown-revocation-and-safe-reclamation/README.md) — 4 reports. Turn logical closure into a charged, resumable proof of effect completion or exact quarantine custody before the allocator can reuse backing.
- [10. Observability and crash evidence: internal services](observability-and-crash-evidence/README.md) — 5 reports. Expose bounded, authorized operational evidence and enrich the lower architecture's single terminal record without adding unsafe crash-time dependencies.

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

## Reading and evidence

Use the [minimal-kernel map](../../10-maps/minimal-privileged-kernel.md) for
selective cross-service routes. Each report separates comparative evidence,
proposed owned state, transitions, failure cases, alternatives and unexecuted
verification obligations. The [session journal](../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md)
records six newly introduced and twenty-one reused sources, including scientific
papers, official technical articles and first-party engineering blogs.

The most consequential open joins are product-authority inheritance, domain
stop checkpoints, passive-call drainage, independent recovery escrow,
operation-epoch adoption, exact DMA quarantine and snapshot/crash-evidence
lifetime. The [contract inquiry](../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
tracks the evidence still needed. Literature coverage does not close it.

## Maintaining this index

Inventory every direct component note and service directory, preserve the 0-through-10 numbering,
and update the parent notes index and minimal-kernel map whenever a component
is added, renamed, moved, archived, or superseded.
