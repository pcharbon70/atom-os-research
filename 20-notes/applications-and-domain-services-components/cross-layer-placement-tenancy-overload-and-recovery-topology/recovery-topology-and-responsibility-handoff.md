---
title: "Recovery topology and responsibility handoff"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Recovery topology and responsibility handoff

This study decomposes [Cross-layer placement, tenancy, overload, and recovery topology](../cross-layer-placement-tenancy-overload-and-recovery-topology.md).

Research question: Can each failed component be replaced without depending on itself for authority or outcome truth?

## Research basis and status

Crash-only design puts authoritative state outside replaceable components; restarting cannot repair every corruption or ambiguous effect. [1](../../../30-sources/candea-fox-2003-crash-only-software.md).

Sagas permit visible intermediate commits and semantic compensation; they do not supply outer transaction isolation. [2](../../../30-sources/garcia-molina-salem-1987-sagas.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own the application recovery graph and its semantic handoff inventory. Durable
state, outcomes and repair records must survive the volatile component they recover.
Layer 4 can revoke, replace and rebind declared domains without automatically
gaining authority to inspect arbitrary business data or perform effects.

### Admission, transitions and completion

For each failure domain, name an independent observer, recovery controller, retained
state source, replacement grant path and admission fence. Restore lower dependencies
first where required, validate semantic state, reconcile accepted work and reopen
only qualified modes. Recovery of the application root must not require a secret or
registry service available solely inside that root.

### Failure and adversarial behavior

Cycles between application startup, policy access and storage recovery can make
restart impossible. Repeated deterministic failure should reach bounded quarantine
rather than restart forever. A killed adapter may leave a physical effect pending;
successful process replacement is not successful business recovery.

### Alternatives and unresolved tradeoffs

Fine-grained restart reduces disruption when state ownership is clear. Whole-domain
replacement is safer after memory compromise but enlarges the responsibility
inventory. Manual intervention remains necessary for some corruption and
irreversible uncertainty, with narrow authority and persistent evidence.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Fail the application root, runtime domain, adapter and policy dependency separately; demonstrate an independent recovery route for each claimed boundary.
- Inject persistent corruption and repeated restart failure; reach explicit quarantine without losing accepted operation lookup.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Semantic readiness and degraded lifecycle evidence](../application-manifest-composition-and-authority-envelope/semantic-readiness-and-degraded-lifecycle-evidence.md) — a cross-component contract this service must preserve.
- [Intent-bound grants and compromised-adapter containment](../external-effects-ports-adapters-and-reconciliation/intent-bound-grants-and-compromised-adapter-containment.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [Crash-only software](../../../30-sources/candea-fox-2003-crash-only-software.md).
2. [Sagas](../../../30-sources/garcia-molina-salem-1987-sagas.md).
