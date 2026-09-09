---
title: "Kernel activation checkpoints"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Kernel activation checkpoints

What must be true before a stopped CPU activation can be acknowledged as safe?

## Research basis and status

Brown's neutralization analysis makes restartability an explicit assumption rather than a consequence of interrupt delivery. [1](../../../30-sources/brown-2015-reclaiming-lock-free-memory.md), [2](../../../30-sources/blackham-et-al-2011-timing-analysis-protected-kernel.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../protection-domains-threads-and-address-spaces.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

Each privileged activation has a bounded set of protected pins, locks and operation-commit obligations. A checkpoint contract states whether the current operation is committed, aborted or resumable, and which references are released. This is separate from saving user registers.

### Admission, transitions and completion

Place checkpoints where shared kernel invariants are restored and no untracked callback or lock remains. A stop request closes future entry, then waits for the activation to reach such a point through bounded work or a separately verified recovery procedure. Publish acknowledgement only after both user execution and privileged continuation are excluded for the target domain and epoch.

### Failure and adversarial behavior

Forcing a CPU to halt while it owns a kernel lock does not make that lock or its partially updated structure consistent. Clearing its pins after reset can free objects still named by an interrupted transaction. If no valid recovery proof covers the interrupted state, escalate to a node-level fatal path rather than advertising domain-only recovery.

### Alternatives and unresolved tradeoffs

Long non-preemptible critical sections simplify local invariants but worsen stop latency. Fine-grained restartable transactions improve responsiveness at the cost of recovery-state complexity. Analysis must use the generated binary and processor assumptions, not source-level loop counts alone.

## Verification obligations

Request stop before and after every mutation commit and while each lock or pin is held. Assert checkpoint postconditions independently of acknowledgement delivery. Inject a lost CPU and require explicit STOP_FAILED or node-fatal outcome instead of fabricated quiescence.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Passive handler abort and donation drain](../bounded-invocation-and-transport/passive-handler-abort-and-donation-drain.md) — Accepted passive handlers require a valid stop/checkpoint path.
- [Software and hardware quiescence join](../teardown-revocation-and-safe-reclamation/software-and-hardware-quiescence-join.md) — Execution stop is only one condition of final reclamation.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Reclaiming memory for lock-free data structures: there has to be a better way](../../../30-sources/brown-2015-reclaiming-lock-free-memory.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Timing analysis of a protected operating system kernel](../../../30-sources/blackham-et-al-2011-timing-analysis-protected-kernel.md) — comparative evidence; its methods and limits are recorded in the source note.
