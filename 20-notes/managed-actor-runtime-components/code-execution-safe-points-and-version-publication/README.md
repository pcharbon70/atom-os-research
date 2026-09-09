---
title: "Code execution, safe points and version publication: internal services"
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

# Code execution, safe points and version publication: internal services

## Purpose

Decompose the [parent component](../code-execution-safe-points-and-version-publication.md) into independently
reviewable research contracts. These 6 studies separate state owners,
visibility decisions and residual lifetimes; they are not implementation phases.

## What belongs here

Keep service-level ownership, protocol alternatives, source findings, failure
cases and falsifiers here. Preserve the parent as the integrated component
model. Language execution and code-version visibility belong to the runtime; executable-page publication consumes the lower kernel's complete W^X and instruction-fetch contract.

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

- [Reference interpreter and language-observation oracle](reference-interpreter-and-language-observation-oracle.md) — covers a checked execution path over immutable validated instructions, including calls, tail calls, exceptions and BIF dispatch.
- [Canonical safe-point and native helper state](canonical-safe-point-and-native-helper-state.md) — covers the canonical activation schema: code generation, continuation, live registers, stack roots, heap bounds, exception state, reductions and receive cursor.
- [Native emission, relocation and artifact validation](native-emission-relocation-and-artifact-validation.md) — covers writable nonexecutable staging pages, relocations, branch targets, code/root maps and the emitted artifact hash.
- [Sealed pages and executable-publication handoff](sealed-pages-and-executable-publication-handoff.md) — covers the candidate image's writer inventory, immutable page manifest and lower publication operation token.
- [Module index, on_load and current-generation commit](module-index-on-load-and-current-generation-commit.md) — covers inactive module indexes, export/fun bindings, pending initialization actor and serialized per-module commit.
- [Logical purge, fun invalidation and literal reclamation](logical-purge-fun-invalidation-and-literal-reclamation.md) — covers logical old-code eligibility, unloaded fun state, literal-copy queues and physically retired code generations.

## Cross-component boundaries

- [Verified instruction and root obligations](../compatibility-manifest-beam-loader-and-verifier/control-flow-root-and-operand-verifier.md) — shared ownership or observation boundary.
- [Retained literal ownership](../terms-private-heaps-shared-binaries-and-tracing-collection/shared-binary-literal-and-fragment-lifetimes.md) — shared ownership or observation boundary.
- [Runtime component inventory](../README.md) — all thirteen parent components.
- [Managed-runtime map](../../../10-maps/managed-actor-runtime.md) — selective research routes.
- [Open inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — decisions awaiting evidence.
- [Dated source manifest](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — exact session provenance.

## Maintaining this index

Inventory every direct child, link directories through their README, and keep
the parent, component inventory, map and session evidence connected. Add a new
service only for a distinct responsibility; do not split or merge to meet a
numerical quota. Do not turn research completion into checked implementation.
