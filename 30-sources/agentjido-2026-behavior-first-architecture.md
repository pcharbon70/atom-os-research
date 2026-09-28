---
title: "Behavior-First Architecture"
kind: source
created: "2026-09-28"
published: null
citation_key: "agentjido-behavior-first-architecture"
container: "Agent Jido project documentation"
edition: null
url: "https://jido.run/docs/reference/behavior-first-architecture"
accessed: "2026-09-28"
tags: [agent-frameworks, actor-model, software-architecture]
aliases: []
---

# Behavior-First Architecture

## Reference

Agent Jido, [“Behavior-First Architecture”](https://jido.run/docs/reference/behavior-first-architecture),
project reference article, accessed 28 September 2026. A publication date is
not stated on the page.

## Research question or contribution

Why separate stable agent behavior contracts from processes, prompts, and
specific language implementations?

## Method

The official article's contract and trade-off sections were read against the
version-pinned v3 package guides. It is practitioner design rationale, not an
independent evaluation.

## Findings

The article frames Action, Signal, and Agent as distinct work, communication,
and state-transition boundaries. It argues that OTP-like behavior contracts
let one runtime own concurrency, failure, and lifecycle while application
code supplies domain decisions. Its current site content may evolve
independently of the pinned beta package.

## Relevance

This supports a framework-neutral Kay contract: the OS owns protected
admission and effects, while several agent decision engines can implement the
same unprivileged behavior interface.

## Limits

The page's shorthand that an Action is a “named capability” is conceptual.
A validated name or schema does not confer a Kay kernel capability or grant.
The article does not demonstrate containment or durable external effects.

## Derived work

- [Native agent behavior framework](../20-notes/native-agent-behavior-framework.md).
