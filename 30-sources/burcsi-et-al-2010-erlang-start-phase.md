---
title: "Start-phase control of distributed systems written in Erlang/OTP"
kind: source
created: "2026-09-04"
authors:
  - "Péter Burcsi"
  - "Attila Kovács"
  - "Antal Tátrai"
published: 2010
citation_key: "burcsi-et-al-2010-erlang-start-phase"
container: "Acta Universitatis Sapientiae, Informatica"
edition: "Volume 2, issue 1, pages 10–27"
isbn: null
doi: null
url: "https://arxiv.org/abs/1003.1395"
accessed: "2026-09-04"
tags:
  - dependency-graphs
  - erlang
  - lifecycle
  - otp
  - startup
aliases:
  - "Erlang start-phase control"
---

# Start-phase control of distributed systems written in Erlang/OTP

## Reference

Péter Burcsi, Attila Kovács, and Antal Tátrai. “[Start-Phase Control of
Distributed Systems Written in Erlang/OTP](https://arxiv.org/abs/1003.1395).”
*Acta Universitatis Sapientiae, Informatica* 2, no. 1, pages 10–27, 2010.

## Research question or contribution

The paper asks how an Erlang/OTP system can start independent components in
parallel without replacing safe dependency ordering with ad hoc concurrency.
It adds an explicit dynamic condition/dependency graph and wrapper supervision
logic to coordinate initialization acknowledgements.

## Method

The authors implement a prototype against the historical OTP R11B/Erlang 5.5
environment and measure synthetic CPU-heavy initialization on a four-core
machine. Reported results use small run counts and compare sequential startup
with different parallelism limits. The paper demonstrates feasibility and a
performance opportunity, not contemporary OTP compatibility.

## Findings

- Traditional acknowledgement-driven startup serializes work even when some
  components have no dependency relationship. An explicit graph makes safe
  concurrency a planning decision rather than hidden application convention.
- Initialization conditions can distinguish creation from the point at which a
  dependent may proceed. Supervisory linkage must remain established while
  work is parallelized.
- Bounded parallelism performed better than both full serialization and
  unconstrained starts in the synthetic tests; some measured cases approached
  twofold speedup on four cores.
- A wrong or cyclic dependency graph can deadlock or fail startup. Validation
  and diagnostics are therefore safety and operability requirements, not mere
  optimization.
- The prototype's wrappers and library modifications are one implementation,
  not part of the abstract requirement for typed dependencies and readiness.

## Relevance

Atom OS application orchestration should compile its manifest into a validated
DAG, start dependency-ready nodes concurrently within CPU, memory, I/O, and
recovery budgets, and require an explicit readiness result before publishing a
service generation. Each task is tagged with the plan and service incarnation
so a late completion from an abandoned start cannot activate stale state.

The design should go beyond the paper by distinguishing `requires`,
`start-after`, `ready-after`, and `health-coupled` edges. Parallelism is capped
by the admission governor rather than only by core count. Strict OTP adapters
preserve OTP's externally visible application behavior while native bundles
use the richer lifecycle.

## Limits

The experimental platform and OTP release are historical, workload is
synthetic, dependency conditions were not exercised in the performance tests,
and results are based on few runs. The paper does not address capability
delegation, crash consistency, service draining, rollback of external effects,
mixed-version activation, or distributed ownership fencing. Its quantitative
speedups must not be projected onto Atom OS without new measurements.

## Derived work

- [Application lifecycle and dependency orchestration](../20-notes/otp-like-system-services-components/application-lifecycle-and-dependency-orchestration.md)
- [Service-domain bootstrap and manifest controller](../20-notes/otp-like-system-services-components/service-domain-bootstrap-and-manifest-controller.md)
