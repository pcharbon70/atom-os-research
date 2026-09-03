---
title: "Managed actor runtime components"
kind: map
created: "2026-09-03"
tags:
  - actor-model
  - archive-navigation
  - directory-index
  - beam
  - virtual-machines
aliases:
  - "Managed runtime component notes"
---

# Managed actor runtime components (`managed-actor-runtime-components`)

## Purpose

This directory collects the detailed implementation research for the thirteen
components numbered 0 through 12 in the [managed actor runtime
layer](../managed-actor-runtime-layer.md).

## What belongs here

Put component-level architecture syntheses here when they develop one part of
the managed runtime in enough detail to require its own compatibility boundary,
evidence, objects, state machines, failure analysis, implementation program,
and verification plan. Keep the integrated runtime model and other broad
operating-system syntheses in the parent notes directory.

## Index

### Subdirectories

- None yet.

### Documents

- [0. Runtime-domain bootstrap and kernel adapter](runtime-domain-bootstrap-and-kernel-adapter.md) —
  develops a transactional, idempotent, capability-confined adapter as the
  runtime's only kernel-ABI consumer.
- [1. Compatibility manifest, BEAM loader, and verifier](compatibility-manifest-beam-loader-and-verifier.md) —
  defines versioned compatibility profiles, private staged parsing, structural
  and profile validation, immutable lowering, and atomic publication.
- [2. Actor identity, lifecycle, and process state](actor-identity-lifecycle-and-process-state.md) —
  develops generation-safe routing identities, transactional spawn, bounded
  exit cleanup, and precise link, monitor, alias, and resource ordering.
- [3. Terms, private heaps, shared binaries, and tracing collection](terms-private-heaps-shared-binaries-and-tracing-collection.md) —
  develops the term ownership model, private generational heaps, exact roots,
  collector reserve, immutable sharing, and memory accounting.
- [4. Signal ingress, mailboxes, and selective receive](signal-ingress-mailboxes-and-selective-receive.md) —
  separates physical ingress from logical mailbox order and develops atomic
  admission, selective-receive charging, correlation, and overload profiles.
- [5. Reduction scheduler and kernel scheduling contexts](reduction-scheduler-and-kernel-scheduling-contexts.md) —
  composes actor reductions, safe points, local queues, adaptive stealing, and
  NUMA hints with kernel-enforced scheduling budgets.
- [6. Timers, events, and asynchronous I/O integration](timers-events-and-asynchronous-io-integration.md) —
  develops hybrid timer queues, generation-safe cancellation, bounded expiry,
  one-shot event handling, and completion ownership.
- [7. Code execution, safe points, and version publication](code-execution-safe-points-and-version-publication.md) —
  develops the interpreter-first execution path, load-time lowering, W^X code
  publication, safe-point metadata, epochs, and old-code retirement.
- [8. Native work, ports, and drivers](native-work-ports-and-drivers.md) —
  makes isolated service domains the default native boundary and defines
  request, cancellation, incarnation, and trusted-NIF compatibility rules.
- [9. Distribution gateway and remote actor semantics](distribution-gateway-and-remote-actor-semantics.md) —
  develops authenticated, attenuated, credit-bound gateway sessions while
  preserving signal profiles, ordering scope, incarnations, and uncertainty.
- [10. Failure translation and the OTP boundary](failure-translation-and-the-otp-boundary.md) —
  separates typed runtime failure mechanisms from OTP restart policy and
  places runtime-domain recovery outside the failed runtime.
- [11. Resource accounting and overload control](resource-accounting-and-overload-control.md) —
  develops hierarchical reservations and ledgers, protected reserves,
  observable overload policy, and explicit ETS-like shared-table semantics.
- [12. Observability, deterministic testing, and crash evidence](observability-deterministic-testing-and-crash-evidence.md) —
  develops metered trace rings, deterministic choice schedules, replay scope,
  and preallocated cross-boundary crash records.

## Maintaining this index

Inventory every direct component note, preserve the 0-through-12 numbering,
and update the parent notes index and managed-runtime map whenever a component
is added, renamed, moved, archived, or superseded.
