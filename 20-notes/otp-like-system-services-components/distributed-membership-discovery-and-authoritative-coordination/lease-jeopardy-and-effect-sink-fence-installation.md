---
title: "Lease jeopardy and effect-sink fence installation"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Lease jeopardy and effect-sink fence installation

This study decomposes [Distributed membership, discovery, and authoritative coordination](../distributed-membership-discovery-and-authoritative-coordination.md).

Research question: When is a successor entitled to perform effects that an old owner may still attempt?

## Research basis and status

Chubby sequencers require resource-side checking; consensus leadership alone cannot
fence external effects. [1](../../../30-sources/burrows-2006-chubby.md) [2](../../../30-sources/ongaro-ousterhout-2014-raft.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The lease service owns grant identity and monotonic fencing order. Each effect sink
owns its accepted high-water fence and in-flight operations. The holder owns a
conservative deadline only within a declared timing model; these records are not
interchangeable.

### Admission, transitions and completion

Grant through authoritative coordination, enter jeopardy when renewal becomes
uncertain, close new work before the safe holder deadline and install a higher fence
at every required sink before successor exclusivity. Couple fence checking with
effect admission, then settle older accepted operations according to the sink's
protocol.

### Failure and adversarial behavior

Rejecting later stale requests does not prove an earlier accepted request aborted.
Device commands already issued may complete after takeover. If clock/pause bounds or
durable sink fencing are unavailable, time-only authority fails; require another
exclusion mechanism or refuse the operation.

### Alternatives and unresolved tradeoffs

Per-operation quorum barriers avoid some lease timing assumptions but still need
sink-side enforcement against delayed requests. Multi-sink ownership is not atomic
without a transfer protocol covering every sink. Choose availability tradeoffs
explicitly rather than claiming universal singleton behavior.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Pause the old holder beyond renewal uncertainty, grant a successor, then deliver its delayed old command; the sink must enforce the current fence.
- Let an old command cross admission before the fence changes; takeover must reconcile that effect, not label it absent.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Naming, registry, and local discovery](../naming-registry-and-local-discovery/README.md) — publishes current bindings and watch revisions.
- [Device-service policy and management](../device-service-policy-and-management/README.md) — settles hardware outcomes and buffer custody.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [Chubby](../../../30-sources/burrows-2006-chubby.md).
2. [Raft](../../../30-sources/ongaro-ousterhout-2014-raft.md).
