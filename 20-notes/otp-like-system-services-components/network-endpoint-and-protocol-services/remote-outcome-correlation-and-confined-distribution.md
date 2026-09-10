---
title: "Remote outcome correlation and confined distribution"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Remote outcome correlation and confined distribution

This study decomposes [Network endpoint and protocol services](../network-endpoint-and-protocol-services.md).

Research question: How can remote messaging preserve uncertainty and limit compatibility-peer authority?

## Research basis and status

RIFL requires durable result rendezvous; standard Erlang distribution assumes a
trusted peer set rather than per-operation confinement. [1](../../../30-sources/lee-et-al-2015-rifl.md) [2](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The gateway owns protocol decoding, peer/session mapping, bounded compatibility
state and authorized native endpoints. Applications or their outcome service own
effect commitment. Packet delivery, peer admission and durable application
completion are separate proof points.

### Admission, transitions and completion

Translate only approved remote operations into native capabilities. Bind application
acknowledgements to logical operation, digest, service identity and protocol
profile. After reconnect, query durable status or retry under declared idempotency
rules. Preserve outcome identity even though the transport correlation changes.

### Failure and adversarial behavior

A transport acknowledgement cannot prove that a request parsed or committed. Gateway
death leaves accepted remote work unresolved. Atom-table growth, forged references
and ambient spawn/inspection operations require explicit limits or rejection; TLS
authentication alone does not remove distribution's trust assumptions.

### Alternatives and unresolved tradeoffs

A trusted-cell OTP adapter improves compatibility but has a wider authority surface
than native typed protocols. Keep that boundary explicit and differential-test
selected semantics. Native operation-status APIs are stronger only where their
actual sinks participate.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Acknowledge bytes then crash the peer before application admission; the client must not observe ApplicationCommitted.
- Use a trusted-cell peer to request an undelegated native operation; decoding success cannot create the missing capability.

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

1. [RIFL](../../../30-sources/lee-et-al-2015-rifl.md).
2. [OTP 29.0.6 system-services documentation](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md).
