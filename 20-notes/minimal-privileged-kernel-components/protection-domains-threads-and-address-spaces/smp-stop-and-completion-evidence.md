---
title: "SMP stop and completion evidence"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# SMP stop and completion evidence

How can a domain stop certificate cover every CPU that might still execute its old incarnation?

## Research basis and status

Reclamation and timing research inform the obligations, but this whole-domain SMP protocol remains unverified. [1](../../../30-sources/mckenney-slingwine-1998-read-copy-update.md), [2](../../../30-sources/blackham-et-al-2011-timing-analysis-protected-kernel.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../protection-domains-threads-and-address-spaces.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

The stop coordinator owns an immutable target set for a domain stop epoch, CPU incarnation identifiers and preallocated acknowledgement records. The domain lifecycle is authoritative: CLOSING → STOPPING → STOPPED or STOP_FAILED. STOPPED is not yet QUIESCENT or REAPED.

### Admission, transitions and completion

Freeze membership and the execution-participant set under the same synchronization used by dispatch and migration. Send bounded stop requests tagged with domain generation, stop epoch and CPU incarnation. Each matching CPU acknowledges only after the activation checkpoint postconditions hold. Combine acknowledgements without allocating and reject duplicates or evidence from another CPU incarnation.

### Failure and adversarial behavior

A CPU joining or receiving a migrating thread after the snapshot can evade the stop set unless migration admission participates in freezing. A delayed acknowledgement from a reused logical CPU number cannot certify its successor. A missing acknowledgement is a failure result; elapsed time is not substitute evidence.

### Alternatives and unresolved tradeoffs

An all-CPU target set is conservative and simple but adds unrelated participants and availability dependencies. A precise run-set can reduce work only if maintained exactly. The pre-execution no-stop path is valid solely for a domain proved never execution-eligible and with no active kernel effects.

## Verification obligations

Race migration, dispatch, CPU reincarnation and thread creation with target freezing. Delay and duplicate acknowledgements, and interrupt one activation before checkpoint. Verify exact coverage and late-evidence handling without changing the original stop epoch or claiming hardware drainage.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Passive handler abort and donation drain](../bounded-invocation-and-transport/passive-handler-abort-and-donation-drain.md) — Accepted passive handlers require a valid stop/checkpoint path.
- [Software and hardware quiescence join](../teardown-revocation-and-safe-reclamation/software-and-hardware-quiescence-join.md) — Execution stop is only one condition of final reclamation.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Read-copy update: Using execution history to solve concurrency problems](../../../30-sources/mckenney-slingwine-1998-read-copy-update.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Timing analysis of a protected operating system kernel](../../../30-sources/blackham-et-al-2011-timing-analysis-protected-kernel.md) — comparative evidence; its methods and limits are recorded in the source note.
