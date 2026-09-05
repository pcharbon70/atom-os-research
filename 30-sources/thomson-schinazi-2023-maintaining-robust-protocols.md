---
title: "Maintaining Robust Protocols"
kind: source
created: "2026-09-05"
authors:
  - "Martin Thomson"
  - "David Schinazi"
published: "2023-06"
citation_key: "thomson-schinazi-2023-maintaining-robust-protocols"
container: "RFC 9413"
edition: null
isbn: null
doi: "10.17487/RFC9413"
url: "https://www.rfc-editor.org/rfc/rfc9413.html"
accessed: "2026-09-05"
tags:
  - interoperability
  - protocol-design
  - protocol-evolution
aliases:
  - "RFC 9413"
---

# Maintaining Robust Protocols

## Reference

Martin Thomson and David Schinazi. “[Maintaining Robust
Protocols](https://www.rfc-editor.org/rfc/rfc9413.html).” RFC 9413, June 2023.

## Research question or contribution

The RFC re-examines the robustness principle and explains how permissive
acceptance can create ambiguity, ossification, divergent implementations, and
security problems in evolving protocols.

## Method

This is an Internet Architecture Board design analysis grounded in protocol
experience. It gives guidance and examples rather than a formal theorem or
benchmark.

## Findings

- Silently accepting malformed or underspecified input can make incompatible
  interpretations permanent.
- Validation, explicit extension points, greasing, and clear failure behavior
  can preserve evolvability better than indiscriminate tolerance.
- Protocol implementations must consider the ecosystem effects of both strict
  and permissive behavior.

## Relevance

Layer 5 contracts should reject unknown critical variants, preserve optional
extension data deliberately, make negotiation explicit, and avoid “best
effort” reinterpretation of commands or durable events.

## Limits

The RFC does not specify an application message format, state migration,
capability model, or semantic conformance suite. Its recommendations require
profile-specific judgment.

## Derived work

- [Typed commands, queries, events, and protocol contracts](../20-notes/applications-and-domain-services-components/typed-commands-queries-events-and-protocol-contracts.md)
- [Application evolution, schema compatibility, and migration](../20-notes/applications-and-domain-services-components/application-evolution-schema-compatibility-and-migration.md)
