---
title: "Unified Extensible Firmware Interface specification, version 2.11"
kind: source
created: "2026-09-02"
authors:
  - "Unified Extensible Firmware Interface Forum"
published: 2024
citation_key: "uefi-forum-2024-uefi-2-11"
container: "UEFI Forum specifications"
edition: "2.11"
isbn: null
doi: null
url: "https://uefi.org/specs/UEFI/2.11/"
accessed: "2026-09-02"
tags:
  - boot
  - firmware
  - memory-map
  - uefi
aliases:
  - "UEFI 2.11"
---

# Unified Extensible Firmware Interface specification, version 2.11

## Reference

Unified Extensible Firmware Interface Forum. *Unified Extensible Firmware
Interface Specification*, release 2.11, December 2024.
[Official HTML specification](https://uefi.org/specs/UEFI/2.11/) and
[versioned PDF](https://uefi.org/sites/default/files/resources/UEFI_Spec_Final_2.11.pdf).

## Research question or contribution

What exact ownership, lifetime, and data-format obligations exist at the UEFI
loader-to-operating-system transition?

## Method

The boot manager, system table, boot services, memory allocation, configuration
table, and runtime services sections were read as normative interface
definitions. The analysis focuses on handoff rather than firmware internals.

## Findings

- `GetMemoryMap()` returns a descriptor array, a descriptor size and version,
  and a map key. Consumers must stride by the returned descriptor size rather
  than assuming the currently known structure size.
- `ExitBootServices()` succeeds only with the current map key. A loader must
  obtain a new map and retry when the key has become stale; after a failed first
  attempt, the allowed boot-service calls are restricted.
- After successful exit, boot-services function pointers and handle protocols
  are invalid. Boot-services code and data become reclaimable, while runtime
  ranges and configuration data retain different lifetime requirements.
- The memory map describes installed RAM and firmware-reserved ranges, but
  other tables can refine platform topology, interrupt controllers, and memory
  attributes. The formats therefore cannot be collapsed by reinterpreting one
  table as complete truth about every physical address.
- Runtime services are an optional continuing firmware dependency with their
  own virtual-address transition. Retaining them enlarges the run-time trust
  and failure boundary.

## Relevance

A normalized handoff should be produced only after the final successful exit,
copy every borrowed descriptor it needs, preserve the source revision and raw
provenance, and represent retained runtime services as a typed external gate.
The kernel must never keep a live pointer into reclaimable boot-services data.

## Limits

UEFI standardizes an interface, not firmware correctness. It does not prove
that descriptors are mutually consistent, that configuration tables are safe
to parse, or that reported topology matches hardware. Platform errata and
secure-boot policy are outside the memory-handoff contract.

## Derived work

- [Normalized boot handoff and feature discovery](../20-notes/kernel-hardware-and-architecture-components/normalized-boot-handoff-and-feature-discovery.md)
