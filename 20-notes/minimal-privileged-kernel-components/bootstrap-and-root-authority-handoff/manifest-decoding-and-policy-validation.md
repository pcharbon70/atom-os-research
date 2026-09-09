---
title: "Manifest decoding and policy validation"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Manifest decoding and policy validation

What must be established before a boot description may influence privileged object creation?

## Research basis and status

capDL describes authority configurations; description validity and intended security policy are different questions. [1](../../../30-sources/kuz-et-al-2010-capdl.md), [2](../../../30-sources/sel4-foundation-2026-capdl-loader-contract.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../bootstrap-and-root-authority-handoff.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

A bounded decoder owns the normalized BootAuthorityManifest and its validation result. Firmware parsing remains below this boundary; package selection and signature policy remain above it. The input includes a trusted provenance decision, schema version, canonical lengths, object indices, permitted rights, and immutable device-profile references. A digest detects a mismatch with an authorized description; it cannot establish who authorized an arbitrary replacement.

### Admission, transitions and completion

Decode into reserved scratch storage without following input pointers. Check arithmetic before extent calculation, reject duplicate identifiers and overlapping backing, and validate every reference before graph traversal. Then check rights attenuation, maximum anchor depth, exclusive domain roots, and recovery dependencies. Cycles must be judged by relationship type: a prohibited recovery dependency is not equivalent to a permissible shared-object relationship. Publish one immutable validated representation that the constructor consumes without reparsing mutable input.

### Failure and adversarial behavior

A structurally valid graph can still grant a child the power to disable its supervisor. Treat that as a policy-check failure, not a parser success that permits boot. Unknown schema fields affecting authority must fail closed. A rejected manifest must not leave a partly usable root capability.

### Alternatives and unresolved tradeoffs

A rich policy language offers flexibility but enlarges trusted parsing and evaluation. Prefer an externally compiled, length-delimited construction format with explicit semantic checks. The open question is which security properties can be checked locally and which require a separate policy model.

## Verification obligations

Mutate every length, index and range boundary; introduce recovery cycles, duplicate roots and hidden reset authority. Check that rejection leaves no published capability or account debit. Compare the normalized graph with a separately generated expected graph, including deliberately valid-but-overprivileged manifests.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Product authority and durable detachment](../capability-spaces-and-authority/product-authority-and-durable-detachment.md) — Construction must preserve effect-bearing authority.
- [Recovery escrow and reserve admission](../failure-boundaries-and-recovery-topology/recovery-escrow-and-reserve-admission.md) — Bootstrap must provision an independently usable recovery path.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [capDL: A language for describing capability-based systems](../../../30-sources/kuz-et-al-2010-capdl.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [capDL Loader](../../../30-sources/sel4-foundation-2026-capdl-loader-contract.md) — comparative evidence; its methods and limits are recorded in the source note.
