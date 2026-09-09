---
title: "Typed failure provenance and compatible projection"
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

# Typed failure provenance and compatible projection

This study decomposes [Failure translation and the OTP boundary](../failure-translation-and-the-otp-boundary.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Failure-detector theory distinguishes suspicion from fact; OTP compatibility requires its documented term-valued exit observations. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md), [2](../../../30-sources/chandra-toueg-1996-failure-detectors.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. The runtime implements observations and actor termination; OTP-like services choose restart policy, and an outer service handles runtime corruption.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own a typed event with subject generation, origin, evidence class, operation phase and exact semantic reason. Keep actor-supplied data separate from authenticated kernel/service observations. Diagnostic summaries may be bounded without replacing compatible reasons.

### Admission, transitions and completion

Classify local actor exit, native service loss, gateway loss, resource refusal and runtime-domain fault before projecting them to language signals. Preserve exact required transformations such as explicit untrappable kill producing killed. Seal the winning reason once; retain later evidence as supplementary context.

### Failure and adversarial behavior

A timeout cannot become proof of nonexecution or remote death. A digest is not an arbitrary Erlang exit term. If exact reason lifetime cannot be maintained within reserves, use declared domain failure policy instead of emitting a counterfeit compatible reason.

### Alternatives and unresolved tradeoffs

A rich extension event improves diagnostics but must not alter existing EXIT/DOWN tuples. Maintaining two views costs metadata; merging them into one untyped reason makes recovery policy depend on ambiguous strings or actor-controlled terms.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Feed forged kernel-shaped actor data and preserve its untrusted evidence class.
- Compare large compound exit reasons through links, trapped exits and monitors.
- Classify identical transport errors occurring before and after possible effect publication differently.

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
2. [Unreliable failure detectors](../../../30-sources/chandra-toueg-1996-failure-detectors.md).
