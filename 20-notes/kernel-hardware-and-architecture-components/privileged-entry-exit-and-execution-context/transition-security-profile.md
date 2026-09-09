---
title: "Transition-security profile"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - privileged-entry-exit-and-execution-context
aliases: []
---

# Transition-security profile

Architectural state restoration and protection-domain isolation are related but distinct. A transition-security profile should state what residual microarchitectural exposure is addressed and what remains outside its claim.

## Scope and research question

Which transition effects are required beyond restoring visible registers and page tables?

This report refines [component 2: Privileged entry, exit and execution context](../privileged-entry-exit-and-execution-context.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

Bind a profile to processor/firmware class, privilege path, enabled features, threat assumptions and mitigation sequence. Separate register-state isolation, translation permissions, speculation controls and timing-channel claims. Component 2 owns the transition sequence; policy chooses admissible profiles and component 1 realizes their leaves. Runtime actors and their tracing collector remain unprivileged consumers, not owners of privileged mitigation controls.

### Protocol and publication points

Threat assumptions selected → applicable mechanisms discovered → sequence validated → profile admitted → transitions carry profile identity. A feature or mitigation change requires a coordinated profile transition before affected execution resumes. Performance shortcuts must preserve the declared threat model; a trace should identify the selected sequence without leaking sensitive register contents.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Meltdown and LazyFP motivate different failure boundaries and cannot be combined into a claim that one fence or eager restore defeats all transient leakage. Precise exceptions are not universally memory barriers. A logical model that omits caches, predictors or interrupt interference cannot establish timing noninterference merely because its functional tests pass.

### Alternatives and tradeoffs

One maximum-mitigation profile simplifies administration but may be unavailable or prohibitively costly on some implementations. Per-class profiles expose complexity but make guarantees honest. Sharing execution resources between distrustful domains needs an explicit residual-risk decision.

### Cross-architecture realization

Different ISAs and revisions provide different speculation, state and context-synchronization facilities. The research does not establish a universal mitigation catalog or declare cross-ISA security equivalence. Backend claims must name their actual mechanism and evidence.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Test visible-state leakage separately from transient and timing observations.
- Make an unsupported mitigation or changed firmware profile cause explicit admission failure or narrower recorded guarantees.
- Insert exception boundaries into memory-model litmus tests; reject any proof that assumes undocumented fence strength.

Processor-specific residual-channel analysis and measurable isolation budgets remain open, independently of functional correctness.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Early vector and stack admission](early-vector-stack-admission.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Meltdown](../../../30-sources/lipp-et-al-2018-meltdown.md) — Architectural access denial is not a complete transient-execution boundary.
- [LazyFP](../../../30-sources/stecklina-prescher-2018-lazyfp.md) — Negative evidence for fault-triggered extended-state isolation.
- [Relaxed exception semantics for Arm-A](../../../30-sources/simner-et-al-2024-relaxed-exception-semantics.md) — Precise exception transitions are not general memory barriers.
- [Time protection](../../../30-sources/ge-et-al-2019-time-protection.md) — Temporal isolation exceeds timer precision.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
