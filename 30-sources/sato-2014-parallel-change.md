---
title: "Parallel Change"
kind: source
created: "2026-09-09"
authors:
  - "Danilo Sato"
published: "2014-05-13"
citation_key: "sato-2014-parallel-change"
container: "martinfowler.com"
edition: null
isbn: null
doi: null
url: "https://martinfowler.com/bliki/ParallelChange.html"
accessed: "2026-09-09"
tags:
  - application-architecture
  - distributed-systems
aliases: []
---

# Parallel Change

## Reference

Danilo Sato. “[Parallel Change](https://martinfowler.com/bliki/ParallelChange.html).”
martinfowler.com, 2014-05-13.

The named author is Danilo Sato, not the site's owner Martin Fowler.

## Research question or contribution

How can an incompatible interface change be introduced incrementally?

## Method

Read the complete post, including the worked refactoring, deployment examples and cautions. This is a practitioner pattern, not an evaluated distributed protocol.

## Findings

The pattern adds a new interface, migrates consumers, then removes the old one. Coexistence costs and forgotten contraction are explicit drawbacks.

## Relevance

Atom OS inference: pair staged interface evolution with writer fencing, mixed-generation histories and irreversible-effect cutoffs. Compare its compatibility advice with [RFC 9413](thomson-schinazi-2023-maintaining-robust-protocols.md); silently accepting security-relevant unknown meaning is not our chosen profile.

## Limits

The example does not prove concurrent shared-data migration safe. Its permissive-parsing suggestion must not override critical-field validation.

## Derived work

- [Expand-contract transitions and old-writer exclusion](../20-notes/applications-and-domain-services-components/application-evolution-schema-compatibility-and-migration/expand-contract-transitions-and-old-writer-exclusion.md).
- [Rollback cutoffs, canaries, and retirement evidence](../20-notes/applications-and-domain-services-components/application-evolution-schema-compatibility-and-migration/rollback-cutoffs-canaries-and-retirement-evidence.md).
- [Application internal-services research session](../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md).
