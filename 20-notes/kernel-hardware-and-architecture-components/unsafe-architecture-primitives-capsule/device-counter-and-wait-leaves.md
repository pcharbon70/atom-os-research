---
title: "Device, counter and wait leaves"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - unsafe-architecture-primitives-capsule
aliases: []
---

# Device, counter and wait leaves

Device accesses, counter observations and wait/terminal instructions belong in a small leaf family whose side effects are explicit. These facilities expose mechanisms; they do not own driver servicing, timer policy or recovery decisions.

## Scope and research question

What must be declared when an apparently simple read, write or halt can have external or irreversible effects?

This report refines [component 1: Unsafe architecture-primitives capsule](../unsafe-architecture-primitives-capsule.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

Device leaves bind access width, byte order, authorized region, mapping type and read/write side effects. Counter leaves record source generation, width and ordering relative to surrounding execution. Wait leaves state which wake conditions remain enabled and which predicates must be rechecked. Terminal leaves accept only the appropriate preclassified or post-seal fault context; a normal caller cannot obtain reset authority from a raw port number.

### Protocol and publication points

Validate a prepared access or wait condition → execute a bounded local sequence → expose observation or local issue status. Posted-write receipt requires a separately selected safe completion mechanism. A waiter registers interest and rechecks work before entering the architecture-specific wait sequence; after wake it rechecks rather than assuming the expected event occurred. Halt/reset leaves follow a prevalidated finite fallback policy.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

A read-to-clear register is not a harmless readback target. A single MMIO instruction may stall indefinitely on a broken interconnect, so bounded software instruction count does not prove bounded wall time. Masking every wake source before halt creates a progress failure. Terminal diagnostics must not depend on an ordinary device driver or allocator.

### Alternatives and tradeoffs

Inlining all accesses is fast but hides repetition, widths and ordering from review. A generic callback interface can obscure bounds. Statically bound leaves plus explicit ordered, relaxed and completion variants make those tradeoffs inspectable.

### Cross-architecture realization

Port I/O is not universally present; counter access may be privilege-gated or firmware-mediated. WFI/WFE/HLT-like operations have architecture-specific wake semantics. No generic Wait operation promises physical power removal or immunity from nonordinary events.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Delay a posted write and verify issue status is not reported as receipt.
- Inject work between the final condition test and wait entry; demonstrate a wake or visible pending condition.
- Exercise inaccessible counter/MMIO registers, spurious wakeups and a failed optional terminal sink.

Interconnect timeout behavior, wakeup proofs and terminal-action availability remain platform-profile obligations.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Generated ABI and binary assurance](generated-abi-and-binary-assurance.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Linux device-I/O contracts](../../../30-sources/linux-kernel-community-2026-device-io-contracts.md) — Posted-write receipt differs from CPU-side ordering.
- [RISC-V privileged architecture](../../../30-sources/risc-v-international-2026-privileged-architecture.md) — Privilege and trap semantics qualified by extensions.
- [Zig language reference](../../../30-sources/zig-project-2026-language-reference-0-16.md) — Lifetime discipline, atomics and assembly remain explicit obligations.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
