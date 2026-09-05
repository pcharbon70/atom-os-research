---
title: "On the Criteria To Be Used in Decomposing Systems into Modules"
kind: source
created: "2026-09-05"
authors:
  - "David L. Parnas"
published: 1972
citation_key: "parnas-1972-decomposing-systems-into-modules"
container: "Communications of the ACM 15(12)"
edition: null
isbn: null
doi: "10.1145/361598.361623"
url: "https://doi.org/10.1145/361598.361623"
accessed: "2026-09-05"
tags:
  - information-hiding
  - modularity
  - software-architecture
aliases:
  - "Parnas module decomposition"
---

# On the Criteria To Be Used in Decomposing Systems into Modules

## Reference

David L. Parnas. “[On the Criteria To Be Used in Decomposing Systems into
Modules](https://doi.org/10.1145/361598.361623).” *Communications of the ACM*
15, no. 12, 1972.

## Research question or contribution

Parnas compares decomposition by processing step with decomposition around
hidden design decisions and argues that modules should conceal choices likely
to change.

## Method

The paper develops two decompositions of the same system and analyzes the
resulting interfaces, change propagation, independent development, and
comprehensibility. It is an analytical case comparison rather than a modern
controlled evaluation.

## Findings

- A flowchart or execution phase is not automatically a useful module
  boundary.
- Interfaces should reveal what a client needs while hiding representations,
  algorithms, device choices, and other volatile decisions.
- Information hiding limits the parts of a system that must understand or
  change with one decision.

## Relevance

Layer 5 ports, bounded contexts, projections, persistence policies, and
adapters should hide volatile choices without hiding failure or authority
semantics that clients must handle. The paper supports modularity but does not
decide actor, supervision, tenant, or protection-domain granularity.

## Limits

The example predates modern actor runtimes, distributed failure models,
capabilities, and online evolution. Information hiding cannot justify an
interface that conceals `Indeterminate`, overload, version, or revocation
states essential to correct clients.

## Derived work

- [Applications and domain services layer](../20-notes/applications-and-domain-services-layer.md)
- [Application manifest, composition, and authority envelope](../20-notes/applications-and-domain-services-components/application-manifest-composition-and-authority-envelope.md)
- [External effects, ports, adapters, and reconciliation](../20-notes/applications-and-domain-services-components/external-effects-ports-adapters-and-reconciliation.md)
