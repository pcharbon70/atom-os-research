---
title: "Jido Signal 3.0.0-beta.4"
kind: source
created: "2026-09-28"
published: "2026-09-05"
citation_key: "agentjido2026jidosignalv3"
container: "Hex package and version-tagged project guides"
edition: "3.0.0-beta.4"
url: "https://hex.pm/packages/jido_signal/3.0.0-beta.4"
accessed: "2026-09-28"
tags: [agent-frameworks, elixir, event-delivery]
aliases: []
---

# Jido Signal 3.0.0-beta.4

## Reference

Agent Jido, [Jido Signal 3.0.0-beta.4](https://hex.pm/packages/jido_signal/3.0.0-beta.4),
published 5 September 2026. Read the version-tagged
[README](https://github.com/agentjido/jido_signal/blob/v3.0.0-beta.4/README.md),
[event bus](https://github.com/agentjido/jido_signal/blob/v3.0.0-beta.4/guides/event-bus.md),
[serialization](https://github.com/agentjido/jido_signal/blob/v3.0.0-beta.4/guides/serialization.md),
and [context extensions](https://github.com/agentjido/jido_signal/blob/v3.0.0-beta.4/guides/signal-extensions.md)
guides. The tagged [Router](https://github.com/agentjido/jido_signal/blob/v3.0.0-beta.4/guides/signal-router.md)
and [Dispatch](https://github.com/agentjido/jido_signal/blob/v3.0.0-beta.4/guides/signals-and-dispatch.md)
guides describe the rest of the package's delivery infrastructure.

## Research question or contribution

How can typed event envelopes and replay support agents without turning a
message or its metadata into an authority token?

## Method

The pinned README and guides were read for routing, serialization, cursor,
storage, and delivery claims. Jido v3's Hex metadata names beta.4 as its
required Signal dependency. The user's Signal bullet repeated the Action URL;
this record uses the actual Signal package.

## Findings

- Signals use a CloudEvents-style envelope with type, source, data, context,
  and optional typed schemas. The bus provides local ordered delivery and
  durable subscription cursors with stored-before-send, at-least-once replay.
- The included memory Store is bounded and process-local. A custom persistent
  Store is needed when records must survive a bus restart. Retry and broader
  delivery policy remain application-owned.
- Serialization supports canonical JSON and safe Erlang term reading for
  trusted Erlang systems. Context extensions are small transport metadata,
  not evidence that the named source was authenticated.

## Event infrastructure

| Component | Supported role and boundary |
| --- | --- |
| [Signal value and typed data](https://github.com/agentjido/jido_signal/blob/v3.0.0-beta.4/guides/signals-and-dispatch.md) | CloudEvents 1.0-style `id`, `type`, `source`, payload, time, and extensions; UUID7 IDs and optional static data schemas. An ID is message identity, not business idempotency or authorization. |
| [Serialization and context](https://github.com/agentjido/jido_signal/blob/v3.0.0-beta.4/guides/serialization.md) | Canonical map/JSON and Erlang-term profiles, with small extension and trace fields kept apart from domain payload. A claimed source is not an authenticated principal. |
| [Router](https://github.com/agentjido/jido_signal/blob/v3.0.0-beta.4/guides/signal-router.md) | Exact and wildcard type paths, priority, registration order, optional match predicate, and ordered targets. It performs lookup, not target execution or rights checks. |
| [Dispatch adapters](https://github.com/agentjido/jido_signal/blob/v3.0.0-beta.4/guides/signals-and-dispatch.md#dispatch-adapters) | PID, Phoenix PubSub, HTTP, logger, and custom delivery adapters are independent of the Bus. Built-in HTTP accepts trusted configuration; it lacks an untrusted-URL/SSRF boundary, retry loop, and durable outbox. |
| [Local Bus and Store](https://github.com/agentjido/jido_signal/blob/v3.0.0-beta.4/guides/event-bus.md) | Local ordered subscriptions, retained records and cursor replay, durable one-target cursor subscriptions with stored-before-send, acknowledgement, and at-least-once redelivery. The included bounded memory Store is not restart-durable; a custom persistent Store is needed. |

The Bus has no retry timer, negative acknowledgement, dead-letter queue,
lease, or competing-consumer policy. A durable cursor can pin retained records
until the bounded Store refuses publication. The package's v3 migration guide
also removes several v2 Bus features; they must not be assumed in a Kay
analogy. Kay needs its own admission, storage, backpressure, trust, and sink
contracts around these useful messaging patterns.

## Relevance

Kay can standardize a versioned event envelope and causal identifiers while
relying on its own protected endpoint identity, grant, and provenance checks.
Duplicate events and replay require stable operation IDs at effect sinks.

## Limits

This is a public beta with a changing v3 API. Its bus semantics do not imply
exactly-once external effects, trustworthy sender claims, or a cross-domain
security boundary. No Jido `.beam` package is an implementation dependency.

## Derived work

- [Native agent behavior framework](../20-notes/native-agent-behavior-framework.md).
