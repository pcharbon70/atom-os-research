---
title: "2026-09-26 safe agent delegation deep dive"
kind: journal
created: "2026-09-26"
tags: [ai-agents, capabilities, information-flow, research-session, security]
aliases: []
---

# 2026-09-26 safe agent delegation deep dive

## Observations

The user asked whether native support for safely delegated agent work could
be a Kay OS advantage, then directed an architecture/design update and the
usual connected research documentation. This session records the adoption of
that full-system requirement. It does not establish a secure implementation,
predict an adoption rate, or close an implementation gate.

The starting reading was a user-supplied [AgentKernel explainer](https://wa-discord-bot.fly.dev/papers/agentkernel-the-trust-native-agentic-operating-system).
The primary paper was checked directly. The explainer's Elixir snippets are
its own illustrations, not source-paper implementation evidence. Expiry
inheritance alone cannot propagate early revocation, and a non-executable
label alone does not prove that a model ignores instructions inside data.
The Kay design records enforceable alternatives to both assumptions.

## Question and method

The operational question was whether useful human delegation could retain a
bounded effect and disclosure envelope under deliberate agent compromise.
The review combined a position paper, a constrained agent-defense prototype,
attack and benchmark research, official host-kernel documentation, and
previously archived authority and human-interaction foundations.

Primary full text was read for architecture, threat assumptions, evaluation,
and limitations. AgentKernel's Sections 4–7 support an architectural reading;
CaMeL v2's Sections 3–7 and 9 expose its interpreter, input/memory assumptions,
side-channel limits, and cost/utility trade-offs. Greshake v2 Sections 3–5
and AgentDojo v3 Sections 3–4 inform attack fixtures and outcome measurement.
Landlock's rules, inheritance, descriptor, compatibility, and limitation
sections establish that host kernels already constrain agent resource access.

The new source notes were checked for existing duplicates. Original primary
claims, Kay interpretation, and unexecuted proposals are separate. Existing
source notes were reused without resetting their original creation/access
metadata. No source claim was treated as transferred Kay assurance.

AgentKernel's arXiv record displays an August v1 date alongside a September
identifier. The source note preserves that unresolved discrepancy and the
record's pending DOI status. Landlock is living documentation pinned by access
date, not a qualified Linux build. CaMeL and AgentDojo are versioned historical
evaluations, not current model rankings.

## Environment

- Archive: `/home/ducky/code/atom-os-research`.
- Starting archive HEAD: `0cc5243ed517a76bc4d57d3745a3aadd0740b092`.
- Date: 2026-09-26; local timezone: America/Toronto.
- Documentation checking interpreter: Python 3.12.12.
- Execution boundary: local archive editing and primary-source reading;
  no Kay image, QEMU session, physical fixture, model benchmark, or hostile
  workload was executed.

The worktree already contained edits in the PoC map, privilege-transition
research/index, stream README, M1 README/Phase 2, and M2 README/Phases 1–2.
Their starting contents were fingerprinted for preservation. This session
does not revise those files, phase numbering, acceptance gates, or recorded
completion state. Research cases here are not a new phased implementation plan.

## Evidence and resulting model

The [architecture](../20-notes/safe-agent-delegation-and-execution.md) now owns
twelve `AGD-*` requirements and explicit placement across the existing layers.
The [assurance study](../20-notes/agent-delegation-threat-model-and-assurance.md)
maps fourteen `AGT-*` case families to those requirements. All cases remain
specified and not run. The [inquiry](../40-inquiries/how-can-kay-os-safely-delegate-work-to-agents.md)
retains profile, policy, provider, and usability decisions as open.

The design selects deterministic authority ceilings; protected services for
task/grant, context/memory, inference/tool, human interaction, and evidence
functions; separate domains under runtime/native compromise; aggregate
delegation reservations; conservative provenance; explicit disclosure; and
sink-checked revocation. It preserves the existing five-layer ownership,
compiled-BEAM and process-local-GC requirements, and native CLI PoC boundary.

The alternatives considered were optional middleware, an enlarged privileged
semantic kernel, a confined hosted broker, and native capability/service
integration. The last is the architectural direction. A hosted broker remains
a fair comparison and experimental option, with its host dependencies named.
Lower bypass risk and usable autonomy are hypotheses to test, not measured
competitive advantages.

The umbrella architecture, minimal kernel, managed runtime, system services,
applications, security synthesis, grant issuer, trusted-interaction broker,
and exact-effect adapter contracts were connected to the new requirement.
Root guidance, the home map, affected thematic routes, and local inventories
were updated together.

Independent review identified two assurance-oracle ambiguities: the revocation
case needed rejection before admission after the fence, and mandatory audit
exhaustion needed to block effect admission rather than merely withhold a
success certificate. Both were corrected before handoff.
An additional review aligned the kernel extension with sink admission rather
than earlier authorization, and clarified that changed parameters still inside
an expressly granted range are valid positive controls. Envelope preservation
also explicitly covers later handle transfers, discovery, and tool updates.

## Documentation verification

The complete integration passed the following checks from the archive root:

```text
python3 validate_archive.py
Archive validation passed: 1030 completed documents, 99 directories,
10782 local links, and 396 source notes checked; 30 deep-dive source
manifests classify 384 introduced and 586 reused source uses;
12 source notes entered outside a deep-dive manifest.

git diff --check
Exit 0; no whitespace errors.
```

The complete authored diff and new documents were reviewed for stale paths,
accidental rewrites, source/interpretation boundaries, and consistent
requirement ownership. All nine pre-existing modified files retained their
starting SHA-256 fingerprints. No validator or schema behavior changed, so
validator unit tests were not required. Changes were uncommitted at the initial
documentation handoff; subsequent commits record their publication.

These checks establish document structure and navigation only; they do not
execute the `AGT-*` cases or demonstrate an OS security property.

## Source manifest

### Newly introduced sources

- [AgentKernel](../30-sources/zou-et-al-2026-agentkernel.md) — lifecycle architecture, host dependency, and explicit validation gaps.
- [Landlock](../30-sources/linux-kernel-2026-landlock.md) — official existing-kernel confinement, inheritance, and descriptor/ABI boundaries.
- [Indirect prompt injection](../30-sources/greshake-et-al-2023-indirect-prompt-injection.md) — hostile retrieved content, nominal reads as disclosures, and qualitative evaluation limits.
- [AgentDojo](../30-sources/debenedetti-et-al-2024-agentdojo.md) — separate utility and attack outcomes, state-based oracles, and persistence limits.
- [CaMeL](../30-sources/debenedetti-et-al-2025-camel.md) — controlled execution and data-flow prototype, assumptions, overhead, and leakage limits.

### Reused sources

- [Protection of information](../30-sources/saltzer-schroeder-1975-protection-information.md) — complete mediation, bounded mechanism, and usable least privilege.
- [The confused deputy](../30-sources/hardy-1988-confused-deputy.md) — explicit object authority at service boundaries.
- [Capability myths demolished](../30-sources/miller-et-al-2003-capability-myths.md) — attenuation, confinement, and revocation limits.
- [User interaction design for secure systems](../30-sources/yee-2002-user-interaction-design-secure-systems.md) — understandable intent and protected human delegation.
- [Macaroons](../30-sources/birgisson-et-al-2014-macaroons.md) — constrained delegation and credential-verifier assumptions.
- [seL4 information-flow enforcement](../30-sources/murray-et-al-2013-sel4-information-flow.md) — configured assurance and excluded-channel discipline.

## Threads

The [agent topic map](../10-maps/safe-agent-delegation.md) connects the evidence
to the existing security and system layers. Persistent provenance and remote
provider authority require careful profile-specific design before claims of
safe autonomy can be made.

## Follow-ups

Select a deployment profile and explicit owners, policies, resource limits,
and usability criteria through the inquiry. Then develop executable admission
and revocation models and paired useful/hostile workloads. Any later phased
implementation plan must use the required planning templates and retain the
distinction between research obligations, task delivery, and test evidence.
