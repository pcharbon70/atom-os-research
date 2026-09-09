---
title: "What the Proofs Assume"
kind: source
created: "2026-09-09"
authors: ["seL4 Foundation"]
published: null
citation_key: "sel4-foundation-2026-proof-assumptions"
container: "seL4 verification documentation"
edition: null
isbn: null
doi: null
url: "https://sel4.systems/Verification/assumptions.html"
accessed: "2026-09-09"
tags: [capabilities, kernel-internal-services, microkernels]
aliases: []
---

# What the Proofs Assume

## Reference

seL4 Foundation. [What the Proofs Assume](https://sel4.systems/Verification/assumptions.html). seL4 verification documentation; publication date not stated. Accessed 2026-09-09.

## Research question or contribution

What remains outside a kernel correctness or security theorem?

## Method

Read the assembly, hardware management, boot, virtual-memory, DMA, information-channel and binary-verification qualifications.

## Findings

The page states assumptions about machine behavior and selected low-level mechanisms. DMA and timing channels require explicit qualifications; binary verification applies to supported configurations, not every build.

## Relevance

Maintain separate assurance obligations for authority enforcement, hardware completion, bootstrap configuration and availability. The proposed Zig kernel inherits none of seL4's proofs.

## Limits

This is a high-level explanation, not a complete versioned theorem inventory. Historical code-size figures and configuration coverage must not be generalized to all current seL4 platforms.

## Derived work

- [Device completion and reset composition](../20-notes/minimal-privileged-kernel-components/memory-mappings-and-architecture-resource-bindings/device-completion-and-reset-composition.md) — proposed contract constrained by this evidence.
- [Fault taxonomy and bounded capture](../20-notes/minimal-privileged-kernel-components/fault-capture-and-containment/fault-taxonomy-and-bounded-capture.md) — proposed contract constrained by this evidence.
- [Containment escalation and terminal handoff](../20-notes/minimal-privileged-kernel-components/fault-capture-and-containment/containment-escalation-and-terminal-handoff.md) — proposed contract constrained by this evidence.
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md) — selective architectural context.
