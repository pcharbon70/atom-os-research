---
title: "Native agent behavior framework for Kay OS"
kind: note
created: "2026-09-28"
maturity: developing
tags: [agent-frameworks, ai-agents, capabilities, system-architecture, workflows]
aliases: ["Kay OS agent behavior integration"]
---

# Native agent behavior framework for Kay OS

## Question and status

Assuming Kay has implemented and qualified its [safe agent delegation and
execution](safe-agent-delegation-and-execution.md) profile, where should a
reusable, OS-native **agent behavior** framework live? It should admit an
LLM-driven agent, a rule-based or BDI agent, and a fixed workflow through the
same task, event, action, and effect boundaries. The operator should be able
to run agents as ordinary system-supported workloads without conferring
kernel privilege or using Jido's `.beam` packages.

**Recommendation:** provide a framework-neutral agent service and API in
**Layer 4 (OTP-like system services)**. Define agent behaviors, goals, plans,
decision providers, and domain results in **Layer 5 (applications and domain
services)**. Reuse Layer 3's BEAM-compatible actors and supervision, and
Layers 1–2's existing isolation and capability mechanisms. This is a named
cross-layer feature, **not a sixth architectural layer**. The framework
service itself is user-mode software. Its queue and state correctness matter
for recovery, while the protected grant issuer and effect brokers remain the
authority trust base. Agents and their decision engines remain untrusted for
authorization.

This is a **research proposal**, not an implemented component, a completed
security qualification, or an addition to the existing CLI-first PoC gates.
The user's counterfactual assumption lets us design the next integration
level; it does not turn the unexecuted [AGT qualification
cases](agent-delegation-threat-model-and-assurance.md) into evidence.

## Terminology and operational standard

An **agent** here is a persistent or transient workload with explicit state,
which consumes observations, selects a next step under a goal or policy, and
may propose further actions. The decision procedure can be deterministic,
symbolic, learned, LLM-based, or a composition. A simple actor or fixed
workflow can use the same API without being called an intelligent agent.
**Behavior identity** names a versioned definition; **instance identity**
names its logical running state; **incarnation** names one activation after
start or restart; **task identity** names the human or standing-authority
delegation; **actor identity** names the executing process or domain. None
implies another's authority.

Operational success requires: (1) useful non-LLM and LLM behavior behind one
contract; (2) every observation, memory read/write, inference call, child
start, and external effect constrained by the installed task profile;
(3) honest outcomes after restart, replay, revocation, and uncertain remote
effects; (4) resource and stop control that remains available under hostile
agent load; and (5) measured utility and cost relative to a well-confined
hosted implementation. Passing model behavior benchmarks alone cannot meet
this standard.

## Research basis and cross-source interpretation

