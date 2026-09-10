---
title: "Session authentication, reconnect, and trust revalidation"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Session authentication, reconnect, and trust revalidation

This study decomposes [Network endpoint and protocol services](../network-endpoint-and-protocol-services.md).

Research question: What identity and replay state can survive path change, reconnect or credential rotation?

## Research basis and status

QUIC path migration differs from creating a new connection; credential delivery
alone does not authenticate a network session. [1](../../../30-sources/iyengar-thomson-2021-quic.md) [2](../../../30-sources/spiffe-project-2026-workload-api.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The session engine owns negotiated protocol, peer identity, connection and path
generations, credential/trust revisions and replay state. Endpoint authority defines
permitted communication; a selected handshake profile must establish possession and
transcript binding.

### Admission, transitions and completion

Separate protocol-supported path migration inside one authenticated connection from
reconnect after connection loss. Reconnect creates fresh transport state and
wire-visible identity according to the protocol. Logical operation IDs may continue
under application retry rules, but old stream credits and acknowledgements cannot.

### Failure and adversarial behavior

Credential removal does not automatically terminate established sessions. Apply
declared reauthentication or drain policy at trust changes. Early data requires
explicit replay-safe operation classification. Opaque session IDs cannot serve as
ordered global epochs or as proof of exclusive service ownership.

### Alternatives and unresolved tradeoffs

Long-lived sessions tolerate issuer outages but delay policy changes; frequent
reauthentication increases dependency and handshake cost. This study does not select
TLS, a crypto library or an attestation scheme; those need separate compatibility
and hostile-wire qualification.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Replay frames from a closed connection into a reconnect and verify transport/session identity rejects them.
- Rotate credentials during a legitimate path migration; preserve valid connection state while enforcing the declared trust-removal policy.

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

1. [QUIC RFC 9000](../../../30-sources/iyengar-thomson-2021-quic.md).
2. [SPIFFE Workload API](../../../30-sources/spiffe-project-2026-workload-api.md).
