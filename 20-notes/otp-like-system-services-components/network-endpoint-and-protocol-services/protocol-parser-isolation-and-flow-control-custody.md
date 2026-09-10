---
title: "Protocol-parser isolation and flow-control custody"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Protocol-parser isolation and flow-control custody

This study decomposes [Network endpoint and protocol services](../network-endpoint-and-protocol-services.md).

Research question: Which resource bounds survive hostile frames, fragmented messages and slow consumers?

## Research basis and status

QUIC separates connection and stream credit; isolated queue architectures make
payload custody explicit. [1](../../../30-sources/iyengar-thomson-2021-quic.md) [2](../../../30-sources/heiser-et-al-2026-sddf-design.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The protocol service owns frame limits, reassembly state, stream counts,
retransmission storage, parser budgets and buffer return paths. Network drivers own
packet transport. Application codecs can occupy narrower failure domains than the
transport engine.

### Admission, transitions and completion

Reserve memory for admitted streams and reassembly before granting remote credit.
Validate lengths and state transitions before expansion or allocation. Propagate
slow-consumer pressure toward the peer; distinguish protocol credits from the
service's actual retained-memory accounting. Reserve finite close/error capacity.

### Failure and adversarial behavior

A small wire message may request excessive state or decompression. Reliable flow
control does not bound unrelated metadata unless each category is charged. A parser
crash must release or transfer tracked buffers without allowing stale callbacks to
return them twice.

### Alternatives and unresolved tradeoffs

Shared parsers reduce copies and scheduling overhead but enlarge the failure
boundary. Worker isolation limits compromise while requiring bounded handoff queues.
Select streaming versus complete-frame validation per codec and never infer safety
from the transport RFC alone.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Send many sparse fragments and incomplete streams at maximum credit; total retained state must stay within the admitted budget.
- Stall the application while delivering control frames; reliable data must not be silently overwritten and connection close must remain bounded.

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
2. [sDDF design](../../../30-sources/heiser-et-al-2026-sddf-design.md).
