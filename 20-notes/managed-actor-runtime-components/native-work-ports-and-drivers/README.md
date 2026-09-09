---
title: "Native work, ports and drivers: internal services"
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

# Native work, ports and drivers: internal services

## Purpose

Decompose the [parent component](../native-work-ports-and-drivers.md) into independently
reviewable research contracts. These 4 studies separate state owners,
visibility decisions and residual lifetimes; they are not implementation phases.

## What belongs here

Keep service-level ownership, protocol alternatives, source findings, failure
cases and falsifiers here. Preserve the parent as the integrated component
model. Protected service domains are the default native boundary. Regular and dirty NIFs remain inside the runtime memory-failure domain.

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

- [Native service broker and attenuated handles](native-service-broker-and-attenuated-handles.md) — covers a broker table of runtime-epoch/slot/generation handles, allowed operation sets, service incarnations and admission credits.
- [Native request outcomes and cancellation drain](native-request-outcomes-and-cancellation-drain.md) — covers request identity, caller/service generations, publication phase, terminal outcome and residual cleanup.
- [Native buffer leases, port ownership and driver handoff](native-buffer-leases-port-ownership-and-driver-handoff.md) — covers buffer lease generations, port owner identity, command sequence and service/device incarnation bindings.
- [Trusted NIF segments, resources and domain risk](trusted-nif-segments-resources-and-domain-risk.md) — covers an admitted module manifest covering each name/arity entry, permitted regular/dirty CPU/dirty I/O transitions, callbacks, resource types and upgrade/destructor behavior.

## Cross-component boundaries

- [I/O ownership and terminal completion](../timers-events-and-asynchronous-io-integration/asynchronous-operation-records-and-buffer-completion.md) — shared ownership or observation boundary.
- [Failure projection without unsafe retry](../failure-translation-and-the-otp-boundary/service-loss-uncertainty-and-supervisor-handoff.md) — shared ownership or observation boundary.
- [Runtime component inventory](../README.md) — all thirteen parent components.
- [Managed-runtime map](../../../10-maps/managed-actor-runtime.md) — selective research routes.
- [Open inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — decisions awaiting evidence.
- [Dated source manifest](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — exact session provenance.

## Maintaining this index

Inventory every direct child, link directories through their README, and keep
the parent, component inventory, map and session evidence connected. Add a new
service only for a distinct responsibility; do not split or merge to meet a
numerical quota. Do not turn research completion into checked implementation.
