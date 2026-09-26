---
title: "Safe agent delegation and execution"
kind: note
created: "2026-09-26"
maturity: developing
tags:
  - ai-agents
  - capabilities
  - information-flow
  - security
  - system-architecture
aliases:
  - "Kay OS agent security architecture"
---

# Safe agent delegation and execution

Kay OS adopts **safe delegation of work to potentially compromised AI agents**
as a full-system architectural requirement, by user direction on 2026-09-26.
Humans must be able to grant useful, understandable task authority whose
limits survive malicious model output, tools, retrieved content, and child
agents. Enforcement belongs to the existing capability kernel and separately
protected system services. Models, their prompts, and agent orchestration
remain unprivileged.

This is an adopted design requirement with proposed mechanisms and unexecuted
qualification cases. It is not a claim of implemented containment, formal
verification, or competitive superiority. It adds no sixth architectural
layer and selects no model, inference vendor, global identity registry, or
agent framework. The existing CLI-first PoC, Zig/x86-64 target, compiled-BEAM
profile, and process-local tracing-GC obligations retain their acceptance
meaning. This research does not add agent execution to those delivery gates;
future implementation decomposition must explicitly trace the requirements
below when an agent profile is selected.

## Question and operational standard

Can a human delegate a useful task while every locally mediated effect stays
inside the authorized object, operation, destination, time, and resource
envelope even when the entire agent workload is hostile?

An **agent** is a workload that uses model output to choose actions. A
**task contract** is a protected record of permitted work; prose expressing a
goal is not itself an executable permission. **Authority containment** limits
effects. **Information-flow enforcement** limits where protected data can
travel. **Semantic correctness** concerns whether the work is true, useful,
or faithful to human intent. These are separate claims with different tests.

The [threat model and assurance study](agent-delegation-threat-model-and-assurance.md)
defines falsifiers, observable outcomes, comparison methods, and evidence
requirements. The [open inquiry](../40-inquiries/how-can-kay-os-safely-delegate-work-to-agents.md)
tracks unresolved policy, provenance, provider, and usability choices.

## Research basis and interpretation

The following evidence informs the design; the contracts that follow are Kay
OS synthesis, not guarantees transferred from these works.

| Evidence | What it contributes | Boundary on the conclusion |
| --- | --- | --- |
| [AgentKernel](../30-sources/zou-et-al-2026-agentkernel.md) | An integrated identity, input, memory, and action mediation proposal | Architectural argument; empirical and formal validation remain pending |
| [CaMeL](../30-sources/debenedetti-et-al-2025-camel.md) | A prototype coupling controlled execution with data-flow policy | Restricted threat model and interpreter; no Kay kernel assurance |
| [Indirect prompt injection](../30-sources/greshake-et-al-2023-indirect-prompt-injection.md) | Concrete hostile-content paths into agent behavior | Qualitative demonstrations, not deployment prevalence |
| [AgentDojo](../30-sources/debenedetti-et-al-2024-agentdojo.md) | Separate task-utility and attacker-success evaluation | Benchmark environment does not qualify native OS containment |
| [Landlock](../30-sources/linux-kernel-2026-landlock.md) | Existing kernel enforcement against ambient resource access | Host-specific resource coverage; no interpretation of human goals |

[Saltzer and Schroeder](../30-sources/saltzer-schroeder-1975-protection-information.md),
[the confused deputy](../30-sources/hardy-1988-confused-deputy.md), and
[capability analysis](../30-sources/miller-et-al-2003-capability-myths.md)
ground complete mediation and explicit authority. [Yee](../30-sources/yee-2002-user-interaction-design-secure-systems.md)
connects authority to understandable human action. [Macaroons](../30-sources/birgisson-et-al-2014-macaroons.md)
inform restricted delegation without selecting a Kay credential format.
[seL4 information-flow work](../30-sources/murray-et-al-2013-sel4-information-flow.md)
illustrates why an assurance claim must state its configuration and excluded
channels.

Established operating systems can constrain agent processes. Kay's proposed
advantage is coherent default delegation across its services, with usable
human control and verifiable absence of bypasses. A fresh design also incurs
compatibility, implementation, and assurance costs. Comparative benefit must
be measured against a competently confined hosted system.

## Required contracts and ownership

These stable IDs identify architecture requirements, not implementation tasks
or passing tests. The linked assurance document owns the `AGT-*` cases.

