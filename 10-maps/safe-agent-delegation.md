---
title: "Safe agent delegation"
kind: map
created: "2026-09-26"
tags: [ai-agents, capabilities, information-flow, security]
aliases: ["Agent security research"]
---

# Safe agent delegation

## Scope

This map follows human authorization through an agent task, its descendants,
memory, tools, and observed effects. It connects the full-system requirement
adopted on 2026-09-26 to Kay OS's existing five layers. Proposed contracts,
hosted evidence, and unexecuted native qualification remain distinct.

## Start here

- [Safe agent delegation and execution](../20-notes/safe-agent-delegation-and-execution.md)
  — the adopted requirement, layer ownership, twelve stable requirements,
  proposed mediation and memory contracts, and remaining decisions.
- [Threat model and assurance](../20-notes/agent-delegation-threat-model-and-assurance.md)
  — fourteen adversarial case families, profile boundaries, useful-work
  controls, and reproducible evidence requirements; none has run for Kay.
- [Open inquiry](../40-inquiries/how-can-kay-os-safely-delegate-work-to-agents.md)
  — deployment, policy, provider, provenance, human-control, and evaluation
  decisions still requiring evidence.
- [2026-09-26 research session](../50-journal/2026-09-26-safe-agent-delegation-deep-dive.md)
  — exhaustive provenance and the documentation verification record.

## Trails

### From agent attacks to enforcement

- [Indirect prompt injection](../30-sources/greshake-et-al-2023-indirect-prompt-injection.md)
  supplies concrete hostile-input paths.
- [AgentDojo](../30-sources/debenedetti-et-al-2024-agentdojo.md) supplies a
  benchmark method with task utility and attacker outcomes.
- [CaMeL](../30-sources/debenedetti-et-al-2025-camel.md) gives a prototype
  comparison for data-flow policy, with important model and channel limits.
- [AgentKernel](../30-sources/zou-et-al-2026-agentkernel.md) supplies the
  lifecycle architecture that prompted this research; validation remains open.
- [Landlock](../30-sources/linux-kernel-2026-landlock.md) grounds the comparison
  in existing host-kernel confinement rather than an assumed absence of it.

### Authority and isolation across layers

- [System security](authentication-and-authorization.md) connects subject,
  actor, grant, local capability, revocation, and exact effect.
- [Minimal kernel](minimal-privileged-kernel.md) owns the deterministic
  enforcement substrate; [managed runtime](managed-actor-runtime.md) separates
  cheap actors from protection against runtime/native compromise.
- [System services](otp-like-system-services.md) own protected brokering,
  task admission, credentials, context/memory, and evidence.
- [Applications](applications-and-domain-services.md) define useful task
  meaning, staged changes, publication, and honest recovery.

### Human control, disclosure, and completion

- [Trusted-interaction broker](../20-notes/authentication-and-authorization-components/trusted-interaction-broker.md)
  binds a human decision to the actual request and excludes agent-generated
  confirmations from that path.
- [Grant compiler and issuer](../20-notes/authentication-and-authorization-components/grant-compiler-and-issuer.md)
  attenuates task authority and conserves aggregate reservations.
- [Intent-bound effects](../20-notes/applications-and-domain-services-components/external-effects-ports-adapters-and-reconciliation/intent-bound-grants-and-compromised-adapter-containment.md)
  bind destinations and artifacts and expose remote-provider trust.
- [seL4 information-flow evidence](../30-sources/murray-et-al-2013-sel4-information-flow.md)
  keeps configuration and excluded channels visible in the assurance claim.

## Open questions

The [agent inquiry](../40-inquiries/how-can-kay-os-safely-delegate-work-to-agents.md)
owns profile selection, policy usability, provenance fidelity, cloud-model
disclosure, and comparison evidence. The broader [security inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
continues to own the shared identity and authorization architecture. Adopting
agent requirements does not establish semantic correctness or modify PoC gates.
