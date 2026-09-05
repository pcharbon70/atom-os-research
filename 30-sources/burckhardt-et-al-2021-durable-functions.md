---
title: "Durable Functions: Semantics for Stateful Serverless"
kind: source
created: "2026-09-05"
authors:
  - "Sebastian Burckhardt"
  - "Chris Gillum"
  - "David Justo"
  - "Konstantinos Kallas"
  - "Connor McMahon"
  - "Christopher S. Meiklejohn"
published: 2021
citation_key: "burckhardt-et-al-2021-durable-functions"
container: "Proceedings of the ACM on Programming Languages 5(OOPSLA)"
edition: null
isbn: null
doi: "10.1145/3485510"
url: "https://www.microsoft.com/en-us/research/wp-content/uploads/2021/10/DF-Semantics-Final.pdf"
accessed: "2026-09-05"
tags:
  - durable-execution
  - formal-semantics
  - workflows
aliases:
  - "Durable Functions semantics"
---

# Durable Functions: Semantics for Stateful Serverless

## Reference

Sebastian Burckhardt, Chris Gillum, David Justo, Konstantinos Kallas, Connor
McMahon, and Christopher S. Meiklejohn. “[Durable Functions: Semantics for
Stateful Serverless](https://doi.org/10.1145/3485510).” *Proceedings of the ACM
on Programming Languages* 5, OOPSLA, 2021, article 133.

## Research question or contribution

The paper formalizes the behavior of actors, orchestrations, and critical
sections in Azure Durable Functions and relates the implementation's event-
history replay model to higher-level abstract semantics.

## Method

The authors present several formal models, prove equivalences under stated
restrictions, connect them to the deployed runtime, and discuss practical
programming constraints and history growth.

## Findings

- Durable replay can give convenient stateful abstractions over failure-prone
  execution when nondeterminism and external effects cross explicit APIs.
- Orchestration history is both a recovery mechanism and a potential source of
  unbounded replay/storage cost.
- High-level semantics remain conditional on implementation restrictions and
  on what the participating substrate records.

## Relevance

Atom OS can provide generic durable-workflow mechanisms in Layer 4 while Layer
5 owns the business state machine, determinism contract, effects,
compensations, terminal outcomes, and history-retention policy.

## Limits

This is a serverless platform with its own storage, scheduling, and programming
model. The proof does not make arbitrary external effects atomic, supply
capability security, or establish performance on Atom OS.

## Derived work

- [Workflows, process managers, timers, and compensation](../20-notes/applications-and-domain-services-components/workflows-process-managers-timers-and-compensation.md)
- [Durable state, journals, snapshots, and projections](../20-notes/applications-and-domain-services-components/durable-state-journals-snapshots-and-projections.md)
