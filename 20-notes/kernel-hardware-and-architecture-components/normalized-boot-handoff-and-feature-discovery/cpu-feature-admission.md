---
title: "CPU feature admission"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - normalized-boot-handoff-and-feature-discovery
aliases: []
---

# CPU feature admission

CPU discovery should publish evidence about a particular CPU incarnation, separately from the set of features the kernel requires or chooses to enable. A firmware topology entry is a candidate, not proof that its execution environment is safe.

## Scope and research question

How does the architecture admit heterogeneous or restarted CPUs without using instructions or state formats they cannot support?

This report refines [component 0: Normalized boot handoff and feature discovery](../normalized-boot-handoff-and-feature-discovery.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

Separate KernelRequiredProfile, raw per-CPU feature evidence, enabled controls, erratum policy and the final admitted profile. Evidence binds hardware identity to logical CPU identity and incarnation. Include address widths, privileged facilities, extended-state shape and instruction prerequisites. The lifecycle component owns admission to online membership; this service supplies the validated local facts and rejects incompatible requirements.

### Protocol and publication points

Candidate → LocallyObserved → RequirementsChecked → ControlsEnabled → LocalValidationComplete → AdmissionEvidenceSealed. Observing a feature does not enable it; enabling a control does not prove associated context storage exists. Required features must hold on every admitted execution CPU. Optional features form explicitly authorized execution classes; migration checks the destination class before restoring a dependent context. Offline/restart invalidates old evidence.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Combining topology from one discovery generation with feature observations from another can misidentify a CPU. Boot-CPU feature bits must not be copied into all secondary records. A hypervisor or retained monitor may filter facilities; that is part of the execution-environment evidence. Unknown required semantics cause rejection rather than an optimistic instruction probe outside a declared recovery region.

### Alternatives and tradeoffs

A system-wide feature intersection simplifies migration but sacrifices specialized hardware. Feature classes preserve performance opportunities while increasing scheduling and context-format obligations. Runtime checks at every leaf are defensive but cannot replace a coherent admitted-profile lifecycle.

### Cross-architecture realization

CPUID/control-state discovery on x86, ID registers and feature controls on AArch64, and ISA/firmware evidence on RISC-V are distinct mechanisms. Normalization should preserve missing, unavailable and prohibited values rather than translating them all into a false Boolean.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Admit CPUs with deliberately unequal feature/state-size sets and attempt incompatible migrations.
- Restart a CPU identity and replay its previous feature witness; the new incarnation must reject it.
- Separate reported, enabled and locally validated states in tests so no intermediate state authorizes optional instructions.

Feature-class change, firmware dishonesty and revalidation after microcode or execution-environment changes remain open.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Static mechanism discovery](static-mechanism-discovery.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Intel system-programming documentation](../../../30-sources/intel-2026-system-programming-documentation.md) — ISA-specific privileged state and completion requirements.
- [Arm A-profile architecture](../../../30-sources/arm-2026-a-profile-system-architecture-documentation.md) — Architecture-specific exception, ordering and state contracts.
- [RISC-V privileged architecture](../../../30-sources/risc-v-international-2026-privileged-architecture.md) — Privilege and trap semantics qualified by extensions.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
