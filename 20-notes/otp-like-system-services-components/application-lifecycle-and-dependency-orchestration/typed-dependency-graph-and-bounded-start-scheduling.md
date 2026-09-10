---
title: "Typed dependency graph and bounded start scheduling"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Typed dependency graph and bounded start scheduling

This study decomposes [Application lifecycle and dependency orchestration](../application-lifecycle-and-dependency-orchestration.md).

Research question: Which dependencies constrain preparation, readiness, use and shutdown?

## Research basis and status

Typed graphs and OTP application dependencies provide different contracts; neither
turns callback success into native readiness. [1](../../../30-sources/oasis-2025-tosca-2.md) [2](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The compiler owns interface constraints and separate start-after, ready-after,
requires-interface, health-coupled and stop-before relations. It records whether a
dependency must already exist or may be activated. Group-leader membership remains a
compatibility concern, not native ownership.

### Admission, transitions and completion

Resolve each required interface and its capture revision. Reject cycles unless a
named rendezvous protocol can prepare the entire cyclic group; collapse only such
proved groups before scheduling. Execute independent vertices within a bounded
concurrency budget while retaining explicit readiness barriers.

### Failure and adversarial behavior

Optional absence must select a declared degraded mode. A graph can be syntactically
acyclic but contain a hidden callback wait cycle; readiness contracts must expose
these dependencies. Dynamic discovery invalidates the plan assumptions and requires
controlled replanning.

### Alternatives and unresolved tradeoffs

A flat ordered list simplifies implementation but overserializes unrelated services
and conceals dependency types. Arbitrary callback-driven startup is flexible but
difficult to validate. Exact graph limits and supported rendezvous protocols remain
unselected.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Create a cycle containing an optional edge and verify optionality does not silently justify deadlock.
- Compare serial and bounded-parallel schedules; both must expose the same valid publication set.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Service-domain bootstrap and manifest controller](../service-domain-bootstrap-and-manifest-controller/README.md) — reconciles desired service generations within the boot envelope.
- [Release, update, rollback, and state migration](../release-update-rollback-and-state-migration/README.md) — coordinates code/state transitions and retention.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [TOSCA 2.0](../../../30-sources/oasis-2025-tosca-2.md).
2. [OTP 29.0.6 system-services documentation](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md).
