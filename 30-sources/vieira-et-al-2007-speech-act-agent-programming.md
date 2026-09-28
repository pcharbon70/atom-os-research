---
title: "On the Formal Semantics of Speech-Act Based Communication in an Agent-Oriented Programming Language"
kind: source
created: "2026-09-28"
authors: ["Renata Vieira", "Alvaro Moreira", "Michael Wooldridge", "Rafael H. Bordini"]
published: 2007
citation_key: "vieira2007speechact"
container: "Journal of Artificial Intelligence Research 29, 221–267"
url: "https://www.cs.ox.ac.uk/people/michael.wooldridge/pubs/jair2007a.pdf"
accessed: "2026-09-28"
tags: [agent-communication, agent-frameworks, formal-semantics]
aliases: []
---

# On the Formal Semantics of Speech-Act Based Communication in an Agent-Oriented Programming Language

## Reference

Renata Vieira, Alvaro Moreira, Michael Wooldridge, and Rafael H. Bordini,
[“On the Formal Semantics of Speech-Act Based Communication in an Agent-Oriented Programming Language”](https://www.cs.ox.ac.uk/people/michael.wooldridge/pubs/jair2007a.pdf),
Journal of Artificial Intelligence Research 29 (2007), 221–267.

## Research question or contribution

How can an AgentSpeak agent process communication with precise operational
semantics, including message effects on beliefs and intentions?

## Method

The authors extend AgentSpeak's structural operational semantics for
speech-act messages and work through agent communication examples. This is a
formal language study, not a Kay or hardware-security experiment.

## Findings

Goal and plan execution can be modeled separately from communication; an
agent's interpretation of a received message is an explicit transition rule.
The paper also explains the limits of attributing real mental states to
arbitrary agents.

## Relevance

Non-LLM agents can implement deterministic or symbolic decision behavior
behind the same Kay observation/decision interface. A message's declared
performative or goal is still only a claim until the receiving boundary
authenticates its origin and applicable authority.

## Limits

The formal semantics are specific to AgentSpeak. They do not establish
security of a generic event bus, authorization of external effects, or a
universal cognitive model. Kay's behavior interface is an extrapolation.

## Derived work

- [Native agent behavior framework](../20-notes/native-agent-behavior-framework.md).
