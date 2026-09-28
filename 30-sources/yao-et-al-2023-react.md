---
title: "ReAct: Synergizing Reasoning and Acting in Language Models"
kind: source
created: "2026-09-28"
authors: ["Shunyu Yao", "Jeffrey Zhao", "Dian Yu", "Nan Du", "Izhak Shafran", "Karthik Narasimhan", "Yuan Cao"]
published: 2023
citation_key: "yao2023react"
container: "International Conference on Learning Representations"
edition: "arXiv:2210.03629"
url: "https://arxiv.org/abs/2210.03629"
accessed: "2026-09-28"
tags: [agent-frameworks, language-models, planning]
aliases: []
---

# ReAct: Synergizing Reasoning and Acting in Language Models

## Reference

Shunyu Yao and colleagues,
[“ReAct: Synergizing Reasoning and Acting in Language Models”](https://arxiv.org/abs/2210.03629),
ICLR 2023. The arXiv record began in October 2022.

## Research question or contribution

Can an LLM alternate reasoning, external actions, and observations to solve
tasks better than reasoning-only or action-only prompting?

## Method

The paper evaluates prompted agents on question answering, fact verification,
and interactive ALFWorld/WebShop tasks, with ablations and qualitative failure
analysis. It studies model behavior, not OS mediation.

## Findings

Interleaving thoughts, proposed actions, and feedback can improve task
completion in the evaluated settings. The paper also shows wrong action
selection and hallucinated observations in some trajectories.

## Relevance

ReAct is one possible Kay decision provider. Its proposed action must remain
data until the protected effect path accepts it. Model reasoning traces are
diagnostic material, not an authority source or proof of correctness.

## Limits

The reported benchmark gains depend on the evaluated models and tasks.
Nothing in the paper establishes native isolation, grant enforcement, or
exactly-once execution. A model-neutral Kay framework must also work without
ReAct or any LLM.

## Derived work

- [Native agent behavior framework](../20-notes/native-agent-behavior-framework.md).
