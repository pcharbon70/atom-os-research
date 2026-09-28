---
title: "Where should native agent behavior live in Kay OS?"
kind: inquiry
created: "2026-09-28"
status: open
tags: [agent-frameworks, ai-agents, system-architecture, workflows]
aliases: []
---

# Where should native agent behavior live in Kay OS?

## Why this matters

Once [safe delegation](../20-notes/safe-agent-delegation-and-execution.md)
is available, ordinary users and system services should be able to run
agents whose decisions come from rules, symbolic plans, models, or a mixture.
Without a common contract, each application would improvise event routing,
identity, effects, restart, and human control. An overprivileged shared host
would create a new deputy and bypass the very security model it consumes.

## Operational question

Can a Layer 4 agent service and Layer 5 behavior API support at least one
deterministic agent and one LLM agent through the same versioned contract,
while all effect and disclosure outcomes satisfy the selected [AGD
requirements](../20-notes/safe-agent-delegation-and-execution.md#required-contracts-and-ownership)
and [AGT cases](../20-notes/agent-delegation-threat-model-and-assurance.md#adversarial-case-registry)?
Does a separate architectural layer yield a measurable boundary or ownership
advantage that cannot be represented within the current five layers?

Evidence must include useful completion and cost, hostile-code attempts to
bypass protected brokers, duplicate delivery, crash/restart, revocation, and
multi-tenant/child accounting. The [native framework study](../20-notes/native-agent-behavior-framework.md)
proposes `NAB-01` through `NAB-09` as additional behavior and lifecycle
falsifiers. Those cases are specified but unrun.

## Working hypotheses

- The preferred placement is a **Layer 4 user-mode agent host service** plus
  **Layer 5 behavior definitions and SDK**. Layer 3 contributes actors, and
  Layer 2 enforces existing domain and resource primitives. This needs no
  sixth layer or agent reasoning syscall.
- The agent host can be untrusted for authorization if protected grant,
  context, inference, effect, approval, and audit brokers independently check
  its requests. The host's own durability and queue guarantees still require
  qualification.
- A model-neutral `decide` contract can admit finite-state, BDI, and LLM
  providers; provider-specific memory or context is an extension, not the
  security contract.
- An agent-authored Flow or Signal is data. Its schema and provenance can
  constrain processing, but neither supplies rights.

## Paths to explore

1. Select a first legitimate system task with a meaningful safe effect and a
   comparable non-agent baseline. Define its domain owner and human subject.
2. Specify versioned event, definition, task, instance, turn, decision,
   effect-intent, and outcome records. Test schema upgrade and old-checkpoint
   handling without reviving rights.
3. Decide whether the Layer 4 host keeps a durable turn journal itself or
   delegates to an existing persistence service. State the commit, outbox,
   idempotency, and indeterminate-result contract for each effect class.
4. Pin the trusted Action registry, update authority, code-loading route,
   resource ceilings, and domain split. Analyze compromise of each host,
   runtime, provider, and final sink.
5. Compare local versus cloud inference: disclosure, accounting, latency,
   cancellation, hidden state, and provider trust. Keep a no-model provider
   working throughout.
6. Run `NAB-*` behavior cases and applicable `AGT-*` security cases against a
   Kay build, then compare with a competently confined hosted service. Record
   raw sink observations and useful completion.

## Findings

The [2026-09-28 deep dive](../50-journal/2026-09-28-native-agent-behavior-deep-dive.md)
found that Jido v3's useful contribution is the distinction between
immutable Agent values, live OTP actors, typed events and actions, and
post-commit directives. Its own pinned guides assign authorization,
durability of general workflows, and external-effect recovery to the host.
AIOS provides hosted evidence for shared agent-serving services, while
CoALA, ReAct, and AgentSpeak expose multiple decision models. None shows
that Kay requires a sixth privilege or semantic layer.

The [proposed architecture](../20-notes/native-agent-behavior-framework.md)
places common lifecycle and API contracts in Layer 4, domain behavior in
Layer 5, and all protection in the already selected boundaries. This is a
reasoned placement, not implementation or qualification evidence.

## Outcome

Open. Choose the first profile, code and definition formats, storage owner,
trusted registry, and measurable usability/security thresholds before an
implementation milestone can claim an agent framework is integrated.
