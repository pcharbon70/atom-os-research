---
title: "Extended-state ownership and context transfer"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - privileged-entry-exit-and-execution-context
aliases: []
---

# Extended-state ownership and context transfer

Execution context is the complete enabled architectural state belonging to an execution domain, not a fixed integer-register array. Its transfer must prevent a new domain from observing another domain's residual state.

## Scope and research question

How are state shape, CPU ownership and migration kept consistent as optional architectural facilities expand?

This report refines [component 2: Privileged entry, exit and execution context](../privileged-entry-exit-and-execution-context.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

A context profile identifies supported integer, floating-point/vector, debug and other enabled state components, size/alignment and save/restore rules. Thread storage and live CPU state have separate owners. A transfer record binds old/new context incarnations, CPU, profile and completion. Kernel use of extended state requires an explicit bounded borrowing policy; ordinary entry code must not acquire it accidentally through compiler output.

### Protocol and publication points

Stored(old) → RestoreValidated → CpuOwned(old) → SaveInProgress → Stored(old) → ScrubOrRestore(new) → CpuOwned(new). Domain transitions require eager isolation of enabled state; same-domain thread switching may use a separately justified optimization. Migration first proves the destination supports the context profile and that no CPU retains conflicting live ownership. Failure mid-transfer pins the involved records and disallows ordinary return.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

LazyFP is evidence that waiting for a first-use fault can fail to isolate stale state on affected hardware. Eager transfer addresses that failure class, not all microarchitectural channels. Unknown state extensions, truncated buffers and inconsistent control masks can make restore itself unsafe. Merely copying a language handle cannot transfer hardware ownership.

### Alternatives and tradeoffs

Always saving the largest possible state simplifies policy but wastes memory and time. Profile-shaped storage limits cost while making extension enablement an explicit lifecycle change. Lazy techniques require a separate threat model and proof, not an assumption that the processor will fault safely.

### Cross-architecture realization

x86 extended-state discovery, Arm optional vector/matrix state and RISC-V extension status differ. The common contract is complete enabled-state ownership; it does not require identical byte layouts or automatic compatibility between CPUs.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Fill every enabled state component with domain-specific sentinels and test switching, faults and migration.
- Attempt restore on a CPU with a smaller or incompatible state profile.
- Inject failure during save/restore and verify no second CPU can acquire the same live context.

Complete extension catalogs, migration compatibility relations and leakage testing remain profile-specific research obligations.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Nested-event and terminal handoff](nested-event-and-terminal-handoff.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [LazyFP](../../../30-sources/stecklina-prescher-2018-lazyfp.md) — Negative evidence for fault-triggered extended-state isolation.
- [Intel system-programming documentation](../../../30-sources/intel-2026-system-programming-documentation.md) — ISA-specific privileged state and completion requirements.
- [Arm A-profile architecture](../../../30-sources/arm-2026-a-profile-system-architecture-documentation.md) — Architecture-specific exception, ordering and state contracts.
- [RISC-V privileged architecture](../../../30-sources/risc-v-international-2026-privileged-architecture.md) — Privilege and trap semantics qualified by extensions.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
