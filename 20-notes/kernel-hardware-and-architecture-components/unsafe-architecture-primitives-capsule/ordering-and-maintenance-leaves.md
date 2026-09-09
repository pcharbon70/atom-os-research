---
title: "Ordering and maintenance leaves"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - unsafe-architecture-primitives-capsule
aliases: []
---

# Ordering and maintenance leaves

The capsule should expose distinct local effects for compiler ordering, CPU-memory ordering, translation maintenance and instruction-context synchronization. Semantic components assemble these leaves into larger protocols.

## Scope and research question

How can the interface prevent one fence or flush from being treated as every kind of completion?

This report refines [component 1: Unsafe architecture-primitives capsule](../unsafe-architecture-primitives-capsule.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

Each leaf names affected access classes, memory type, address range, shareability domain, local scope and required preconditions. A compiler clobber constrains code generation; it is not itself a device or CPU barrier. Translation operations consume validated backend context/range descriptions from component 3. Cache operations consume plans from component 4. The capsule owns instructions and clobbers, not remote target sets or reclaimed frames.

### Protocol and publication points

Receive a validated immutable leaf plan → check exact context/feature generation → execute the prescribed sequence → return its local postcondition. The caller then advances its own protocol ledger. Publication, invalidation and completion are separate transitions. An unexpected fault transfers evidence to component 9 while the semantic operation retains ownership; no raw exception handler silently marks a global operation successful.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

The relaxed-exception research rules out using exception entry/return as a general replacement for memory ordering. A locally completed instruction-fetch action does not prove another CPU observed new code. Cache invalidation can destroy dirty data if the plan omitted ownership and preservation preconditions.

### Alternatives and tradeoffs

Always choosing the strongest available operation may simplify individual calls but cannot fix wrong scope or missing ownership. Precise leaves permit conservative strengthening within an effect domain; optimizations must refine the same caller-visible postcondition.

### Cross-architecture realization

Arm data barriers and instruction synchronization, RISC-V FENCE/FENCE.I/SFENCE.VMA, and x86 ordering/serialization facilities are not mnemonic equivalents. Their effects must be lowered from the semantic request and the exact profile.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Use litmus tests distinguishing compiler publication, store buffering and exception-boundary ordering.
- Make a fake local fence succeed while another CPU has not acted; global completion must stay open.
- Inject range overflow, stale context identifiers and dirty-data invalidation without a preservation proof.

Cross-layer compiler-to-ISA refinement and concurrent interruption of leaf sequences are not proved.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Device, counter and wait leaves](device-counter-and-wait-leaves.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Relaxed exception semantics for Arm-A](../../../30-sources/simner-et-al-2024-relaxed-exception-semantics.md) — Precise exception transitions are not general memory barriers.
- [x86-TSO](../../../30-sources/sewell-et-al-2010-x86-tso.md) — Store buffering within a deliberately limited formal domain.
- [RISC-V unprivileged architecture](../../../30-sources/risc-v-international-2026-unprivileged-architecture.md) — Local instruction-fetch synchronization scope.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
