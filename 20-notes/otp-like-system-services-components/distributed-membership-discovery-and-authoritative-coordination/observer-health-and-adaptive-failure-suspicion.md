---
title: "Observer health and adaptive failure suspicion"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Observer health and adaptive failure suspicion

This study decomposes [Distributed membership, discovery, and authoritative coordination](../distributed-membership-discovery-and-authoritative-coordination.md).

Research question: How can a slow failure detector avoid blaming healthy peers?

## Research basis and status

Lifeguard adjusts probing and suspicion using local-health heuristics; DAGOR
distinguishes local queue delay from downstream response time. [1](../../../30-sources/dadgar-et-al-2018-lifeguard.md) [2](../../../30-sources/zhou-et-al-2018-dagor.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The detector owns local probe progress, bounded suspicion timers, independently
sourced reports and observation confidence. It does not own authoritative membership
or exclusive leases. All observations bind the subject incarnation and the
observer's identity and epoch.

### Admission, transitions and completion

Measure local scheduling and receive progress before interpreting missing replies.
Use bounded adaptive suspicion and prioritize communicating suspicion to the
affected peer. Preserve independent-report identities so duplicates do not simulate
corroboration. Export evidence with uncertainty rather than a definitive crash
assertion.

### Failure and adversarial behavior

CPU saturation, packet loss and a stalled observer can generate correlated false
positives. Longer suspicion reduces some false failovers but delays real detection.
A malicious peer can send misleading health information; heuristics are not
Byzantine consensus or authenticated authority transfer.

### Alternatives and unresolved tradeoffs

Fixed timers are simpler and may suffice under strong scheduling bounds. Adaptive
detectors improve measured behavior in particular deployments but require local
calibration. Recovery policy must distinguish observation degradation from
permission to evict or reassign a resource.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Pause the observer only, then the subject only, under equal offered load; distinguish false suspicion and real-detection latency.
- Replay one corroborating message repeatedly and ensure it counts as one source, not an independent quorum.

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
2. [DAGOR](../../../30-sources/zhou-et-al-2018-dagor.md).
