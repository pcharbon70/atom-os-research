---
title: "Distribution gateway and remote actor semantics: internal services"
kind: map
created: "2026-09-09"
tags:
  - actor-model
  - beam
  - managed-runtime
  - system-architecture
  - directory-index
aliases: []
---

# Distribution gateway and remote actor semantics: internal services

## Purpose

Decompose the [parent component](../distribution-gateway-and-remote-actor-semantics.md) into independently
reviewable research contracts. These 4 studies separate state owners,
visibility decisions and residual lifetimes; they are not implementation phases.

## What belongs here

Keep service-level ownership, protocol alternatives, source findings, failure
cases and falsifiers here. Preserve the parent as the integrated component
model. Gateway authentication, transport sessions and BEAM node-incarnation identity are distinct. Compatible sends do not acquire delivery-completion results.

The split follows actual semantic and lifecycle distinctions, not a uniform
number of reports. All studies remain developing and their tests unexecuted.
They concern the full system architecture rather than a particular boot fixture.

## Shared contracts

- Preserve the parent compatibility profile; label restricted behavior and
  new APIs explicitly. Public OTP behavior and internal ERTS mechanisms are
  different evidence classes.
- Keep ordinary actors and automatic process-local tracing collection outside
  the privileged kernel. Native runtime corruption can compromise the domain.
- Bind operations to the relevant object, actor, domain and service generations;
  a transport session is not automatically a new external BEAM identity.
- Distinguish private preparation, publication, terminal semantic outcome and
  final storage reclamation. Cancellation and wakeups are not universal
  completion receipts.
- Charge deferred work and preserve finite recovery/evidence capacity. No
  literature throughput result establishes a hard latency bound here.

## Index

### Subdirectories

- None.

### Documents

- [Gateway session authentication and profile negotiation](gateway-session-authentication-and-profile-negotiation.md) — covers bounded handshake state, authenticated peer identity, selected protocol/profile, route authority and session epoch.
- [Remote PID/reference identity and route rebinding](remote-pid-reference-identity-and-route-rebinding.md) — covers a mapping from external PID/reference identity to authorized current route, with separate node creation and transport session generation.
- [Hostile ETF decoding and distributed signal ingress](hostile-etf-decoding-and-distributed-signal-ingress.md) — covers frame/decompression budgets, parser arena, provisional atoms, peer charge and decoded signal envelope.
- [Send credits, ordering and disconnect outcomes](send-credits-ordering-and-disconnect-outcomes.md) — covers byte/message/control credits, sender-order channel assignments and optional tracked-send receipts.

## Cross-component boundaries

- [Local order-preserving ingress](../signal-ingress-mailboxes-and-selective-receive/striped-ingress-order-and-node-reclamation.md) — shared ownership or observation boundary.
- [Disconnect knowledge and uncertainty](../failure-translation-and-the-otp-boundary/service-loss-uncertainty-and-supervisor-handoff.md) — shared ownership or observation boundary.
- [Runtime component inventory](../README.md) — all thirteen parent components.
- [Managed-runtime map](../../../10-maps/managed-actor-runtime.md) — selective research routes.
- [Open inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — decisions awaiting evidence.
- [Dated source manifest](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — exact session provenance.

## Maintaining this index

Inventory every direct child, link directories through their README, and keep
the parent, component inventory, map and session evidence connected. Add a new
service only for a distinct responsibility; do not split or merge to meet a
numerical quota. Do not turn research completion into checked implementation.
