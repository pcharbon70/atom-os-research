---
title: "Devicetree specification, release 0.4"
kind: source
created: "2026-09-02"
authors:
  - "Devicetree.org Technical Steering Committee"
published: 2023
citation_key: "devicetree-org-2023-devicetree-specification-0-4"
container: "Devicetree specification"
edition: "0.4"
isbn: null
doi: null
url: "https://github.com/devicetree-org/devicetree-specification/releases/tag/v0.4"
accessed: "2026-09-02"
tags:
  - boot
  - devicetree
  - hardware-discovery
  - memory-map
aliases:
  - "DTSpec 0.4"
---

# Devicetree specification, release 0.4

## Reference

Devicetree.org Technical Steering Committee. *Devicetree Specification*,
release 0.4, 28 June 2023.
[Official release](https://github.com/devicetree-org/devicetree-specification/releases/tag/v0.4)
and [specification project](https://www.devicetree.org/specifications/).

## Research question or contribution

What validation and lifetime rules follow from accepting a flattened device
tree as the boot program's hardware-description handoff?

## Method

The flattened format, client program requirements, CPU and memory nodes,
memory reservation block, `/reserved-memory`, and interrupt description were
read as the normative transport and base vocabulary.

## Findings

- A flattened device tree is a size- and offset-described binary object with
  structure, string, and reservation blocks. Each block, token, string offset,
  cell width, and alignment must be checked within the declared total size.
- The memory reservation block protects ranges the client must not overwrite,
  including boot or firmware data that may remain live. `/reserved-memory`
  adds named static or dynamic reservations; `no-map` and `reusable` are
  mutually exclusive.
- Address and size cell counts are inherited through the tree. Treating every
  `reg` tuple as fixed-width host-endian integers is incorrect.
- `compatible` strings and binding-specific properties identify mechanisms;
  they do not prove that a device is trustworthy or that every optional
  property is present.
- Under a UEFI boot, the UEFI memory map rather than the device-tree `/memory`
  node is the source for system memory. Static reserved-memory declarations
  must also be represented consistently in the UEFI map; a consumer must not
  add usable RAM from the device tree.

## Relevance

A device-tree adapter should be a bounded, non-recursive or depth-bounded
parser that copies the blob before reclaim, preserves binding provenance, and
emits only validated descriptors. On UEFI, only the UEFI map seeds usable RAM;
device-tree reservations can restrict that view but cannot enlarge it.
Conflicts should become reserved/conflicted facts, never usable RAM.

## Limits

The base specification does not validate vendor bindings or prove that a tree
matches physical hardware. Bindings evolve separately. Board-specific devices
and policy remain outside a common boot snapshot.

## Derived work

- [Normalized boot handoff and feature discovery](../20-notes/kernel-hardware-and-architecture-components/normalized-boot-handoff-and-feature-discovery.md)