| ID | Required property | Existing owner | Qualification cases |
| --- | --- | --- | --- |
| AGD-01 | Distinguish originating subject, current actor, task, workload generation, and grant | Identity/session services and grant issuer | AGT-01, AGT-04 |
| AGD-02 | Contain compromised agents, native tools, and runtimes within declared protection domains | Kernel domains; runtime native boundary | AGT-02, AGT-14 |
| AGD-03 | Mediate every protected effect and prohibit ambient bypass routes | Kernel plus storage, network, tool, and device brokers | AGT-02, AGT-03, AGT-14 |
| AGD-04 | Bind authority to exact operations, objects, versions, parameters, and destinations | Grant issuer and final effect sink | AGT-03, AGT-09 |
| AGD-05 | Attenuate delegation and conserve aggregate task resources | Grant issuer, admission/accounting, kernel budgets | AGT-04, AGT-11 |
| AGD-06 | Preserve protected provenance and conservative flow restrictions across memory and inference | Context/memory services and qualified flow tracker | AGT-05, AGT-06 |
| AGD-07 | Authorize model/provider disclosure and external effects independently of local read permission | Network, inference, secret, and federation brokers | AGT-07, AGT-14 |
| AGD-08 | Bind human approval to its actual scope and preserve independent stop/control paths | Trusted-interaction broker and operator services | AGT-08, AGT-11 |
| AGD-09 | Fence revoked and stale authority through descendants, queues, restart, and sinks | Kernel revocation plus service epochs | AGT-04, AGT-09, AGT-10 |
| AGD-10 | Distinguish planned, admitted, completed, and indeterminate effects with protected evidence | Resource services, audit, reconciliation | AGT-10, AGT-12 |
| AGD-11 | Keep deterministic authority ceilings independent of model classification | Policy/issuance services within kernel-held envelopes | AGT-01, AGT-13 |
| AGD-12 | Declare profile coverage, residual trust, usability, and evidence before a security claim | Release/profile owners and assurance tooling | All AGT cases, profile-specific coverage |

### Placement across the five layers

| Layer | Agent-related responsibility | Excluded interpretation |
| --- | --- | --- |
| 1: Hardware/architecture support | Supply existing privilege, memory, DMA, device, and input-routing mechanisms under the qualified platform profile | CPU mode or a TEE does not identify a trustworthy instruction |
| 2: Minimal kernel | Enforce protected domains, typed handles, bounded IPC, derivation, resource accounts, revocation, and completion boundaries | No LLM, prompt parser, semantic firewall, or agent-specific reasoning syscall |
| 3: Managed runtime | Preserve explicit handles and subject/actor context; isolate native boundaries and account for actor work | A BEAM PID or supervision tree is not a hardware security boundary |
| 4: System services | Own task admission, identity, policy, grants, context/memory, inference/tool brokering, trusted interaction, and audit | Running in user mode does not remove these services from the relevant trust base |
| 5: Applications | Define goals, domain invariants, proposed plans, staged work, and publication semantics | An agent-generated plan, manifest, or success statement cannot authorize its own effects |

This extends the existing [security architecture](authentication-and-authorization-across-the-five-layer-architecture.md).
An agent may contain many BEAM actors. Under a runtime-compromise threat,
mutually distrustful agents and security brokers require separate kernel
protection domains. Sharing a runtime or inference service explicitly adds
that runtime/service to the confidentiality and integrity trust base. Native
tools and unsafe extensions receive their own confined domains where that
profile promises native-compromise containment. Tracing GC remains outside
the kernel and does not erase data already disclosed to another domain.

## Task admission and authority

The existing [grant issuer](authentication-and-authorization-components/grant-compiler-and-issuer.md)
compiles typed policy decisions into bounded authority. Agent support adds a
task binding and lifecycle, not a parallel authorization engine. Conceptually:

```text
effective authority = human or standing-task grant
                    ∩ operator policy
                    ∩ issuer's held parent capability
                    ∩ approved tool/service profile
                    ∩ current data-flow restrictions
                    ∩ current epochs, lifetime, and available budget
```

Each term can constrain authority. An unsigned or merely self-declared tool
manifest supplies no rights; approval selects a profile whose implementation
must be confined and tested. A signed artifact establishes provenance under
its verifier's assumptions, not trustworthy behavior. A task may use several
separately authorized grants; the resulting composition must be explicitly
reviewed rather than silently pooling permissions across unrelated tasks.

The proposed logical task record binds:

- task ID and generation, originating subject, current actor/workload
  incarnation, issuer, and bounded delegation lineage;
- object identities and generations, permitted actions, parameter bounds,
  effect audiences, expected versions, and approved tool/profile revisions;
- allowed source classes, disclosure destinations, persistent-memory scope,
  and required provenance/flow profile;
