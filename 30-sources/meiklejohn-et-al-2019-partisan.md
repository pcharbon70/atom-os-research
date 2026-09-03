---
title: "PARTISAN: Scaling the distributed actor runtime"
kind: source
created: "2026-09-03"
authors:
  - "Christopher S. Meiklejohn"
  - "Heather Miller"
  - "Peter Alvaro"
published: 2019
citation_key: "meiklejohn-et-al-2019-partisan"
container: "2019 USENIX Annual Technical Conference"
edition: "USENIX ATC '19, 63-76"
isbn: null
doi: null
url: "https://www.usenix.org/conference/atc19/presentation/meiklejohn"
accessed: "2026-09-03"
tags:
  - actor-model
  - distributed-systems
  - erlang
  - networking
aliases:
  - "PARTISAN"
---

# PARTISAN: Scaling the distributed actor runtime

## Reference

Christopher S. Meiklejohn, Heather Miller, and Peter Alvaro. “[PARTISAN:
Scaling the Distributed Actor
Runtime](https://www.usenix.org/conference/atc19/presentation/meiklejohn).”
*2019 USENIX Annual Technical Conference*, pages 63–76, 2019.

## Research question or contribution

PARTISAN asks whether Erlang applications should be able to select connection
topology, parallel channels, and channel affinity instead of accepting one
full-mesh distribution design for every workload.

## Method

The authors implement a replacement distribution layer with configurable
topologies and channels and evaluate it on distributed applications and
benchmarks, comparing throughput and scaling with conventional Erlang
distribution.

## Findings

- Full mesh is not universally appropriate; application-selected overlays can
  reduce connection and coordination costs.
- Multiple parallel channels and traffic affinity can remove head-of-line and
  single-channel bottlenecks for selected workloads.
- The reported improvements are strongly workload- and configuration-specific.
  The application or deployment must understand its communication pattern.

## Relevance

PARTISAN supports making Atom OS gateway topology and channel allocation
replaceable policies while keeping actor signal compatibility above them.
Explicit routes also create a natural place for attenuated authority, credits,
profile negotiation, and failure-domain alignment.

## Limits

The work improves transport and topology rather than proving secure admission,
exactly-once effects, or a universal overlay. It does not supply capability
security or kernel-enforced budgets, and its benchmark gains cannot be assumed
for embedded targets or arbitrary actor graphs.

## Derived work

- [Distribution gateway and remote actor semantics](../20-notes/managed-actor-runtime-components/distribution-gateway-and-remote-actor-semantics.md)
- [2026-09-03 component research journal](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md)
