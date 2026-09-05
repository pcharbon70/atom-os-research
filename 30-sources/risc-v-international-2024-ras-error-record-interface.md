---
title: "RISC-V RERI Architecture Specification"
kind: source
created: "2026-09-05"
authors:
  - "RERI Task Group"
published: "2024-05-24"
citation_key: "risc-v-international-2024-ras-error-record-interface"
container: "RISC-V Ratified Specifications Library"
edition: "Version v1.0, ratified 2024-05-24"
isbn: null
doi: null
url: "https://docs.riscv.org/reference/ras-eri/index.html"
accessed: "2026-09-05"
tags:
  - diagnostics
  - hardware-errors
  - ras
  - risc-v
aliases:
  - "RISC-V RERI 1.0"
---

# RISC-V RERI Architecture Specification

## Reference

RERI Task Group, RISC-V International. *RISC-V RERI Architecture
Specification*, version v1.0, ratified 2024-05-24. [Official HTML
specification](https://docs.riscv.org/reference/ras-eri/index.html) and
[versioned PDF](https://docs.riscv.org/reference/ras-eri/_attachments/riscv-reri.pdf).

## Research question or contribution

What standardized error-record semantics can a RISC-V operating system rely on
when the optional RERI facility is present, and which recovery conclusions
remain outside the specification?

## Method

The ratified introduction, bank layout, status, capture/overwrite, signaling,
address, implementation-specific information, reset, and injection rules were
read as normative interface definitions. RERI is treated as a separately
discovered optional platform facility, not as a mandatory property of the base
privileged ISA.

## Findings

- An implementation exposes memory-mapped banks containing up to 63 error
  records. The bank reports a layout version, vendor and implementation
  identity, instance identity, and record count; software must inspect these
  before interpreting later fields.
- Each record independently reports validity, corrected (`CE`), uncorrected
  deferred (`UED`), and uncorrected immediate (`UEC`) classes, priority,
  address/information type, transaction type, standardized or custom error
  code, and optional implementation-specific information and timestamp.
- A UEC record's containable bit says the error has not propagated beyond the
  detecting hardware unit and therefore *may* be containable. The specification
  explicitly leaves the actual recovery determination to the handler using
  further evidence; the bit is not a resume or recovery proof.
- Address provenance is explicit: no address, supervisor physical, guest
  physical, virtual, or component-specific information. Optional information
  registers can be implementation-defined and timestamps have unspecified
  clock, resolution, and frequency.
- Hardware sets `rdip` when a new record makes `v` valid and clears `rdip` when
  a later error updates an already valid record. Software first reads that state
  as-is, writes `sinv`, and rechecks: `v=0` means the prior record was
  invalidated; `v=1,rdip=1` means a new record arrived after invalidation; and
  `v=1,rdip=0` indicates possible overwrite during collection. Only a retry of
  that last case sets `rdip` through `srdp` before rereading. Error class and
  priority determine which records may replace others.
- Reset preservation is implementation dependent but uniform within a bank.
  A handler must not assume either that reset erased stale evidence or that a
  warm reset retained it.
- Record injection's `eid` expiry sets the selected record valid. When the
  record was invalid and signaling is configured, the resulting `v` 0→1
  transition generates the configured RAS signal; signaling may be disabled.
  This tests the software reporting path, not the hardware detector or corrupt-
  data propagation path. The captured status has no persistent normative “injected”
  flag. The specification warns that hardware injection controls require
  protection against malicious use.

## Relevance

Atom should define a versioned RERI raw-block decoder, preserve bank/profile
identity and overwrite/lost-evidence state, and map every field into independently valid
normalized facts. `containable` should contribute evidence to a conservative
classifier but must never mint `LocalResumePostcondition` by itself. Discovery
must distinguish `reri-v1.0` from `ras = none` and from vendor firmware records.
As a proposed Atom protocol, an Atom-initiated injection is labeled only when
authenticated out-of-band session metadata binds it to the captured record;
without such evidence, origin remains unknown. This does not exclude an
implementation-specific mechanism with its own independently validated
provenance contract.

This source corrects a broad statement in the existing architecture-fault note:
the mandatory privileged ISA still supplies no universal RAS taxonomy, but a
ratified optional RERI taxonomy now exists and should be supported explicitly.

## Limits

RERI standardizes error records, not how every platform discovers banks,
routes signals, contains corrupt data, resets a component, or recovers a
request. Many fields are WARL, optional, unspecified, or implementation
specific. A conforming minimal record can contain little more than validity and
read-in-progress state. RERI therefore improves evidence interoperability but
does not establish hardware correctness, completeness, or recoverability.

## Derived work

- [Bounded capture routine](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/bounded-capture-routine.md)
- [Fault decoder](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/fault-decoder.md)
- [Containment classifier and promotion](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/containment-classifier-and-promotion.md)
- [Architecture faults and diagnostics](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics.md)
