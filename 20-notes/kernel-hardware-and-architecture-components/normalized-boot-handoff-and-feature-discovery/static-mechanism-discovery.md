---
title: "Static mechanism discovery"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - normalized-boot-handoff-and-feature-discovery
aliases: []
---

# Static mechanism discovery

Static discovery should describe topology, controllers, counters and retained firmware gates without initializing them. This prevents a descriptive table from becoming authority to issue interrupts, reset devices or execute arbitrary firmware policy.

## Scope and research question

Which bounded facts can be extracted early while leaving mechanism activation to its owning component?

This report refines [component 0: Normalized boot handoff and feature discovery](../normalized-boot-handoff-and-feature-discovery.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

MechanismDescriptor identifies namespace, register extent, access method, revision, dependencies and source provenance. CpuCandidate and topology relations remain separate from online membership. FirmwareGateDescriptor states calling convention, retained privilege, resource lifetime, concurrency restrictions and failure contract. Restrict ACPI or device-tree parsing to a versioned allowlist of static records; AML or dynamic firmware policy needs a different boundary.

### Protocol and publication points

Locate bounded root records → validate structure and checksums → copy required tables → resolve references within declared extents → reconcile identities → publish inactive descriptors. Child references never authorize out-of-range reads. A controller owner later validates the descriptor against its backend and obtains resource authority before activation. Topology updates publish a new evidence generation rather than editing the sealed boot snapshot.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Checksums detect corruption but not trusted intent. Duplicate hardware identities, cycles, impossible affinity links and overlapping register regions must remain conflicts. A CPU proximity domain is not a scheduling mandate. An interrupt description is not evidence that routing or remapping is enabled. Unexpected dynamic firmware calls would defeat the normalizer's bounded, side-effect-free contract.

### Alternatives and tradeoffs

Early dynamic firmware evaluation can discover more devices but expands privileged execution and makes bounds difficult to establish. Static allowlists intentionally defer unsupported policy. Hard-coded board descriptions reduce parsing but still need explicit provenance and cannot become a portable discovery contract.

### Cross-architecture realization

ACPI is not synonymous with x86 and device tree is not synonymous with RISC-V. Discovery formats and processor architecture are separate axes. Controller-specific details remain typed descriptors for APIC, GIC or RISC-V interrupt backends, without flattening their identity spaces.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Fuzz cyclic references, repeated IDs, unknown revisions and conflicting controller ranges.
- Use a backend spy to verify discovery performs no device writes, CPU starts or firmware-policy execution.
- Replace a descriptor generation between inspection and activation; require revalidation or rejection.

The minimum static record allowlist and trust treatment of contradictory firmware remain architecture-profile decisions.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Snapshot sealing and custody](snapshot-sealing-and-custody.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [ACPI 6.6](../../../30-sources/uefi-forum-2025-acpi-6-6.md) — Structured discovery with explicit table validation.
- [Devicetree 0.4](../../../30-sources/devicetree-org-2023-devicetree-specification-0-4.md) — Bounded blob structure and reserved-memory descriptions.
- [Intel system-programming documentation](../../../30-sources/intel-2026-system-programming-documentation.md) — ISA-specific privileged state and completion requirements.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
