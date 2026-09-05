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
accessed: "2026-09-05"
tags:
  - boot
  - crash-evidence
  - firmware
  - hardware-errors
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

What exact ownership, lifetime, data-format, and crash-record obligations exist
at the UEFI loader-to-operating-system transition and runtime boundary?

## Method

The boot manager, system table, boot services, memory allocation, configuration
table, runtime services, authenticated-variable, and Common Platform Error
Record sections were read as normative interface definitions. Firmware
internals remain outside the evidence claim.

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
- `HwErrRec####` variables can retain CPER hardware-error records in nonvolatile
  storage. UEFI permits a fatal Machine Check, NMI, or INIT path to invoke
  `SetVariable()` even when a runtime call was interrupted, but does not promise
  that the interrupted call completes or that firmware latency is bounded.
- CPER is a versioned evidence envelope with record and creator identifiers,
  section descriptors, validity bits, severity, timestamp, previous-session and
  simulated flags, restart/precision/context flags, and explicit lost-record
  indications. Those identifiers describe evidence; they are not authorization
  tokens.
- Successful variable replacement is crash-atomic at the variable level under
  the specified power-failure behavior, but available nonvolatile storage may be
  small. Base hardware-error variables do not by themselves establish encrypted
  contents, authenticated origin, or anti-replay freshness.

## Relevance

A normalized handoff should be produced only after the final successful exit,
copy every borrowed descriptor it needs, preserve the source revision and raw
provenance, and represent retained runtime services as a typed external gate.
The kernel must never keep a live pointer into reclaimable boot-services data.
For diagnostics, CPER should remain an immutable source view and firmware NVRAM
an optional bounded adapter after a reserved-memory record has already sealed.

## Limits

UEFI standardizes an interface, not firmware correctness. It does not prove
that descriptors are mutually consistent, that configuration tables are safe
to parse, or that reported topology matches hardware. Platform errata and
secure-boot policy are outside the memory-handoff contract. The specification
does not prove that firmware completes a fatal-context write within Atom's
deadline or that a stored CPER record is truthful, confidential, authentic, or
fresh.

## Derived work

- [Normalized boot handoff and feature discovery](../20-notes/kernel-hardware-and-architecture-components/normalized-boot-handoff-and-feature-discovery.md)
- [Fault decoder](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/fault-decoder.md)
- [Crash-safe sink](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/crash-safe-sink.md)
