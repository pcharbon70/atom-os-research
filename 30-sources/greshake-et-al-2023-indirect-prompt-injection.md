---
title: "Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection"
kind: source
created: "2026-09-26"
authors:
  - "Kai Greshake"
  - "Sahar Abdelnabi"
  - "Shailesh Mishra"
  - "Christoph Endres"
  - "Thorsten Holz"
  - "Mario Fritz"
published: 2023
citation_key: "greshake2023indirectpromptinjection"
container: "arXiv:2302.12173v2"
edition: null
isbn: null
doi: "10.48550/arXiv.2302.12173"
url: "https://arxiv.org/abs/2302.12173v2"
accessed: "2026-09-26"
tags:
  - agent-security
  - prompt-injection
  - threat-model
aliases: []
---

# Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection

## Reference

Kai Greshake, Sahar Abdelnabi, Shailesh Mishra, Christoph Endres, Thorsten
Holz, and Mario Fritz. 2023. *Not what you've signed up for: Compromising
Real-World LLM-Integrated Applications with Indirect Prompt Injection*.
[arXiv version 2, 5 May 2023](https://arxiv.org/abs/2302.12173v2).
[Full text](https://arxiv.org/html/2302.12173v2), especially Sections 3–5.

## Research question or contribution

Can attacker-controlled retrieved data redirect an application acting for a
legitimate user? The paper supplies a threat taxonomy and feasibility
demonstrations of indirect prompt injection.

## Method

Section 4 tests synthetic LLM applications with prepared tool responses,
Bing Chat reading local HTML, and code completion. Synthetic interfaces do
not contact real target services. These are qualitative demonstrations.

## Findings

Retrieved instructions can change model behavior and tool use. Section 4.2.1
shows why nominal read operations such as searches or URL retrieval can carry
information outward. Sections 4.2–4.3 include persistence, manipulated content,
and concealed injections.

## Relevance

Kay interpretation: distinguish information access from authority to act.
Network reads need destination and disclosure controls; persistence and
derived summaries need provenance. Assume compromised agent behavior when
testing enforcement, independently of whether a detector recognizes an
injection. These are Kay design requirements, not defenses validated here.

## Limits

Sections 5.2–5.4 leave success-rate measurement and broader agent evaluation
open. Changing black-box services constrain reproducibility. Hosted
demonstrations establish neither kernel escape nor protection against one;
no Kay OS execution occurred.

## Derived work

- [Safe agent delegation and execution](../20-notes/safe-agent-delegation-and-execution.md).
- [Agent delegation threat model and assurance](../20-notes/agent-delegation-threat-model-and-assurance.md).
- [Safe delegation inquiry](../40-inquiries/how-can-kay-os-safely-delegate-work-to-agents.md).
