---
title: "Offline grants, provenance, and reconnect admission"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Offline grants, provenance, and reconnect admission

This study decomposes [Offline collaboration, replication, and conflict semantics](../offline-collaboration-replication-and-conflict-semantics.md).

Research question: What authority does a disconnected device have, and what can revocation mean while it is absent?

## Research basis and status

Local-first research argues for locally usable user-owned documents; its scope is not arbitrary scarce-resource or external-effect transactions. [1](../../../30-sources/kleppmann-et-al-2019-local-first-software.md).

The archived WASI design principles favor explicit imports and resource handles; correct host enforcement is still assumed. [2](../../../30-sources/wasi-project-2026-design-principles.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own offline operation provenance, tentative status, requested domain actions and
reconnect policy. Layer 4 authenticates devices, issues bounded grants and supplies
current policy epochs. A signature attributes submitted content; it does not prove
the operation is authorized for integration now.

### Admission, transitions and completion

Classify operations as locally permitted content, tentative proposals or online-only
effects. Record subject, device, lifecycle and grant epoch with each operation. On
reconnect validate current realm binding, schema and invariant policy, then
integrate, quarantine or preserve an exportable draft according to disclosure rules.
State-based merge requires equivalent authenticated provenance where that property
is promised.

### Failure and adversarial behavior

A revoked device can retain bytes it already saw; refusing future writes does not
erase them. Selective acceptance can break causal dependencies, so rejected
predecessors require an explicit dependent-operation policy. Malicious causal graphs
and signature floods need bounded validation before durable admission.

### Alternatives and unresolved tradeoffs

Revalidation on reconnect gives stronger current-policy control but may reject
legitimate-looking offline work. Preauthorized irrevocable limited operations offer
different semantics and must be declared in advance. Universal immediate revocation
and unrestricted disconnected commit cannot both be assumed.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Revoke a device during partition and reconnect a dependent chain of edits; show accepted, rejected and exportable states explicitly.
- Submit attributable but unauthorized operations and oversized causal contexts; neither may bypass policy or exhaust recovery capacity.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Escrow rights conservation and transfer](../invariants-transactions-and-concurrency-policy/escrow-rights-conservation-and-transfer.md) — a cross-component contract this service must preserve.
- [Directed compatibility and behavioral fixture matrices](../application-evolution-schema-compatibility-and-migration/directed-compatibility-and-behavioral-fixture-matrices.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [Local-First Software](../../../30-sources/kleppmann-et-al-2019-local-first-software.md).
2. [WASI Design Principles](../../../30-sources/wasi-project-2026-design-principles.md).