| Work | Demonstrated or documented contribution | Kay interpretation and limit |
| --- | --- | --- |
| [Jido v3](../30-sources/agentjido-2026-jido-v3-beta-1.md) | Immutable Agent value, live OTP Agent Server, explicit turn/commit/directive stages; beta documents external effect and durability gaps | Copy the separation of state, actor, and proposed effect as a concept; do not reuse packages or infer kernel confinement |
| [Jido Action v3](../30-sources/agentjido-2026-jido-action-v3-beta-11.md) | Validated Actions, declarative Flow, trusted registry for stored plans, in-memory Exec | Use allowlisted declarative plan data; schema validity cannot grant authority; Kay owns durable execution |
| [Jido Signal v3](../30-sources/agentjido-2026-jido-signal-v3-beta-4.md) | Typed event envelope, local ordering, durable cursor and at-least-once replay | Define a versioned OS event profile; bind origin at protected ingress; do not infer rights from fields |
| [Jido's behavior-first article](../30-sources/agentjido-2026-behavior-first-architecture.md) | Reusable behavioral contracts above OTP processes | Adopt framework-neutral roles, with Kay's security meaning defined separately |
| [AgentSpeak communication semantics](../30-sources/vieira-et-al-2007-speech-act-agent-programming.md) | Explicit message and decision transitions for symbolic agents | Non-LLM decision procedures deserve first-class support; a claimed performative is not a grant |
| [CoALA](../30-sources/sumers-et-al-2024-cognitive-architectures-language-agents.md) and [ReAct](../30-sources/yao-et-al-2023-react.md) | Distinct memory, decision, and action functions; one LLM thought/action/observation loop | LLMs are optional decision providers; generated steps remain proposals |
| [AIOS](../30-sources/mei-et-al-2025-aios.md) | Common agent-serving scheduler, context, model, tool, and SDK abstractions with hosted throughput results | Shared inference is promising; AIOS's “kernel” runs over Ubuntu and does not establish Kay privilege isolation |
| [Temporal practitioner account](../30-sources/egger-androulakis-2025-dynamic-ai-agents-temporal.md) | Durable orchestration can replay recorded nondeterministic choices | Record decisions before replay; external effects still need independent ID, sink state, and reconciliation |
| [Current security systematization](../30-sources/zhang-et-al-2026-when-agent-becomes-kernel.md) | Separates deterministic provenance checks from uncertain semantic judgment | Keep model output outside the trusted mediator and report semantic residual risk |

The earlier [AgentKernel](../30-sources/zou-et-al-2026-agentkernel.md),
[CaMeL](../30-sources/debenedetti-et-al-2025-camel.md), and
[AgentDojo](../30-sources/debenedetti-et-al-2024-agentdojo.md) research remains
the relevant security, flow, and utility baseline. Those studies do not
qualify the proposed Kay implementation either.

## Layer placement decision

| Placement | Benefit | Cost or boundary problem | Decision |
| --- | --- | --- | --- |
| Layer 2 kernel | Uniform admission primitive | Enlarges privileged code with semantic state, model policy, storage, and rapid framework evolution | Reject; use existing domains, capabilities, IPC, budgets, and revocation |
| Layer 3 managed runtime | Cheap actors, BEAM scheduling and collection | Coupling agent protocol to BEAM execution and confusing actor identity with task authority; runtime compromise crosses co-hosted trust | Reuse actor mechanism, keep framework policy above it |
| Layer 4 system services | Common task admission, host lifecycle, queues, durable turn records, provider routing, and broker integration | A host with effect credentials would become a dangerous deputy | Preferred framework service; split untrusted host from protected issuer/sinks |
| Layer 5 application library only | Domain-owned goals and fast experimentation | Each application would rebuild lifecycle, replay, queue, and shared provider controls | Keep behavior definitions and SDK here, use Layer 4's common service |
| New sixth layer | Highlights agents in diagrams | Duplicates Layer 4 policy and Layer 5 domain meaning without a distinct privilege or execution contract | Do not add now; revisit only if an independently verifiable boundary cannot fit existing owners |

The five layers describe ownership and trust boundaries, not product feature
categories. “Agent-native” means an OS-supported contract and service. It
does not mean an LLM governs scheduling, capability derivation, memory
mapping, or recovery. A deterministic system service may itself be written
using the agent behavior API, but essential boot, grant issuance, revocation,
fault containment, and stop paths cannot depend on a model or an
unrecovered agent host.

### Ownership map

| Owner | New responsibility | Retained boundary |
| --- | --- | --- |
| Layer 1 hardware support | None specific to agent semantics | Platform privilege, time, device and memory mechanisms |
| Layer 2 Kay kernel | Apply existing domain, handle, IPC, time, resource, and revocation controls to agent domains | Never parse prompts, goals, Flow data, or Signal meaning |
| Layer 3 managed actor runtime | Schedule agent host/behavior actors; preserve BEAM and process-local tracing GC; report crash and runtime work | PID, mailbox, links, and supervision are not grants or hardware isolation |
| Layer 4 agent host service | Registry of versioned behavior definitions, instance activation, bounded event admission, serialized turns, checkpoint/outbox coordination, supervision, provider interface, observability | No ambient effect or credential authority; security brokers independently check requests |
| Layer 4 protected services | Authenticate origin, issue task grants, label context, broker inference/tools/credentials, reserve effects, fence revocation, retain audit | Explicit, separately protected TCB with bounded held authority |
| Layer 5 domains | Define goals, Action schemas, admissible effects, plans, invariants, success criteria, human-facing previews, and recovery meaning | Domain correctness and approved publication stay application concerns |

An agent host serving mutually distrustful tasks must not share their
secrets, writable memory, or authority simply because it shares an API. If
the selected threat profile includes runtime compromise, tasks and protecting
brokers need separate kernel protection domains. Shared inference, parsing,
and native model libraries create declared confidentiality and integrity
dependencies; a provider call is a data-disclosure effect. The chosen
deployment must name every such trust assumption.

## Proposed model-neutral behavior contract

Kay should define a small versioned data protocol, independent of Elixir,
Jido, one model API, and BEAM bytecode details:

```text
Behavior manifest: definition_id + version + input/state schemas
                 + decision-provider kind + action registry references
                 + maximum requested tool/observation profile
                 + declared resource and recovery policy

Turn input:       authenticated ingress reference + task_id + instance_id
                 + incarnation + turn_id + typed observation references
Turn proposal:    candidate state + proposed action/child/inference requests
                 + causal references + completion claim
Turn outcome:     accepted state revision + effect operation IDs
                 + per-effect admitted/completed/denied/indeterminate status
```

The manifest is checked by its owning application and the service installer;
its declared maximum only **reduces** rights a protected issuer might grant.
Signing a manifest can establish authorship, not safe behavior. The trusted
issuer binds a task grant to a selected version and domain, and a protected
sink checks the current grant and exact effect at final admission. Neither a
Signal's `source` field nor a model's assertion about its goals is sufficient.

Each behavior implementation supplies `initial_state`,
`decide(observations, state, limits) -> candidate_state + proposals`, and
`restore(checkpoint, current_task_context)`. A rule engine, BDI interpreter,
finite state machine, and LLM planner can all implement `decide`; the API
does not privilege one. Observations and remembered text carry origin,
classification, and policy references. A proposal is inert data until the
relevant protected service admits it. The service host records revisions and
outcomes; an agent-controlled completion claim cannot certify an external
effect.

### Turn, effect, and replay semantics

1. A protected ingress authenticates the transport and associates a task,
   instance incarnation, label set, and bounded event record. An event's
   untrusted payload may still contain hostile instructions.
2. The host serializes a turn for that instance and loads a checkpoint under
   **current** grant, label, definition-version, and epoch policy. A stale
   checkpoint cannot restore a revoked right.
3. The decision provider computes a candidate and proposed operations inside
   its protection domain and resource budget. Any synchronous read, model
   call, or network request made during decision is already an external or
   disclosure operation and must use a protected broker; the framework cannot
   assume Action code is pure merely because its output is validated.
4. Before live state advances, the host durably records the chosen decision,
   candidate revision, and pending effect intents or records that durability
   was not requested. If a required write fails, no new turn is reported as
   committed. This is an internal atomicity target, not atomicity with an
   external service.
5. An effect broker independently checks object/version/arguments,
   destination, data labels, approval digest, budget, and revocation fence at
   the final admission point. It reserves audit and an operation ID before
   dispatch. A rejected proposal is an explicit outcome, not a silent retry.
6. On restart, replay restores the recorded decision; it does not ask an LLM
   to invent the past again. Pending effects are queried or reconciled by
   operation ID before a retry. Where a sink lacks deduplication or query,
   completion is indeterminate and the system cannot promise exactly once.

The host should expose `proposed`, `state_committed`, `effect_admitted`,
`effect_completed`, `denied`, `cancelled`, and `indeterminate` separately.
Cancellation of a turn cannot roll back a committed state or a remote effect.
The stop path remains outside the agent's mailbox and available with reserved
resources. At-least-once events use stable event and operation IDs; sender
ordering alone does not prevent duplicate effects. The event log and
checkpoint are data with retention, access, and provenance rules, not a way
to launder old messages into commands.

### Plans, plugins, and distribution

A stored or agent-authored plan is versioned declarative data. It names only
installed, reviewed Action descriptors in a trusted registry. Parsing cannot
create code, load an arbitrary module, or widen the task's tool profile.
Registration, update, or fallback changes require the same issuer/sink
constraints as direct calls. Generated native code runs in an explicitly
confined domain when permitted; a Flow graph does not grant it the host's
capabilities. Exact effect arguments are checked at the sink after all
expansion, redirects, and parameter substitution.

Child agents are new instances linked to the parent's task and shared
aggregate budget. Their grant is an attenuation and has its own incarnation.
Remote agents are peers with independently held authority: Kay can mediate
its local release and requests but cannot inspect or control a remote model's
hidden state or external credentials. Cross-node messages require
authenticated endpoints, bounded transport, replay controls, and explicit
fencing; local registry membership does not establish global ownership.

## Conformance and evidence still needed

The [AGT case families](agent-delegation-threat-model-and-assurance.md) remain
mandatory for any claimed safe delegation profile. The additional framework
questions below exercise **behavior interoperability and lifecycle**. They
are proposed cases, not executed tests or new PoC gates.

| Case | Required observation |
| --- | --- |
| NAB-01 model neutrality | A finite-state or BDI agent and an LLM agent use the same versioned task, event, proposal, and outcome interface; each completes a legitimate task |
| NAB-02 schema versus rights | A well-typed but unauthorized Action fails at the protected sink; a permitted action succeeds |
| NAB-03 pre-commit work | A crash after an Action's synchronous broker request but before state commit retains the actual effect status and does not imply rollback |
| NAB-04 duplicate/replay | Duplicate Signals, restart, and replay do not silently repeat a protected effect; unsupported remote idempotency is reported indeterminate |
| NAB-05 plan mutation | Stored/generated plan data cannot load new code, choose an unregistered Action, or expand a grant |
| NAB-06 identity and child | PID reuse, restarts, parent exit, child spawn, and remote retry preserve task/instance/incarnation distinctions and aggregate quotas |
| NAB-07 revocation/stop | Revoke during a queued turn or model call; final sink rejects later admission, and independent stop remains responsive |
| NAB-08 provenance | A retrieved Signal or memory summary cannot supply a grant or trusted human approval; labels survive save/restore |
| NAB-09 useful service | Compare legitimate completion, false denial, approval burden, latency, inference cost, and resource overhead to a competently confined hosted agent service |

The first useful prototype **after** the assumed delegation substrate exists
should run a deterministic non-LLM agent that watches a typed system event,
produces a preview or draft, and requests one bounded effect. This tests the
OS behavior contract without hiding protocol faults behind model
variability. Add an LLM decision provider through the same interface, then a
child and a durable restart case. Before claiming protection, run the
applicable AGT cases against hostile native code and every reachable effect
path as well as the NAB interoperability cases. Pin the Kay build, BEAM/OTP
profile, model/provider, grants, host comparison, fixtures, budgets, and raw
sink observations. None of these trials has been performed in this session.

## Alternatives and unresolved decisions

The feature could be an application library with no shared Layer 4 host; that
would simplify early prototyping but duplicate admission, replay, inference
routing, and observation APIs. A monolithic host with its own credentials
would centralize them and enlarge the impact of a host compromise. A separate
sixth layer would give the feature visual prominence but currently adds no
distinct protection or semantic owner. These alternatives should be revisited
only if measured deployment, compatibility, or failure evidence changes the
boundary analysis.

The open [agent behavior inquiry](../40-inquiries/where-should-native-agent-behavior-live-in-kay-os.md)
tracks the first definition/serialization format, trusted registry custody,
durability backend, provider mix, per-tenant isolation, distributed ownership,
and user-facing control profile. The existing [safe delegation
inquiry](../40-inquiries/how-can-kay-os-safely-delegate-work-to-agents.md)
continues to own the security profile. This proposal selects neither Jido's
implementation nor a model, inference vendor, or agent language.

## Connections

- [Safe agent delegation and execution](safe-agent-delegation-and-execution.md)
  — fixed authority and effect boundaries into which this service fits.
- [Managed actor runtime](managed-actor-runtime-layer.md) and
  [OTP-like system services](otp-like-system-services-layer.md) — actor
  mechanism and reusable service ownership.
- [Applications and domain services](applications-and-domain-services-layer.md)
  — goals, invariants, meaningful outcomes, and publication gates.
- [Agent behavior map](../10-maps/native-agent-behavior.md) and
  [research session](../50-journal/2026-09-28-native-agent-behavior-deep-dive.md)
  — curated route and exact source provenance.

## Sources

The [research basis](#research-basis-and-cross-source-interpretation) links
each substantively used primary work and separates its claims from Kay's
proposed contracts. The [deep-dive journal](../50-journal/2026-09-28-native-agent-behavior-deep-dive.md)
is the authoritative session source manifest.
