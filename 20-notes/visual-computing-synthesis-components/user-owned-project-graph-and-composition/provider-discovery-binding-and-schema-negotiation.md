---
title: "Provider discovery, binding, and schema negotiation"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - project-graph
  - software-architecture
  - visual-computing
aliases: []
---

# Provider discovery, binding, and schema negotiation

This study decomposes [User-owned project graph and composition](../user-owned-project-graph-and-composition.md).

Research question: How can replaceable providers attach to durable objects
without becoming their sole interpreter or inheriting ambient authority?

## Research basis and status

Webstrates and Potluck demonstrate multiple tools over durable shared content,
but also expose the semantic and complexity limits of a common substrate.
Hexagonal architecture supplies a practitioner precedent for semantic ports and
replaceable adapters. [1](../../../30-sources/klokmose-et-al-2015-webstrates-shareable-dynamic-media.md)
[2](../../../30-sources/litt-et-al-2022-potluck-dynamic-documents.md)
[3](../../../30-sources/cockburn-2005-hexagonal-architecture.md)

The proposed registry and negotiation protocol is not implemented.

## Development

### Owned state and trust boundary

The binding service owns provider offers, immutable package digests, supported
type/schema ranges, operations, semantic-protocol profiles, resource demands,
and binding generations. It does not own project data or accept a provider's
claim that possession of a type name grants access.

### Admission, transitions, and completion

Discovery returns policy-filtered candidates. Selection validates provenance,
compatibility, declared degradation behavior, and resource ceilings, then asks
the authority service for separate observe, act, and mutate facets. A binding
becomes current only after durable publication; replacement advances its
generation and withdraws old facets before the successor handles commands.

### Failure and adversarial behavior

Offers may lie about schemas, consume unbounded resources, squat on generic
types, or return capabilities hidden in values. Validators parse packages in
isolation, providers receive copied metadata until admission, and receivers
enforce binding generation plus project authority. Removal must leave a
system-readable semantic fallback rather than an opaque orphan.

### Alternatives and unresolved tradeoffs

One application per format reduces negotiation but restores package ownership.
A universal schema improves fallback but cannot anticipate every medium.
Namespaced schemas plus required semantic summaries retain extensibility; the
minimum fallback vocabulary and provider ranking policy remain unresolved.

## Verification obligations

- Create with provider A, remove it, inspect through the system fallback, and
  edit with independently built provider B.
- Advertise false compatibility, cyclic dependencies, excessive resources, and
  capability-bearing return values; admission must fail without data exposure.
- Replace providers during pending commands and prove binding generations route
  each result to the correct project operation.

## Connections

- [Internal-service index](README.md) — project composition responsibilities.
- [Plural representation providers](../plural-representations-and-cross-view-consistency/provider-registration-negotiation-and-representation-contracts.md) — specializes view contracts.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — provenance.

## Sources

1. [Webstrates](../../../30-sources/klokmose-et-al-2015-webstrates-shareable-dynamic-media.md).
2. [Potluck](../../../30-sources/litt-et-al-2022-potluck-dynamic-documents.md).
3. [Hexagonal architecture](../../../30-sources/cockburn-2005-hexagonal-architecture.md).
