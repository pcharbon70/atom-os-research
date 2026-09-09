---
title: "Pressure states and protected recovery capacity"
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

# Pressure states and protected recovery capacity

This study decomposes [Resource accounting and overload control](../resource-accounting-and-overload-control.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

SEDA supplies explicit overload boundaries but also negative latency and queue-growth results; accounting identifies who must pay when work is deferred. [1](../../../30-sources/welsh-et-al-2001-seda.md), [2](../../../30-sources/banga-et-al-1999-resource-containers.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Runtime ledgers attribute consumption beneath hard kernel domain limits; actor policy cannot mint memory, CPU or cleanup reserve.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own class-specific pressure thresholds, hysteresis, admission-close state and protected reserve balances. Signals include queue age, scan work, allocation rate, retained parents and cleanup backlog, not merely percentage memory used.

### Admission, transitions and completion

Move from normal operation to soft pressure, closed ordinary admission and recovery-only work under explicit policy. Refuse new work before publication where its API permits refusal. Once admitted, preserve its required semantics and ownership; the recovery lane performs bounded cleanup and evidence, not arbitrary actor work.

### Failure and adversarial behavior

Silent dropping of admitted ordinary messages is not a compatible overload response. Killing actors solely to free memory is an explicit resource-profile decision, not an implied OTP behavior. Exhausted recovery capacity can require domain quarantine; no controller can create capacity after the hard limit.

### Alternatives and unresolved tradeoffs

Feedback can improve useful throughput but reacts late to bursts. Static reservations are predictable and may waste idle capacity. Combine measured soft policy with hard prepublication accounting, keeping the assumptions behind any latency claim visible.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Drive sustained overload with unmatched mailboxes and verify no hidden message drops.
- Oscillate around thresholds and test hysteresis.
- Exhaust ordinary resources while preserving a bounded exit/evidence path, then test reserve exhaustion separately.

Record the exact profile, tested revision, schedule/input bounds and resource
observations before claiming this contract holds. A semantic pass does not
establish latency or corruption containment.

## Connections

- [Component service index](README.md) — sibling responsibilities and shared boundaries.
- [Shared-object retention](../terms-private-heaps-shared-binaries-and-tracing-collection/shared-binary-literal-and-fragment-lifetimes.md) — a contract this service must compose with.
- [Bounded shared-operation work](../reduction-scheduler-and-kernel-scheduling-contexts/reduction-costs-and-yieldable-work-continuations.md) — a contract this service must compose with.
- [Open runtime inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — unresolved design and evidence.
- [Research session](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — source manifest and reading limitations.

## Sources

1. [SEDA](../../../30-sources/welsh-et-al-2001-seda.md).
2. [Resource containers](../../../30-sources/banga-et-al-1999-resource-containers.md).
