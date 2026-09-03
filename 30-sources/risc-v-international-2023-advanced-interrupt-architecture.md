---
title: "The RISC-V advanced interrupt architecture"
kind: source
created: "2026-09-02"
authors:
  - "John Hauser"
published: 2023
citation_key: "risc-v-international-2023-advanced-interrupt-architecture"
container: "RISC-V Ratified Specifications Library"
edition: "Version 1.0, with 2025-03-12 clarifications"
isbn: null
doi: null
url: "https://docs.riscv.org/reference/aia/index.html"
accessed: "2026-09-02"
tags:
  - interrupt-controllers
  - interrupts
  - message-signaled-interrupts
  - risc-v
aliases:
  - "RISC-V AIA 1.0"
---

# The RISC-V advanced interrupt architecture

## Reference

John Hauser, editor. *The RISC-V Advanced Interrupt Architecture*, version 1.0,
ratified June 2023, including clarifications dated 2025-03-12.
[Official specification](https://docs.riscv.org/reference/aia/index.html).

## Documented mechanism

The specification defines ISA interrupt extensions, the per-hart Incoming MSI
Controller, the Advanced Platform-Level Interrupt Controller, IPI mechanisms,
and IOMMU interactions for virtual interrupt delivery.

## Method

This is a normative architecture and controller specification. The analysis
focuses on identities, pending/enabled state, delivery, claim, routing, and the
boundary between wired and message-signaled sources.

## Findings

- AIA distinguishes ISA facilities from separately instantiated platform
  components. A kernel cannot infer an IMSIC, APLIC, IOMMU, capacity, or
  topology from the RISC-V ISA name alone.
- An IMSIC contains interrupt files per hart and privilege/virtualization
  context. Each file records pending and enabled bits for MSI identities; an
  MSI is a configured memory write naming the target file and identity.
- A combined read/write of a top-interrupt CSR can return and claim the
  highest-priority eligible identity by clearing its pending bit.
- Writes and controller-state changes may become visible only eventually, and
  the specification exposes priority, identity-count, routing, and
  virtualization limits.
- APLIC supports wired sources and can deliver directly or translate them to
  MSIs, so wired trigger semantics and downstream message delivery remain
  different layers of one route.

## Relevance

The common event model should describe source kind, controller chain, route,
delivery identity, target context, and completion needs as feature data. A
flat raw interrupt number would conflate identifiers whose scope is a
controller, hart interrupt file, privilege level, or virtual context.

## Limits

AIA does not choose a concrete platform topology, prove a controller
implementation, define driver-side device acknowledgement, or supply the
kernel's capability and storm-accounting policies. Smaller RISC-V systems may
use the older PLIC or another controller instead.

## Derived work

- [Interrupt event fabric](../20-notes/kernel-hardware-and-architecture-components/interrupt-event-fabric.md)
