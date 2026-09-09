---
title: "Scheduling control and capacity admission"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Scheduling control and capacity admission

Who may allocate CPU service, and what admission argument makes that allocation meaningful?

## Research basis and status

Scheduling-context capabilities separate authority over CPU time from ordinary thread identity. [1](../../../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md), [2](../../../30-sources/blackham-et-al-2011-timing-analysis-protected-kernel.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../scheduling-contexts-and-temporal-authority.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

SchedulingControl limits CPU or admission-domain scope, priority ceilings, budget/period choices, refill capacity and delegation. A SchedulingContext owns consumable execution credit and at most one active binding. Structural reconfiguration is permitted only while unbound and not donated.

### Admission, transitions and completion

Check proposed capacity against the selected scheduling profile before committing a context or moving it to a new admission domain. Reserve scheduling metadata, timeout delivery and exceptional-work allowance along with ordinary budget. Publish the context only after its payer and configuration are fixed. A thread becomes dispatchable only when ready, currently bound, gate-valid and funded for the required handler quantum.

### Failure and adversarial behavior

A budget object alone does not prove a deadline or interrupt-response bound. Firmware pauses, interrupt work, non-preemptible kernel sections and contention need explicit assumptions. Increasing a priority ceiling or moving a context can invalidate an earlier capacity analysis even when its numeric budget is unchanged.

### Alternatives and unresolved tradeoffs

Static admission offers stronger analyzability but reduces flexibility. Dynamic admission is possible with a checked profile and a failure result when capacity is unavailable. Avoid accepting configurations merely because average utilization appears low.

## Verification obligations

Overcommit each admission domain, attempt reconfiguration while donated, and race dispatch with budget exhaustion. Verify scope and ceiling attenuation. Analyze kernel paths separately from workload execution and report measured maxima as measurements, not established worst-case bounds.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Kernel activation checkpoints](../protection-domains-threads-and-address-spaces/kernel-activation-checkpoints.md) — Kernel work must reach a consistent, bounded checkpoint.
- [Recovery escrow and reserve admission](../failure-boundaries-and-recovery-topology/recovery-escrow-and-reserve-admission.md) — Recovery needs authority and metadata as well as CPU time.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Scheduling-context capabilities: A principled, light-weight operating-system mechanism for managing time](../../../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Timing analysis of a protected operating system kernel](../../../30-sources/blackham-et-al-2011-timing-analysis-protected-kernel.md) — comparative evidence; its methods and limits are recorded in the source note.
