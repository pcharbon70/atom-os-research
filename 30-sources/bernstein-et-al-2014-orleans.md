---
title: "Orleans: Distributed virtual actors for programmability and scalability"
kind: source
created: "2026-09-03"
authors:
  - "Philip A. Bernstein"
  - "Sergey Bykov"
  - "Alan Geller"
  - "Gabriel Kliot"
  - "Jorgen Thelin"
published: 2014
citation_key: "bernstein-et-al-2014-orleans"
container: "Microsoft Research Technical Report"
edition: "MSR-TR-2014-41"
isbn: null
doi: null
url: "https://www.microsoft.com/en-us/research/publication/orleans-distributed-virtual-actors-for-programmability-and-scalability/"
accessed: "2026-09-03"
tags:
  - actor-model
  - distributed-systems
  - scalability
  - virtual-actors
aliases:
  - "Orleans virtual actors"
---

# Orleans: Distributed virtual actors for programmability and scalability

## Reference

Philip A. Bernstein, Sergey Bykov, Alan Geller, Gabriel Kliot, and Jorgen
Thelin.
“[Orleans: Distributed Virtual Actors for Programmability and
Scalability](https://www.microsoft.com/en-us/research/publication/orleans-distributed-virtual-actors-for-programmability-and-scalability/).”
Microsoft Research Technical Report MSR-TR-2014-41, 2014.

## Research question or contribution

The report develops the virtual-actor abstraction for stateful cloud services:
actors have stable logical identities while the runtime activates, places,
deactivates, and recreates their in-memory incarnations on demand.

## Method

The authors describe Orleans' programming and runtime model, including the
directory, placement, activation, persistence conventions, and request
handling, then report experience and performance from several production
services on Microsoft Azure.

## Findings

- Separating logical actor identity from a particular in-memory activation can
  simplify placement, lifecycle, and failover for a targeted service model.
- Runtime-managed activation and location reduce application code but transfer
  substantial consistency, membership, and resource-management obligations to
  the platform.
- The 2014 report describes at-least-once delivery through automatic resend in
  important failure situations. [Current Orleans
  documentation](https://learn.microsoft.com/en-us/dotnet/orleans/implementation/messaging-delivery-guarantees)
  clarifies that at-most-once is now the default and at-least-once applies when
  retries are configured. Neither mode makes side effects exactly once.
- Production evidence shows the design can support high-scale services, but
  its semantics intentionally differ from explicit Erlang process lifetime,
  PID incarnation, links, and monitors.

## Relevance

Orleans is useful comparative evidence for Atom OS distribution gateways and
service naming. Stable logical service names can live above the runtime, while
runtime PIDs remain incarnation-specific. Gateways should make reconnect,
duplicate, refusal, and ambiguous completion visible and should not silently
turn an expired PID into a new actor activation. Optional virtual-actor
services can be built as an OTP-like policy layer without changing the base
BEAM contract.

## Limits

This is a system report and production account rather than a formal
exactly-once or failure-detector result. It targets Azure middle-tier
applications, not BEAM compatibility, capability security, or embedded/bare-
metal systems. Delivery defaults have also changed since the 2014 report, so
its historical semantics must not be presented as the current Orleans default.
Reported performance cannot be transferred to Atom OS.

## Derived work

- [Distribution gateway and remote actor semantics](../20-notes/managed-actor-runtime-components/distribution-gateway-and-remote-actor-semantics.md)
- [Actor identity, lifecycle, and process state](../20-notes/managed-actor-runtime-components/actor-identity-lifecycle-and-process-state.md)
- [Managed actor runtime layer](../20-notes/managed-actor-runtime-layer.md)
- [2026-09-03 component research journal](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md)
