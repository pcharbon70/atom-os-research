---
title: "Typestate: A Programming Language Concept for Enhancing Software Reliability"
kind: source
created: "2026-09-05"
authors:
  - "Robert E. Strom"
  - "Shaula Yemini"
published: 1986
citation_key: "strom-yemini-1986-typestate"
container: "IEEE Transactions on Software Engineering SE-12(1)"
edition: null
isbn: null
doi: "10.1109/TSE.1986.6312929"
url: "https://doi.org/10.1109/TSE.1986.6312929"
accessed: "2026-09-05"
tags:
  - protocol-design
  - software-reliability
  - type-systems
aliases:
  - "Typestate"
---

# Typestate: A Programming Language Concept for Enhancing Software Reliability

## Reference

Robert E. Strom and Shaula Yemini. “[Typestate: A Programming Language Concept
for Enhancing Software Reliability](https://doi.org/10.1109/TSE.1986.6312929).”
*IEEE Transactions on Software Engineering* SE-12, no. 1, 1986.

## Research question or contribution

The paper associates operations with abstract object states so that a compiler
can reject sequences that would use a value in an invalid state.

## Method

The authors define typestate and a static data-flow analysis, then illustrate
how the approach detects protocol misuse. The evidence is language-design and
analysis work, not a distributed actor evaluation.

## Findings

- Whether an operation is valid can depend on an object's abstract state, not
  only on its nominal type.
- State changes can be reflected in checked interfaces, making some lifecycle
  errors unrepresentable.
- Aliasing and control flow constrain what can be proved statically.

## Relevance

Atom OS command handles, workflow steps, effect tickets, migration phases, and
application lifecycle interfaces can expose state-constrained facets. Runtime
validation remains necessary across asynchronous messages and untyped or
mixed-version boundaries.

## Limits

Typestate does not establish authorization, durability, exactly-once effects,
fair scheduling, or distributed progress. Static state cannot prove that a
remote actor is still in the advertised incarnation.

## Derived work

- [Typed commands, queries, events, and protocol contracts](../20-notes/applications-and-domain-services-components/typed-commands-queries-events-and-protocol-contracts.md)
- [Application evolution, schema compatibility, and migration](../20-notes/applications-and-domain-services-components/application-evolution-schema-compatibility-and-migration.md)
