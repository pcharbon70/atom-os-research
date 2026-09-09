---
title: "Cross-component completion composition"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - typed-kernel-facing-architecture-facade
aliases: []
---

# Cross-component completion composition

The facade should compose completion evidence structurally while preserving its scope. A single unqualified Done value cannot safely represent every memory, CPU, device and diagnostic obligation.

## Scope and research question

How can callers join multiple component protocols without losing the distinctions needed for reclamation and authority transfer?

This report refines [component 10: Typed kernel-facing architecture facade](../typed-kernel-facing-architecture-facade.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

CompletionPredicate names operation identity, object generation, resource range, participant incarnation set and guarantee class. A CompositeOperation contains an immutable dependency graph. CPU translation, software-reader lifetime, executable publication, DMA permission, device traffic and evidence custody contribute distinct predicates. The facade composes their owners; it does not mint substitute completion proofs.

### Protocol and publication points

Validate a well-founded dependency graph → reserve retained ownership → admit constituent operations → collect identity-matched predicates → evaluate the declared join → transfer the permitted authority or release resources → publish terminal disposition. A failed contributor preserves the unmet dependency and retained custody. Retry creates explicit successor relations rather than editing historical evidence.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

A completion may be valid but cover the wrong range, generation or participant set. Joining local instruction synchronization with remote notification does not establish remote execution readiness. Cyclic dependencies can deadlock even when each component is locally correct. A newer membership snapshot cannot erase an older target's obligation.

### Alternatives and tradeoffs

Hand-written joins in each caller can optimize a hot path but duplicate subtle scope checks. A typed composition service centralizes those checks at a modeling and storage cost. A universal global stop may simplify some joins but has severe availability implications and still needs verified stop semantics.

### Cross-architecture realization

Completion kinds deliberately retain architectural differences. An Arm synchronization, x86 invalidation or RISC-V remote operation enters a join only through its documented semantic predicate, not by matching opcode categories.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Substitute a valid predicate from another generation or narrower range; the join must stay incomplete.
- Create a cross-component dependency cycle and require admission-time rejection or an explicitly proved acyclic protocol.
- Complete every contributor except one retained software reader; no composite release may occur.

The cross-component dependency graph and completeness of release joins need formal refinement and adversarial fault exploration.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Conformance, observation and escape hatches](conformance-observation-and-escape-hatches.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [CertiKOS](../../../30-sources/gu-et-al-2016-certikos.md) — Observable refinement with explicit machine-model exclusions.
- [The Multikernel](../../../30-sources/baumann-et-al-2009-multikernel.md) — Explicit inter-core protocols and replicated-state tradeoffs.
- [CleanQ](../../../30-sources/haecki-et-al-2019-cleanq.md) — Transfer-set conservation under cooperative ownership assumptions.
- [Arm SMMUv3 architecture](../../../30-sources/arm-2025-smmuv3-architecture.md) — IOMMU command and translation-cache synchronization scope.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
