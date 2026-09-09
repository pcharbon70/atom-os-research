---
title: "Authorization and execution-context admission"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - typed-kernel-facing-architecture-facade
aliases: []
---

# Authorization and execution-context admission

Permission to perform an operation and ability to perform it safely in the current context are independent admission checks. Exceptional execution must not silently widen authority.

## Scope and research question

How does a caller prove both resource authority and context suitability before the facade accepts effects?

This report refines [component 10: Typed kernel-facing architecture facade](../typed-kernel-facing-architecture-facade.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

OperationSchema declares required capability, object generation, context class, interrupt/preemption constraints, allocation and blocking rules, and result custody. Context witnesses describe observed kernel state and are validated where needed. NmiContext and FatalContext narrow allowed operations. Crash-context authority is available only after its declared seal; it does not turn arbitrary corrupted state into a trusted caller.

### Protocol and publication points

Resolve current object → validate authority → validate context and dependencies → reserve bounded resources → accept or reject without operation effects. If a context transition invalidates prerequisites, revalidate at the effect boundary. No generic fallback silently allocates, sleeps or invokes firmware in a context that forbids it.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

A compile-time parameter can be forged or stale if it merely asserts a runtime condition. Zig's type system cannot prove that interrupts remain masked or that a caller holds a particular live lease. Context admission also cannot prove recovery safety after arbitrary memory corruption; terminal paths need a smaller declared trust base.

### Alternatives and tradeoffs

One universal interface is easy to call but hides context-dependent behavior. Separate context-specific surfaces make restrictions reviewable at the cost of more explicit call sites. Static checking and runtime checks should complement each other, not be advertised as substitutes.

### Cross-architecture realization

Interrupt-mask state, privilege levels and firmware-call restrictions differ by backend. The portable context contract states permitted effects; a backend witness must justify it without pretending that all architectures have the same mask or exception hierarchy.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Invoke each operation from every context class and verify rejection precedes hardware effects where forbidden.
- Change context state between preliminary validation and acceptance; the operation must revalidate or hold an appropriate guard.
- Attempt a privileged action with a diagnostic ID or an exceptional-context witness alone; neither may confer authority.

The completeness of operation effect schemas and their behavior under nested faults require an independent audit.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Split-phase operation and terminal ownership](split-phase-operation-and-terminal-ownership.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [Zig language reference](../../../30-sources/zig-project-2026-language-reference-0-16.md) — Lifetime discipline, atomics and assembly remain explicit obligations.
- [Linux entry/exit handling](../../../30-sources/linux-kernel-community-2026-entry-exit-handling.md) — Ordering and instrumentation restrictions in partial entry states.
- [Flux OSKit](../../../30-sources/ford-et-al-1997-flux-oskit.md) — Component dependencies include their execution environment.
- [CertiKOS](../../../30-sources/gu-et-al-2016-certikos.md) — Observable refinement with explicit machine-model exclusions.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
