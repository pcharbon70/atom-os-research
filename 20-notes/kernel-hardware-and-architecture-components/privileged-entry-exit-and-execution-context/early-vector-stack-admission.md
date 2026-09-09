---
title: "Early vector and stack admission"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - privileged-entry-exit-and-execution-context
aliases: []
---

# Early vector and stack admission

Early entry must establish a safe stack and CPU-local identity before invoking ordinary kernel code. Hardware-provided entry state is only the beginning of this protocol.

## Scope and research question

Which state is trustworthy when an event arrives before entry bookkeeping is complete?

This report refines [component 2: Privileged entry, exit and execution context](../privileged-entry-exit-and-execution-context.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

Per-CPU entry storage includes normal, hard-entry, NMI-like and terminal stack profiles, CPU incarnation, nesting state and a minimal raw-frame location. Installation requires mapped storage, vector validity and a known addressing regime. Component 2 owns these resources; component 1 owns irreducible leaf code. Component 9 owns the reserved evidence slots referenced by the entry record.

### Protocol and publication points

HardwareEntry → SafeStack → RawStateCaptured → KernelAddressing → BookkeepingReady. Every intermediate instruction range has a declared reentry/fault policy. Save overwrite-prone architectural state before enabling any event that can replace it. Publish ordinary context tokens only after their invariants hold. A failure before that point uses the separately prepared terminal route, never a fabricated normal frame.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

An interrupted stack/base transition can make a second entry interpret user-controlled memory as kernel state. Guard pages detect some overflows but cannot rescue an entry whose own stack selection failed. Early diagnostics must not introduce instrumentation or stack use exceeding the remaining emergency reserve.

### Alternatives and tradeoffs

A single stack reduces storage but couples unrelated failure modes. Dedicated stacks add memory and reentry complexity; their sharing rules must be declared rather than inferred from vector names. Saving every register immediately simplifies reasoning but increases entry cost.

### Cross-architecture realization

x86 hardware frame/IST mechanisms, Arm ELR/SPSR and vector instructions, and RISC-V scratch/CSR entry require different early sequences. None universally supplies a complete software execution context or an independent stack for every event.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Inject each supported event at every transition cut and inspect stack/base selection.
- Corrupt normal-stack guards while preserving independent emergency storage; validate bounded terminal transfer.
- Verify that no ordinary dispatch or context-token constructor is reachable before bookkeeping is coherent.

The first safe instruction boundary and nested-transition proof remain specific to each backend profile.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Frame normalization and bounded dispatch](frame-normalization-and-dispatch.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Linux entry/exit handling](../../../30-sources/linux-kernel-community-2026-entry-exit-handling.md) — Ordering and instrumentation restrictions in partial entry states.
- [AArch64 Exception Model](../../../30-sources/arm-2025-aarch64-exception-model.md) — Hardware exception capture is only part of software context preservation.
- [RISC-V privileged architecture](../../../30-sources/risc-v-international-2026-privileged-architecture.md) — Privilege and trap semantics qualified by extensions.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
