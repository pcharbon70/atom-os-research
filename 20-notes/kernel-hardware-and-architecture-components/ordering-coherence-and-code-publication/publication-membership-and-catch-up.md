---
title: "Publication membership and catch-up"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - ordering-coherence-and-code-publication
aliases: []
---

# Publication membership and catch-up

A frozen publication target set is safe only if CPUs outside it cannot later execute with stale fetch state. Persistent generation evidence must connect publication to CPU joining, migration and return admission.

## Scope and research question

How does a CPU becoming eligible after publication prove it has caught up?

This report refines [component 4: Ordering, coherence and code publication](../ordering-coherence-and-code-publication.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

Maintain parent-owned CodePublicationGenerationState and exact image/address-space generation commitments. Membership witnesses name CPU identity plus incarnation, not a hardware number. A CPU admission guard records the publication generation and required synchronization program/digest it has completed. Component 7 controls lifecycle membership; component 2 checks the resulting evidence before user return.

### Protocol and publication points

Close execution admission → freeze current participants → synchronize the exact set → commit persistent publication generation. A later entrant executes the committed catch-up program in an admissible neutral context, verifies the still-current state and only then joins execution eligibility. A concurrent newer generation forces catch-up continuation or retry under bounded policy; it cannot be skipped because an earlier publication completed.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

CPU-number reuse causes ABA if acknowledgements omit incarnation. A CPU in neither the frozen set nor a closed future-admission path can escape synchronization. Removing a member from a software mask is not evidence it stopped fetching. Generation wrap must be a lifecycle event with drainage, not modular arithmetic.

### Alternatives and tradeoffs

Synchronizing every physically possible CPU wastes work and still needs a policy for absent CPUs. Generation-based deferred catch-up scales better but enlarges persistent state and admission obligations. Treating first use as an ordinary cache miss supplies no equivalent proof.

### Cross-architecture realization

Remote fetch maintenance mechanisms differ; the common result is current per-CPU admission evidence. Higher-privilege remote-operation APIs need their exact completion contract examined rather than being treated as universal post-handler acknowledgement.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Join a CPU at every cut between set freeze, final acknowledgement and commit.
- Replay acknowledgements after CPU restart and image-generation reuse.
- Race repeated publication with a slow entrant; demonstrate safe failure or bounded deferral without stale execution.

The interaction among publication, CPU removal and neutral-context catch-up remains a major formalization gap.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Executable retirement and quarantine](executable-retirement-and-quarantine.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [The Multikernel](../../../30-sources/baumann-et-al-2009-multikernel.md) — Explicit inter-core protocols and replicated-state tradeoffs.
- [RISC-V unprivileged architecture](../../../30-sources/risc-v-international-2026-unprivileged-architecture.md) — Local instruction-fetch synchronization scope.
- [RISC-V SBI](../../../30-sources/risc-v-international-2025-supervisor-binary-interface.md) — Separate higher-privilege start and remote-operation contracts.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