- lifetime, delegation depth, concurrency, CPU/memory/I/O/storage limits,
  model-call reservation, and any provider spending envelope;
- policy and revocation epochs, staged-work/publication rules, approval
  bindings, audit requirements, and reconciliation policy.

These are protocol semantics, not a frozen ABI or a demand that every field
reside in the kernel. The kernel authenticates local invocation and enforces
its object rights; resource servers enforce application-specific constraints.
The issuer validates a proposal against authority the human or an authorized
standing policy actually granted. A natural-language classifier cannot mint
permission by deciding that an action seems helpful.

Launch first installs the complete capability, endpoint, namespace, inherited
handle, shared-memory, and resource envelope; only then may the workload run.
Later handle transfers, endpoint discovery, tool updates, and delegated grants
must preserve that envelope and its lineage as well. A broker cannot install
an unrestricted capability in response to a narrow task request. Adding a new
route or tool revision requires admission under the current approved profile.
Unsupported enforcement fails task admission with an explicit explanation.
Imported agent identity terminates at the federation gateway in a new local
decision. No global agent registry is mandatory, and a local credential makes
no claim about a remote agent's internal execution.

## Mandatory mediation of effects

The broker boundary must include native commands, shell interpreters, tool
servers (including MCP transports), subprocesses, filesystem and shared-memory
access, networking, credentials, devices, inference, and later GUI automation.
It is a coverage requirement, not a fixed count of adapters. A compatibility
interface that reaches protected resources must terminate at an enforcing
service. Uncovered raw access invalidates that profile's containment claim.

A tool name allowlist is insufficient. The final sink must validate the
actual operation and canonical parameters against the grant in the same
transaction that admits the effect. Bind file/object generations, recipients,
amounts, payload digests, and expected versions where relevant. Resolve names
under the intended authority; redirects or renamed targets need renewed
validation. A shell command or generic script cannot inherit its broker's
broader permissions.

Credentials remain in a separately protected service. An agent receives an
operation facet, not the human's reusable login token or environment secrets.
Where an external provider accepts only broad credentials, a validating broker
must be their exclusive holder and the only path to that provider. The broker
then remains trusted for that credential's real scope. If the remote tool
itself holds broad authority outside Kay's control, disclose that residual
scope or exclude it from the strong profile; a local sandbox cannot constrain
the remote service's private credentials.

Cloud inference is a disclosure operation. Permission to read a private file
does not grant permission to upload it as context, an embedding, a diagnostic,
or a search query. Check the provider, destination, data classes, session
reuse, and policy before transmission. Local inference needs a qualified
domain/device path too. TLS protects transport, not the recipient from seeing
the plaintext. Provider retention or deletion promises remain external trust.

## Provenance, perception, and persistent memory

The context service attaches protected metadata to admitted content: source
object and version, authenticated origin where available, task/realm,
integrity and confidentiality restrictions, derivation references, and label
issuer/version. Claiming a role in text cannot set these fields. Authentic
origin does not imply correct content. Origin, authorization, sensitivity,
and model confidence remain separate facts.

Filters and semantic classifiers may quarantine content or request narrower
work. Their failure must not widen a grant. Marking retrieved text as data
helps presentation, but cannot prove that an LLM will refrain from following
it. A summary, embedding, tool description, log, cached answer, or generated
script cannot become trusted instruction simply through persistence.

For general model inference, the safe default is conservative dependencies
on all content and retained state actually made available to that inference.
Derived outputs retain the combined confidentiality restrictions and the
applicable integrity restrictions. The model's claim that it used only one
sentence cannot remove other dependencies. Fine-grained labels require a
qualified tracker covering data, control, exceptions, and relevant retained
state. An LLM segmentation heuristic supplies a retrieval hint, not permission
to declassify data or endorse it as trusted control.

Memory writes carry payload/version, labels, dependency evidence, retention,
and sharing rules. Reads and retrieval recheck current task authority;
cross-task reuse never copies old capabilities or approvals. Copying or
summarizing does not erase labels. Missing or contradictory provenance blocks
flows needing that evidence; benign work may continue in a narrower domain.
Declassification (relaxing confidentiality) and endorsement (accepting lower
integrity data for control) require separately authorized, scoped decisions
with their own evidence.

A strong flow profile mediates **all** egress from a domain that has seen
protected data, including outbound request arguments, telemetry, and later
sessions. Partition or destroy reusable model contexts/caches before crossing
incompatible policies; merely clearing a chat transcript does not establish
sanitization. Unrestricted native execution cannot claim fine-grained model
taint soundness. It needs conservative domain confinement or a separately
qualified runtime. Timing/covert channels remain declared limits.

