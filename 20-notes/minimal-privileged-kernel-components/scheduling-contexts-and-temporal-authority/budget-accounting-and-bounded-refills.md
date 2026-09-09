---
title: "Budget accounting and bounded refills"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Budget accounting and bounded refills

How can finite replenishment metadata preserve the promised service envelope?

## Research basis and status

The scheduling-context paper explicitly bounds replenishment storage and discusses the resulting loss of usable budget. [1](../../../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md), [2](../../../30-sources/ge-et-al-2019-time-protection.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../scheduling-contexts-and-temporal-authority.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

A context records remaining credit, a finite ordered refill structure, time-conversion identity and overflow rules. Binding state is independent of Available or Exhausted budget. BEAM reductions are a runtime work metric and are not interchangeable with kernel-measured execution time.

### Admission, transitions and completion

Debit elapsed chargeable execution at dispatch transitions and schedule eligible replenishments using a monotonic, profile-defined clock. Handle quantization, arithmetic overflow and counter discontinuity explicitly. When refill capacity is exhausted, discard or conservatively merge credit only if the resulting schedule cannot exceed the declared service envelope. Preserve an auditable ledger of consumed, pending and discarded credit.

### Failure and adversarial behavior

Combining two refills at the earlier release time can create service that the original envelope prohibited. Charging only completed user quanta misses kernel work on behalf of a domain. Treating a clock-era change as a huge positive balance can mint time authority.

### Alternatives and unresolved tradeoffs

Fewer refill entries simplify bounds but reduce service under frequent preemption. More entries improve utilization at a metadata and update cost. Polling-style fallback is a policy/profile choice, not permission to claim sporadic-server semantics after changing the algorithm.

## Verification obligations

Generate adversarial preemption schedules, refill saturation and counter-boundary cases. For every sliding interval in the declared model, verify that granted execution stays within its envelope plus explicitly stated overrun allowance. Check conservation independently of throughput measurements.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Kernel activation checkpoints](../protection-domains-threads-and-address-spaces/kernel-activation-checkpoints.md) — Kernel work must reach a consistent, bounded checkpoint.
- [Recovery escrow and reserve admission](../failure-boundaries-and-recovery-topology/recovery-escrow-and-reserve-admission.md) — Recovery needs authority and metadata as well as CPU time.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Scheduling-context capabilities: A principled, light-weight operating-system mechanism for managing time](../../../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Time protection: The missing OS abstraction](../../../30-sources/ge-et-al-2019-time-protection.md) — comparative evidence; its methods and limits are recorded in the source note.
