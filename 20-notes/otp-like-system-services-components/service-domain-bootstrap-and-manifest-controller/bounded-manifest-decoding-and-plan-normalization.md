---
title: "Bounded manifest decoding and plan normalization"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Bounded manifest decoding and plan normalization

This study decomposes [Service-domain bootstrap and manifest controller](../service-domain-bootstrap-and-manifest-controller.md).

Research question: How can service desired state be interpreted without acquiring authority or producing partial effects?

## Research basis and status

TOSCA separates typed representation from orchestration; its modeling capabilities
are not protected object capabilities. [1](../../../30-sources/oasis-2025-tosca-2.md) [2](../../../30-sources/miller-et-al-2003-capability-myths.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The decoder owns an immutable input snapshot, import digests, schema profile,
diagnostics budget and normalized plan. It runs without device, process-creation or
mutable discovery authority. Imported service names are unresolved requirements, not
ambient capability lookups.

### Admission, transitions and completion

Bound bytes, nesting, imports, nodes and edges before expansion. Canonicalize
identities and detect duplicates before computing the plan digest. Resolve interface
versions and typed dependency relations; retain provenance for every derived value.
Acceptance returns a closed plan and explicit unsatisfied constraints, never a
partly activated graph.

### Failure and adversarial behavior

A valid signature can cover an unaffordable graph or excessive authority request.
Reject integer overflow in aggregate budgets, ambiguous encodings and digest
substitution. A resolver restart discards temporary analysis rather than executing
cached callbacks.

### Alternatives and unresolved tradeoffs

A rich orchestration language improves expressiveness but enlarges trusted
interpretation. Prefer a small declarative profile; unresolved dynamic discovery
must become a separately authorized reconciliation input. The exact canonical
encoding and evolution rules remain open.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Expand a small manifest into excessive imports and require bounded rejection without any adapter call.
- Permute equivalent input ordering and test deterministic plans; conflicting duplicate identities must fail, not silently overwrite.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Application lifecycle and dependency orchestration](../application-lifecycle-and-dependency-orchestration/README.md) — coordinates readiness, publication and drain.
- [Naming, registry, and local discovery](../naming-registry-and-local-discovery/README.md) — publishes current bindings and watch revisions.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [TOSCA 2.0](../../../30-sources/oasis-2025-tosca-2.md).
2. [Capability myths demolished](../../../30-sources/miller-et-al-2003-capability-myths.md).
