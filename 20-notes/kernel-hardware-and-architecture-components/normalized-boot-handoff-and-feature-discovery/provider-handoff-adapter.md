---
title: "Provider handoff adapter"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - normalized-boot-handoff-and-feature-discovery
aliases: []
---

# Provider handoff adapter

The adapter should terminate one precisely versioned provider contract and produce owned input for normalization. It is a privileged boundary translator, not a firmware compatibility layer that remains callable indefinitely.

## Scope and research question

What must become true before provider-owned pointers and execution services can disappear?

This report refines [component 0: Normalized boot handoff and feature discovery](../normalized-boot-handoff-and-feature-discovery.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

Keep a ProviderSession containing protocol revision, entry-mode evidence, mapped input extents, owned scratch storage, outstanding provider resources, and retained-service descriptors. The early assembly shim owns only establishment of a declared execution environment; the adapter owns provider calls and byte custody. Neither publishes allocator-ready memory or starts discovered CPUs. A module address is a borrowed extent until the copy or explicit retention succeeds.

### Protocol and publication points

Admitted → EnvironmentEstablished → InputsCollected → ExitAttemptedRestricted → ProviderTerminated → EnvelopeOwned. For UEFI, final-map acquisition and ExitBootServices form one retryable transaction; a stale key requires a refreshed map. After the first exit attempt, firmware may already have partially shut down boot services: retry only through the services permitted by that specification, not a generic rollback or cleanup callback. After success, no boot-service call is legal. A native-loader route discharges its own retention conditions. Post-exit failure follows a kernel-owned terminal path.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

The dangerous cut is successful provider termination followed by a failed copy or absent scratch mapping. Reserve post-termination storage and establish addressability beforehand. Retained runtime services are an explicit ongoing trust dependency, not an exception hidden inside the normalizer. Source authentication does not establish parser safety, and a checksummed envelope does not authenticate its producer.

### Alternatives and tradeoffs

A separate loader image makes resident kernel parsing smaller but remains trusted boot code. A discardable in-kernel adapter simplifies custody tracking but increases early privileged code. Select by explicit dependencies and verifiable teardown, not by assuming either placement makes hostile bytes safe.

### Cross-architecture realization

UEFI, native-loader protocols, and a device-tree handoff differ in retained services and entry assumptions independently of ISA. x86-64, AArch64 and RISC-V shims must each establish their own stack, addressing and privilege preconditions; no shared C or Zig procedure ABI specifies firmware entry.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Inject a changed final-map key and verify that only the successful map reaches normalization.
- Poison every borrowed provider pointer at its declared release point; subsequent reads must use owned or retained storage.
- Fail each acquisition and each post-termination step; check the cleanup mechanism is still legal in that state.

Exact adapter/provider state refinements and recovery from partial termination remain unverified.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Bounded envelope parser](bounded-envelope-parser.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [UEFI specification](../../../30-sources/uefi-forum-2024-uefi-2-11.md) — Provider memory-map and service-lifetime contracts.
- [Limine boot protocol](../../../30-sources/limine-project-2026-limine-boot-protocol.md) — Versioned provider handoff, not a kernel ABI.
- [BootStomp](../../../30-sources/redini-et-al-2017-bootstomp.md) — Empirical motivation for adversarial early-input analysis.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
