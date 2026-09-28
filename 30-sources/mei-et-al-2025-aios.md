---
title: "AIOS: LLM Agent Operating System"
kind: source
created: "2026-09-28"
authors: ["Kai Mei", "Xi Zhu", "Wujiang Xu", "Mingyu Jin", "Wenyue Hua", "Zelong Li", "Shuyuan Xu", "Ruosong Ye", "Yingqiang Ge", "Yongfeng Zhang"]
published: "2025-08-12"
citation_key: "mei2025aios"
container: "arXiv"
edition: "arXiv:2403.16971v5"
url: "https://arxiv.org/abs/2403.16971v5"
accessed: "2026-09-28"
tags: [agent-frameworks, operating-systems, resource-management]
aliases: []
---

# AIOS: LLM Agent Operating System

## Reference

Kai Mei and colleagues,
[“AIOS: LLM Agent Operating System”](https://arxiv.org/html/2403.16971),
arXiv:2403.16971v5, 12 August 2025. The identifier reflects its original
2024 submission; this note reads version 5.

## Research question or contribution

Can common scheduling, context, memory, storage, tool, and access services
serve agents from different frameworks more efficiently?

## Method

The paper implements an AIOS service layer and SDK over Ubuntu 22.04, then
compares multiple hosted agent frameworks using GPT-4o-mini or one local
Llama-3.1-8B/Mistral-7B model on an RTX A5000. It reports task scores and
concurrent throughput/latency, with up to 2.1× throughput in a tested case.

## Findings

Shared inference scheduling and tool management can be factored from agent
application code. Framework adapters let distinct decision loops use common
services. The paper's “AIOS kernel” depends on conventional OS calls for
hardware and process isolation; its agent-memory manager handles interaction
history rather than virtual memory. The study's access manager uses agent
groups and prompts for certain destructive operations.

## Relevance

Kay can study a shared inference/resource service and a stable agent API
without placing LLMs in its privileged kernel. The paper motivates measuring
concurrent utility and latency alongside security.

## Limits

The Ubuntu/GPU results establish neither bare-metal portability nor Kay
capability enforcement. Its throughput gain is workload and scheduler
specific; task scores include prompt changes and parameter validation, so
they cannot isolate one architectural cause. The paper focuses on LLM agents
and does not show model-neutral behavior interoperability.

## Derived work

- [Native agent behavior framework](../20-notes/native-agent-behavior-framework.md).
