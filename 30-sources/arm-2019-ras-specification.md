---
title: "Arm reliability, availability, and serviceability specification"
kind: source
created: "2026-09-05"
authors:
  - "Arm Limited"
published: 2019
citation_key: "arm-2019-ras-specification"
container: "Arm architecture specifications"
edition: "DDI 0587C.b"
isbn: null
doi: null
url: "https://documentation-service.arm.com/static/63f368eb9567172d4e2aadfa"
accessed: "2026-09-05"
tags:
  - arm64
  - diagnostics
  - hardware-errors
  - ras
aliases:
  - "Arm RAS DDI 0587C.b"
---

# Arm reliability, availability, and serviceability specification

## Reference

Arm Limited. *Arm Reliability, Availability, and Serviceability (RAS)
Specification*, DDI 0587C.b, July 2019. [Official
PDF](https://documentation-service.arm.com/static/63f368eb9567172d4e2aadfa).

## Research question or contribution

What ordering, validity, overflow, priority, and clearing semantics govern Arm
standard error records?

## Method

The normative error-record access, status, ordering, overwrite, clear, and
error-exception portions were read alongside the current A-profile architecture
manual. The standalone RAS issue is pinned so current decoder work does not
depend solely on a mutable `latest` URL.

## Findings

- Status validity, address validity, miscellaneous validity, correction,
  deferral, poison, uncorrected type, and overflow are independent fields.
  Fields whose prerequisite validity bits are absent can be architecturally
  unknown.
- Error records can be overwritten by higher-priority events, and simultaneous
  error ordering can be implementation defined. Software cannot equate one
  observed record with the chronologically first physical error.
- Software must capture status plus conditionally valid address and
  miscellaneous registers before applying the prescribed write-one-to-clear
  sequence. Clearing only a convenient subset can lose evidence or leave
  misleading state.
- After the W1C write, software reads `ERR<n>STATUS` back to determine whether
  validity actually cleared or a concurrent new error remains pending; write
  retirement alone is not the acknowledgement postcondition.
- Memory-mapped record ordering depends on the required device-memory mapping
  and access sequence; direct system-register reads can have different
  speculation and ordering properties.
- An uncorrected-error type can describe uncontainable, unrecoverable,
  latent/restartable, or signaled/recoverable state, but the handler still
  determines the concrete recovery action.
- Node inventory, extended syndrome, routing, and parts of error priority remain
  implementation-defined platform inputs.

## Relevance

The Arm capture backend must be generated from a pinned node/profile table that
fixes access path, register count, ordering, validity prerequisites, and exact
clear program. The decoder must preserve unknown and overflow. Arm's
recoverable labels may support a classifier premise but cannot independently
mint an Atom resume proof.

## Limits

This issue predates later Arm architectural extensions and does not identify a
specific SoC's nodes, firmware delegation, interrupt controller, or errata. A
concrete port must additionally pin the current A-profile manual issue and the
selected processor/platform documentation.

## Derived work

- [Bounded capture routine](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/bounded-capture-routine.md)
- [Fault decoder](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/fault-decoder.md)
- [Containment classifier and promotion](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/containment-classifier-and-promotion.md)
