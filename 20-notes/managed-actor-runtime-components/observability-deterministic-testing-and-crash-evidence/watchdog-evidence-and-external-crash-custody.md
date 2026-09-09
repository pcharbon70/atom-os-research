---
title: "Watchdog evidence and external crash custody"
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

# Watchdog evidence and external crash custody

This study decomposes [Observability, deterministic testing and crash evidence](../observability-deterministic-testing-and-crash-evidence.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Failure detection distinguishes budget starvation from suspected stalled work; recovery must not depend on trusting the failed runtime. [1](../../../30-sources/chandra-toueg-1996-failure-detectors.md), [2](../../../30-sources/candea-fox-2003-crash-only-software.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Production traces, complete test schedules and crash evidence have different loss and trust contracts, even when they share an event schema.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own pre-registered bounded runtime descriptors, progress counters and optional crash sections. The kernel owns the minimum fault/budget record; an outer evidence service owns sealing, retention and authorized export. Runtime-written memory becomes untrusted after corruption.

### Admission, transitions and completion

Publish progress at genuine safe points with the current bounded phase. Compare it with independent granted CPU and idle state before declaring suspicion. On fault, freeze through the external protocol, validate each optional section independently and seal a manifest even when sections are absent or corrupt.

### Failure and adversarial behavior

Checksums detect accidental changes, not a malicious runtime forging a self-report. A watchdog counter incremented inside a stuck loop can falsely imply useful progress. Failed capture of one section must not block mandatory evidence, and exporting a full heap requires explicit privacy authority.

### Alternatives and unresolved tradeoffs

Small headers preserve containment and low failure-path cost but limit root-cause detail. Full dumps provide context at substantial storage and secret-exposure cost. Decide retention and redaction outside the failing domain; never treat a recovered heap as a trusted restart checkpoint.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Corrupt descriptor lengths and pointers and bound the external parser.
- Run a budget-starved domain and a spinning funded worker; distinguish their evidence.
- Fail optional section capture while still sealing the independent minimum and missing-section bitmap.

Record the exact profile, tested revision, schedule/input bounds and resource
observations before claiming this contract holds. A semantic pass does not
establish latency or corruption containment.

## Connections

- [Component service index](README.md) — sibling responsibilities and shared boundaries.
- [Failure evidence classification](../failure-translation-and-the-otp-boundary/typed-failure-provenance-and-compatible-projection.md) — a contract this service must compose with.
- [Observation and recovery limits](../resource-accounting-and-overload-control/pressure-states-and-protected-recovery-capacity.md) — a contract this service must compose with.
- [Open runtime inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — unresolved design and evidence.
- [Research session](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — source manifest and reading limitations.

## Sources

1. [Unreliable failure detectors](../../../30-sources/chandra-toueg-1996-failure-detectors.md).
2. [Crash-only software](../../../30-sources/candea-fox-2003-crash-only-software.md).
