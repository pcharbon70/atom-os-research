---
title: "Primitive contract registry"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - unsafe-architecture-primitives-capsule
aliases: []
---

# Primitive contract registry

Every raw primitive should have an inspectable effect contract and a narrow set of authorized importers. An instruction mnemonic or an unsafe marker is insufficient to explain the state in which execution is valid.

## Scope and research question

How can reviewers identify the complete preconditions and effects of each privileged leaf?

This report refines [component 1: Unsafe architecture-primitives capsule](../unsafe-architecture-primitives-capsule.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

PrimitiveContract records backend, privilege, feature prerequisites, admitted context classes, CPU incarnation, inputs, register/flag clobbers, compiler memory effects, architectural scope, possible faults and postconditions. It links a model and concrete test identities. Feature witnesses refer to protected enabled-state records, not copyable evidence that remains valid forever. The semantic component validates authority before invoking the capsule; the capsule never grants mapping or device access.

### Protocol and publication points

Specified → BackendBound → PreconditionsValidated → Invoked → LocalEffectEstablished. Proof status is separate metadata, progressing only with actual evidence. Rebind or feature disable invalidates dependent witnesses. A registry query cannot mint authority. Generated inventories must expose every assembly symbol and foreign mechanism boundary, including terminal paths and compiler-emitted helpers.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

A stale witness can authorize an instruction after CPU migration or restart. Module privacy helps trusted-code organization but does not constitute a security boundary against arbitrary privileged memory corruption. In Zig, token copying is not intrinsically prohibited; validate current protected state and consume generations where the operation demands uniqueness.

### Alternatives and tradeoffs

Per-call full dynamic checking is expensive but easy to observe. Static composition and lexical wrappers reduce accidental misuse; lifecycle-sensitive checks still need runtime state. A giant architecture interface makes the inventory look smaller while obscuring effect differences.

### Cross-architecture realization

The contract names effects shared across ISAs, but register encodings and instruction availability remain backend-specific. No architecture's local primitive can issue a global completion witness solely because its own instruction retired.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Reject cross-CPU, wrong-context and stale-feature witness use.
- Scan imports, linked symbols and assembly sites; every privileged mechanism must map to a contract.
- Have an adversarial backend omit or widen one declared effect and require conformance failure.

The registry schema and generated call-graph/effect checks remain proposals, not a sound compiler-enforced effect system.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Register, control and local-mask leaves](register-control-and-mask-leaves.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Zig language reference](../../../30-sources/zig-project-2026-language-reference-0-16.md) — Lifetime discipline, atomics and assembly remain explicit obligations.
- [Serval](../../../30-sources/nelson-et-al-2019-serval.md) — Symbolic machine-code analysis within a declared model.
- [CertiKOS](../../../30-sources/gu-et-al-2016-certikos.md) — Observable refinement with explicit machine-model exclusions.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
