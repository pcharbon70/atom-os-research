---
title: "Feature profiles and backend binding"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - typed-kernel-facing-architecture-facade
aliases: []
---

# Feature profiles and backend binding

A backend profile is a semantic promise, not a bag of available instructions. Static binding should reduce dispatch complexity without hiding unsupported or weaker behavior.

## Scope and research question

How can the same facade remain meaningful across architectures and optional facilities while preserving every caller's required guarantee?

This report refines [component 10: Typed kernel-facing architecture facade](../typed-kernel-facing-architecture-facade.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

BackendProfile identifies specification revisions, enabled facilities, trusted firmware dependencies, operation support and exact completion predicates. Build-time selection binds the ordinary mechanism implementation. Runtime feature-class witnesses cover heterogeneous CPUs and changing execution environments. Unsupported, unavailable and prohibited outcomes remain distinguishable where callers need them.

### Protocol and publication points

Declare required semantics → select a candidate profile → validate architectural and firmware evidence → bind implementations → run conformance obligations → admit current execution-class witnesses → expose operations. Optional facilities extend explicitly named profiles; they do not silently weaken a baseline operation or change its object lifetime.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

A function present in every backend may have different effects and failure models. Dynamic fallback can violate context budgets or isolation guarantees. A compiler target feature is not proof that every online CPU may execute it. Version drift in Zig, firmware or specifications requires requalification of the affected boundary rather than a compatibility assumption.

### Alternatives and tradeoffs

One lowest-common-denominator profile is easier to port but can conceal important stronger capabilities. Many narrowly named profiles improve precision but can overwhelm clients. Choose profiles from distinct semantic obligations, not one profile per instruction or an arbitrary feature count.

### Cross-architecture realization

x86-64, AArch64 and RISC-V backends share object and effect contracts only where an actual refinement exists. Higher-privilege PSCI or SBI services remain explicit trusted dependencies, not native kernel instructions.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Replace a required facility with a weaker stub; conformance must fail instead of accepting an identically named function.
- Withdraw a CPU feature witness during migration; a dependent operation must reject or move only under a validated policy.
- Exercise unsupported operations and verify rejection has no hidden allocation, firmware call or partial effect.

A minimal useful profile lattice and the cost of checking dynamic witnesses have not been established experimentally.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Cross-component completion composition](cross-component-completion-composition.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Zig language reference](../../../30-sources/zig-project-2026-language-reference-0-16.md) — Lifetime discipline, atomics and assembly remain explicit obligations.
- [Flux OSKit](../../../30-sources/ford-et-al-1997-flux-oskit.md) — Component dependencies include their execution environment.
- [Intel system-programming documentation](../../../30-sources/intel-2026-system-programming-documentation.md) — ISA-specific privileged state and completion requirements.
- [Arm A-profile architecture](../../../30-sources/arm-2026-a-profile-system-architecture-documentation.md) — Architecture-specific exception, ordering and state contracts.
- [RISC-V privileged architecture](../../../30-sources/risc-v-international-2026-privileged-architecture.md) — Privilege and trap semantics qualified by extensions.
- [Arm PSCI 1.3](../../../30-sources/arm-2024-power-state-coordination-interface.md) — Firmware CPU requests and OS admission have different states.
- [RISC-V SBI](../../../30-sources/risc-v-international-2025-supervisor-binary-interface.md) — Separate higher-privilege start and remote-operation contracts.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
