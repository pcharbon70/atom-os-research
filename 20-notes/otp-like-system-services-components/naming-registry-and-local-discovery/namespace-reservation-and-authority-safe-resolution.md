---
title: "Namespace reservation and authority-safe resolution"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Namespace reservation and authority-safe resolution

This study decomposes [Naming, registry, and local discovery](../naming-registry-and-local-discovery.md).

Research question: What does resolving a name authorize, and who may reserve it?

## Research basis and status

Object capabilities distinguish designation with authority from ambient name lookup;
revisioned stores supply consistency, not permission. [1](../../../30-sources/miller-et-al-2003-capability-myths.md) [2](../../../30-sources/etcd-project-2026-api-guarantees.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The namespace service owns canonical naming rules, reservation ownership, quotas and
visibility policy. Stable names, service identity, object incarnation and invocation
facets are distinct. A resolver cannot create authority simply by recognizing a
service name.

### Admission, transitions and completion

Reserve names under a namespace-specific capability before service preparation.
Validate grammar, normalization, length and collision rules without atom interning
arbitrary external input. Resolution returns a generation-bound candidate and only
the operation facet allowed by the caller's delegation ceiling.

### Failure and adversarial behavior

Name squatting, Unicode aliases and hash flooding threaten both authority and
capacity. A found binding must not let an unauthorized caller invoke the service or
inspect private metadata. Receiver-side generation checks remain necessary because
lookup and use are separate operations.

### Alternatives and unresolved tradeoffs

Pre-derived capabilities avoid repeated discovery and reduce namespace exposure.
Dynamic names help replaceable services but require consistency and disclosure
policy. OTP atom registration belongs in a bounded compatibility namespace rather
than defining the native naming grammar.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Reserve visually confusable or canonically equivalent names under different owners and verify deterministic collision policy.
- Resolve through read-only namespace authority and attempt an unauthorized service operation; no authority amplification is permitted.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Application lifecycle and dependency orchestration](../application-lifecycle-and-dependency-orchestration/README.md) — coordinates readiness, publication and drain.
- [Distributed membership, discovery, and authoritative coordination](../distributed-membership-discovery-and-authoritative-coordination/README.md) — separates candidate discovery from authoritative ownership.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [Capability myths demolished](../../../30-sources/miller-et-al-2003-capability-myths.md).
2. [etcd API guarantees](../../../30-sources/etcd-project-2026-api-guarantees.md).
