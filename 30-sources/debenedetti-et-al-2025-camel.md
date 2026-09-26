---
title: "Defeating prompt injections by design"
kind: source
created: "2026-09-26"
authors:
  - "Edoardo Debenedetti"
  - "Ilia Shumailov"
  - "Tianqi Fan"
  - "Jamie Hayes"
  - "Nicholas Carlini"
  - "Daniel Fabian"
  - "Christoph Kern"
  - "Chongyang Shi"
  - "Andreas Terzis"
  - "Florian Tramèr"
published: 2025
citation_key: "debenedetti-et-al-2025-camel"
container: "arXiv:2503.18813v2"
edition: null
isbn: null
doi: "10.48550/arXiv.2503.18813"
url: "https://arxiv.org/abs/2503.18813v2"
accessed: "2026-09-26"
tags: [ai-agents, capabilities, information-flow, prompt-injection]
aliases: ["CaMeL"]
---

# Defeating prompt injections by design

## Reference

Edoardo Debenedetti et al. *Defeating Prompt Injections by Design*.
arXiv:2503.18813v2, 24 June 2025.
[Versioned full text](https://arxiv.org/html/2503.18813v2).

## Research question or contribution

CaMeL separates planning from untrusted-data processing and enforces policies
through an interpreter tracking dependencies and permitted readers.

## Method

Sections 3–5 define the threat model and mechanisms; Section 6 evaluates an
AgentDojo prototype; Sections 7 and 9 discuss leakage and usability.

## Findings

Controlling tool selection alone leaves argument substitution exposed. The
prototype adds data-flow checks. Its abstract reports 77% task completion
against 84% undefended in the stated evaluation. Section 6.5 reports increased
token usage; these are hosted benchmark results, not native kernel costs.

## Relevance

Kay should test exact argument/destination enforcement and conservative
dependency tracking separately from model behavior. CaMeL's named capabilities
do not prescribe Kay's kernel-object representation or select a runtime.

## Limits

The principal threat model trusts the user prompt and uncompromised memory.
Incorrect text without prohibited flows is outside its protection. Side
channels, policy quality, interpreter correctness, and declassification remain
limits. Its result does not establish arbitrary native-code containment.

## Derived work

- [Safe agent delegation](../20-notes/safe-agent-delegation-and-execution.md).
- [Threat model and assurance](../20-notes/agent-delegation-threat-model-and-assurance.md).
