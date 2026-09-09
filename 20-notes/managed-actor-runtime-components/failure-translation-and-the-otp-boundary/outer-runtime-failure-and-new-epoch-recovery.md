---
title: "Outer runtime failure and new-epoch recovery"
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

# Outer runtime failure and new-epoch recovery

This study decomposes [Failure translation and the OTP boundary](../failure-translation-and-the-otp-boundary.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

A component cannot be its own reliable recovery authority after corruption; watchdog silence alone is only a liveness observation. [1](../../../30-sources/candea-fox-2003-crash-only-software.md), [2](../../../30-sources/chandra-toueg-1996-failure-detectors.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. The runtime implements observations and actor termination; OTP-like services choose restart policy, and an outer service handles runtime corruption.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own the runtime-facing evidence and shutdown protocol, while the outer supervisor owns domain freeze, teardown and successor launch. Domain epoch separates every old actor, timer, native request and route from the replacement.

### Admission, transitions and completion

On suspicion, request independent budget/fault evidence and apply external policy. On authenticated domain fault, stop admissions and freeze or kill without relying on runtime cooperation. Preserve a minimal external record, revoke old routes and publish a successor only under fresh authority and identity.

### Failure and adversarial behavior

Memory recovered from a corrupted domain is evidence, not a trusted checkpoint. Restart cannot restore arbitrary actor state or reverse external effects. A stuck old participant must not be marked quiescent simply to unblock code or buffer reclamation.

### Alternatives and unresolved tradeoffs

Several smaller runtime domains limit correlated failure but add distribution and memory overhead. One large runtime shares resources efficiently and accepts broader native/collector risk. The appropriate partition depends on application trust and recovery requirements.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Corrupt runtime evidence descriptors and verify outer capture remains bounded.
- Distinguish budget starvation from a worker consuming CPU without progress.
- Attempt old-epoch delivery during successor launch and reject it without losing cleanup obligations.

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

1. [Crash-only software](../../../30-sources/candea-fox-2003-crash-only-software.md).
2. [Unreliable failure detectors](../../../30-sources/chandra-toueg-1996-failure-detectors.md).
