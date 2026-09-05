---
title: "Protocol Buffers Language Guide and Schema Evolution Practices"
kind: source
created: "2026-09-05"
authors:
  - "Google Protocol Buffers Team"
published: null
citation_key: "google-2026-protocol-buffers-evolution"
container: "Protocol Buffers Documentation"
edition: null
isbn: null
doi: null
url: "https://protobuf.dev/programming-guides/proto3/"
accessed: "2026-09-05"
tags:
  - protocol-buffers
  - protocol-evolution
  - schemas
aliases:
  - "Proto3 evolution guidance"
---

# Protocol Buffers Language Guide and Schema Evolution Practices

## Reference

Google Protocol Buffers Team. “[Language Guide (proto3)](https://protobuf.dev/programming-guides/proto3/)”
and “[Proto Best Practices](https://protobuf.dev/best-practices/dos-donts/).”
Accessed 5 September 2026.

## Research question or contribution

The official documentation defines Protocol Buffers schemas, unknown-field
behavior, and concrete practices for changing long-lived wire formats.

## Method

The current language guide and best-practices pages were read for stable field
identity, removal, type changes, unknown values, and reader/writer
compatibility. This is product documentation, not a comparative experiment.

## Findings

- Field numbers are durable wire identities and must never be reused.
- Removed field numbers and names should be reserved to prevent accidental
  reinterpretation.
- Some changes are wire-safe only under conditions; unknown fields can survive
  binary round trips but may be lost by other transformations.
- Decoding compatibility says nothing about domain invariants or intended
  behavior.

## Relevance

Atom OS needs stable IDs, explicit critical/optional variants, unknown-field
policy, fixtures in both directions, and compatibility matrices for commands,
queries, events, state, snapshots, and outcomes. Protocol Buffers is an
example, not the mandated encoding.

## Limits

The guidance is format-specific and living documentation pinned only by access
date. It does not establish authorization, semantic compatibility,
idempotency, ordering, or migration correctness.

## Derived work

- [Typed commands, queries, events, and protocol contracts](../20-notes/applications-and-domain-services-components/typed-commands-queries-events-and-protocol-contracts.md)
- [Application evolution, schema compatibility, and migration](../20-notes/applications-and-domain-services-components/application-evolution-schema-compatibility-and-migration.md)
