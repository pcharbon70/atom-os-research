---
title: "Ordinary-memory synchronization"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - ordering-coherence-and-code-publication
aliases: []
---

# Ordinary-memory synchronization

The ordinary-memory contract should begin with the source language and then justify its lowering to hardware. Successful execution on a strongly ordered processor is not evidence that a shared protocol is race-free or portable.

## Scope and research question

Which synchronization effects may shared kernel objects assume, and in which execution contexts?

This report refines [component 4: Ordering, coherence and code publication](../ordering-coherence-and-code-publication.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

For every shared field declare owner, atomic width/alignment, allowed access orders and the invariant protected. Distinguish locks, release/acquire publication, reference admission and intentionally specialized primitives. Lock contracts name whether readers can interrupt writers. Snapshot storage lifetime is a separate obligation from checking a sequence number.

### Protocol and publication points

Construct private state → release-publish its identity → acquire current state → operate under the declared owner/lock/atomic protocol → close admission → drain readers before reuse. A failed generation recheck discards a logical observation; it cannot legalize an already invalid pointer access or source-language data race. Bounded contexts need a bounded retry/fallback contract rather than a generic spin loop.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

An interrupt reader spinning on an odd sequence while its writer is suspended can livelock. Recycled pointer-bearing snapshots are unsafe without independent lifetime protection. A wider atomic may lower to a helper or lock unsuitable for entry context. Acquire/release naming alone does not establish a correct reference-count or reclamation algorithm.

### Alternatives and tradeoffs

Sequential consistency simplifies some reasoning but does not solve lifetime, deadlock or wrong ownership. Specialized lock-free paths can reduce contention only after their progress and memory-model assumptions are explicit. Ordinary short locks may be easier to verify where interruption rules permit them.

### Cross-architecture realization

x86-TSO covers a limited ordinary-memory domain, not devices, page tables or executable modification. Arm and RISC-V require their own model mappings. Zig atomics and pointer lifetime rules must be respected independently of a borrowed Linux algorithm.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Run message-passing, store-buffering, failed-CAS and publication/reclamation litmus cases under the declared model.
- Suspend a writer in every intermediate state and invoke readers from admitted interrupt contexts.
- Retain a reader across generation rollover and attempted storage reuse; forbid stale dereference.

A complete source-language model and compiler/ISA refinement for the proposed kernel protocols remains to be established.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Typed MMIO ordering and completion](typed-mmio-ordering-and-completion.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [x86-TSO](../../../30-sources/sewell-et-al-2010-x86-tso.md) — Store buffering within a deliberately limited formal domain.
- [Concurrency in the Linux kernel](../../../30-sources/alglave-et-al-2018-linux-kernel-concurrency.md) — Executable litmus models and reclamation reasoning.
- [Sequence counters and sequential locks](../../../30-sources/linux-kernel-community-2026-sequence-counter-contracts.md) — Reader consistency does not establish pointer lifetime or bounded progress.
- [Zig language reference](../../../30-sources/zig-project-2026-language-reference-0-16.md) — Lifetime discipline, atomics and assembly remain explicit obligations.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
