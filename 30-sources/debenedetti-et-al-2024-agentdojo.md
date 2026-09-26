---
title: "AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents"
kind: source
created: "2026-09-26"
authors:
  - "Edoardo Debenedetti"
  - "Jie Zhang"
  - "Mislav Balunović"
  - "Luca Beurer-Kellner"
  - "Marc Fischer"
  - "Florian Tramèr"
published: 2024
citation_key: "debenedetti2024agentdojo"
container: "arXiv:2406.13352v3"
edition: null
isbn: null
doi: "10.48550/arXiv.2406.13352"
url: "https://arxiv.org/abs/2406.13352v3"
accessed: "2026-09-26"
tags:
  - agent-security
  - prompt-injection
  - security-evaluation
aliases: []
---

# AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents

## Reference

Edoardo Debenedetti, Jie Zhang, Mislav Balunović, Luca Beurer-Kellner,
Marc Fischer, and Florian Tramèr. 2024. *AgentDojo: A Dynamic Environment
to Evaluate Prompt Injection Attacks and Defenses for LLM Agents*.
[arXiv version 3, 24 November 2024](https://arxiv.org/abs/2406.13352v3).
[Full text](https://arxiv.org/html/2406.13352v3), especially Sections 3–4.

## Research question or contribution

AgentDojo evaluates useful task completion and attacker objectives together
in an extensible environment for agents encountering untrusted tool data.

## Method

Sections 3–4 define simulated application state, tools, 97 user tasks, and
629 security cases. Deterministic checks inspect outputs and state changes.
The paper evaluates model agents, attacks, and defenses through hosted model
interfaces and a Python environment.

## Findings

Benign failures and attack-induced failures both occur. Section 4.3 reports
benefits from restricting available tools, but also attacks using the same
tools needed for legitimate work. Defense evaluation therefore requires
utility alongside attack success.

## Relevance

Kay interpretation: pair benign workloads with adversarial variants, inspect
actual effects, and test harmful arguments to authorized operations. Add
deterministically hostile executors to exercise kernel and broker containment
independently of a model's susceptibility. These extensions remain untested.

## Limits

The benchmark does not establish kernel isolation or native-tool confinement.
Section 4.3 excludes ongoing tasks sharing an unreset context and identifies
limits of preselecting tools. These historical model results are not current
rankings or security guarantees; pin code, cases, models, and configuration
for any reproduction. No local benchmark was run.

## Derived work

- [Agent delegation threat model and assurance](../20-notes/agent-delegation-threat-model-and-assurance.md).
- [Safe agent delegation and execution](../20-notes/safe-agent-delegation-and-execution.md).
- [Safe delegation inquiry](../40-inquiries/how-can-kay-os-safely-delegate-work-to-agents.md).
