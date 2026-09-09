---
title: "Systematic exploration, differential oracles and shrinking"
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

# Systematic exploration, differential oracles and shrinking

This study decomposes [Observability, deterministic testing and crash evidence](../observability-deterministic-testing-and-crash-evidence.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Controlled schedule exploration finds races ordinary repetition can miss; replay reproduces a history but does not by itself prove it correct. [1](../../../30-sources/christakis-et-al-2013-concuerror.md), [2](../../../30-sources/aumayr-et-al-2018-actor-record-replay.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Production traces, complete test schedules and crash evidence have different loss and trust contracts, even when they share an event schema.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own executable invariants, bounded scenario models, differential observation rules and minimized failure artifacts. Distinguish semantic conformance, concurrency safety, resource accounting and performance properties; one passing result does not establish the others.

### Admission, transitions and completion

Generate actor inputs and schedules around publication, exit, alias, timer, GC, table and native-completion boundaries. Explore bounded alternatives with documented reductions and fairness assumptions. Shrink a failure while preserving the same violated property and external input identity, then replay the reduced case against reference and candidate engines.

### Failure and adversarial behavior

Partial-order reduction is only sound for the modeled independence relation; selective receive and shared tables complicate that relation. Unsupported operations cannot be silently treated as deterministic. Passing a bounded search is not exhaustive verification of an unbounded runtime.

### Alternatives and unresolved tradeoffs

Application-level instrumentation is accessible but misses lower runtime races. Runtime-level choice hooks expose those races at implementation cost. Use both with explicit coverage, adding fault injection rather than expecting one tool to cover corrupted memory or DMA.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Seed known lost-wakeup, duplicate-release and first-match defects and ensure the models find them.
- Shrink a timer/exit race without removing the required timing or identity condition.
- Publish explored bounds, unsupported operations and failing schedules alongside all pass claims.

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

1. [Concuerror](../../../30-sources/christakis-et-al-2013-concuerror.md).
2. [Actor record and replay](../../../30-sources/aumayr-et-al-2018-actor-record-replay.md).
