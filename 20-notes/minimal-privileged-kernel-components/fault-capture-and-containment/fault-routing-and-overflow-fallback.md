---
title: "Fault routing and overflow fallback"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Fault routing and overflow fallback

How does fault delivery remain useful when the normal handler is full, blocked or inside the failed scope?

## Research basis and status

Fault-endpoint mechanisms provide a comparison; independent routing and overflow contracts remain explicit system obligations. [1](../../../30-sources/sel4-foundation-2026-reference-manual.md), [2](../../../30-sources/banga-et-al-1999-resource-containers.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../fault-capture-and-containment.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

Each faultable domain or thread has a preinstalled primary route, finite record capacity and an independent sticky fallback path. Reservations are charged before execution eligibility. The fallback reports that attention is needed; it does not grant the recipient permission to kill a domain.

### Admission, transitions and completion

Publish the record and signal the primary route without blocking the hard fault path. If the route cannot accept a resolvable thread fault, leave that exact thread FAULT_BLOCKED, preserve the available record or loss state and signal the independently funded fallback. Handler replacement uses generation-checked route installation, so an old fault cannot be silently delivered as a new thread's event.

### Failure and adversarial behavior

Allocating a fresh fault queue after resource exhaustion creates a circular dependency. Routing to a helper in the same fatal domain defeats independence. Automatically treating queue overflow as domain-fatal converts a resource-management failure into unauthorized lifecycle escalation.

### Alternatives and unresolved tradeoffs

One common route is simple but can couple unrelated failure scopes through capacity. Partitioned reservations preserve isolation but consume more idle storage. Shared overflow notification is acceptable only with explicit coalescing and a query path that cannot monopolize cleanup.

## Verification obligations

Fill the primary route, stop its handler and exhaust child memory while generating another fault. Verify the thread stays blocked, the fallback remains usable and no termination right is inferred. Exercise record loss and coalescing without claiming exhaustive event delivery.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [SMP stop and completion evidence](../protection-domains-threads-and-address-spaces/smp-stop-and-completion-evidence.md) — Fatal domain handling uses the existing stop protocol.
- [Post-seal crash enrichment](../observability-and-crash-evidence/post-seal-crash-enrichment.md) — Higher-level evidence enriches, but never replaces, lower fatal capture.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [seL4 reference manual, version 16.0.0](../../../30-sources/sel4-foundation-2026-reference-manual.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Resource containers: A new facility for resource management in server systems](../../../30-sources/banga-et-al-1999-resource-containers.md) — comparative evidence; its methods and limits are recorded in the source note.
