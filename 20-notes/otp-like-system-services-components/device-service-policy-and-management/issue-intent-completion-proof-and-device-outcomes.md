---
title: "Issue intent, completion proof, and device outcomes"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Issue intent, completion proof, and device outcomes

This study decomposes [Device-service policy and management](../device-service-policy-and-management.md).

Research question: What can software honestly conclude after a driver crashes near a hardware command?

## Research basis and status

Queue ownership and durable result tracking support bookkeeping, but neither
atomically couples a software log to a hardware doorbell. [1](../../../30-sources/heiser-et-al-2026-sddf-design.md) [2](../../../30-sources/lee-et-al-2015-rifl.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The outcome service owns operation IDs, request digests, issue intents, observed
device sequences and class-specific completion proofs. Hardware may own effects that
outlive the driver. Durable logs record knowledge, not retroactive certainty about
physical execution.

### Admission, transitions and completion

Record intent before issue where the profile permits, then correlate command and
completion to the exact queue/reset generation. Distinguish NotIssued,
DeviceCompleted, MediaDurable or other class proof points. A cancel request becomes
terminal only when evidence shows it beat the effect boundary.

### Failure and adversarial behavior

Crash between intent and doorbell, or doorbell and issue receipt, is indeterminate
unless authoritative hardware state resolves it. Driver restart cannot justify
replaying actuator commands. A late completion may refine a pending outcome, but
must not complete a different request reusing a slot.

### Alternatives and unresolved tradeoffs

Per-command durable intent adds latency and wear; volatile tracking supplies a
weaker crash profile. Device-native operation IDs or authoritative status queries
can improve recovery. Each class must declare what is provable and which uncertainty
is unavoidable.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Crash immediately before and after the command write and compare observed outcomes against an independent device model.
- Lose completion after an irreversible effect; recovery must not report NotIssued or automatically issue again.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Network endpoint and protocol services](../network-endpoint-and-protocol-services/README.md) — separates transport session state from application outcomes.
- [Supervision and recovery policy](../supervision-and-recovery-policy/README.md) — owns restart admission, quarantine and escalation.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [sDDF design](../../../30-sources/heiser-et-al-2026-sddf-design.md).
2. [RIFL](../../../30-sources/lee-et-al-2015-rifl.md).
