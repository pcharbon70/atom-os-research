---
title: "Linux reliability, availability, and serviceability documentation"
kind: source
created: "2026-09-02"
authors:
  - "The Linux kernel development community"
published: null
citation_key: "linux-kernel-community-2026-ras-documentation"
container: "The Linux Kernel documentation"
edition: "Latest documentation accessed 2026-09-02"
isbn: null
doi: null
url: "https://www.kernel.org/doc/html/latest/admin-guide/RAS/main.html"
accessed: "2026-09-02"
tags:
  - diagnostics
  - fault-containment
  - hardware-errors
  - kernel-interfaces
  - ras
aliases:
  - "Linux RAS documentation"
---

# Linux reliability, availability, and serviceability documentation

## Reference

The Linux kernel development community. [*Reliability, Availability and
Serviceability (RAS)*](https://www.kernel.org/doc/html/latest/admin-guide/RAS/main.html),
latest documentation accessed 2026-09-02.

## Research question or contribution

How does a mature portable kernel collect, normalize, report, and sometimes
contain hardware-error evidence supplied through several architecture and
firmware mechanisms?

## Method

The current RAS guide and its linked EDAC, machine-check, APEI, trace-event,
memory-failure, and error-record material were read as implementation precedent.
The analysis extracts distinctions and failure constraints rather than treating
Linux policy or its user-space ABI as a proposed Atom OS interface.

## Findings

- Error detection and correction reporting distinguishes corrected events from
  uncorrected events; a corrected-event count can inform maintenance but does
  not prove that a later uncorrected failure is predictable.
- Error evidence may be harvested from memory controllers, CPU machine-check
  facilities, firmware-defined APEI sources, PCIe, or device-specific paths.
  Source, severity, containment, and notification context are therefore
  independent fields rather than one portable exception number.
- A normalized record is useful for reporting, but raw source registers and
  firmware records remain necessary because decoding evolves and vendor data
  can exceed a common schema.
- Some errors can be associated with a page or component and routed into a
  containment action; others are asynchronous, imprecise, or evidence of wider
  machine corruption. Handler return alone does not establish recovery.
- Polling, interrupt, and exception delivery have different timeliness and
  overwrite risks. Collection must account for source-specific latching and
  record lifetime.
- RAS reporting can expose physical topology, physical addresses, error
  locations, and source-register details. Diagnostics therefore require an
  explicit confidentiality and access policy.

## Relevance

The proposed architecture-fault component should keep raw and normalized data,
represent confidence and containment separately, and defer restart policy to a
higher recovery service. It should use bounded preallocated capture records and
versioned decoders so a new decoder can interpret evidence after a crash.

## Limits

Linux supports many legacy and vendor mechanisms and has a larger policy and
compatibility surface than this project requires. The documentation describes
software interfaces, not proof that particular hardware reports complete or
accurate containment information. Online content may change after the access
date.

## Derived work

- [Architecture faults and diagnostics](../20-notes/architecture-faults-and-diagnostics.md)
- [Kernel hardware and architecture support layer](../20-notes/kernel-hardware-and-architecture-support-layer.md)
- [Kernel hardware and architecture support map](../10-maps/kernel-hardware-and-architecture-support.md)
