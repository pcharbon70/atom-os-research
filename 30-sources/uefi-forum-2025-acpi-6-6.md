---
title: "Advanced Configuration and Power Interface specification, version 6.6"
kind: source
created: "2026-09-02"
authors:
  - "Unified Extensible Firmware Interface Forum"
published: 2025
citation_key: "uefi-forum-2025-acpi-6-6"
container: "UEFI Forum specifications"
edition: "6.6"
isbn: null
doi: null
url: "https://uefi.org/specs/ACPI/6.6/"
accessed: "2026-09-02"
tags:
  - acpi
  - boot
  - firmware
  - hardware-discovery
  - topology
aliases:
  - "ACPI 6.6"
---

# Advanced Configuration and Power Interface specification, version 6.6

## Reference

Unified Extensible Firmware Interface Forum. *Advanced Configuration and Power
Interface Specification*, release 6.6, May 2025.
[Official HTML specification](https://uefi.org/specs/ACPI/6.6/) and
[versioned PDF](https://uefi.org/sites/default/files/resources/ACPI_Spec_6.6.pdf).

## Research question or contribution

Which ACPI data can a boot normalizer use as early immutable platform facts,
and which parts imply a continuing interpreter or firmware dependency?

## Method

The table discovery, system-description tables, address-map, MADT, SRAT, SLIT,
and namespace portions were inspected. Static tables are distinguished from
AML methods and run-time power-management policy.

## Findings

- Root and child tables are length-delimited, signature/version identified,
  and checksummed. Validating an outer pointer is therefore insufficient; every
  followed table requires independent bounds, length, and checksum validation.
- MADT entries describe processors and several interrupt-controller families,
  including APIC, GIC, and RISC-V controller structures. Entry types and
  lengths are extensible and unknown entries must not be decoded as known ones.
- SRAT and SLIT describe processor, memory, and initiator proximity, but these
  are topology inputs rather than scheduling or allocation decisions.
- The UEFI memory map and ACPI address-map interfaces have different purposes.
  Reserved firmware and MMIO ranges cannot be inferred safely from topology
  tables alone.
- AML namespace evaluation is executable platform behavior with much larger
  complexity and run-time effects than copying static discovery tables.

## Relevance

The early boot component should parse only a small allowlist of static tables,
copy their validated bytes, retain unknown records for audit, and publish
descriptive topology. AML and power policy should be deferred to a separately
isolated service or omitted from the first platform profile.

## Limits

Checksums detect accidental corruption, not a malicious or defective firmware
producer. ACPI permits broad platform variation and does not establish that
two tables agree. A concrete port must pin the accepted table set and quirks.

## Derived work

- [Normalized boot handoff and feature discovery](../20-notes/normalized-boot-handoff-and-feature-discovery.md)
