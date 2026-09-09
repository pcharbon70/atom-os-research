---
title: "Reduction costs and yieldable work continuations"
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

# Reduction costs and yieldable work continuations

This study decomposes [Reduction scheduler and kernel scheduling contexts](../reduction-scheduler-and-kernel-scheduling-contexts.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

ERTS's yielding helper machinery demonstrates explicit continuation/destructor needs; resource attribution must include work outside instruction dispatch. [1](../../../30-sources/erlang-otp-team-2026-yielding-c-code-contracts.md), [2](../../../30-sources/banga-et-al-1999-resource-containers.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Runtime reductions select actors; kernel contexts enforce CPU authority. Neither is a hard real-time guarantee by itself.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own the work-cost catalog and continuation records for BIFs, copying, receive scans, collection, table operations and cleanup. A continuation stores rooted values, progress and a charge context rather than pointers into a previous native stack.

### Admission, transitions and completion

Charge bounded progress increments, check remaining budget and yield through canonical actor state. Resume only after validating actor, object and code generations. Destruction on exit frees private preparation or completes an already published operation through its proper owner; it cannot simply discard shared atomic work.

### Failure and adversarial behavior

Counting a million-element helper as one reduction defeats responsiveness. Charging its total after completion also leaves an unbounded interval. Transformed C routines need audited stack/macro restrictions; the existence of YCF is not a promise that arbitrary Zig or C code can be suspended safely.

### Alternatives and unresolved tradeoffs

Manual state machines expose ownership but are verbose. Generated continuations reduce repetition while enlarging generator trust. Validate by forcing every yield and by maintaining a straightforward reference implementation for results.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Run each helper with a one-unit yield budget and compare results with its reference.
- Exit the actor at every continuation point and reconcile allocated resources.
- Measure maximum non-yielding time for adversarial term and table sizes.

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

1. [Automatic Yielding of C Code](../../../30-sources/erlang-otp-team-2026-yielding-c-code-contracts.md).
2. [Resource containers](../../../30-sources/banga-et-al-1999-resource-containers.md).
