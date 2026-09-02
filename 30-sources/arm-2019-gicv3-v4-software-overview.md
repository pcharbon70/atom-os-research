---
title: "Arm CoreLink GICv3 and GICv4 software overview"
kind: source
created: "2026-09-02"
authors:
  - "Arm Limited"
published: 2019
citation_key: "arm-2019-gicv3-v4-software-overview"
container: "Arm AArch64 Programmer's Guides"
edition: "DAI0492, version 3.0"
isbn: null
doi: null
url: "https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/Learn%20the%20Architecture/GICv3_v4_overview.pdf"
accessed: "2026-09-02"
tags:
  - arm64
  - interrupt-controllers
  - interrupts
  - multicore
aliases:
  - "GICv3/v4 software overview"
---

# Arm CoreLink GICv3 and GICv4 software overview

## Reference

Arm Limited. *Arm CoreLink GICv3 and GICv4: Software Overview*, DAI0492,
version 3.0, 2019.
[Official guide](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/Learn%20the%20Architecture/GICv3_v4_overview.pdf).

## Documented mechanism

The guide explains GICv3/v4 interrupt types, source state, priority, routing,
acknowledgement, end-of-interrupt, and selected virtualization mechanisms for
an explicit AArch64 configuration.

## Method

This is an official software guide that complements, but does not replace, the
normative GIC architecture specification. The analysis extracts controller
state and flow obligations rather than copying register-level APIs.

## Findings

- The controller tracks inactive, pending, active, and active-and-pending
  states for ordinary sources; locality-specific interrupts use a different,
  simpler form.
- Edge-triggered and level-sensitive sources enter and leave those states
  differently. For a level source, device deassertion and controller
  deactivation are separate events.
- Acknowledgement chooses a pending interrupt and makes it active. Priority
  drop and deactivation can be coupled or separated depending on configured
  EOI mode.
- GICv3 supports per-CPU private interrupts, shared interrupts, software-
  generated interrupts, and MSI-backed locality-specific interrupts, with
  routing and capacity constraints exposed by the implementation.
- Reconfiguration should occur while a source is disabled; reset values and
  several capacities are implementation-defined.

## Relevance

An interrupt facade must retain a flow-specific state machine and cannot
reduce every source to `ack(); handler(); eoi()`. Binding, affinity migration,
and teardown need explicit stabilization, active-state drainage, and
generation changes before a route or destination can be reused.

## Limits

The guide deliberately treats a subset of GIC configurations, predates later
revisions, and is not the normative register specification. Exact behavior,
errata, ITS/LPI tables, security state, and virtualization support must be
pinned for the chosen controller implementation.

## Derived work

- [Interrupt event fabric](../20-notes/interrupt-event-fabric.md)
