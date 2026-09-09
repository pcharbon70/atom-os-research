---
title: "Compatibility manifest, BEAM loader and verifier: internal services"
kind: map
created: "2026-09-09"
tags:
  - actor-model
  - beam
  - managed-runtime
  - system-architecture
  - directory-index
aliases: []
---

# Compatibility manifest, BEAM loader and verifier: internal services

## Purpose

Decompose the [parent component](../compatibility-manifest-beam-loader-and-verifier.md) into independently
reviewable research contracts. These 4 studies separate state owners,
visibility decisions and residual lifetimes; they are not implementation phases.

## What belongs here

Keep service-level ownership, protocol alternatives, source findings, failure
cases and falsifiers here. Preserve the parent as the integrated component
model. Compatibility is a versioned language/runtime claim. A validated container or signed module is not proof of hostile-code isolation.

The split follows actual semantic and lifecycle distinctions, not a uniform
number of reports. All studies remain developing and their tests unexecuted.
They concern the full system architecture rather than a particular boot fixture.

## Shared contracts

- Preserve the parent compatibility profile; label restricted behavior and
  new APIs explicitly. Public OTP behavior and internal ERTS mechanisms are
  different evidence classes.
- Keep ordinary actors and automatic process-local tracing collection outside
  the privileged kernel. Native runtime corruption can compromise the domain.
- Bind operations to the relevant object, actor, domain and service generations;
  a transport session is not automatically a new external BEAM identity.
- Distinguish private preparation, publication, terminal semantic outcome and
  final storage reclamation. Cancellation and wakeups are not universal
  completion receipts.
- Charge deferred work and preserve finite recovery/evidence capacity. No
  literature throughput result establishes a hard latency bound here.

## Index

### Subdirectories

- None.

### Documents

- [Compatibility profile and conformance catalog](compatibility-profile-and-conformance-catalog.md) — covers the profile hash, accepted compiler/container/instruction versions, BIF/library surface and a catalog of observable cases.
- [Bounded container parser and private interning](bounded-container-parser-and-private-interning.md) — covers an immutable byte snapshot, checked chunk directory, bounded decode arena and provisional atom/import tables.
- [Control-flow, root and operand verifier](control-flow-root-and-operand-verifier.md) — covers a verification worklist and abstract state for initialized X/Y slots, stack depth, catch/try regions, valid branch targets and live roots.
- [Runtime-call effects and import binding](runtime-call-effects-and-import-binding.md) — covers generated call descriptors naming module/function/arity, allocation and GC effects, yielding/blocking class, required authority, exceptions and work accounting.

## Cross-component boundaries

- [Execution and root contract](../code-execution-safe-points-and-version-publication/canonical-safe-point-and-native-helper-state.md) — shared ownership or observation boundary.
- [Load-transaction accounting](../resource-accounting-and-overload-control/hierarchical-reservations-and-ledger-reconciliation.md) — shared ownership or observation boundary.
- [Runtime component inventory](../README.md) — all thirteen parent components.
- [Managed-runtime map](../../../10-maps/managed-actor-runtime.md) — selective research routes.
- [Open inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — decisions awaiting evidence.
- [Dated source manifest](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — exact session provenance.

## Maintaining this index

Inventory every direct child, link directories through their README, and keep
the parent, component inventory, map and session evidence connected. Add a new
service only for a distinct responsibility; do not split or merge to meet a
numerical quota. Do not turn research completion into checked implementation.
