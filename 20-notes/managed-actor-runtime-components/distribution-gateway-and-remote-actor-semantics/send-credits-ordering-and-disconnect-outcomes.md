---
title: "Send credits, ordering and disconnect outcomes"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - actor-model
  - beam
  - managed-runtime
  - system-architecture
aliases: []
---

# Send credits, ordering and disconnect outcomes

This study decomposes [Distribution gateway and remote actor semantics](../distribution-gateway-and-remote-actor-semantics.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Parallel channels can improve selected workloads; a disconnected session cannot prove application consumption or nonexecution. [1](../../../30-sources/meiklejohn-et-al-2019-partisan.md), [2](../../../30-sources/chandra-toueg-1996-failure-detectors.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Gateway authentication, transport sessions and BEAM node-incarnation identity are distinct. Compatible sends do not acquire delivery-completion results.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own byte/message/control credits, sender-order channel assignments and optional tracked-send receipts. Ordinary compatible send returns remain unchanged. Any accepted/completed/indeterminate result belongs to an explicitly separate extension with a named proof boundary.

### Admission, transitions and completion

Reserve before encoding, publish on a stable ordering path and return credits exactly once at their documented custody boundary. Changing channels requires a per-order-domain cutover or bounded merge. Disconnect terminates affected relations with the selected semantics and drains local custody records without asserting remote actor death.

### Failure and adversarial behavior

Gateway acceptance is not peer receipt; peer receipt is not actor consumption; consumption is not durable effect. Postpublication loss can be Indeterminate even before an acknowledgement. A generic nodedown event cannot claim that every earlier message has drained unless a real barrier establishes that ordering.

### Alternatives and unresolved tradeoffs

Per-sender channel affinity is simpler than sequence-merge buffers but may concentrate traffic. Extra channels can reduce head-of-line blocking while increasing credit and ordering state. Measure topology costs separately from semantic conformance.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Switch channels between ordered signals and detect any inversion.
- Disconnect at each receipt boundary and report only what that boundary proves.
- Duplicate acknowledgements and ensure credit totals and relation termination remain consistent.

Record the exact profile, tested revision, schedule/input bounds and resource
observations before claiming this contract holds. A semantic pass does not
establish latency or corruption containment.

## Connections

- [Component service index](README.md) — sibling responsibilities and shared boundaries.
- [Local order-preserving ingress](../signal-ingress-mailboxes-and-selective-receive/striped-ingress-order-and-node-reclamation.md) — a contract this service must compose with.
- [Disconnect knowledge and uncertainty](../failure-translation-and-the-otp-boundary/service-loss-uncertainty-and-supervisor-handoff.md) — a contract this service must compose with.
- [Open runtime inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — unresolved design and evidence.
- [Research session](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — source manifest and reading limitations.

## Sources

1. [PARTISAN](../../../30-sources/meiklejohn-et-al-2019-partisan.md).
2. [Unreliable failure detectors](../../../30-sources/chandra-toueg-1996-failure-detectors.md).
