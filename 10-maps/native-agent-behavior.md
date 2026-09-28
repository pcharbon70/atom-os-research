---
title: "Native agent behavior"
kind: map
created: "2026-09-28"
tags: [agent-frameworks, ai-agents, system-architecture, workflows]
aliases: ["Agent behavior integration"]
---

# Native agent behavior

## Scope

This map follows the **behavior framework above safe delegation**: how a
non-LLM or LLM agent receives observations, selects an Action, commits state,
requests protected effects, and survives restart. The proposed placement is
a Layer 4 user-mode service with Layer 5 behavior definitions, using the
existing actor runtime and capability kernel. No Jido package or `.beam`
implementation is selected.

## Start here

- [Native agent behavior framework](../20-notes/native-agent-behavior-framework.md)
  — the Jido-wide component map, Kay subsystem ownership, model-neutral data
  contract, turn/effect protocol, and unexecuted infrastructure cases.
- [Placement and qualification inquiry](../40-inquiries/where-should-native-agent-behavior-live-in-kay-os.md)
  — open profile, storage, registry, provider, and evidence choices.
- [2026-09-28 deep dive](../50-journal/2026-09-28-native-agent-behavior-deep-dive.md)
  — exact source manifest, methods, limits, and archive verification.
- [Safe agent delegation](safe-agent-delegation.md) — the adopted authority
  envelope that every behavior implementation consumes.

## Trails

### Framework infrastructure without a package dependency

- [Jido v3](../30-sources/agentjido-2026-jido-v3-beta-1.md) separates
  definitions and instances, Plugin facets, AgentServer and named instance,
  persistence, input resources, scheduling, topology, children, and
  observation as well as Turns and Directives.
- [Jido Action v3](../30-sources/agentjido-2026-jido-action-v3-beta-11.md)
  supplies Actions, Instructions, Flow graphs, trusted stored-plan registries,
  in-memory execution, graph inspection, and telemetry.
- [Jido Signal v3](../30-sources/agentjido-2026-jido-signal-v3-beta-4.md)
  supplies event envelopes, type routing, Dispatch adapters, and a local Bus
  with at-least-once replay; Kay still needs protected origin and deduplication.
- [Behavior-first architecture](../30-sources/agentjido-2026-behavior-first-architecture.md)
  gives the project's rationale for contract-first OTP-like design.

The [component and service mapping](../20-notes/native-agent-behavior-framework.md#jido-v3-infrastructure-as-the-primary-reference)
shows how those package boundaries become Kay's definition registry, instance
directory, event fabric, executor, extension/input host, persistence,
topology controller, and observation interface. The pinned Jido core-scope
guide distinguishes these supported components from deferred cluster and
transport services.

### Decision models and system ownership

- [AgentSpeak communication semantics](../30-sources/vieira-et-al-2007-speech-act-agent-programming.md)
  supplies a non-LLM symbolic-agent route.
- [CoALA](../30-sources/sumers-et-al-2024-cognitive-architectures-language-agents.md)
  and [ReAct](../30-sources/yao-et-al-2023-react.md) separate memory,
  observation, decisions, and external action for LLM providers.
- [AIOS](../30-sources/mei-et-al-2025-aios.md) offers an agent-serving
  comparison on a host OS; its “kernel” is not Kay's privileged kernel.
- [Managed actor runtime](managed-actor-runtime.md), [system services](otp-like-system-services.md),
  and [applications](applications-and-domain-services.md) trace the proposed
  responsibility across Layers 3–5.

### Reliability and trustworthy effects

- [Temporal's dynamic agent article](../30-sources/egger-androulakis-2025-dynamic-ai-agents-temporal.md)
  distinguishes recorded nondeterministic decisions from replayable control.
- [Agent security systematization](../30-sources/zhang-et-al-2026-when-agent-becomes-kernel.md)
  reinforces deterministic mediation of proposed actions.
- [Safe delegation architecture](../20-notes/safe-agent-delegation-and-execution.md)
  and [assurance cases](../20-notes/agent-delegation-threat-model-and-assurance.md)
  supply the non-bypass, provenance, approval, budget, and revocation checks.

## Open questions

The [inquiry](../40-inquiries/where-should-native-agent-behavior-live-in-kay-os.md)
tracks the first deployment and whether a layer change ever becomes justified
by a genuinely new boundary. Proposed `NAB-*` cases and existing `AGT-*`
cases have not been run for this integration.
