---
title: "Executable publication transaction"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - ordering-coherence-and-code-publication
aliases: []
---

# Executable publication transaction

Executable publication should admit an immutable image only while all affected execution is controlled, then commit after translation and instruction-fetch obligations are complete. Installing an executable mapping is an intermediate effect.

## Scope and research question

When is an image safe for every authorized executor to enter?

This report refines [component 4: Ordering, coherence and code publication](../ordering-coherence-and-code-publication.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

A publication operation holds SealedCode, authorized mapping scope, an exact PublicationSetWitness, execution-suspension participation and preallocated result storage. It references the parent address-space and image incarnations, target set and backend plan digest. Component 3 performs subordinate mapping operations; component 4 alone establishes PublishedCode authority.

### Protocol and publication points

Reserve all resources → accept operation → close and drain execution admission → establish data visibility → install RX while suspended → perform instruction-state actions → collect per-target fetch acknowledgements → atomically commit publication and release the operation's suspension contribution. Parent-state checks still govern the final commit. Cancellation after visible effects must drain/restrict them before returning a terminal resource state.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

An executor entering between the last acknowledgement and publication commit can observe an unqualified generation unless admission and membership are coupled. A stale successful mapping token does not prove the same image/space still exists. Partial publication cannot return an ordinary pre-admission error or abandon suspension and pins.

### Alternatives and tradeoffs

Stop-the-world publication is easier to reason about but has responsiveness costs. Fine-grained suspension can narrow disruption only with complete executor tracking. In-place compatible patching is a distinct weaker profile and cannot substitute for immutable publication or revocation.

### Cross-architecture realization

The instruction-fetch action differs across x86, Arm and RISC-V. Arm writer-side ISB is not broadcast; RISC-V FENCE.I is local. Data visibility, context synchronization and lifecycle admission must all be accounted rather than inferred from one instruction.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Try to enable RX before execution admission closes and require rejection.
- Delay one CPU acknowledgement, cancel concurrently and verify no premature execution or frame release.
- Close the address space at final commit and check the parent protocol's retain/quarantine outcome.

Publication/cancellation linearizability and complete executor-set discovery need a composed model.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Publication membership and catch-up](publication-membership-and-catch-up.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Arm threaded code-publication article](../../../30-sources/bramley-2025-arm-self-modifying-code-threads.md) — Writer-side synchronization does not synchronize every executing core.
- [RISC-V unprivileged architecture](../../../30-sources/risc-v-international-2026-unprivileged-architecture.md) — Local instruction-fetch synchronization scope.
- [Relaxed exception semantics for Arm-A](../../../30-sources/simner-et-al-2024-relaxed-exception-semantics.md) — Precise exception transitions are not general memory barriers.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
