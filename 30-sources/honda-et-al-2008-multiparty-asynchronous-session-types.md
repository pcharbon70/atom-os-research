---
title: "Multiparty Asynchronous Session Types"
kind: source
created: "2026-09-05"
authors:
  - "Kohei Honda"
  - "Nobuko Yoshida"
  - "Marco Carbone"
published: 2008
citation_key: "honda-et-al-2008-multiparty-asynchronous-session-types"
container: "Proceedings of POPL 2008"
edition: null
isbn: null
doi: "10.1145/1328438.1328472"
url: "https://doi.org/10.1145/1328438.1328472"
accessed: "2026-09-05"
tags:
  - actor-protocols
  - formal-methods
  - session-types
aliases:
  - "Multiparty session types"
---

# Multiparty Asynchronous Session Types

## Reference

Kohei Honda, Nobuko Yoshida, and Marco Carbone. “[Multiparty Asynchronous
Session Types](https://doi.org/10.1145/1328438.1328472).” *Proceedings of the
35th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages*,
2008.

## Research question or contribution

The paper describes a global multiparty conversation, projects compatible
endpoint types, and proves communication-safety and progress properties under
its asynchronous formal model.

## Method

It defines global and local type systems, projection and operational
semantics, proves metatheoretic results, and applies the approach to protocol
examples.

## Findings

- A global protocol can expose sequencing and branching obligations spanning
  several participants.
- Well-formed projection can give each endpoint a locally checkable view.
- The proved properties depend on exact typing, projection, channel, and
  progress assumptions.

## Relevance

Session types are promising optional assurance for high-consequence workflows
and mixed-version actor protocols. They should supplement, not replace,
capability checks, durable outcomes, overload policy, schema validation, and
recovery state.

## Limits

The formal result is not a security, persistence, or fault-tolerance theorem.
Real systems must handle actor crashes, upgrades, deadlines, mailbox limits,
authorization, and messages from untyped peers.

## Derived work

- [Typed commands, queries, events, and protocol contracts](../20-notes/applications-and-domain-services-components/typed-commands-queries-events-and-protocol-contracts.md)
- [Semantic observability, testing, and assurance](../20-notes/applications-and-domain-services-components/semantic-observability-testing-and-assurance.md)
