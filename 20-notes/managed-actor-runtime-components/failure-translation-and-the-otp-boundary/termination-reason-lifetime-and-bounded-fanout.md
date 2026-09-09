---
title: "Termination reason lifetime and bounded fan-out"
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

# Termination reason lifetime and bounded fan-out

This study decomposes [Failure translation and the OTP boundary](../failure-translation-and-the-otp-boundary.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Visible-resource release and process death do not imply all memory has vanished; causal accounting includes deferred cleanup after actor execution ends. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md), [2](../../../30-sources/banga-et-al-1999-resource-containers.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. The runtime implements observations and actor termination; OTP-like services choose restart policy, and an outer service handles runtime corruption.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own recovery-held reason storage and fan-out cursors after actor execution stops. Relation records remain generation-correct while the actor's ordinary heap becomes reclaimable. Reserve accounting covers both metadata and the work of delivering exact reason values.

### Admission, transitions and completion

Select one outcome, acquire its durable-for-cleanup representation, dispose or transfer directly visible resources and then publish relation observations in bounded slices. Each recipient follows ordinary term ownership rules. Continue late native/shared-object draining without letting it change the sealed reason.

### Failure and adversarial behavior

A million monitors or a large reason defeats any assumption that exit is constant-time. Dropping observations to make a benchmark finish changes compatibility. The cleanup reserve may cover only a declared maximum admitted fan-out; exhaustion escalates transparently rather than creating uncharged work.

### Alternatives and unresolved tradeoffs

Copying the reason once into recovery-owned storage simplifies actor-heap release but still requires safe recipient representation. Keeping the whole old heap avoids initial copy but can retain much more memory. Measure both under failure storms and constrain admission accordingly.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Exit with a large reason and high monitor count under memory pressure.
- Interrupt cleanup after every fan-out slice and resume without duplicate DOWN signals.
- Verify table/name disposition is visible before death observations while deferred bytes remain honestly charged.

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

1. [OTP 29.0.6 managed-runtime documentation](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md).
2. [Resource containers](../../../30-sources/banga-et-al-1999-resource-containers.md).
