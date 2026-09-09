---
title: "Thread readiness and reversible suspension"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Thread readiness and reversible suspension

How can administrative suspension preserve a thread's logical wait state without confusing it with terminal stop?

## Research basis and status

Scheduling-context mechanisms separate possession of time authority from thread execution state. [1](../../../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md), [2](../../../30-sources/sel4-foundation-2026-reference-manual.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../protection-domains-threads-and-address-spaces.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

A thread has a logical operation state, an administrative suspension overlay, a bound scheduling context and domain membership. Ready means eligible for scheduler consideration; it does not mean runnable with positive budget. Passive receive, active call, timeout wait and fault-blocked states retain their identities through suspension.

### Admission, transitions and completion

Suspension moves the domain through SUSPENDING to ADMIN_SUSPENDED only after its execution acknowledgements. Save the logical state rather than rewriting all members to Ready. Replies, deadlines and notifications that arrive while suspended select their normal outcomes and update the saved wait state. Resume removes the overlay and reevaluates every gate, context binding and budget condition.

### Failure and adversarial behavior

Resuming every suspended thread as runnable can replay a completed call, lose a pending fault or run an exhausted scheduling context. A missing acknowledgement yields SUSPEND_FAILED, not assumed completion. A later valid acknowledgement can refine the result; terminal closing remains distinct and irreversible.

### Alternatives and unresolved tradeoffs

A single flattened state enum becomes difficult to maintain as waits and administrative states multiply. Orthogonal state dimensions simplify reasoning only if allowed combinations are explicit. They must not permit an aborted handler to masquerade as a reusable suspended worker.

## Verification obligations

Deliver reply, timeout, fault and domain close at every suspension boundary. Resume with exhausted or transferred budget. Check that exactly the original logical operation progresses, no terminal state reopens, and Ready never bypasses dispatch prerequisites.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Passive handler abort and donation drain](../bounded-invocation-and-transport/passive-handler-abort-and-donation-drain.md) — Accepted passive handlers require a valid stop/checkpoint path.
- [Software and hardware quiescence join](../teardown-revocation-and-safe-reclamation/software-and-hardware-quiescence-join.md) — Execution stop is only one condition of final reclamation.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Scheduling-context capabilities: A principled, light-weight operating-system mechanism for managing time](../../../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [seL4 reference manual, version 16.0.0](../../../30-sources/sel4-foundation-2026-reference-manual.md) — comparative evidence; its methods and limits are recorded in the source note.
