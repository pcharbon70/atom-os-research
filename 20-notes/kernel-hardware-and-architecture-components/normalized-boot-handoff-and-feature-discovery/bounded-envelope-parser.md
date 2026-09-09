---
title: "Bounded envelope parser"
kind: note
created: "2026-09-08"
maturity: developing
tags:
  - architecture-support
  - kernel-architecture
  - normalized-boot-handoff-and-feature-discovery
aliases: []
---

# Bounded envelope parser

The envelope parser should convert an addressable byte extent into structurally valid records without dereferencing provider pointers or performing hardware effects. Structural validity remains separate from whether a record's claims are true.

## Scope and research question

Can malformed input be rejected with bounded work before it influences resource authority?

This report refines [component 0: Normalized boot handoff and feature discovery](../normalized-boot-handoff-and-feature-discovery.md). It concerns the full system architecture. Its objects and protocols are proposed synthesis; cited specifications, papers and engineering accounts supply constraints and precedents, not proof of this design.

## Development

### Owned state and authority boundary

An EnvelopeView carries a validated base extent, format version and a fixed resource budget. Parsed records retain source offsets and revisions. Use checked offset/length arithmetic, fixed-endian decoding, explicit alignment and record-count limits. A schema classifies singleton, repeatable, optional and critical records. Parsed output is owned by the boot transaction; no caller receives unchecked slices into memory that may be reclaimed.

### Protocol and publication points

Addressable → HeaderChecked → RecordsBounded → StructureValidated → ParsedView. Validate total extent before indexing; check multiplication and addition before computing an end; reject duplicate singletons and overlapping record encodings where the schema forbids them. Unknown optional records may remain opaque provenance; unknown critical semantics reject the handoff. Seal the structural result before semantic reconciliation; an error returns its bounded offset and reason, not a partially trusted snapshot.

The local sketch must be read with the parent's integrated lifecycle. It does not erase intermediate completion obligations or transfer another component's authority.

### Failure model and negative evidence

A parser can be memory-safe but algorithmically exploitable. Repeated references, recursive structures, adversarial sorting and huge strings need explicit budgets. Copying a changing source twice creates a validation/use mismatch: consume a single owned input snapshot or retain a source whose immutability is established. Digest comparison detects some mutation, not adversarial authenticity.

### Alternatives and tradeoffs

A universal firmware parser maximizes compatibility but exposes unrelated grammars. One normalized format narrows the resident parser and makes adapters separately testable. Zero-copy views reduce copying only when their full lifetime is accounted; otherwise copying bounded control data is the safer contract.

### Cross-architecture realization

The envelope format is architecture-neutral. Endianness, address width, alignment, physical addressability and firmware-pointer translation belong to explicit decoders rather than host-native casts. ACPI and flattened device tree remain input grammars, not the kernel object model.

## Verification obligations and open questions

The following are falsification criteria, not executed tests or verified results:

- Generate truncation at every field boundary, maximum integers, duplicate records, unknown critical revisions and zero-length loops.
- Assert memory use is bounded by the accepted envelope budget and runtime by the chosen parsing/sorting bounds.
- Mutate the original provider buffer after acquisition; semantic output must not change or follow replacement pointers.

A proof of total parsing, corpus coverage and worst-case resource bounds has not been produced.

Any eventual experiment must record the implementation and specification revisions, privilege and firmware dependencies, initial state, injected failures, observable transition trace and retained-resource accounting. Successful examples alone would not establish completeness of this contract.

## Connections

- [Service decomposition](README.md) — local ownership boundaries and complete inventory.
- [Memory extent reconciler](memory-extent-reconciler.md) — a related part of the same integrated component; neither service can substitute for the other's completion evidence.
- [Architecture-layer inquiry](../../../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md) — unresolved cross-component proof and trust questions.
- [Research session](../../../50-journal/2026-09-08-kernel-architecture-internal-services-deep-dive.md) — source-read depth, reconciliation and evidence limitations.

## Sources

- [BootStomp](../../../30-sources/redini-et-al-2017-bootstomp.md) — Empirical motivation for adversarial early-input analysis.
- [UEFI specification](../../../30-sources/uefi-forum-2024-uefi-2-11.md) — Provider memory-map and service-lifetime contracts.
- [Devicetree 0.4](../../../30-sources/devicetree-org-2023-devicetree-specification-0-4.md) — Bounded blob structure and reserved-memory descriptions.

These sources support the constraints above. The proposed object division, transition composition and verification obligations are our synthesis and remain unverified.
