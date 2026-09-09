---
title: "Interrupt accounting and quarantine"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - interrupt-event-fabric
aliases: []
---

# Interrupt accounting and quarantine

Interrupts need an admission and recovery budget independent of the failing driver. A source that exhausts its account must not be able to refill itself or monopolize the CPU while reporting its own failure.

## Scope and research question

How can overload be contained without losing the evidence or authority needed for recovery?

This report refines [component 5: Interrupt event fabric](../interrupt-event-fabric.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

A prevalidated debit plan binds source generation, account, bounded hard-path work and management route. Counters distinguish raw observations, coalescing, receiver backlog, budget exhaustion and quarantine. Recovery facets belong outside the driver's failure subtree. Diagnostic source identifiers convey no reset or re-enable authority.

### Protocol and publication points

ActiveBudgeted → BudgetExhausted or StormSuspected → flow-safe masking/stabilization → Quarantined → independently authorized diagnosis/recovery → new admitted generation. Recovery rechecks endpoint, route, sink and account conditions. If masking cannot prove delivery exclusion, preserve that uncertainty and escalate the affected scope instead of reporting complete containment.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

A hardware source may continue generating traffic after software masking. Error notification itself can become an interrupt storm. Accounting on the ordinary receiver is too late to bound privileged hard-path cost. Dropping the management route during driver teardown can make quarantine permanently unowned.

### Alternatives and tradeoffs

Rate limiting only in user space cannot bound kernel entry cost. Permanently disabling a source is safe for CPU availability only if the controller actually excludes it, and sacrifices service. Scoped quarantine permits recovery at the cost of explicit retained resources and independent authority.

### Cross-architecture realization

Masking and delivery guarantees vary by source/controller and remapping profile. Resource budgets bound admitted software work, not a physically malfunctioning interconnect. Time protection requires more than an interrupt counter.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Drive a source past its budget while verifying unrelated supervisor progress and retained fault evidence.
- Attempt self-refill or self-recovery with a driver completion facet; reject it.
- Race recovery with teardown and repeated interrupt arrival; only a currently authorized generation may rearm.

Budget selection, fairness and containment under controller failure require explicit system-level evaluation.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Polling and interrupt handoff](polling-and-interrupt-handoff.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Linux low-level core APIs](../../../30-sources/linux-kernel-community-2026-low-level-core-apis.md) — Engineering precedent; Linux contracts are not Atom proofs.
- [Time protection](../../../30-sources/ge-et-al-2019-time-protection.md) — Temporal isolation exceeds timer precision.
- [When poll is better than interrupt](../../../30-sources/yang-et-al-2012-when-poll-is-better-than-interrupt.md) — Workload-dependent evidence, not a universal polling advantage.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
