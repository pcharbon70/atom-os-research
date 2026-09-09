---
title: "Service loss, uncertainty and supervisor handoff"
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

# Service loss, uncertainty and supervisor handoff

This study decomposes [Failure translation and the OTP boundary](../failure-translation-and-the-otp-boundary.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Crash-only design needs state and retry assumptions; failure suspicion does not justify replaying arbitrary external effects. [1](../../../30-sources/chandra-toueg-1996-failure-detectors.md), [2](../../../30-sources/candea-fox-2003-crash-only-software.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. The runtime implements observations and actor termination; OTP-like services choose restart policy, and an outer service handles runtime corruption.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own the translation from service/gateway operation evidence into runtime events. The operation owner retains request disposition; the supervisor receives enough identity and uncertainty to choose reconciliation, retry or escalation. The runtime does not implement application restart strategies.

### Admission, transitions and completion

Before publication, release private preparation and report refusal. After publication, use protocol-proven completion/nonexecution if available; otherwise preserve uncertainty even when an acceptance acknowledgement was never seen. Deliver the compatible port/relation projection plus an authorized diagnostic reference.

### Failure and adversarial behavior

A service process disappearing says nothing by itself about device state or a durable write. Automatically retrying an indeterminate request can duplicate effects. An old completion may close its old ledger entry but must not act as a response for a replacement request.

### Alternatives and unresolved tradeoffs

Service-specific idempotency keys and durable result lookup can support stronger recovery. They require explicit retention and atomicity and belong to that service protocol. A generic runtime retry loop is not an adequate substitute.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Lose a service immediately after submission and before acknowledgement.
- Restart caller and service, then replay the old result against both new generations.
- Verify supervision receives uncertainty without an implicit retry being launched.

Record the exact profile, tested revision, schedule/input bounds and resource
observations before claiming this contract holds. A semantic pass does not
establish latency or corruption containment.

## Connections

- [Component service index](README.md) — sibling responsibilities and shared boundaries.
- [Actor cleanup ownership](../actor-identity-lifecycle-and-process-state/exit-cursor-and-process-state-snapshots.md) — a contract this service must compose with.
- [Independent evidence custody](../observability-deterministic-testing-and-crash-evidence/watchdog-evidence-and-external-crash-custody.md) — a contract this service must compose with.
- [Open runtime inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — unresolved design and evidence.
- [Research session](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — source manifest and reading limitations.

## Sources

1. [Unreliable failure detectors](../../../30-sources/chandra-toueg-1996-failure-detectors.md).
2. [Crash-only software](../../../30-sources/candea-fox-2003-crash-only-software.md).
