---
title: "RISC-V platform-level interrupt controller specification"
kind: source
created: "2026-09-02"
authors:
  - "RISC-V Task Group"
published: "2023-03-11"
citation_key: "risc-v-international-2023-platform-level-interrupt-controller"
container: "RISC-V Ratified Specifications Library"
edition: "Version 1.0.0, ratified"
isbn: null
doi: null
url: "https://docs.riscv.org/reference/plic/index.html"
accessed: "2026-09-02"
tags:
  - interrupt-controllers
  - interrupts
  - risc-v
aliases:
  - "RISC-V PLIC 1.0.0"
---

# RISC-V platform-level interrupt controller specification

## Reference

RISC-V Task Group. *RISC-V Platform-Level Interrupt Controller Specification*,
version 1.0.0, ratified 2023-03-11.
[Official specification](https://docs.riscv.org/reference/plic/index.html).

## Documented mechanism

The specification defines the PLIC's source priorities, per-context enables
and thresholds, notifications, non-idempotent claim operation, and explicit
completion messages.

## Method

This is a normative controller specification. The analysis focuses on the
observable flow and scope of source, target context, claim, and completion
rather than its example register-map maxima.

## Findings

- A target claims by reading a context-specific claim/complete register. The
  controller atomically selects the highest-priority pending enabled source,
  returns its identifier, and clears its pending bit; zero means no claimable
  source.
- Claim is a non-idempotent MMIO operation. It cannot be treated as an
  ordinary cached read or safely repeated without changing controller state.
- Completion is a later write of the claimed source identifier to the same
  target context. Controller completion is distinct from clearing the
  device-side interrupt condition.
- Source identity and priority are controller concerns, while the association
  of target contexts with harts and privilege modes is partly a platform
  concern outside this specification.

## Relevance

The interrupt fabric needs a flow token that remembers the exact target
context and claimed identity until the valid completion point. It also needs a
platform profile rather than assuming PLIC context numbers are global CPU or
capability identities.

## Limits

The PLIC specification does not define capability authority, event delivery to
drivers, storm containment, CPU hotplug, virtualization, or the semantics of a
particular device's interrupt line. AIA/IMSIC is a different mechanism family
and requires a different flow plan.

## Derived work

- [Interrupt event fabric](../20-notes/interrupt-event-fabric.md)
