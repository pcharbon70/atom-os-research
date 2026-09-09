---
title: "Validated less-privileged return"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - privileged-entry-exit-and-execution-context
aliases: []
---

# Validated less-privileged return

Returning to a less-privileged domain should consume an exact current return authority, not replay an arbitrary saved register block. The last transition remains faultable and must have its own failure route.

## Scope and research question

What prevents a stale or forged return image from crossing privilege, mapping or code-publication boundaries?

This report refines [component 2: Privileged entry, exit and execution context](../privileged-entry-exit-and-execution-context.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

UserReturnEnvelope binds target domain/thread and CPU incarnations, register shape, stack/program addresses, permitted status, translation activation and current execution-admission evidence. Component 3 owns mapping/activation facts; component 4 owns code-publication generation. Component 2 validates and commits the return using those dependencies. A return authorization neither grants new memory mappings nor repairs absent code-publication completion.

### Protocol and publication points

ReturnPrepared → EnvelopeValidated → DependenciesPinned → FinalStateRestored → ReturnArmed → LessPrivileged. Keep admission closed or current dependency guards held while final state is installed. If an earlier validation can be invalidated by concurrent mapping or lifecycle changes, revalidate under the final guard. A fault at the return instruction transfers the armed record and evidence custody into nested-fault handling rather than treating the return as completed.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Canonical address checks alone do not establish legal privilege, segment/status combinations, mapped stack or execution eligibility. Reusing an old frame after migration can bind the wrong CPU state. An exception return is not automatically an ordinary-memory or instruction-publication barrier. Diagnostics cannot release the envelope's storage while a faulting final transition still references it.

### Alternatives and tradeoffs

Always using the general return path reduces special-case analysis but does not remove validation. A fast path may be added only as refinement of the same admitted envelope; separate acceptance rules would create a privilege bypass.

### Cross-architecture realization

IRET/SYSRET-like, ERET and SRET paths differ in validation, restored state and synchronization. The facade promises a validated transition, not one instruction. Research on Arm exceptions specifically warns against assuming return itself supplies a general memory fence.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Fuzz privilege/status bits, malformed addresses, selectors and enabled extended-state combinations.
- Race mapping restriction and code retirement with final return admission; require exclusion or current proof.
- Inject a fault at the final restore/return sequence and verify that custody and terminal handling remain valid.

Final-return linearization, concurrent admission closure and return-fault recovery are unproved.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Extended-state ownership and context transfer](extended-state-ownership-transfer.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Linux entry/exit handling](../../../30-sources/linux-kernel-community-2026-entry-exit-handling.md) — Ordering and instrumentation restrictions in partial entry states.
- [Relaxed exception semantics for Arm-A](../../../30-sources/simner-et-al-2024-relaxed-exception-semantics.md) — Precise exception transitions are not general memory barriers.
- [Intel system-programming documentation](../../../30-sources/intel-2026-system-programming-documentation.md) — ISA-specific privileged state and completion requirements.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
