---
title: "Membership epochs, tombstones, and federated candidates"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Membership epochs, tombstones, and federated candidates

This study decomposes [Distributed membership, discovery, and authoritative coordination](../distributed-membership-discovery-and-authoritative-coordination.md).

Research question: How can delayed advertisements remain harmless across reboot, removal and cell boundaries?

## Research basis and status

Weak membership and authenticated workload identity provide observations and
identity, not authoritative resource ownership. [1](../../../30-sources/dadgar-et-al-2018-lifeguard.md) [2](../../../30-sources/spiffe-project-2026-workload-api.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The membership service owns admitted identity, boot epoch, within-epoch incarnation
and sequence, removal revision and bounded candidate records. Federation gateways
own which observations cross trust domains; they do not extend local authority
transitively.

### Admission, transitions and completion

Authenticate advertisements and bind them to the currently admitted epoch. Compare
monotonically ordered incarnations only within their defined epoch. An opaque new
boot nonce requires a newer authoritative re-admission decision, not lexicographic
comparison. Export candidates with explicit staleness and protocol constraints.

### Failure and adversarial behavior

Tombstones can be collected only under a delay/identity-retirement rule that
prevents resurrection. Without a message lifetime bound, require never-reused epochs
and authoritative admission. A compromised authenticated member can lie about
reachability; callers must still authenticate and authorize actual operations.

### Alternatives and unresolved tradeoffs

Global all-to-all membership improves convenience but expands traffic and correlated
failure. Scoped cells and selective gateways limit reach while requiring explicit
cross-cell transfer semantics. Gossip convergence does not create a globally ordered
membership transaction.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Restore an old node image and replay advertisements after administrative removal; stale epochs must not rejoin automatically.
- Partition two cells, mutate candidate views independently and reconnect; merged hints must not transfer an exclusive lease.

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

1. [Lifeguard](../../../30-sources/dadgar-et-al-2018-lifeguard.md).
2. [SPIFFE Workload API](../../../30-sources/spiffe-project-2026-workload-api.md).
