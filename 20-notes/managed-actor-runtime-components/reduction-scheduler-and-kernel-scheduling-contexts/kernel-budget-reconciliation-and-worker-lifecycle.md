---
title: "Kernel budget reconciliation and worker lifecycle"
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

# Kernel budget reconciliation and worker lifecycle

This study decomposes [Reduction scheduler and kernel scheduling contexts](../reduction-scheduler-and-kernel-scheduling-contexts.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Scheduling-context capabilities make budget enforceable; resource containers distinguish the account charged from the thread doing the work. [1](../../../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md), [2](../../../30-sources/banga-et-al-1999-resource-containers.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Runtime reductions select actors; kernel contexts enforce CPU authority. Neither is a hard real-time guarantee by itself.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own worker-to-context bindings, CPU observations and lifecycle state. Activation records attribute actor work and named runtime-system work beneath the domain budget. Processor topology is a hint, not a grant of execution time.

### Admission, transitions and completion

Adopt a context only after the worker is initialized; sample qualified kernel CPU usage around activation boundaries and reconcile totals with explicit uncertainty. For withdrawal, close new actor claims, release the current actor at a safe point, transfer queued work and remove the progress participant before returning the context.

### Failure and adversarial behavior

The kernel may preempt at any instruction and may deny further budget. A cooperative drain must therefore have an external fallback; it cannot depend on a revoked worker running forever. Ordinary asynchronous sends do not donate contexts or create budget for their receiver.

### Alternatives and unresolved tradeoffs

Fine time sampling improves attribution but costs overhead. Batched sampling is cheaper and must expose its error bounds. Select tolerances experimentally, retaining unassigned system work as visible charged debt instead of laundering it into idle time.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Compare actor plus system CPU charges with kernel context totals under forced preemption.
- Withdraw the last worker while pending cleanup exists and exercise outer policy.
- Verify asynchronous message chains never increase granted CPU budget.

Record the exact profile, tested revision, schedule/input bounds and resource
observations before claiming this contract holds. A semantic pass does not
establish latency or corruption containment.

## Connections

- [Component service index](README.md) — sibling responsibilities and shared boundaries.
- [Safe-point handoff](../code-execution-safe-points-and-version-publication/canonical-safe-point-and-native-helper-state.md) — a contract this service must compose with.
- [Funded control and recovery](../resource-accounting-and-overload-control/pressure-states-and-protected-recovery-capacity.md) — a contract this service must compose with.
- [Open runtime inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — unresolved design and evidence.
- [Research session](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — source manifest and reading limitations.

## Sources

1. [Scheduling-context capabilities](../../../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md).
2. [Resource containers](../../../30-sources/banga-et-al-1999-resource-containers.md).
