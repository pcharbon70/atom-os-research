---
title: "Hexagonal Architecture"
kind: source
created: "2026-09-05"
authors:
  - "Alistair Cockburn"
published: "2005-09-04"
citation_key: "cockburn-2005-hexagonal-architecture"
container: "HaT Technical Report 2005.02"
edition: null
isbn: null
doi: null
url: "https://alistair.cockburn.us/hexagonal-architecture"
accessed: "2026-09-05"
tags:
  - application-architecture
  - ports-and-adapters
  - practitioner-literature
aliases:
  - "Ports and adapters"
---

# Hexagonal Architecture

## Reference

Alistair Cockburn. “[Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture).”
HaT Technical Report 2005.02, 4 September 2005.

## Research question or contribution

Cockburn proposes organizing an application around semantic ports, with
technology-specific adapters outside, so the application can be driven by
users, tests, batch jobs, or other programs and can run without one particular
UI or database.

## Method

This is a practitioner architecture pattern supported by examples and design
experience rather than a peer-reviewed experiment.

## Findings

- The important asymmetry is inside application meaning versus outside
  technologies, not a fixed “top” and “bottom.”
- Ports express application conversations; adapters translate a particular UI,
  store, network, or test harness into them.
- Replaceable adapters improve testability and contain technology churn.

## Relevance

Layer 5 should own typed domain ports and context translators while Layer 4
provides generic storage, network, device, and identity mechanisms. Atom OS
extends each port contract with authority, deadline, backpressure, generation,
idempotency, and outcome semantics.

## Limits

The pattern does not solve partial failure, authorization, exactly-once
effects, migration, resource exhaustion, or adapter compromise.

## Derived work

- [External effects, ports, adapters, and reconciliation](../20-notes/applications-and-domain-services-components/external-effects-ports-adapters-and-reconciliation.md)
- [Presentation sessions, semantic views, and user outcomes](../20-notes/applications-and-domain-services-components/presentation-sessions-semantic-views-and-user-outcomes.md)
