---
title: "ACPI Specification 6.6"
kind: source
created: "2026-08-29"
authors:
  - "UEFI Forum"
published: 2025
citation_key: "uefi-forum-2025-acpi-6-6"
container: "Advanced Configuration and Power Interface Specification"
edition: "Version 6.6"
isbn: null
doi: null
url: "https://uefi.org/sites/default/files/resources/ACPI_Spec_6.6.pdf"
accessed: "2026-08-29"
tags:
  - acpi
  - hardware-discovery
  - numa
  - operating-systems
  - power-management
  - ras
aliases:
  - "ACPI 6.6"
---

# ACPI Specification 6.6

## Reference

UEFI Forum. *Advanced Configuration and Power Interface Specification*,
version 6.6, May 2025. [Official PDF](https://uefi.org/sites/default/files/resources/ACPI_Spec_6.6.pdf)
and [ACPI specification page](https://uefi.org/specifications/). Accessed
2026-08-29.

## Research question or contribution

What platform topology, interrupt, NUMA, power, thermal, and hardware-error
information can ACPI provide, and what complexity would an ACPI-capable kernel
need to contain?

## Method

The reading sampled the table-discovery model, namespace and AML execution,
MADT interrupt topology, SRAT/SLIT NUMA description, GTDT timer description,
IORT I/O topology, power and sleep objects, and APEI hardware-error interfaces.

## Findings

- ACPI is both a collection of declarative tables and an executable namespace
  whose control methods are encoded in AML. Supporting the full model is much
  more than parsing a few packed structures.
- Tables cover CPU and interrupt-controller enumeration, proximity domains and
  distance, timers, I/O translation topology, power states, thermal policy
  hooks, and standardized error records.
- Firmware data is untrusted input from the kernel's perspective: lengths,
  checksums, revisions, overlapping ranges, identifiers, references, and AML
  resource effects require validation before use.
- ACPI can support hardware replacement and standards-based servers well, but
  it brings a large parser/interpreter and substantial firmware variation into
  the bring-up path.

## Relevance

ACPI should be one front end to a normalized resource graph, not the identity
or API used by memory, interrupt, timer, IOMMU, or power subsystems. A minimal
first target can defer AML while admitting a declared table subset; physical
server support will eventually require a tested interpreter strategy.

## Limits

The specification describes compliant behavior, not real firmware defects. It
does not establish that a table is correct or that a power transition is safe
on a particular board. PCI, processor, interrupt-controller, and IOMMU details
remain in other specifications.

## Derived work

- [Hardware and architecture support for the Zig kernel](../20-notes/hardware-and-architecture-support-for-the-zig-kernel.md)
- [Hardware and architecture support map](../10-maps/hardware-and-architecture-support.md)
- [Reference hardware-contract inquiry](../40-inquiries/which-hardware-contract-should-the-kernel-adopt.md)
