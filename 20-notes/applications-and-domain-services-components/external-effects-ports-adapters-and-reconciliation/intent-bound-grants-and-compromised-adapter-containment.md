---
title: "Intent-bound grants and compromised-adapter containment"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Intent-bound grants and compromised-adapter containment

This study decomposes [External effects, ports, adapters, and reconciliation](../external-effects-ports-adapters-and-reconciliation.md).

Research question: What prevents a compromised adapter from using its legitimate access for a different effect?

## Research basis and status

The archived WASI design principles favor explicit imports and resource handles; correct host enforcement is still assumed. [1](../../../30-sources/wasi-project-2026-design-principles.md).

Wedge demonstrates reduced-privilege compartments in Linux applications; it does not validate Kay OS isolation costs. [2](../../../30-sources/bittau-et-al-2008-wedge.md).

The model below is proposed Kay OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own the intended action, target, quantity, payload digest, originating commit and
repair policy. Layer 4 derives a narrow invocation grant, and the effect sink
validates it. Protection separates memory, but a compromised adapter can still
misuse any authority it actually holds.

### Admission, transitions and completion

Bind the grant to an authenticated committed intent, exact endpoint generation,
operation ID, request digest, limits and revocation policy. The sink checks these
before admission and atomically records use where one-shot semantics are promised.
The adapter may translate representation only within the qualified equivalence; it
cannot choose another payee, device or amount.

### Failure and adversarial behavior

If the adapter holds a general endpoint credential and the provider cannot enforce
intent bindings, compromise may permit arbitrary actions within that credential's
scope. Record this residual trust explicitly. Local process isolation, code
signatures and redacted logs do not remove it; an independent validating broker
helps only if the adapter cannot bypass the broker.

### Alternatives and unresolved tradeoffs

Per-intent grants minimize delegated power but increase issuance and sink-validation
cost. Long-lived narrow credentials are operationally simpler yet create a larger
residual effect domain. Select the profile from consequence and actual provider
capabilities, not from the word sandbox.

### Delegated agents and publication effects

The user decision of 2026-09-26 applies this adapter boundary to [safe agent
delegation](../../safe-agent-delegation-and-execution.md). The agent, generated
program, or tool adapter may be fully compromised. The trusted grant issuer
and effect sink must therefore validate authority independently, in protection
domains that the agent cannot corrupt. They bind the human subject, executing
workload and incarnation, task and parent delegation, operation ID, target and
endpoint generation, exact payload or artifact digest, destination, expiry,
and resource limits. Identifiers in an agent-generated request are claims
until authenticated against the protected delegation record.

Preparation authority does not imply publication authority. Where policy
requires human approval, a separate grant binds the reviewed artifact and
destination through the trusted interaction path. Changing the artifact,
recipient, or relevant target version invalidates that binding. An agent may
submit a proposal but cannot approve it through synthetic GUI input or a
forged conversation. Shells, browser automation, MCP tools, raw sockets, and
cloud APIs must not offer an alternate route around the enforcing sink.

The adapter must not hold an ambient user credential that defeats those
constraints. If a remote provider accepts only a broad credential, keep it in
a separately protected broker and restrict the adapter to validated requests.
The broker remains trusted for that credential's scope, and the provider's
participation and retention semantics remain explicit assumptions. Inference
requests that disclose data to a remote model also require a scoped effect
grant; model output cannot authorize a later action.

At revocation, close new admissions and invalidate descendants within the
declared revocation scope. Record the race with requests already accepted by
the sink. Cancellation, restart, or grant expiry does not prove those requests
had no effect. Persist operation identity and reconcile an uncertain outcome
before any non-idempotent retry; compensation is a separately authorized
effect. The [assurance study](../../agent-delegation-threat-model-and-assurance.md)
specifies the adversarial evidence needed for this proposed contract.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Compromise the adapter in a model and mutate target, amount, digest or generation; the enforcing sink must reject each unauthorized variation.
- Attempt a direct provider call bypassing the broker; either prove it unavailable or record the adapter as trusted for that credential scope.
- Replace an approved artifact, destination, task identity, or delegation
  parent; require sink rejection. Revoke while dispatch and child delegation
  race, then restart the agent and adapter; no stale grant may admit a new
  effect, while previously accepted work retains a queryable or explicitly
  indeterminate outcome.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Step dispatch, receipt correlation, and resume](../workflows-process-managers-timers-and-compensation/step-dispatch-receipt-correlation-and-resume.md) — a cross-component contract this service must preserve.
- [Semantic admission classes and protected recovery reserve](../cross-layer-placement-tenancy-overload-and-recovery-topology/semantic-admission-classes-and-protected-recovery-reserve.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-kay-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [WASI Design Principles](../../../30-sources/wasi-project-2026-design-principles.md).
2. [Wedge](../../../30-sources/bittau-et-al-2008-wedge.md).
