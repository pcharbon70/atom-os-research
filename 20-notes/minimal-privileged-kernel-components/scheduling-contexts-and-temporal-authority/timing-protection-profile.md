---
title: "Timing-protection profile"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Timing-protection profile

What additional contract is needed when allocating CPU time must also prevent information leakage through timing?

## Research basis and status

Time-protection research distinguishes budget enforcement from partitioning or flushing shared microarchitectural state. [1](../../../30-sources/ge-et-al-2019-time-protection.md), [2](../../../30-sources/sel4-foundation-2026-proof-assumptions.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../scheduling-contexts-and-temporal-authority.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

A timing-protection profile identifies security-domain membership, shared microarchitectural resources, interrupt ownership, switch obligations and residual channels. It is distinct from a SchedulingContext's budget and priority. The architecture layer supplies only mechanisms its machine profile can actually support; the kernel controls when those mechanisms are required.

### Admission, transitions and completion

Before admitting a domain under a confidentiality claim, inventory resources shared with distrustful domains and select supported partition, maintenance and switch-padding requirements. Bind that profile to every dispatch and migration route. A switch completes security admission only when the required lower-layer operations finish; a new CPU cannot join the security domain by bypassing profile qualification.

### Failure and adversarial behavior

A domain can observe contention even when every participant stays within its budget. Variable cleanup duration can itself expose another domain's activity. An unpartitionable device, shared interconnect or undocumented hardware state may leave a residual channel that software cannot eliminate. Functional capability confinement does not prove this stronger property.

### Alternatives and unresolved tradeoffs

Spatial partitioning may reduce utilization; flushing and padding can increase switch cost and depend on hardware guarantees. A deployment may explicitly choose availability isolation without timing confidentiality. It must not silently weaken a requested confidentiality profile because a faster backend lacks a required mechanism.

## Verification obligations

Construct representative contention channels and measure switch behavior under adversarial prior activity, then vary migration and interrupt placement. Record residual leakage, observer resolution and unsupported resources. Measurements falsify particular claims but do not prove absence of every channel; a stronger conclusion needs a stated model and compositional noninterference argument.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Kernel activation checkpoints](../protection-domains-threads-and-address-spaces/kernel-activation-checkpoints.md) — Kernel work must reach a consistent, bounded checkpoint.
- [Recovery escrow and reserve admission](../failure-boundaries-and-recovery-topology/recovery-escrow-and-reserve-admission.md) — Recovery needs authority and metadata as well as CPU time.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Time protection: The missing OS abstraction](../../../30-sources/ge-et-al-2019-time-protection.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [What the Proofs Assume](../../../30-sources/sel4-foundation-2026-proof-assumptions.md) — comparative evidence; its methods and limits are recorded in the source note.
