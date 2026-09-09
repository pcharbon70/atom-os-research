---
title: "Deterministic choice log and external input capture"
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

# Deterministic choice log and external input capture

This study decomposes [Observability, deterministic testing and crash evidence](../observability-deterministic-testing-and-crash-evidence.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Actor replay research records external inputs as well as order; Concuerror controls selected concurrency interactions rather than arbitrary native execution. [1](../../../30-sources/aumayr-et-al-2018-actor-record-replay.md), [2](../../../30-sources/christakis-et-al-2013-concuerror.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Production traces, complete test schedules and crash evidence have different loss and trust contracts, even when they share an event schema.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own a replay manifest, enabled-choice set, ordered choices and recorded nondeterministic values. Bind runtime/profile/module hashes, service models, initial inputs, clock model, quotas and log schema. A random seed alone is not sufficient evidence.

### Admission, transitions and completion

At each declared choice point, record the selected actor or event plus an enabled-set digest. Capture time/random/service values at their modeled boundary. Replay verifies the manifest and enabled set before applying each choice; a mismatch terminates with divergence rather than selecting an alternative silently.

### Failure and adversarial behavior

Real devices, uncontrolled NIF threads and live peers lie outside the claim unless their effects are mediated by deterministic adapters. Production trace loss invalidates a complete replay claim. Recording only final mailbox contents misses selective-receive and cancellation races.

### Alternatives and unresolved tradeoffs

Single-domain controlled scheduling is tractable but omits unmodeled interleavings beneath its abstractions. Finer instruction recording can increase coverage at much higher cost. State the exact boundary and test it with deliberately introduced external nondeterminism.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Replay identical inputs with different physical worker scheduling and verify declared observations.
- Alter a module hash or enabled set and require explicit divergence.
- Inject an unrecorded clock read or native result and verify the harness rejects the completeness claim.

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

1. [Actor record and replay](../../../30-sources/aumayr-et-al-2018-actor-record-replay.md).
2. [Concuerror](../../../30-sources/christakis-et-al-2013-concuerror.md).
