---
title: "Generated ABI and binary assurance"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - unsafe-architecture-primitives-capsule
aliases: []
---

# Generated ABI and binary assurance

The assembly boundary should be derived from one representation schema and checked against the linked binary. Correct source declarations cannot establish what a compiler emitted at entry, interrupt or foreign-function boundaries.

## Scope and research question

How can saved frames and procedure calls agree across generated offsets, Zig code, assembly and foreign components?

This report refines [component 1: Unsafe architecture-primitives capsule](../unsafe-architecture-primitives-capsule.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

One ABI schema defines field width, offset, alignment, stack convention, preserved/clobbered registers, calling convention, permitted instructions and helper dependencies. Generate constants for assembly and compile-time checks for language-visible records. Keep hardware entry frames distinct from ordinary C ABI aggregates. Attach binary symbol, code range and build identity to each reviewed primitive contract.

### Protocol and publication points

Schema → generated representations → compile-time layout checks → link → disassembly and helper census → model/translation checks → evidence-bound release of a backend profile. A compiler or flags change invalidates dependent binary evidence. Naked/entry symbols call ordinary functions only after stack and register prerequisites are established. Foreign code has explicit allocator, panic, blocking and callback assumptions.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

A compiler may use vector registers in apparently integer code, introduce a helper call, or instrument an early-entry function. Layout equality does not prove calling convention or lifetime agreement. Serval and translation validation motivate checks but their verified domains do not cover arbitrary SMP interference, cache behavior or transient-execution leakage.

### Alternatives and tradeoffs

Hand-maintained assembly offsets avoid generator complexity but duplicate the authoritative representation. Generated offsets still require independent checks to catch generator bugs. Whole-program verification offers stronger assurance only for the machine behavior actually modeled.

### Cross-architecture realization

Procedure ABI, hardware entry ABI and boot ABI are separate on every ISA. Zig extern layout may describe a C boundary; it does not describe an interrupt frame or confer linear resource ownership. Cross-ISA backends may use different raw frames while preserving normalized semantic records.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Deliberately alter one generated offset and require build or binary-conformance rejection.
- Inspect entry-critical call graphs for unexpected helpers, allocation, instrumentation and extended-state use.
- Run ABI sentinel tests across a narrow foreign boundary and separately inject nested entry around its admissible call sites.

No compiler-output proof, binary qualification or executing entry test was performed by this research.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Primitive contract registry](primitive-contract-registry.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Zig language reference](../../../30-sources/zig-project-2026-language-reference-0-16.md) — Lifetime discipline, atomics and assembly remain explicit obligations.
- [Serval](../../../30-sources/nelson-et-al-2019-serval.md) — Symbolic machine-code analysis within a declared model.
- [Translation validation for a verified OS kernel](../../../30-sources/sewell-et-al-2013-translation-validation.md) — Checking compiler output rather than trusting source structure.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
