---
title: "Pending-outcome presentation and session recovery"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Pending-outcome presentation and session recovery

This study decomposes [Presentation sessions, semantic views, and user outcomes](../presentation-sessions-semantic-views-and-user-outcomes.md).

Research question: How should a user distinguish apparent responsiveness from actual domain completion?

## Research basis and status

Google SRE guidance starts indicators from user-relevant behavior and explicit measurement populations, not process uptime alone. [1](../../../30-sources/jones-et-al-2016-service-level-objectives.md).

Local-first research argues for locally usable user-owned documents; its scope is not arbitrary scarce-resource or external-effect transactions. [2](../../../30-sources/kleppmann-et-al-2019-local-first-software.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own presentation mapping for pending, committed, proven not committed, terminated
with surviving effects, fenced and indeterminate outcomes. Domain outcome records
remain authoritative. Local animation, selection and navigation state can be
provisional; the view must not silently promote them to committed truth.

### Admission, transitions and completion

Show accepted responsibility with a recoverable operation reference. Refresh state
from an authoritative revision or declared projection frontier after commit. On
session restart, reconcile pending operations before offering duplicate
consequential actions. Preserve useful drafts separately from accepted operations,
subject to confidentiality and retention policy.

### Failure and adversarial behavior

A spinner disappearing on timeout can imply failure and provoke duplicate
submission. A success toast based on transport acknowledgment can mislead users
about a later rejected effect. A repair case cannot be presented as resolved merely
because it was assigned to an operator. Error wording must remain useful without
disclosing protected state.

### Alternatives and unresolved tradeoffs

Optimistic editing is appropriate where rollback of provisional display is
understandable. Irreversible actions warrant explicit pending and uncertainty
states. The proposed vocabulary needs accessibility and user studies; technical
honesty alone does not establish that people understand it.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Run lost-response scenarios with users and alternative modalities; measure duplicate attempts and correct interpretation, not just response time.
- Restart the desktop while domain work continues; no raw input is replayed and unresolved outcomes remain discoverable.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Operation identity and honest outcome ledgers](../typed-commands-queries-events-and-protocol-contracts/operation-identity-and-honest-outcome-ledgers.md) — a cross-component contract this service must preserve.
- [Effect reconciliation and unqueryable repair](../external-effects-ports-adapters-and-reconciliation/effect-reconciliation-and-unqueryable-repair.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [Service Level Objectives](../../../30-sources/jones-et-al-2016-service-level-objectives.md).
2. [Local-First Software](../../../30-sources/kleppmann-et-al-2019-local-first-software.md).
