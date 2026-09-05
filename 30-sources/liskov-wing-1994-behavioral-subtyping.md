---
title: "A Behavioral Notion of Subtyping"
kind: source
created: "2026-09-05"
authors:
  - "Barbara H. Liskov"
  - "Jeannette M. Wing"
published: 1994
citation_key: "liskov-wing-1994-behavioral-subtyping"
container: "ACM Transactions on Programming Languages and Systems 16(6)"
edition: null
isbn: null
doi: "10.1145/197320.197383"
url: "https://doi.org/10.1145/197320.197383"
accessed: "2026-09-05"
tags:
  - behavioral-compatibility
  - protocol-evolution
  - type-systems
aliases:
  - "Behavioral subtyping"
---

# A Behavioral Notion of Subtyping

## Reference

Barbara H. Liskov and Jeannette M. Wing. “[A Behavioral Notion of
Subtyping](https://doi.org/10.1145/197320.197383).” *ACM Transactions on
Programming Languages and Systems* 16, no. 6, 1994, pages 1811–1841.

## Research question or contribution

The paper formalizes when an object of one type can safely substitute for
another using behavioral constraints, including invariants, preconditions,
postconditions, and history properties.

## Method

The authors define a constraint-based model and proof rules for behavioral
subtyping. It addresses typed object abstractions rather than asynchronous
wire protocols directly.

## Findings

- Structural shape alone is insufficient for safe substitution.
- A purported subtype cannot demand stronger preconditions or provide weaker
  guarantees while remaining substitutable.
- Mutable objects require history constraints, not merely per-call signatures.

## Relevance

Application protocol and schema evolution must preserve behavioral contracts
as well as decoding. Atom OS compatibility tests should cover invariants,
outcomes, ordering, authorization expectations, and mixed-version histories.

## Limits

The model does not directly cover message duplication, partial failure,
timeouts, capability revocation, or rolling actor upgrades. The reports use it
as a compatibility principle, not as a complete distributed proof.

## Derived work

- [Typed commands, queries, events, and protocol contracts](../20-notes/applications-and-domain-services-components/typed-commands-queries-events-and-protocol-contracts.md)
- [Application evolution, schema compatibility, and migration](../20-notes/applications-and-domain-services-components/application-evolution-schema-compatibility-and-migration.md)
