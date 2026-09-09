---
title: "Term representation and copy boundary"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - actor-model
  - beam
  - managed-runtime
  - system-architecture
aliases: []
---

# Term representation and copy boundary

This study decomposes [Terms, private heaps, shared binaries and tracing collection](../terms-private-heaps-shared-binaries-and-tracing-collection.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Heap-architecture research separates copying semantics from physical copying; Orca's transfer guarantees rely on stronger type facts than unrestricted BEAM provides. [1](../../../30-sources/sagonas-wilhelmsson-2006-efficient-memory-management.md), [2](../../../30-sources/clebsch-et-al-2017-orca.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Automatic tracing collection and term interpretation remain unprivileged runtime responsibilities; kernel pages do not encode BEAM object ownership.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own tag/layout descriptors, checked object sizes and a total classification of private, immediate and explicitly shared values. Observable equality, term ordering, arithmetic and exceptions must survive representation changes. A term word is never interpreted as an ambient native pointer or capability.

### Admission, transitions and completion

Validate each object class before traversal, then copy ordinary compound terms into private destination storage while retaining permitted immutable shared objects through explicit handles. Preserve graph sharing where allowed without exposing mutation. Binaries, literals and native resource wrappers follow their own lifetime protocols rather than a universal shallow copy.

### Failure and adversarial behavior

Integer overflow in size calculation, malformed bitstring offsets and a forged tag can turn a language error into domain corruption. Loader and external decoder validation are necessary but not sufficient: runtime constructors and native interfaces also enter this trust boundary.

### Alternatives and unresolved tradeoffs

Compact tags save memory but couple the collector and code generator tightly. Wider descriptors simplify validation at a cost per object. Zero-copy mutable transfer is a separate verified profile, not an optimization inferred from actors being isolated.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Differentially test term equality, ordering and bitstring edge cases across representations.
- Copy nested shared subgraphs and verify sender collection cannot damage the receiver.
- Reject forged tags and out-of-range sizes before following pointers.

Record the exact profile, tested revision, schedule/input bounds and resource
observations before claiming this contract holds. A semantic pass does not
establish latency or corruption containment.

## Connections

- [Component service index](README.md) — sibling responsibilities and shared boundaries.
- [Root materialization](../code-execution-safe-points-and-version-publication/canonical-safe-point-and-native-helper-state.md) — a contract this service must compose with.
- [Physical and retained accounting](../resource-accounting-and-overload-control/hierarchical-reservations-and-ledger-reconciliation.md) — a contract this service must compose with.
- [Open runtime inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — unresolved design and evidence.
- [Research session](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — source manifest and reading limitations.

## Sources

1. [Sagonas and Wilhelmsson: memory management](../../../30-sources/sagonas-wilhelmsson-2006-efficient-memory-management.md).
2. [Orca: collector and type-system co-design](../../../30-sources/clebsch-et-al-2017-orca.md).
