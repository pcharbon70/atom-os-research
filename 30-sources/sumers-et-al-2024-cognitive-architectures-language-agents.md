---
title: "Cognitive Architectures for Language Agents"
kind: source
created: "2026-09-28"
authors: ["Theodore R. Sumers", "Shunyu Yao", "Karthik Narasimhan", "Thomas L. Griffiths"]
published: 2024
citation_key: "sumers2024coala"
container: "Transactions on Machine Learning Research"
edition: "arXiv:2309.02427v3"
url: "https://arxiv.org/abs/2309.02427v3"
accessed: "2026-09-28"
tags: [agent-frameworks, cognitive-architecture, language-models]
aliases: []
---

# Cognitive Architectures for Language Agents

## Reference

Theodore R. Sumers, Shunyu Yao, Karthik Narasimhan, and Thomas L. Griffiths,
[“Cognitive Architectures for Language Agents”](https://arxiv.org/html/2309.02427),
Transactions on Machine Learning Research, 2024; arXiv v3 dated 15 March
2024.

## Research question or contribution

How can language agents be described through memory, action, and decision
modules rather than a single prompt loop?

## Method

This conceptual paper analyzes prior cognitive architectures and language
agent systems. It organizes memory into working and long-term forms, actions
into internal and external kinds, and decisions into a repeated planning and
execution process. It is a synthesis, not an OS implementation trial.

## Findings

An LLM call is only one operation inside an agent cycle. Retrieval, reasoning,
and learning modify state differently from external grounded actions. Working
memory persists across model calls in the proposed architecture; episodic,
semantic, and procedural memory have different uses.

## Relevance

Kay can expose a model-neutral cycle with typed observations, working state,
optional memory, a decision provider, and proposed actions. The memory
taxonomy helps identify which records need provenance and current policy at
restore or retrieval.

## Limits

The taxonomy does not define Kay authorization, durable effects, scheduling
budgets, or isolation. Its examples predominantly involve language models;
using the decomposition for symbolic agents is Kay synthesis.

## Derived work

- [Native agent behavior framework](../20-notes/native-agent-behavior-framework.md).
