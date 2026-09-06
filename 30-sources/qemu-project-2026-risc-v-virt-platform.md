---
title: "QEMU RISC-V virt platform documentation"
kind: source
created: "2026-09-05"
authors:
  - "QEMU contributors"
published: null
citation_key: "qemu-risc-v-virt-docs-2026-09-05"
container: "QEMU documentation"
edition: "master documentation; displayed version 11.1.50"
isbn: null
doi: null
url: "https://www.qemu.org/docs/master/system/riscv/virt.html"
accessed: "2026-09-05"
tags:
  - boot
  - emulation
  - proof-of-concept
  - risc-v
aliases:
  - "QEMU virt target evidence"
---

# QEMU RISC-V virt platform documentation

## Reference

QEMU contributors. *'virt' Generic Virtual Platform (virt)*. QEMU master
documentation, displaying version 11.1.50 when accessed 2026-09-05.
[Official page](https://www.qemu.org/docs/master/system/riscv/virt.html).
The page does not identify a publication date or immutable source revision.

## Research question or contribution

Does an established emulator provide a plausible first target for a small
protected Atom OS kernel?

## Method

Read the platform description, device inventory, generated-DTB behavior, boot
options, and version label. No QEMU binary, firmware, or guest was run.

## Findings

`virt` is synthetic rather than a model of a particular physical board. It
supports RV32/RV64 CPUs, interrupt controllers, NS16550-compatible serial I/O,
and virtio transports. QEMU can generate a device tree for guest discovery.
Documented boot configurations include supervisor-mode payloads with OpenSBI.

## Relevance

Project inference: this is a useful candidate for the first boot/protection
experiment. A single-core profile can postpone physical-board variation while
testing an actual guest privilege boundary.

## Limits

A moving manual is not a pinned implementation or an Atom OS boot result.
Select and test the precise emulator, firmware, CPU features, and invocation.
No performance, hardware-fidelity, or hostile-device guarantee is inferred.

## Derived work

- [Proof-of-concept research readiness](../20-notes/proof-of-concept-research-readiness.md)
- [Proof-of-concept map](../10-maps/proof-of-concept.md)
