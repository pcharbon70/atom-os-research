---
title: "Devicetree Specification 0.4"
kind: source
created: "2026-08-29"
authors:
  - "Devicetree Specification contributors"
published: 2023
citation_key: "devicetree-org-2023-devicetree-0-4"
container: "Devicetree Specification"
edition: "Release v0.4"
isbn: null
doi: null
url: "https://github.com/devicetree-org/devicetree-specification/releases/tag/v0.4"
accessed: "2026-08-29"
tags:
  - boot
  - devicetree
  - hardware-discovery
  - operating-systems
  - platform-description
aliases:
  - "Devicetree v0.4"
  - "DTSpec 0.4"
---

# Devicetree Specification 0.4

## Reference

Devicetree Specification contributors. *Devicetree Specification*, release
v0.4, 28 June 2023. [Official release](https://github.com/devicetree-org/devicetree-specification/releases/tag/v0.4)
and [specification index](https://www.devicetree.org/specifications/). Accessed
2026-08-29.

## Research question or contribution

How can firmware describe a non-self-discovering system without embedding a
board-specific device inventory in the kernel?

## Method

The reading covered the flattened tree format, node and property model,
address and size cells, `reg`, `ranges`, interrupt mappings, CPU and memory
nodes, reserved memory, phandles, and boot-program obligations.

## Findings

- A Devicetree is boot-time data describing hardware that software cannot
  necessarily discover by probing. Nodes form a hierarchy; bindings assign
  semantics to compatible strings and properties.
- Address translation through buses, interrupt-parent relationships, reserved
  memory, and cross-node phandles make the data a graph even though the source
  syntax is a tree.
- The format is compact and has no AML interpreter, which makes it attractive
  for early bring-up and SoCs. Correct operation still depends on binding
  knowledge and on firmware supplying an accurate tree.
- Overlays, optional properties, inherited cells, malformed strings, invalid
  references, and overlapping resources require a validating parser. Raw node
  pointers should not become durable kernel object identity.

## Relevance

Devicetree is the preferred discovery input for the first RV64 bootstrap
profile. The kernel should consume it once into immutable, generation-tagged
CPU, memory, interrupt, timer, bus, and device records, after which drivers use
typed resource handles.

## Limits

The base specification does not define every device binding or guarantee that
boot firmware follows one platform convention. It is not an enumeration
protocol for hot-plug buses and does not decide driver policy.

## Derived work

- [Hardware and architecture support for the Zig kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md)
- [Hardware and architecture support map](../10-maps/hardware-and-architecture-support.md)
- [Reference hardware-contract inquiry](../40-inquiries/which-hardware-contract-should-the-kernel-adopt.md)
