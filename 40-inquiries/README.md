---
title: "Inquiries"
kind: map
created: "2026-08-28"
tags:
  - archive-navigation
  - directory-index
aliases:
  - "Inquiries index"
---

# Inquiries (`40-inquiries`)

## Purpose

Inquiries are active research workbenches organized around answerable
questions.

## What belongs here

Put open questions, provisional hypotheses, evidence paths, findings, and
resolution criteria here. Promote independently useful conclusions to
`20-notes`.

## Index

### Subdirectories

- None yet.

### Documents

- [What evidence would change the kernel language choice?](what-evidence-would-change-the-kernel-language-choice.md) — explicit assumptions and falsifiable conditions for reconsidering Zig versus C.
- [Can C meet the kernel qualification contract?](can-c-meet-the-kernel-qualification-contract.md) — alternative/fallback compiler, ABI, library and privileged-execution qualification; Zig remains selected.
- [Can Zig meet the kernel qualification contract?](can-zig-meet-the-kernel-qualification-contract.md) — chosen-language compiler, C ABI, dependency closure and privileged-execution evidence still needed.
- [Can a minimal bootable system validate the architecture?](can-a-minimal-bootable-system-validate-the-architecture.md) —
  tracks the T7500 / Intel x86-64 first native CLI boot, protected service control, CLI-launched
  BEAM/GC, and integrated recovery/resource/fault gates, informed by nineteen
  requirement studies without treating research completion as gate evidence.
- [How should Atom OS structure applications and domain services?](how-should-atom-os-structure-applications-and-domain-services.md) —
  defines falsifiable semantic, identity, invariant, persistence, workflow,
  effect, presentation, collaboration, extension, evolution, tenancy,
  overload, and recovery criteria for the fifth layer.
- [What visual-computing model should Atom OS adopt?](what-visual-computing-model-should-atom-os-adopt.md) —
  asks whether a user-programmable semantic project can be built from isolated
  actors, primary accessibility semantics, disposable presentation, and
  capability-scoped live tools, with explicit usability and recovery tests.
- [What contract should system-wide authentication and authorization provide?](what-contract-should-system-wide-authentication-and-authorization-provide.md) —
  defines falsifiable evidence, session, policy, grant, capability, revocation,
  recovery, distributed-consistency, and assurance criteria for security
  across all five layers.
- [What contract should the kernel hardware and architecture layer provide?](what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) —
  defines authority, completion, isolation, ordering, portability, recovery,
  and performance criteria for the privileged architecture boundary, with
  unresolved compositional proof obligations from the service decompositions.
- [What contract should the managed actor runtime provide?](what-contract-should-the-managed-actor-runtime-provide.md) —
  defines falsifiable compatibility, memory, signal, scheduling, resource,
  native-isolation, distribution, replay, and fault criteria for the
  unprivileged BEAM-compatible runtime layer.
- [What contract should the minimal privileged kernel provide?](what-contract-should-the-minimal-privileged-kernel-provide.md) —
  defines falsifiable capability, domain, IPC, temporal-isolation, fault,
  teardown, recovery-independence, BEAM-compatibility, and assurance criteria,
  with open compositional obligations from the 54 internal-service studies.
- [What contract should the OTP-like system-services layer provide?](what-contract-should-the-otp-like-system-services-layer-provide.md) —
  defines falsifiable lifecycle, outcome, durability, naming, distributed
  authority, update, overload, evidence, and outer-recovery criteria for the
  unprivileged policy layer.
- [Which BEAM, ERTS, and OTP principles belong in a new kernel?](which-beam-erts-and-otp-principles-belong-in-the-kernel.md) —
  defines layer-placement criteria for required BEAM compatibility, compares
  a pinned ERTS port with a new compatible runtime, and specifies the minimum
  experiments needed to choose between them.

## Maintaining this index

Index every direct inquiry, describe its present focus, and keep `status`
aligned with the actual state of the research.
