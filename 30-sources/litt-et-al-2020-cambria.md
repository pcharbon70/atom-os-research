---
title: "Project Cambria: Translate your data with lenses"
kind: source
created: "2026-09-09"
authors:
  - "Geoffrey Litt"
  - "Peter van Hardenberg"
  - "Orion Henry"
published: "2020-10"
citation_key: "litt-et-al-2020-cambria"
container: "Ink & Switch"
edition: null
isbn: null
doi: null
url: "https://www.inkandswitch.com/cambria/"
accessed: "2026-09-09"
tags:
  - application-architecture
  - distributed-systems
aliases: []
---

# Project Cambria: Translate your data with lenses

## Reference

Geoffrey Litt, Peter van Hardenberg, Orion Henry. “[Project Cambria: Translate your data with lenses](https://www.inkandswitch.com/cambria/).”
Ink & Switch, 2020-10.

This note assesses the October 2020 account, not the maintenance status or guarantees of a current library release.

## Research question or contribution

Can explicit schema transformations support collaboration across software versions?

## Method

Read the first-party prototype account, transformation examples and findings, especially read-time translation and semantic limitations.

## Findings

Cambria composes schema lenses and demonstrates an issue tracker. The account favors retaining writer-schema operations and translating on read. Missing external facts and semantic reassignment require application logic.

## Relevance

Atom OS inference: qualify transformations by meaning, authority and bounded execution, not just round-trip shape. Preserve original operation provenance and explicit loss. Treat branched versions and conflicting transformation paths as separate verification obligations.

## Limits

The authors explicitly describe research work, not a production-complete solution, and report no formal performance measurement. A reversible-looking field mapping does not preserve every domain action.

## Derived work

- [Context translation and anti-corruption boundaries](../20-notes/applications-and-domain-services-components/bounded-contexts-domain-model-and-application-services/context-translation-and-anti-corruption-boundaries.md).
- [Schema lenses and concurrent semantic translation](../20-notes/applications-and-domain-services-components/offline-collaboration-replication-and-conflict-semantics/schema-lenses-and-concurrent-semantic-translation.md).
- [Application internal-services research session](../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md).
