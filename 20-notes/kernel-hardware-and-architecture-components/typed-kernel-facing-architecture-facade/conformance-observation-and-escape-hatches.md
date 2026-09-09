---
title: "Conformance, observation and escape hatches"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - typed-kernel-facing-architecture-facade
aliases: []
---

# Conformance, observation and escape hatches

Conformance should compare observable effects and failure behavior, not merely compile matching function signatures. Escape hatches require narrower review and cannot silently become the normal interface.

## Scope and research question

What evidence would justify claiming that a backend implements the facade's architecture contract?

This report refines [component 10: Typed kernel-facing architecture facade](../typed-kernel-facing-architecture-facade.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

Maintain an operation inventory, effect schema, executable abstract model, backend trace adapter and a ledger of assumptions and exclusions. Observation records contain bounded identifiers and state transitions without authority. A raw escape hatch names its required context, touched state, clobbers, ordering, failure behavior and accountable owner; usage is visible in the review inventory.

### Protocol and publication points

Specify observable contract → derive positive and negative traces → compare a model and independent backend observations → inspect generated privileged code → reconcile deviations → qualify a versioned profile. Fake backends establish orchestration properties only; hardware-facing evidence must separately establish the claimed instruction, device and concurrency effects.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

Tests can agree because both model and backend repeat the same error. Formal results depend on machine models and trusted toolchains; CertiKOS and Serval do not prove every aspect of this architecture. Compiler optimization can invalidate informal assembly assumptions. Logging from critical paths can itself violate the contract being measured.

### Alternatives and tradeoffs

Testing alone gives fast feedback but weak coverage of adversarial interleavings. Formal modeling narrows uncertainty under explicit assumptions; binary validation addresses another boundary. A layered combination is stronger than any single technique but still cannot be represented as a completed proof before evidence exists.

### Cross-architecture realization

Conformance has common protocol tests and architecture-specific instruction, privilege and device tests. Cross-ISA agreement at the API surface is insufficient when one backend's hardware completion or fault model is weaker.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Inject a signature-compatible backend that performs a forbidden extra effect; trace conformance must detect it.
- Corrupt assembly clobber declarations or frame offsets and require generated-code or ABI checks to identify the mismatch.
- Audit every raw escape-hatch caller and verify there is no unbounded logging, allocation or blocking in restricted contexts.

No conformance suite, proof or binary experiment was executed in this research. The proposed evidence ladder remains to be realized.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Canonical object and lifetime registry](canonical-object-and-lifetime-registry.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [CertiKOS](../../../30-sources/gu-et-al-2016-certikos.md) — Observable refinement with explicit machine-model exclusions.
- [Serval](../../../30-sources/nelson-et-al-2019-serval.md) — Symbolic machine-code analysis within a declared model.
- [Translation validation for a verified OS kernel](../../../30-sources/sewell-et-al-2013-translation-validation.md) — Checking compiler output rather than trusting source structure.
- [Zig language reference](../../../30-sources/zig-project-2026-language-reference-0-16.md) — Lifetime discipline, atomics and assembly remain explicit obligations.
- [Tock deployment retrospective](../../../30-sources/schuermann-et-al-2025-tock-decade.md) — Typed interfaces still require sound ABI and runtime validation.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
