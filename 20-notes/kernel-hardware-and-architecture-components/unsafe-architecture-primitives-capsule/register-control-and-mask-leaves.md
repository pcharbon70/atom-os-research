---
title: "Register, control and local-mask leaves"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - unsafe-architecture-primitives-capsule
aliases: []
---

# Register, control and local-mask leaves

Control-register and interrupt-mask primitives should preserve the caller's established state rather than expose arbitrary numeric writes. Each allowed transition needs a feature, field and execution-context contract.

## Scope and research question

How can a local privileged-state change avoid altering unrelated controls or enabling interrupts unexpectedly?

This report refines [component 1: Unsafe architecture-primitives capsule](../unsafe-architecture-primitives-capsule.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

A register descriptor specifies writable, reserved, read-only and side-effect fields plus legal combinations. An interrupt guard binds prior mask state, CPU incarnation, entry depth and a single protected restoration obligation. Read-modify-write is allowed only when register semantics permit it; write-one-to-clear and read-sensitive registers require distinct operations. Profile enabling belongs to semantic admission, not an unreviewed raw setter.

### Protocol and publication points

Validate profile and current context → capture exact prior state → execute declared local transition → establish required synchronization/readback → return scoped state evidence. Nested interrupt guards restore the state observed on entry, never blindly enable interrupts. Restoration consumes the exact guard while migration and incompatible nesting are excluded. Recoverable probes name a bounded fault region and legal recovery PC before execution.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Local interrupt masking neither stops other CPUs nor makes NMI-like execution impossible. A privileged instruction fault after partial effects cannot become a guessed Unsupported result. Exception recovery is valid only for the declared probe family; unexpected failures enter the architecture-fault path. State restoration must not replay a guard after a CPU incarnation changes.

### Alternatives and tradeoffs

Raw register accessors simplify porting but spread reserved-field rules. Typed transition constructors centralize policy-neutral validity; they require maintaining precise models for each register family. A global lock cannot replace CPU-local mask semantics.

### Cross-architecture realization

x86 control/MSR access, AArch64 system registers and RISC-V WARL CSRs have different validation and readback obligations. Arm FEAT_NMI and ordinary IRQ masks are distinct; analogous names on different ISAs do not imply identical exclusion.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Nest guards with initially enabled and initially disabled masks and verify exact restoration.
- Inject NMI-like entry between capture, modification and restoration; forbid use of locks held by the interrupted path.
- Test reserved-field input, denied privilege, feature-disable races and partial-effect fault handling.

Exact register-family recipes, errata and guard restoration proofs require per-profile review.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Ordering and maintenance leaves](ordering-and-maintenance-leaves.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Intel system-programming documentation](../../../30-sources/intel-2026-system-programming-documentation.md) — ISA-specific privileged state and completion requirements.
- [RISC-V privileged architecture](../../../30-sources/risc-v-international-2026-privileged-architecture.md) — Privilege and trap semantics qualified by extensions.
- [A-profile non-maskable interrupts](../../../30-sources/dall-2022-a-profile-non-maskable-interrupts.md) — NMI masking and stack-state behavior are feature-specific.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
