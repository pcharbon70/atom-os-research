---
title: "TLC model configuration and specification options"
kind: source
created: "2026-09-06"
authors: ["TLA+ project"]
published: null
citation_key: "tlaplus-project-2026-tlc-model-configuration"
container: "TLA+ Toolbox documentation"
edition: "Nightly documentation accessed 2026-09-05"
isbn: null
doi: null
url: "https://nightly.tlapl.us/doc/model/overview-page.html"
accessed: "2026-09-05"
tags:
  - formal-methods
  - model-checking
  - testing
aliases: []
---

# TLC model configuration and specification options

## Reference

TLA+ project. [TLC model configuration and specification options](https://nightly.tlapl.us/doc/model/overview-page.html). TLA+ Toolbox documentation. Publication date not established. Nightly documentation accessed 2026-09-05. Accessed 2026-09-05; source record created 2026-09-06.

## Research question or contribution

Evidence relevant to models, fault injection, and measurement in the CLI-first operating-system proof of concept.

## Method

Read Model Overview and Spec Options sections on behavioral specifications, properties and state constraints.

## Findings

TLC distinguishes invariants, deadlocks and temporal properties. Behavioral specifications express fairness. A [state constraint](https://nightly.tlapl.us/doc/model/spec-options-page.html) restricts which successors are explored.

## Relevance

Informs the proposed requirement contract and its negative tests. This source does not establish that Atom implements or passes that contract.

## Limits

A successful constrained run covers its chosen state space and assumptions. Documentation tracking nightly is not a pinned tool release; state constraints must not silently cut off the failure the model intends to test.

## Derived work

- [Models, fault injection, and measurement](../20-notes/proof-of-concept-requirements/models-fault-injection-and-measurement.md)
