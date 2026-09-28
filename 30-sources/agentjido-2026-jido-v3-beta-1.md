---
title: "Jido 3.0.0-beta.1 agent and actor framework"
kind: source
created: "2026-09-28"
published: "2026-09-14"
citation_key: "agentjido2026jidov3"
container: "Hex package and version-tagged project guides"
edition: "3.0.0-beta.1"
url: "https://hex.pm/packages/jido/3.0.0-beta.1"
accessed: "2026-09-28"
tags: [agent-frameworks, actor-model, elixir, research-method]
aliases: []
---

# Jido 3.0.0-beta.1 agent and actor framework

## Reference

Agent Jido, [Jido 3.0.0-beta.1](https://hex.pm/packages/jido/3.0.0-beta.1),
published 14 September 2026. Read the version-tagged
[README](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/README.md),
[actor/agent guide](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/actor-and-agent-framework.md),
[turn/commit guide](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/turns-commit-and-effects.md),
[recoverable effects guide](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/recoverable-effects.md),
and [runtime guide](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/runtime.md).

## Research question or contribution

What behavior and lifecycle contracts does a current OTP agent framework
place above lightweight processes?

## Method

Version-pinned public package metadata and primary project documentation
were read for execution order, state, effects, identity, recovery, and limits.
No package code or BEAM artifact was installed or executed.

## Findings

- An Agent is a validated immutable definition or instance. The live Agent
  Server is an OTP actor that serializes admitted Signals, runs one Action or
  Flow, validates a candidate, persists and commits it, then dispatches
  Directives. A successful call establishes a committed state revision, not
  completion of every external effect.
- Actions or Flows may perform synchronous I/O before commit; a failed turn
  does not undo that work. External idempotency, pending intent, and
  reconciliation remain application responsibilities. Core does not promise a
  universal outbox or exactly-once external effects.
- Logical child ownership, local identity, checkpoints, cancellation, and
  restart are distinct from business completion. A namespaced Agent Ref does
  not prove remote location or authority; an Agent ID is not a credential.

## Relevance

The state/actor/effect separation is a useful design pattern for a
[Kay-native agent behavior service](../20-notes/native-agent-behavior-framework.md).
Kay must put grant validation and final-effect mediation outside the agent
actor's authority and bind recovery to the current task generation.

## Limits

Jido's README calls this an evaluation beta. It reports a skipped
cluster-authority probe, skipped optional Bedrock durability tests, and a
failed Elixir 1.18/OTP 27 example compilation gate; it states beta.1 was
verified only on Elixir 1.20.3/OTP 29.0.5. These are project-reported limits,
not local test results. OTP process supervision does not qualify Kay kernel
isolation. No Jido `.beam` reuse is proposed.

## Derived work

- [Native agent behavior framework](../20-notes/native-agent-behavior-framework.md).
- [Agent behavior inquiry](../40-inquiries/where-should-native-agent-behavior-live-in-kay-os.md).
