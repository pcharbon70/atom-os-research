---
title: "Group candidate caches and bounded history"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Group candidate caches and bounded history

This study decomposes [Naming, registry, and local discovery](../naming-registry-and-local-discovery.md).

Research question: How should non-unique discovery remain useful without becoming an ownership oracle?

## Research basis and status

OTP groups and unique registration have different semantics; consistent coordination
caches depend on explicit validity rules. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md) [2](../../../30-sources/burrows-2006-chubby.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The candidate service owns group membership hints, selector policy, cached revisions
and bounded tombstones. It does not own exclusive leases or sink fences. The client
chooses a candidate under its endpoint and identity constraints.

### Admission, transitions and completion

Return membership with consistency class and observed revision or expiry profile.
Keep ordering promises local to the declared group. When a candidate fails,
re-resolve within a retry budget; do not reinterpret an old group member as current
exclusive owner. Bound negative caches and retired-incarnation metadata.

### Failure and adversarial behavior

A delayed join or stale cache must not resurrect an administratively removed
incarnation. Opaque boot nonces are equality identities, not ordered timestamps.
Under unbounded message delay, deletion requires authoritative re-admission or a
never-reused identity, not an invented safe tombstone timeout.

### Alternatives and unresolved tradeoffs

Eventual groups improve partition availability; unique authoritative bindings
simplify ownership. They must remain different result types. Caching can reduce
registry load, but shortening expiry increases refresh storms and lengthening it
increases stale routing.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Replay membership for a retired incarnation after tombstone collection and verify re-admission policy prevents resurrection.
- Lose authoritative coordination while group discovery works; candidate selection must not grant exclusive write authority.

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

1. [OTP 29.0.6 system-services documentation](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md).
2. [Chubby](../../../30-sources/burrows-2006-chubby.md).
