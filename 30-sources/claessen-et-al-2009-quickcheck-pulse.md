---
title: "Finding Race Conditions in Erlang with QuickCheck and PULSE"
kind: source
created: "2026-09-02"
authors:
  - "Koen Claessen"
  - "Michał Pałka"
  - "Nicholas Smallbone"
  - "John Hughes"
  - "Hans Svensson"
  - "Thomas Arts"
  - "Ulf T. Wiger"
published: "2009-08-31"
citation_key: "claessen-et-al-2009-pulse"
container: "Proceedings of the 14th ACM SIGPLAN International Conference on Functional Programming"
edition: "ICFP '09, 149-160"
isbn: "978-1-60558-332-7"
doi: "10.1145/1596550.1596574"
url: "https://happy-testing.com/hans/papers/ICFP2009-PULSE.pdf"
accessed: "2026-09-02"
tags:
  - concurrency-testing
  - erlang
  - fault-injection
  - property-based-testing
  - scheduling
aliases:
  - "QuickCheck and PULSE"
---

# Finding Race Conditions in Erlang with QuickCheck and PULSE

## Reference

Koen Claessen, Michal H. Palka, Nicholas Smallbone, John Hughes, Hans
Svensson, Thomas Arts, and Ulf T. Wiger. “[Finding Race Conditions in Erlang
with QuickCheck and PULSE](https://doi.org/10.1145/1596550.1596574).”
*Proceedings of the 14th ACM SIGPLAN International Conference on Functional
Programming*, pages 149–160, 2009. DOI 10.1145/1596550.1596574.
[Author-hosted paper](https://happy-testing.com/hans/papers/ICFP2009-PULSE.pdf).

## Research question or contribution

The paper combines property-based command generation, a controllable
user-level scheduler, and trace visualization to make rare Erlang concurrency
failures reproducible in unit-scale tests.

## Method

PULSE intercepts concurrency operations and controls their ordering while
QuickCheck generates operations and shrinks failing cases. The authors apply
the method to an industrial concurrent Erlang case study and use the
visualizer to diagnose the resulting schedules.

## Findings

- Repeating ordinary tests under the host scheduler explores little of the
  relevant ordering space and makes timing-dependent failures hard to replay.
- A controlled scheduler can vary process and communication order while
  retaining a concrete schedule as diagnostic evidence.
- Property-based shrinking reduces a failing concurrent history to a smaller
  counterexample that can expose the protocol error more clearly than a large
  production trace.
- In the reported industrial case, the combined method found and helped
  explain two race conditions and an API weakness. That is case evidence, not
  a completeness guarantee.

## Relevance

The Atom OS runtime should expose a deterministic test mode below OTP policy:
seeded actor scheduling, controllable timers, message and failure injection,
and replayable event identities. This is not the production scheduler. It is a
verification interface for per-sender ordering, monitor/link races, aliases,
timeouts, cancellation, code replacement, and runtime-domain recovery.

## Limits

PULSE does not enumerate every interleaving or prove distributed protocol
correctness. Controlling a user-level scheduler cannot by itself control kernel
interrupts, DMA, native memory races, network behavior, or power loss. The
case study predates current signal, scheduler, and priority-message behavior,
so new compatibility properties and fault models are required.

## Derived work

- [Managed actor runtime layer](../20-notes/managed-actor-runtime-layer.md)
- [Observability, deterministic testing, and crash evidence](../20-notes/managed-actor-runtime-components/observability-deterministic-testing-and-crash-evidence.md)
- [Managed actor runtime map](../10-maps/managed-actor-runtime.md)
- [Managed-runtime contract inquiry](../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md)
- [2026-09-02 research journal](../50-journal/2026-09-02-managed-actor-runtime-deep-dive.md)
- [2026-09-03 component research journal](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md)
