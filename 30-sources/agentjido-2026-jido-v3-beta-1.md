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
The tagged [core-scope guide](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/core-scope.md)
distinguishes supported beta behavior from deferred integration packages;
the [design index](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/docs/design/README.md)
states that its proposals do not override the implemented API.

## Research question or contribution

What behavior and lifecycle contracts does a current OTP agent framework
place above lightweight processes?

## Method

Version-pinned public package metadata and primary project documentation
were read across the complete core infrastructure: authoring, instance
supervision, plugins, input resources, topology, persistence, outcomes, and
observation as well as execution. The tagged guide and design-document trees
were inventoried; claims below use the supported-release guides. Design
proposals are identified as deferred. No package code or BEAM artifact was
installed or executed.

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

## Supported infrastructure and component boundaries

| Component | Documented beta.1 role and limit |
| --- | --- |
| [Agent definition, instance, and state](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/agent-definitions-and-instances.md) | One immutable definition describes schema, routes, plugins, and metadata; an identified instance holds complete validated state. A successful executable returns the complete next state. |
| [DSL, Builder, Codec, and registry](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/builders-and-codecs.md) | Multiple authoring forms meet the same validation. Portable stored declarations resolve only identifiers in a trusted registry; authored definition data differs from checkpoints. |
| [Signal to Command to route](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/signals-commands-and-routes.md) | The live Command preserves the incoming Signal and caller context. Pure and live plugin inputs are separate. Router precedence selects one executable; source strings and IDs are data, not authenticated rights. |
| [Actions, Flows, Instructions, Directives](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/actions-flows-and-instructions.md) | Jido Action runs one target per Turn, which yields complete candidate state and optional Directives. A multi-step Flow remains one Turn; its intermediate results are not committed revisions. |
| [Four-facet Plugin package](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/plugin-contract-and-lifecycle.md) | A package can select Agent preparation/reduction, AgentServer admission/runtime/dispatch, Persistence owned-value conversion, and Topology static contribution. Each facet has a limited callback surface; it does not sandbox untrusted code. |
| [AgentServer lifecycle](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/agent-server-lifecycle.md) | One `:gen_statem` actor serializes Turns, uses owned tasks, coordinates plugin readiness, commit, post-commit dispatch, restart, stop, hibernate/thaw, and a quiescent upgrade boundary. |
| [Named Jido instance](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/deployment-and-shutdown.md) | One supervised application instance owns Registry, Task Supervisor, ephemeral runtime store, spawn registry, and dynamic Agent supervisor. Partitions scope local identity; they are not security tenants. |
| [Persistence and checkpoint](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/compare-and-swap-hibernate-and-thaw.md) | Optional adapters hold portable active/tombstone records with revisions and exact-byte compare-and-swap. A failed required write stops the activation; ambiguous storage outcomes require reload and reconciliation. Checkpoints exclude mailbox and runtime resources. |
| [Input plugins](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/sensors.md) | Heartbeat, Bus, and SensorManager deliver Signals through the normal Turn path. The V2 Sensor behavior and built-in Sensors were removed; inputs do not write Agent state directly. |
| [Scheduler and durable occurrences](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/durable-schedule-occurrences.md) | The Scheduler Plugin can retain one pending occurrence per recurring job with a stable ID and explicit acknowledgement in a later business-state commit. It skips offline/busy slots and does not promise replay of every missed interval. |
| [Topology and controller](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/topology-definitions.md) | Definition, instance, expanded plan, and live controller are separate. Plans cover Agents, groups, one current Bus resource type, ownership and subscriptions; the controller activates, checks readiness, repairs the same target, adds Agents, and accepts exact known-node placement. |
| [Children and ownership](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/ownership-orphans-and-remote-children.md) | Post-commit child Directives create tagged logical relationships with stop/continue/orphan policy. Remote-start replies can be indeterminate; local relationships do not confer cluster ownership. |
| [Errors, outcome, telemetry and audit](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/telemetry-tracing-and-logs.md) | Structured stage and commit status distinguish evaluation, commit, and Directive settlement. Bounded telemetry, debug, optional OpenTelemetry mapping, and a separate Audit Plugin serve different purposes; telemetry is not durable audit. |

The [configuration guide](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/configuration.md)
separates instance, actor, and observability options. Its task-supervisor
limit does not bound Agent mailboxes or plugin processes. The
[admission guide](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/admission-cancellation-and-timeouts.md)
says `max_postponed_signals` bounds received/postponed work, not messages
still waiting in the mailbox; caller timeouts need not cancel started work.
The [portable-state guide](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/portable-state-and-checkpoints.md)
distinguishes durable Agent facts from plugin runtime resources and ephemeral
instance coordination.
The [storage guide](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/storage.md)
describes the binary adapter boundary and the ETS, File, and Redis profiles:
ETS is test/development storage, File has a one-BEAM-writer restriction, and
Redis TTL can expire tombstone fences. Optional integrations require their
own host-provided dependencies and operational qualification. The
[Audit Plugin guide](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/audit-records.md)
describes bounded selected domain facts in Agent state, not a complete
tamper-resistant security audit service.

## Implemented versus deferred scope

The tagged [core-scope guide](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/core-scope.md)
lists supported local topology repair and exact-node placement, but not
membership discovery, automatic rebalance, cluster-exclusive ownership,
transport authentication, durable inboxes, or a general recovery queue.
Its names `jido_durable`, `jido_cluster`, and `jido_fabric` describe possible
future extension owners, not available beta.1 packages. The package's AI
examples and `req_llm` dependency are development/test material, not a
production model-policy or LLM service supplied by core Jido.

## Relevance

The complete infrastructure offers a much stronger reference model for a
[Kay-native agent behavior service](../20-notes/native-agent-behavior-framework.md)
than the Turn loop alone. Kay can study separate definition, execution,
instance, input, plugin, topology, persistence, and observation contracts.
Kay must put grant validation and final-effect mediation outside the agent
actor's authority and bind recovery to the current task generation.

## Limits

Jido's README calls this an evaluation beta. It reports a skipped
cluster-authority probe, skipped optional Bedrock durability tests, and a
failed Elixir 1.18/OTP 27 example compilation gate; it states beta.1 was
verified only on Elixir 1.20.3/OTP 29.0.5. These are project-reported limits,
not local test results. OTP process supervision does not qualify Kay kernel
isolation. Two tagged guides disagree on callback order: the
[Plugin lifecycle guide](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/plugin-contract-and-lifecycle.md)
places live admission after pure preparation, while the
[admission guide](https://github.com/agentjido/jido/blob/v3.0.0-beta.1/guides/admission-cancellation-and-timeouts.md)
says admission precedes it. Exact ordering requires code/test evidence before
copying it as a Kay contract. No Jido `.beam` reuse is proposed.

## Derived work

- [Native agent behavior framework](../20-notes/native-agent-behavior-framework.md).
- [Agent behavior inquiry](../40-inquiries/where-should-native-agent-behavior-live-in-kay-os.md).
