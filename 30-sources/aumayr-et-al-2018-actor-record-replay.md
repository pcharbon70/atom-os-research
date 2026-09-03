---
title: "Efficient and deterministic record and replay for actor languages"
kind: source
created: "2026-09-03"
authors:
  - "Dominik Aumayr"
  - "Stefan Marr"
  - "Clément Béra"
  - "Elisa Gonzalez Boix"
  - "Hanspeter Mössenböck"
published: 2018
citation_key: "aumayr-et-al-2018-actor-record-replay"
container: "15th International Conference on Managed Languages and Runtimes"
edition: "ManLang '18"
isbn: null
doi: "10.1145/3237009.3237015"
url: "https://arxiv.org/abs/1805.06267"
accessed: "2026-09-03"
tags:
  - actor-model
  - debugging
  - observability
  - record-replay
aliases:
  - "Actor record and replay"
---

# Efficient and deterministic record and replay for actor languages

## Reference

Dominik Aumayr, Stefan Marr, Clément Béra, Elisa Gonzalez Boix, and Hanspeter
Mössenböck. “[Efficient and Deterministic Record & Replay for Actor
Languages](https://doi.org/10.1145/3237009.3237015).” *15th International
Conference on Managed Languages and Runtimes*, 2018. [Open
preprint](https://arxiv.org/abs/1805.06267).

## Research question or contribution

The paper asks which high-level nondeterministic events an actor runtime must
record to replay a prior execution deterministically without logging every
low-level thread interaction.

## Method

The authors implement record/replay in an actor-language runtime, log actor
message-order decisions and external inputs, and evaluate trace size and
runtime cost on Savina actor benchmarks and the Acme-Air Web application.

## Findings

- Recording language-level nondeterminism can be substantially smaller and
  more useful than recording underlying lock and thread events.
- The reported Savina average runtime overhead was about 10%, with a 0–20%
  range; Acme-Air showed at most about 1% request-latency increase and roughly
  1.4 MB/s of trace data in the evaluated setup.
- Determinism requires logging external data and the relative ordering choices
  that affect actor behavior, not merely a random seed.
- The paper describes a first step toward production replay. Native code,
  system calls, time, distributed peers, code replacement, and trace loss can
  widen the nondeterminism boundary.

## Relevance

Atom OS should distinguish cheap deterministic test scheduling from optional
production record/replay. The latter needs a versioned replay manifest,
message-selection and timer decisions, external completion values, time and
randomness observations, service incarnations, code generations, and an
explicit completeness/loss marker. Trace bytes and recorder CPU must be
charged so observation cannot defeat containment.

## Limits

The implementation and workloads are not BEAM/ERTS or a capability kernel.
The reported overhead is not a prediction for selective receive, process-local
GC, distributed gateways, or crash-safe trace persistence. Replay reproduces
recorded nondeterminism; it does not prove that a run was correct or reproduce
unlogged hardware corruption.

## Derived work

- [Observability, deterministic testing, and crash evidence](../20-notes/managed-actor-runtime-components/observability-deterministic-testing-and-crash-evidence.md)
- [Managed actor runtime layer](../20-notes/managed-actor-runtime-layer.md)
- [2026-09-03 component research journal](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md)
