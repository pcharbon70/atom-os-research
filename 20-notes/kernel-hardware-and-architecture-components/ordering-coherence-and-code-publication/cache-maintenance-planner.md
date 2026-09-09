---
title: "Cache-maintenance planner"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - ordering-coherence-and-code-publication
aliases: []
---

# Cache-maintenance planner

Cache maintenance should be selected from a semantic request with explicit ownership, aliases and participating agents. A range flush API that omits those dimensions cannot explain what has become visible.

## Scope and research question

How can maintenance plans be complete without overextending the authority or scope of their caller?

This report refines [component 4: Ordering, coherence and code publication](../ordering-coherence-and-code-publication.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

The planner receives an authorized byte extent, physical alias description, cacheability/shareability profile, participating agents, desired clean/invalidate effect and completion point. It derives line size and backend operations from admitted hardware evidence, not caller-supplied constants. Component 3 retains translation ownership and component 8 retains DMA transfer ownership.

### Protocol and publication points

Validate extent and authority → round with checked arithmetic → establish dirty-data preservation requirements → freeze immutable backend plan → execute local/remote actions → record exact effect evidence. Conservative strengthening is allowed only if it stays within authorized scope and preserves dirty data. Failures before acceptance reject; failures after visible effects retain the operation and its missing-agent set.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Outward rounding may touch unrelated mutable data sharing a cache line. Invalidate-without-clean can discard authoritative writes. Different aliases can use incompatible memory types. A local barrier or broadcast-capable operation may still leave execution-context synchronization outstanding on another CPU.

### Alternatives and tradeoffs

Whole-cache operations simplify range bookkeeping but increase interference and can violate unrelated ownership. Range operations improve isolation but need exact granule/alias reasoning. Hardware coherence removes some maintenance, not the need for transfer and publication ordering.

### Cross-architecture realization

Clean, invalidate, points of coherence/unification and shareability are backend-specific. Some profiles have no required explicit maintenance; that is an evidenced no-op effect, not a generic assumption. RISC-V instruction-fetch synchronization remains distinct from data-cache operations.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Exercise zero/overflowing ranges, partial cache lines and incompatible aliases.
- Have one participant miss its maintenance action; completion must remain incomplete.
- Attempt strengthening that expands to an unauthorized or concurrently owned line; reject the plan.

The planner's soundness and cost model need validation against exact cache hierarchies and interference assumptions.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Executable image sealing](executable-image-sealing.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Arm A-profile architecture](../../../30-sources/arm-2026-a-profile-system-architecture-documentation.md) — Architecture-specific exception, ordering and state contracts.
- [RISC-V unprivileged architecture](../../../30-sources/risc-v-international-2026-unprivileged-architecture.md) — Local instruction-fetch synchronization scope.
- [Arm threaded code-publication article](../../../30-sources/bramley-2025-arm-self-modifying-code-threads.md) — Writer-side synchronization does not synchronize every executing core.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
