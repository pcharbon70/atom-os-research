---
title: "The Limine boot protocol"
kind: source
created: "2026-09-02"
authors:
  - "The Limine project"
published: null
citation_key: "limine-project-2026-limine-boot-protocol"
container: "Limine protocol documentation"
edition: "Trunk documentation accessed 2026-09-02"
isbn: null
doi: null
url: "https://github.com/limine-bootloader/limine-protocol/blob/trunk/PROTOCOL.md"
accessed: "2026-09-02"
tags:
  - boot
  - bootloader
  - kernel-interface
  - portability
aliases:
  - "Limine protocol"
---

# The Limine boot protocol

## Reference

The Limine project. *The Limine Boot Protocol*, current trunk documentation
accessed 2 September 2026.
[Canonical protocol document](https://github.com/limine-bootloader/limine-protocol/blob/trunk/PROTOCOL.md).

## Research question or contribution

What does a contemporary cross-architecture loader protocol reveal about a
useful native kernel handoff, response versioning, and borrowed-memory lifetime?

## Method

The general ABI, base revisions, machine-state requirements, memory map,
firmware pointers, device tree, multiprocessor, executable, and measurement
features were reviewed as engineering precedent rather than a normative choice
for this project.

## Findings

- The protocol uses versioned request/response records and specifies an entry
  ABI for x86-64, AArch64, RISC-V, and LoongArch. Optional responses remain
  discoverable instead of being represented by guessed defaults.
- Response structures are placed in bootloader-reclaimable memory. Their
  lifetime is explicit and forces the kernel to copy or preserve what it uses.
- The memory map distinguishes usable, reserved, ACPI, bad, bootloader-
  reclaimable, executable/module, framebuffer, and mapped-reserved ranges;
  even then, some non-usable ranges may overlap or lack page alignment.
- Revisions have changed pointer interpretation, higher-half mapping, cache
  attributes, and which ranges are mapped. A version number therefore changes
  semantics, not merely structure length.
- The protocol can provide raw ACPI, EFI, device-tree, TPM-log, CPU, and timer
  facts but deliberately does not normalize them into kernel policy.

## Relevance

Limine is useful evidence for a narrow loader adapter and a versioned native
`BootEnvelope`. The proposed kernel format should improve on it by using
offsets instead of borrowed pointers, a total length and digest, canonical
non-overlapping memory extents, provenance per record, and explicit conflict
records.

## Limits

The canonical document follows a moving trunk and is not a peer-reviewed
evaluation. A conforming loader is still trusted to implement the protocol.
The project should pin a tested revision rather than depend on `trunk` in a
reproducible build.

## Derived work

- [Normalized boot handoff and feature discovery](../20-notes/kernel-hardware-and-architecture-components/normalized-boot-handoff-and-feature-discovery.md)
