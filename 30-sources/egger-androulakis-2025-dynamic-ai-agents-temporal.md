---
title: "Of course you can build dynamic AI agents with Temporal"
kind: source
created: "2026-09-28"
authors: ["Mason Egger", "Steve Androulakis"]
published: "2025-11-12"
citation_key: "eggerandroulakis2025durableagents"
container: "Temporal blog"
url: "https://temporal.io/blog/of-course-you-can-build-dynamic-ai-agents-with-temporal"
accessed: "2026-09-28"
tags: [agent-frameworks, durable-execution, workflows]
aliases: []
---

# Of course you can build dynamic AI agents with Temporal

## Reference

Mason Egger and Steve Androulakis,
[“Of course you can build dynamic AI agents with Temporal”](https://temporal.io/blog/of-course-you-can-build-dynamic-ai-agents-with-temporal),
Temporal, 12 November 2025.

## Research question or contribution

How can dynamic model decisions coexist with replayable orchestration?

## Method

The practitioner article explains a workflow/activity pattern and examples.
It is vendor guidance, not a Kay experiment or independent comparison.

## Findings

It places nondeterministic model and tool calls in activities and retains
their outcomes in workflow history, while the orchestration path replays
recorded choices after failure. It distinguishes dynamic plans from
unrecorded nondeterminism during recovery.

## Relevance

Kay can durably record a chosen agent decision before attempting its effect,
then resume from the recorded boundary. Recovery still needs the current
grant, idempotency key, and final sink status.

## Limits

The article's broad durability claims do not make an arbitrary external
service transaction atomic with a workflow. It supplies no Kay kernel
assurance or model-neutral behavior API.

## Derived work

- [Native agent behavior framework](../20-notes/native-agent-behavior-framework.md).
