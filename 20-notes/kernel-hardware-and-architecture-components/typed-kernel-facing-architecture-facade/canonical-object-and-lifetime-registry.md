---
title: "Canonical object and lifetime registry"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - typed-kernel-facing-architecture-facade
aliases: []
---

# Canonical object and lifetime registry

The facade should expose one canonical object model with generation-checked views. A convenient wrapper must never become an independent owner of a resource already governed by another component.

## Scope and research question

How can the facade make misuse difficult in Zig while maintaining correct object identity and lifetime across asynchronous operations?

This report refines [component 10: Typed kernel-facing architecture facade](../typed-kernel-facing-architecture-facade.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

Each object kind has a protected registry entry containing identity, generation, owner, allowed operations and outstanding views. IRQBinding and ExecutableImage views refer to their owning components. Authority-bearing handles remain distinct from diagnostic identifiers. Zig structs, tagged unions, opaque pointers and module boundaries organize the interface; registry checks enforce stale-handle rejection and single-consumer transitions.

### Protocol and publication points

Create under the owning component → register a fresh generation → grant constrained views → validate identity and authority at each effectful admission → close new views → drain accepted operations → retire registry entry → permit generation-safe reuse. Borrowed views do not extend lifetime unless their retention is explicitly recorded.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Zig does not provide a general borrow checker or linear type system. A private constructor cannot prevent a caller from copying an already valid value. Pointer hiding does not establish memory safety against arbitrary privileged corruption. Type shape reduces accidental misuse but does not replace the kernel's actual protection boundary.

### Alternatives and tradeoffs

Raw pointers minimize lookup overhead but distribute lifetime reasoning to every caller. Generational registries add validation cost and central metadata, which may be specialized away only where equivalent invariants are proven. Language-enforced linearity would improve ergonomics but is not an assumed Zig facility.

### Cross-architecture realization

Object identity and lifetime are common semantics. ISA-specific register values, physical identifiers and firmware handles stay behind typed backend objects rather than becoming portable authority tokens.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Copy a handle, consume it once and attempt the same effect through the copy; protected state must reject the duplicate.
- Destroy and recreate an object in the same storage; every old view must remain invalid.
- Export diagnostics and verify they contain no value accepted as an authority-bearing handle.

Registry exhaustion, generation wrap and performance of checked views need analysis; no implementation or language-level ownership proof is claimed.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Authorization and execution-context admission](authorization-and-context-admission.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Zig language reference](../../../30-sources/zig-project-2026-language-reference-0-16.md) — Lifetime discipline, atomics and assembly remain explicit obligations.
- [seL4 reference manual](../../../30-sources/sel4-foundation-2026-reference-manual.md) — Capability-mediated authority and distinct kernel object kinds.
- [Tock deployment retrospective](../../../30-sources/schuermann-et-al-2025-tock-decade.md) — Typed interfaces still require sound ABI and runtime validation.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
