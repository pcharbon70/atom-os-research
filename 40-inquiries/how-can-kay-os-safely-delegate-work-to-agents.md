---
title: "How can Kay OS safely delegate work to agents?"
kind: inquiry
created: "2026-09-26"
status: open
tags: [ai-agents, capabilities, information-flow, security, usability]
aliases: ["Safe agent delegation inquiry"]
---

# How can Kay OS safely delegate work to agents?

## Why this matters

Humans may use agents to operate Kay OS and its applications. On 2026-09-26
the user directed the architecture to support useful delegation whose limits
survive compromised agents and tools. The [adopted architecture](../20-notes/safe-agent-delegation-and-execution.md)
connects that requirement to existing capabilities, protected services,
explicit effects, and human control. Its implementation remains unqualified.

## Operational question

Can a pinned deployment complete representative human tasks with bounded,
understandable grants while a malicious agent, child, native tool, or poisoned
memory cannot exceed the granted effect and disclosure envelope?

The answer requires both independently observed containment and useful task
completion. Denying every operation, trusting an agent's success statement,
or reproducing a model benchmark does not establish this system property.
The [assurance study](../20-notes/agent-delegation-threat-model-and-assurance.md)
defines the `AGT-*` adversarial registry and its `AGD-*` requirement mapping.

## Working hypotheses

- Native capability and broker boundaries can make agent confinement the
  ordinary execution path, including generated code and subprocesses.
- A human can understand and grant a bounded task once, with additional
  decisions reserved for genuine authority expansion and selected effects.
- Conservative domain/context provenance can provide a defensible initial
  flow profile; finer dependency tracking may improve utility after separate
  qualification.
- Separate protection domains can bound compromised runtimes while retaining
  cheap BEAM actors inside each admitted trust domain.
- A well-configured hosted baseline can provide many of the same guarantees;
  Kay's proposed integration advantage requires comparative evidence.

These hypotheses are provisional. The architectural requirement is adopted;
the most usable mechanisms and cost/assurance trade-offs remain open.

## Paths to explore

| Open decision | Evidence required before selection | Current state |
| --- | --- | --- |
| First deployment and tools | Concrete useful workflows, explicit reachable-interface inventory, threat assumptions | Unselected; no agent implementation profile authorized by this document |
| Typed task and grant semantics | Executable admission/delegation model, canonicalization and confused-deputy tests | Proposed logical bindings; ABI and service schema open |
| Memory and inference flow profile | Conservative tracking baseline, hidden-state/cross-session tests, measured utility loss | Required policy behavior recorded; tracker/runtime not selected |
| Provider and remote-tool support | Exclusive credential custody, disclosure scopes, remote completion and retention assumptions | Per-provider qualification pending |
| Trusted CLI and later assistive paths | Authentic input/output design, automation separation, comprehension and fatigue studies | Existing broker proposal reused; no tested ceremony |
| Revocation and disconnected operation | Sink fence and in-flight model; explicit maximum stale authority and exposure bounds | Immediate local admission closure required; offline profile unselected |
| Resource and spending bounds | Aggregate reservations, concurrency/retry proof, enforceable provider cost ceilings | Kernel budgets distinguished from service and monetary accounting |
| Release and competitive claim | Predeclared workloads/thresholds, equivalent hosted baseline, retained adversarial evidence | No measured security, usability, or performance result |

A selected implementation needs responsible owners for the profile, policy,
resource sinks, and evidence. Those assignments and acceptance thresholds
remain explicit decisions; a research note cannot invent them. Existing PoC
milestones keep their current scope and evidence status.

## Findings

The [research session](../50-journal/2026-09-26-safe-agent-delegation-deep-dive.md)
introduced the missing agent papers and current confinement documentation,
then connected them with existing capability and secure-interaction research.
The [topic map](../10-maps/safe-agent-delegation.md) supplies the reading route.

The resulting design distinguishes resource authority, permitted information
flows, and semantic correctness. It rejects self-authorized model decisions,
untracked ambient credentials, automatic trust promotion of remembered text,
and revocation claims based only on matching expiry times. No native or hosted
agent experiment was performed in this session.

## Outcome

Open. Resolve only for a named deployment profile after the mapped adversarial
cases, useful-work controls, trust assumptions, and human-control evaluation
have reproducible evidence. Broader profiles remain open independently;
writing the architecture or passing archive validation does not resolve them.
