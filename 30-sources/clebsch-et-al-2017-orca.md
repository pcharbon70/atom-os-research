---
title: "Orca: GC and Type System Co-Design for Actor Languages"
kind: source
created: "2026-09-02"
authors:
  - "Sylvan Clebsch"
  - "Juliana Franco"
  - "Sophia Drossopoulou"
  - "Albert Mingkun Yang"
  - "Tobias Wrigstad"
  - "Jan Vitek"
published: "2017-10"
citation_key: "clebsch-et-al-2017-orca"
container: "Proceedings of the ACM on Programming Languages 1(OOPSLA)"
edition: "Article 72, 1-28"
isbn: null
doi: "10.1145/3133896"
url: "https://2017.splashcon.org/details/splash-2017-OOPSLA/30/Orca-GC-and-Type-System-Co-Design-for-Actor-Languages"
accessed: "2026-09-02"
tags:
  - actor-model
  - capabilities
  - garbage-collection
  - memory-management
  - pony
aliases:
  - "Orca garbage collector"
---

# Orca: GC and Type System Co-Design for Actor Languages

## Reference

Sylvan Clebsch, Juliana Franco, Sophia Drossopoulou, Albert Mingkun Yang,
Tobias Wrigstad, and Jan Vitek. “[Orca: GC and Type System Co-Design for Actor
Languages](https://doi.org/10.1145/3133896).” *Proceedings of the ACM on
Programming Languages* 1, OOPSLA, Article 72, pages 1–28, October 2017. DOI
10.1145/3133896. The [official conference
record](https://2017.splashcon.org/details/splash-2017-OOPSLA/30/Orca-GC-and-Type-System-Co-Design-for-Actor-Languages)
and paper were consulted.

## Research question or contribution

Orca asks what an actor garbage collector can do when the language type system
proves race freedom and constrains which references can cross actor boundaries.
It co-designs Pony’s reference capabilities and runtime to support local and
shared objects without a global stop-the-world phase.

## Method

The paper describes allocation and collection protocols using pseudo-code,
derives safety from Pony’s capability rules, and evaluates an implementation
with microbenchmarks and comparisons to other collectors.

## Findings

- Orca performs concurrent and parallel actor collection without a global
  stop-the-world step and uses actor messages for parts of its coordination.
- The reference-capability type system distinguishes objects that cannot be
  sent, immutable shared objects, and uniquely transferable mutable objects.
  Those guarantees permit zero-copy transfer and sharing without ordinary
  read or write barriers.
- Collection design and language semantics are inseparable here: the runtime
  optimization is justified by properties statically enforced by Pony.
- The reported microbenchmarks show that this co-design can be practical and
  scalable under the tested workloads, but do not establish BEAM compatibility
  or end-to-end service latency.

## Relevance

Orca is a valuable alternative to indiscriminate message copying. It shows a
possible future extension profile in which verified immutable or unique terms
cross actors cheaply. It also supplies a warning: Atom OS cannot import Orca’s
zero-copy conclusions for arbitrary compiled BEAM terms, because ordinary BEAM
code does not carry Pony’s reference-capability proofs. The compatible
baseline should retain process-local tracing collection and copy or explicitly
account shared immutable payloads; richer transfer rules require a separately
verified language/profile contract.

## Limits

The evidence is tied to Pony’s type system and implementation. Performance was
evaluated primarily with author-created synthetic microbenchmarks because a
commercial Pony workload corpus was unavailable. Those tests do not
characterize selective receive, hot code replacement, native extensions,
distributed actors, or runtime-domain failure. The absence of a global
stop-the-world collector does not remove global allocator, metadata, code, or
operating-system failure domains.

## Derived work

- [Managed actor runtime layer](../20-notes/managed-actor-runtime-layer.md)
- [Terms, private heaps, shared binaries, and tracing collection](../20-notes/managed-actor-runtime-components/terms-private-heaps-shared-binaries-and-tracing-collection.md)
- [Managed actor runtime map](../10-maps/managed-actor-runtime.md)
- [Managed-runtime contract inquiry](../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md)
- [2026-09-02 research journal](../50-journal/2026-09-02-managed-actor-runtime-deep-dive.md)
- [2026-09-03 component research journal](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md)
