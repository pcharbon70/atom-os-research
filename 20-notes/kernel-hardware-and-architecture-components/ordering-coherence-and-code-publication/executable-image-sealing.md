---
title: "Executable image sealing"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - ordering-coherence-and-code-publication
aliases: []
---

# Executable image sealing

Sealing should close every path that can modify the executable extent before binding the image identity. Removing one writable mapping is not proof that the physical bytes are immutable.

## Scope and research question

What must be closed before opaque bytes and their metadata commitment can become SealedCode?

This report refines [component 4: Ordering, coherence and code publication](../ordering-coherence-and-code-publication.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

The minimal kernel owns one ExecutableImage aggregate with its resource account, lifetime group and references to authoritative Frame and Mapping objects. Component 4 owns private CodePublicationState. CodeWriteLease and SealedCode are state/authority views, not additional allocation owners. The seal covers initialized bytes, page-granular executable extent, zeroed padding, physical lineage, writer epochs and opaque runtime-metadata commitment.

### Protocol and publication points

WritableOwned → Sealing → WritableTranslationClosing → CodeSealQuiescent → Sealed. Close writer admission before collecting CPU, DMA/device, temporary and diagnostic writer paths. Restrict aliases through their owning components and wait for their exact completion predicates. Hash only the final immutable extent and bind the metadata commitment to that image generation. Failed or interrupted sealing retains references and a named recovery owner.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

A retained writable alias, device write or privileged temporary mapping can modify a supposedly sealed image. Hashing first and closing writers later permits a digest/content mismatch. The kernel does not interpret BEAM stack maps or relocations; a metadata commitment is not proof that runtime metadata is semantically correct.

### Alternatives and tradeoffs

Permanent RW/RX aliases support convenient patching but do not satisfy this immutability contract. Copy-to-seal can simplify writer exclusion at a memory cost, provided the destination has no uncontrolled writer. A runtime-only promise is insufficient across mutually distrustful domains.

### Cross-architecture realization

Write exclusion depends on CPU and device protection mechanisms; cache coherence cannot supply it. Cross-ISA backends may enforce different granules, but the sealed physical extent and remaining writer inventory must remain explicit.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Retain one hidden CPU alias or delayed DMA store and require seal refusal or incomplete state.
- Race writer death and cancellation with alias restriction; verify no unowned retained frame.
- Change padding, physical backing or metadata generation and require a different or rejected sealed identity.

Complete writer/alias enumeration and the combined CodeSealQuiescent proof remain unverified.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Executable publication transaction](executable-publication-transaction.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Thunderclap](../../../30-sources/markettos-et-al-2019-thunderclap.md) — DMA spatial and temporal exposure despite translation protection.
- [Arm threaded code-publication article](../../../30-sources/bramley-2025-arm-self-modifying-code-threads.md) — Writer-side synchronization does not synchronize every executing core.
- [seL4 reference manual](../../../30-sources/sel4-foundation-2026-reference-manual.md) — Capability-mediated authority and distinct kernel object kinds.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
