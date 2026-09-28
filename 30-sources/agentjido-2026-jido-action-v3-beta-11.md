---
title: "Jido Action 3.0.0-beta.11"
kind: source
created: "2026-09-28"
published: "2026-09-13"
citation_key: "agentjido2026jidoactionv3"
container: "Hex package and version-tagged project guides"
edition: "3.0.0-beta.11"
url: "https://hex.pm/packages/jido_action/3.0.0-beta.11"
accessed: "2026-09-28"
tags: [agent-frameworks, elixir, workflows]
aliases: []
---

# Jido Action 3.0.0-beta.11

## Reference

Agent Jido, [Jido Action 3.0.0-beta.11](https://hex.pm/packages/jido_action/3.0.0-beta.11),
published 13 September 2026. Read its version-tagged
[README](https://github.com/agentjido/jido_action/blob/v3.0.0-beta.11/README.md),
[Action](https://github.com/agentjido/jido_action/blob/v3.0.0-beta.11/guides/actions.md),
[Flow](https://github.com/agentjido/jido_action/blob/v3.0.0-beta.11/guides/flows.md),
[storage](https://github.com/agentjido/jido_action/blob/v3.0.0-beta.11/guides/flow-storage.md),
[execution](https://github.com/agentjido/jido_action/blob/v3.0.0-beta.11/guides/execution.md),
and [security](https://github.com/agentjido/jido_action/blob/v3.0.0-beta.11/guides/security.md)
guides.

## Research question or contribution

Which action and plan interfaces can remain inspectable when an agent or model
chooses the next step?

## Method

The pinned documentation was inspected for schema validation, executable
registry, graph execution, durability, and authorization boundaries. Package
metadata confirms the requested beta.11 release exists.

## Findings

- Named Actions validate inputs and outputs. Flows compose Steps, Subflows,
  Choices, Maps, Reduces, bounded Iterates, and a terminal Dispatch. `Jido.Exec`
  owns an in-memory execution session; the outer application owns durable
  orchestration, queues, recovery, distributed coordination, and retries.
- Stored Flow data passes through a Codec with a host-owned trusted Registry;
  data cannot create atoms or derive module names. An Action schema checks
  shape, not a caller's authorization. The security guide assigns tenant
  checks, secrets, resource policy, and external effects to the host.
- Flow nodes discard Action extras, which matters if an outer runtime uses
  extras as proposed directives. Moving an Action into a Flow can therefore
  change effect delivery unless the host supplies an explicit contract.

## Relevance

Kay can define its own versioned, declarative action/plan format and
allowlisted executable registry. Every effectful Action still needs the
[protected delegation boundary](../20-notes/safe-agent-delegation-and-execution.md).

## Limits

The beta.11 tag README still labels some prose and badge as beta.10; the Hex
release and install snippet identify beta.11. This documentation inconsistency
is recorded rather than silently reconciled. The package is an in-memory
workflow library, not a durable or authorization framework. No package
implementation is selected for Kay.

## Derived work

- [Native agent behavior framework](../20-notes/native-agent-behavior-framework.md).
