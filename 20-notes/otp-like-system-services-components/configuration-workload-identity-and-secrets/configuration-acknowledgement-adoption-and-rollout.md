---
title: "Configuration acknowledgement, adoption, and rollout"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Configuration acknowledgement, adoption, and rollout

This study decomposes [Configuration, workload identity, and secrets](../configuration-workload-identity-and-secrets.md).

Research question: How can a controller distinguish a valid candidate from the configuration actually in use?

## Research basis and status

xDS ACK expresses validity and intent, not successful application; NACK need not
mean every resource was rejected. [1](../../../30-sources/envoy-project-2026-xds-protocol.md) [2](../../../30-sources/sun-et-al-2024-anvil.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The adoption tracker owns candidate versions, service incarnation, validation
response and independently reported active digest. Stream nonces correlate responses
only within that stream; they are not durable activation identities.

### Admission, transitions and completion

Prepare derived state privately and report validation separately from the safe-point
adoption receipt. A native complete-snapshot profile may reject the whole candidate,
but that is stronger than generic xDS partial-resource behavior. Reconnect
advertises actual held and active revisions; unknown base state triggers refetch.

### Failure and adversarial behavior

A service may ACK and then crash, or adopt while its reply is lost. The controller
must reobserve rather than count ACKs as a rollout barrier. Cross-service invariants
require shared-generation fencing or a specified mixed-version contract; a published
config pointer alone cannot guarantee them.

### Alternatives and unresolved tradeoffs

Immediate independent adoption maximizes availability but tolerates version skew.
Coordinated activation reduces skew while adding pause and recovery complexity.
Choose per invariant and retain the last usable generation until adoption and
rollback obligations are settled.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- ACK then crash before safe-point adoption; the controller must still report the previous active digest or Unknown.
- NACK one member of a multi-resource update; prove the native all-or-nothing policy explicitly instead of inferring it from xDS.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Network endpoint and protocol services](../network-endpoint-and-protocol-services/README.md) — separates transport session state from application outcomes.
- [Release, update, rollback, and state migration](../release-update-rollback-and-state-migration/README.md) — coordinates code/state transitions and retention.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [xDS protocol](../../../30-sources/envoy-project-2026-xds-protocol.md).
2. [Anvil](../../../30-sources/sun-et-al-2024-anvil.md).
