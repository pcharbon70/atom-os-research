---
title: "AgentKernel: The Trust-Native Agentic Operating System"
kind: source
created: "2026-09-26"
authors:
  - "Zhenhua Zou"
  - "Sheng Guo"
  - "Qiuyang Zhan"
  - "Lepeng Zhao"
  - "Shuo Li"
  - "Zhuotao Liu"
published: "2026-08-29"
citation_key: "zou-et-al-2026-agentkernel"
container: "arXiv"
edition: "arXiv:2609.29647v1"
isbn: null
doi: null
url: "https://arxiv.org/abs/2609.29647"
accessed: "2026-09-26"
tags:
  - agent-security
  - capability-security
  - operating-systems
  - provenance
aliases: []
---

# AgentKernel: The Trust-Native Agentic Operating System

## Reference

Zhenhua Zou, Sheng Guo, Qiuyang Zhan, Lepeng Zhao, Shuo Li, and Zhuotao
Liu. “[AgentKernel: The Trust-Native Agentic Operating
System](https://arxiv.org/html/2609.29647),” arXiv:2609.29647v1. The
[arXiv record](https://arxiv.org/abs/2609.29647) displays a 29 August 2026
submission date; accessed 26 September 2026.

## Research question or contribution

The paper proposes one mandatory boundary for agent identity, input
mediation, memory provenance, and tool execution.

## Method

Architecture, threat model, informal invariant arguments (§§3–5), and
qualitative comparison (§6). Security and performance
measurements remain future work (§7.4).

## Findings

- A registry and agent kernel mediate model, tool, and storage adapters (§4.1).
- Four pillars propose identity and delegation, staged input filtering,
  item-level memory labels, and tool policy with optional LLM validation and
  plan–trace audit (§§4.2–4.5).
- A tool call would yield a resource allowlist installed before its process
  tree runs through Linux eBPF or equivalent host hooks. The conventional
  kernel retains address spaces, devices, and isolation (§1, §4.5, §5.4.3).

## Relevance

The lifecycle decomposition informs [safe agent delegation and
execution](../20-notes/safe-agent-delegation-and-execution.md) and the
[open Kay OS inquiry](../40-inquiries/how-can-kay-os-safely-delegate-work-to-agents.md).

## Limits

- Guarantees assume no alternate model, tool, or storage path or ambient
  credential. Semantic classifiers may miss attacks; taint depends on source
  segmentation; the registry concentrates trust. Formal verification and
  realistic evaluation remain pending (§5.5, §7.4).
- arXiv dates v1 to 29 August 2026 despite its `2609` identifier; the
  discrepancy is unresolved. Its DOI is pending registration.

## Derived work

- [Safe agent delegation and execution](../20-notes/safe-agent-delegation-and-execution.md)
- [How can Kay OS safely delegate work to agents?](../40-inquiries/how-can-kay-os-safely-delegate-work-to-agents.md)
