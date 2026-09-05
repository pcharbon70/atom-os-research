---
title: "Ramoops oops/panic logger"
kind: source
created: "2026-09-05"
authors:
  - "Sergiu Iordache"
published: "2021-02-10"
citation_key: "iordache-2021-ramoops"
container: "The Linux Kernel documentation"
edition: "Updated 10 February 2021; current documentation accessed 2026-09-05"
isbn: null
doi: null
url: "https://docs.kernel.org/admin-guide/ramoops.html"
accessed: "2026-09-05"
tags:
  - crash-dumps
  - diagnostics
  - persistent-memory
  - ras
aliases:
  - "Linux ramoops"
---

# Ramoops oops/panic logger

## Reference

Sergiu Iordache. [*Ramoops oops/panic
logger*](https://docs.kernel.org/admin-guide/ramoops.html), updated 10 February
2021; current Linux kernel documentation accessed 2026-09-05.

## Research question or contribution

What persistence, placement, mapping, overwrite, and corruption assumptions
apply when crash records are written to a predefined RAM region and read after
restart?

## Method

The official reservation, chunking, mapping-type, restart, overwrite, and
software-ECC rules were read as an implementation contract. The document's
“persistent RAM” terminology is kept distinct from cold-power persistence.

## Findings

- Ramoops writes oops/panic records to a predefined RAM range and exposes them
  after a supported restart. Fixed power-of-two chunks bound storage.
- Its occurrence counter resets on restart, and new dumps can overwrite old
  records.
- Mapping type is part of correctness. The document warns that atomic
  operations on strongly ordered mappings are implementation-defined and fail
  on many Arm systems; reserving an address alone does not prove the publication
  primitive works.
- Optional software ECC may detect or repair some RAM corruption after a
  watchdog-style reset. It neither authenticates records nor covers arbitrary
  memory-controller, cache, DMA, or cold-power failure.
- Placement configured dynamically can be best effort.

## Relevance

Ramoops supports the engineering feasibility of a fixed preallocated
reserved-memory first record and exposes the mapping, overwrite, and reset-
survival caveats that Atom must make explicit. As an Atom consequence of the
documented overwrite behavior, first-fatal retention needs a separately
specified slot and reclamation rule rather than inheriting circular-buffer
behavior. An Atom target must also verify the exact physical range, exclusion
from ordinary allocation and DMA, mapping, and retention class before
describing the region as a crash sink. Atom's alternating-bank commit,
first-fatal preservation, authenticated custody, and freshness protocol are
separate synthesis, not properties demonstrated by ramoops.

## Limits

This is implementation documentation, not a formal durability model or
controlled cross-platform evaluation. “Survives restart” does not imply cold-
power retention, malicious-tamper resistance, truthful producer data, DMA
exclusion, or bounded access under failed memory hardware.

## Derived work

- [Crash-safe sink](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/crash-safe-sink.md)
- [Double-fault guard](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/double-fault-guard.md)
- [Architecture faults and diagnostics](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics.md)
