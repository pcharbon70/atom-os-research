---
title: "Endpoint broker, routing, and resolver authority"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Endpoint broker, routing, and resolver authority

This study decomposes [Network endpoint and protocol services](../network-endpoint-and-protocol-services.md).

Research question: How are network destinations selected without making connectivity ambient authority?

## Research basis and status

Capability delegation scopes permitted operations; a transport connection does not
define application authorization. [1](../../../30-sources/miller-et-al-2003-capability-myths.md) [2](../../../30-sources/iyengar-thomson-2021-quic.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The broker owns network namespace, bind/listen/connect/raw-packet facets, peer
constraints, routing policy and connection budgets. Resolver results are candidate
addresses. Workload authentication and operation authorization remain separate
decisions.

### Admission, transitions and completion

Authorize address ranges, ports, direction and protocol before reserving an
endpoint. Bind the resulting handle to caller and endpoint generations. Resolve
through an approved policy and verify the expected peer identity at the eventual
secure-channel boundary; routing success cannot substitute for that check.

### Failure and adversarial behavior

DNS rebinding, address reuse or a peer moving paths must not enlarge authority. A
valid route to a prohibited target still fails policy. Raw traffic privileges
require a distinct facet because they can bypass higher-level parsing, peer and
quota controls.

### Alternatives and unresolved tradeoffs

A centralized broker makes policy consistent but can bottleneck connection churn.
Cached attenuated endpoint handles reduce traffic if lifetime and revocation are
enforced. The exact routing and secure-channel profile remains deliberately
unselected by this decomposition.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Change the resolver answer between authorization and connect; the final destination and peer must still satisfy the original constraints.
- Present a connect-only handle to bind, listen or emit raw packets; each authority boundary must reject it.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Configuration, workload identity, and secrets](../configuration-workload-identity-and-secrets/README.md) — supplies configuration adoption and credential-generation evidence.
- [Durable state, transactions, and outcome recovery](../durable-state-transactions-and-outcome-recovery/README.md) — retains committed state and retry-result responsibility.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [Capability myths demolished](../../../30-sources/miller-et-al-2003-capability-myths.md).
2. [QUIC RFC 9000](../../../30-sources/iyengar-thomson-2021-quic.md).