## Delegation, resources, and stop behavior

Child work derives rights, destinations, lifetime, and delegation depth from
the parent's active envelope. Aggregate accounting must prevent sibling agents
from each spending the entire parent budget. Use authoritative reservations
or partitioned subaccounts for concurrent local and remote work; retries
reuse reservation identities. Kernel CPU and memory accounting is distinct
from provider usage and monetary metering. A strict spend promise requires
enforceable preauthorization and bounded in-flight cost, not an estimate after
the provider has charged it.

Every task and descendant retains revocation lineage through queued requests,
derived handles, persistent jobs, and resource products. Capping child expiry
does not propagate an early parent revocation. Sinks validate current fences
when admitting effects; any offline profile declares its maximum stale-grant
exposure and is excluded where immediate stop is required. No timeout silently
upgrades to success or unlimited offline permission.

Stopping work closes future admission and then tracks admitted effects until
completion, cancellation, or explicit indeterminacy. It cannot unsend data or
undo a remote payment. Supervisors retain independently reserved stop and
recovery resources. Restart creates a new workload generation and reauthorizes
work against current policy; it cannot revive revoked capabilities from a
checkpoint. The existing [kernel lifecycle](minimal-privileged-kernel-layer.md)
and [effect-reconciliation contract](applications-and-domain-services-components/external-effects-ports-adapters-and-reconciliation/intent-bound-grants-and-compromised-adapter-containment.md)
remain authoritative.

## Human control and evidence

The [trusted-interaction broker](authentication-and-authorization-components/trusted-interaction-broker.md)
must identify the agent and originating human, show the actual objects,
operations, destinations, duration, resources, and irreversible consequences,
and bind its receipt to the canonical request. Agents cannot confirm their
own requests through synthesized input or accessibility automation. A
protected CLI ceremony is a valid design direction; a future graphical
interface is not a prerequisite for the requirement.

An initial task grant should permit routine work within its clear bounds.
Additional approval is needed for a genuine authority expansion or a protected
publication/disclosure step, as required by that task's policy. The same
request must not be replayed indefinitely to exhaust the user. Approval
fatigue, overbroad acceptance, accessibility, and the ability to inspect and
stop descendants require usability evidence.

Record task/grant lineage, policy revision, effect intent/digest, admission,
observed result, and reconciliation references through protected audit paths.
Keep model claims separate from sink observations. Minimize sensitive content
in logs and apply the same access/flow rules to evidence. Required durable
audit capacity is reserved before the corresponding effect; exhaustion
prevents that effect rather than producing a false receipt. Diagnostic loss
has explicit markers and must not block the independently reserved stop path.

For a coding task, the initial grant could cover a source snapshot, a private
working copy, confined tests, and bounded computation. A later publication
grant binds the reviewed output digest and destination. A hostile README may
still corrupt the proposed patch, but must not acquire unrelated secrets or
publication authority. Review and domain tests address erroneous permitted
changes; containment alone does not establish correct code.

## Alternatives, design decisions, and remaining evidence

Optional framework hooks cannot support the same claim when bypass routes
remain. Moving all classification and memory policy into the privileged
kernel would enlarge the critical failure domain without making semantic
judgments reliable. A hosted broker using existing OS confinement is a useful
experimental baseline and possible compatibility path, with its host
dependencies recorded. Kay-native capability and service contracts are the
selected architectural direction, subject to qualification.

Open decisions include the first agent deployment profile, exact policy and
label algebra, inference-runtime isolation, provider credential scopes,
trusted CLI ceremony, permissible offline exposure, and usability thresholds.
No numerical acceptance target is invented here. Before executing a release
qualification, owners must pin them and the test environment. An unqualified
feature can remain disabled; it cannot be marketed as protected by this design.

## Connections

- [Agent delegation map](../10-maps/safe-agent-delegation.md) — routes through
  evidence, cross-layer contracts, and the open questions.
- [Assurance study](agent-delegation-threat-model-and-assurance.md) — owns the
  adversarial case registry and evidence standard.
- [Research session](../50-journal/2026-09-26-safe-agent-delegation-deep-dive.md)
  — records primary-source reading, provenance, decisions, and checks.
- [Managed runtime](managed-actor-runtime-layer.md),
  [system services](otp-like-system-services-layer.md), and
  [applications](applications-and-domain-services-layer.md) — integrate the
  requirement into existing ownership rather than creating a parallel stack.

## Sources

Source-specific claims and limits are linked in the research-basis section.
The session journal is the exhaustive source manifest; none of the proposed
Kay protocols above has been experimentally validated in this session.
