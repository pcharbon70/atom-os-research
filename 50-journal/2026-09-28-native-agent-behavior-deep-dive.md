---
title: "2026-09-28 native agent behavior deep dive"
kind: journal
created: "2026-09-28"
tags: [agent-frameworks, ai-agents, research-session, system-architecture]
aliases: []
---

# 2026-09-28 native agent behavior deep dive

## Observations

The user asked how Kay OS could support agents as native OS workloads **after
safe delegation is implemented**, including LLM and non-LLM behavior, and
whether that requires another architectural layer. Jido v3, Jido Action v3,
and Jido Signal v3 were offered as inspiration, with an explicit instruction
not to use Jido's `.beam` implementation. This session produces a proposed
behavior contract and placement analysis, not a Kay implementation result.

The supplied Signal bullet accidentally repeated the Jido Action URL. Hex's
version metadata for Jido 3.0.0-beta.1 lists `jido_signal ~> 3.0.0-beta.4`;
the session therefore examined [Signal beta.4](https://hex.pm/packages/jido_signal/3.0.0-beta.4).
Hex API records confirmed Jido beta.1 was published 14 September 2026,
Action beta.11 on 13 September, and Signal beta.4 on 5 September. The
version-tagged Action README contains stale beta.10 prose/badge despite its
beta.11 install snippet, so release identity and prose were kept separate.

## Question and method

The operational question was whether a reusable, model-neutral agent
behavior service has an owner in the existing five layers while remaining
inside the adopted task authority and effect envelope. The comparison read
version-tagged primary package READMEs and guides for state/actor separation,
Actions/Flows, Signals, persistence, effects, security, and limits. It also
read primary scientific work on hosted agent OS services, language-agent
architecture, LLM action loops, symbolic agent communication, and current
agent security, plus official practitioner articles on behavioral contracts
and durable workflows.

Source claims were not treated as Kay test results. Jido's own documentation
says Actions may perform synchronous I/O before a turn commits, stored Flow
schemas do not authorize an operation, the core does not provide a universal
outbox/exactly-once external effect, and a Signal ID or Agent Ref is not a
credential. Those limits drive Kay's separate protected ingress, broker,
and sink checks. AIOS's evaluated service layer ran on Ubuntu rather than
as a bare-metal agent kernel. CoALA and ReAct concern cognitive organization
and LLM task behavior; AgentSpeak shows the non-LLM design space. The Temporal
article explains recording nondeterministic choices for replay but does not
make external services transactional.

## Environment

- Archive: `/home/ducky/code/atom-os-research`, starting HEAD
  `31729f6c698a52265d1ce7fb8bf48dff4aff37d3` on 28 September 2026.
- Local timezone: America/Toronto; documentation checker: Python 3.12.12.
- Primary package evidence: public Hex release metadata and tagged GitHub
  READMEs/guides for the three exact beta versions, read as text. No Jido
  package, `.beam` file, model, Kay image, QEMU fixture, or agent behavior
  workload was installed or executed.
- Pre-existing worktree edits in the PoC map, privilege-transition research,
  and M1/M2 phased plans were outside this session and preserved. They are
  not evidence for agent integration and no planning gates were changed.

## Evidence and resulting model

The [synthesis](../20-notes/native-agent-behavior-framework.md) recommends a
Layer 4 agent host and API, Layer 5 behavior definitions, Layer 3 actor
execution, and existing Layer 2/1 protection. It makes agent state,
incarnation, task, event, action, and effect identities explicit, and keeps
every requested operation inside the [safe delegation
envelope](../20-notes/safe-agent-delegation-and-execution.md). A separate
privileged or sixth layer has no supported boundary advantage at present.

The [inquiry](../40-inquiries/where-should-native-agent-behavior-live-in-kay-os.md)
remains open on storage, action registry custody, provider mix, isolation,
deployment and test thresholds. `NAB-01`–`NAB-16` are proposed behavior,
infrastructure, and lifecycle qualification cases. The prior `AGT-*`
security cases are still
unexecuted; the assumption in the user's question does not provide evidence
that they passed. The [topic map](../10-maps/native-agent-behavior.md)
routes readers through the design and evidence.

## Follow-up component audit

The first synthesis overemphasized the trust boundary and Agent Turn loop.
After the user pointed out that most of Jido's infrastructure was missing,
this session inventoried the tagged primary documentation for all three
packages. It retrieved 141 README, guide, and Jido design files at the exact
release tags, then read the supported-release guides for authoring, Plugins,
AgentServer and instance lifecycle, Signals, Actions/Flows, persistence,
input resources, scheduling, topology, child ownership, extension boundaries,
and observability. The Jido design index identifies its design documents as
proposals where they differ from the implementation. No package code or
compiled `.beam` artifact was installed or executed.

The expanded [Jido core](../30-sources/agentjido-2026-jido-v3-beta-1.md),
[Action](../30-sources/agentjido-2026-jido-action-v3-beta-11.md), and
[Signal](../30-sources/agentjido-2026-jido-signal-v3-beta-4.md) source notes
now inventory the framework components. The synthesis maps them to a
multi-service Layer 4 framework subsystem, Layer 5 definitions and Actions,
Layer 3 actor execution, and separately protected effect services. It extends
the proposed framework case registry to `NAB-01`–`NAB-16`; all remain unrun.

## Verification

`python3 validate_archive.py` passed with 1044 completed documents, 99
directories, 10897 local links, 406 source notes, and 31 deep-dive manifests.
All 40 version-tagged Jido README/guide URLs cited by the three package
source notes returned HTTP 200 when checked against the publisher's tagged
GitHub content. The 141 downloaded primary documents were an inventory and
reading aid, not installed dependencies or Kay execution evidence.
`git diff --check` passed. The nine pre-existing PoC and phased-plan files
matched their starting content hashes after the research edit. No Kay agent
runtime, model, effect broker, or adversarial case was executed.

## Source manifest

### Newly introduced sources

- [Jido v3 beta.1](../30-sources/agentjido-2026-jido-v3-beta-1.md) — full core infrastructure, owner boundaries, supported versus deferred scope, and beta limits.
- [Jido Action v3 beta.11](../30-sources/agentjido-2026-jido-action-v3-beta-11.md) — Action, Flow, Exec, inspection, stored registry, and host security duties.
- [Jido Signal v3 beta.4](../30-sources/agentjido-2026-jido-signal-v3-beta-4.md) — envelope, Router, Dispatch, Bus, cursor replay, and trust limits.
- [Jido behavior-first article](../30-sources/agentjido-2026-behavior-first-architecture.md) — practitioner rationale for behavior contracts above OTP actors.
- [AIOS](../30-sources/mei-et-al-2025-aios.md) — hosted agent service decomposition and resource evaluation boundary.
- [CoALA](../30-sources/sumers-et-al-2024-cognitive-architectures-language-agents.md) — LLM memory, action, and decision-loop taxonomy.
- [ReAct](../30-sources/yao-et-al-2023-react.md) — optional LLM reasoning/action provider and its benchmark limits.
- [AgentSpeak communication semantics](../30-sources/vieira-et-al-2007-speech-act-agent-programming.md) — non-LLM symbolic-agent decision and message semantics.
- [Temporal dynamic agents article](../30-sources/egger-androulakis-2025-dynamic-ai-agents-temporal.md) — practitioner replay pattern for recorded model decisions.
- [Agent security systematization](../30-sources/zhang-et-al-2026-when-agent-becomes-kernel.md) — deterministic mediator versus semantic judgment.

### Reused sources

- [AgentKernel](../30-sources/zou-et-al-2026-agentkernel.md) — existing lifecycle and mediation architecture comparison.
- [CaMeL](../30-sources/debenedetti-et-al-2025-camel.md) — existing data-flow and interpreter boundary comparison.
- [AgentDojo](../30-sources/debenedetti-et-al-2024-agentdojo.md) — existing paired task-utility and attack-outcome method.

## Threads

Decide the first protected agent deployment profile and domain task before
planning implementation. A hosted prototype can compare interfaces and
recovery but cannot establish Kay kernel containment. Verify that the chosen
compiled-BEAM profile and process-local GC remain compatible with an agent
host; no Jido `.beam` adaptation is required by this research.

## Follow-ups

Select a legitimate deterministic first workload, pin the event/behavior
schema, create a reference state machine for turn/effect admission, and then
qualify model-neutral and LLM providers under the same installed grant. Keep
implementation tasks, milestones, and measured evidence in their normal
planning and journal roles when those decisions become concrete.
