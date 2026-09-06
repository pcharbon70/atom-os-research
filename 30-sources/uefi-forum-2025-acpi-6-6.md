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
accessed: "2026-09-05"
tags:
  - acpi
  - boot
  - crash-evidence
  - firmware
  - hardware-discovery
  - hardware-errors
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
and which error interfaces imply continuing firmware, serialization, or
recovery dependencies?

## Method

The table discovery, system-description tables, address-map, MADT, SRAT, SLIT,
namespace, and Architecture Platform Error Interface portions were inspected.
Static descriptions are distinguished from AML, run-time firmware behavior,
and error-record persistence operations.

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
- APEI separates error-source discovery and notification (HEST), boot-time
  evidence (BERT), serialization/persistence operations (ERST), and controlled
  error injection (EINJ). These are different evidence and control channels and
  must not be collapsed into one generic firmware-fault path.
- ERST defines begin/read/write/clear/execute/status/end protocols and reports
  storage-full, unavailable, failed, empty, and not-found outcomes. Software may
  need to poll a busy indication.
- Error-record order and backend durability are platform dependent. EINJ tests
  the reporting stack but does not prove that a real hardware fault, corrupted
  interconnect, or power loss follows the same path.

## Relevance

The early boot component should parse only a small allowlist of static tables,
copy their validated bytes, retain unknown records for audit, and publish
descriptive topology. AML and power policy should be deferred to a separately
isolated service or omitted from the first platform profile. APEI adapters
should preserve raw CPER evidence, declare firmware and storage dependencies,
bound every poll with a finite deadline and reserved-memory fallback rather
than assuming firmware progress, and distinguish injected from observed faults.

## Limits

Checksums detect accidental corruption, not a malicious or defective firmware
producer. ACPI permits broad platform variation and does not establish that
two tables agree. A concrete port must pin the accepted table set and quirks.

## Derived work

- [Normalized boot handoff and feature discovery](../20-notes/kernel-hardware-and-architecture-components/normalized-boot-handoff-and-feature-discovery.md)
- [Fault decoder](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/fault-decoder.md)
- [Crash-safe sink](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/crash-safe-sink.md)
