---
title: "When the Agent Becomes the Kernel: A Systematization of Security on the Path to AI-Native Operating Systems"
kind: source
created: "2026-09-28"
authors: ["Li Zhang", "Yang Sun", "Jie Shi"]
published: "2026-09-20"
citation_key: "zhang2026agentkernelsecuritysok"
container: "arXiv"
edition: "arXiv:2609.23700v1"
url: "https://arxiv.org/abs/2609.23700"
accessed: "2026-09-28"
tags: [agent-security, operating-systems, reference-monitors]
aliases: []
---

# When the Agent Becomes the Kernel: A Systematization of Security on the Path to AI-Native Operating Systems

## Reference

Li Zhang, Yang Sun, and Jie Shi,
[“When the Agent Becomes the Kernel”](https://arxiv.org/html/2609.23700),
arXiv:2609.23700v1, 20 September 2026.

## Research question or contribution

Which agent trust-boundary crossings can be checked deterministically, and
which still require uncertain semantic judgments?

## Method

The paper systematizes agent attacks and defenses by provenance versus
content-semantic mediation, reviews evaluation validity, and develops an
AI-native OS research agenda. It is an analysis, not an implemented Kay
boundary or measured Kay system.

## Findings

The paper distinguishes a model acting as an increasingly powerful principal
from a tamper-resistant mediator that must bound it. It identifies
authorization and input interpretation gaps that cannot be closed simply by
promoting a model into an OS decision role.

## Relevance

Kay should keep agent decision engines outside the privileged protection
kernel, require deterministic ceilings at effects, and report residual
semantic error separately from authority containment.

## Limits

The paper is a current preprint and systematization. Its broad AI-native OS
trajectory is a research argument; it does not prove a specific deployment
will have an agent-controlled kernel or that semantic failure is eliminable.

## Derived work

- [Native agent behavior framework](../20-notes/native-agent-behavior-framework.md).
