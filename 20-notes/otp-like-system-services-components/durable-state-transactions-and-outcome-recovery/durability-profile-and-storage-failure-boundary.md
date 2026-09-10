---
title: "Durability profile and storage failure boundary"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Durability profile and storage failure boundary

This study decomposes [Durable state, transactions, and outcome recovery](../durable-state-transactions-and-outcome-recovery.md).

Research question: Which failures does a successful persistence acknowledgement actually survive?

## Research basis and status

FSCQ's guarantees depend on a disk model; isolated device queues do not establish
durable media completion. [1](../../../30-sources/chen-et-al-2015-fscq.md) [2](../../../30-sources/heiser-et-al-2026-sddf-design.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The store owns a versioned durability profile binding device incarnation, atomicity,
alignment, cache and flush behavior, corruption assumptions and complete-device-loss
policy. Lower layers own DMA and command completion mechanisms; their success must
be translated accurately.

### Admission, transitions and completion

Qualify the backend before admitting durable transactions. Name separate receipt
points for descriptor acceptance, device completion, cache persistence and
power-loss survival. Persist the profile identity with store metadata so recovery
cannot silently reinterpret an image under weaker replacement hardware.

### Failure and adversarial behavior

Torn writes, lost flush replies and misdirected writes need different recovery
evidence. Checksums detect some damage but cannot recover all acknowledged data. If
an older checkpoint is selected after corruption, report the affected
acknowledgement guarantee rather than returning ordinary successful recovery.

### Alternatives and unresolved tradeoffs

A single device simplifies reasoning but cannot survive its total loss. Replication
improves fault coverage only with an explicit independent-failure and commit
protocol. Do not relabel hosted filesystem durability as a hardware-independent
service property.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Inject lost, torn and reordered writes under the declared model and check every acknowledged transaction's survival claim.
- Replace the backend with a different flush/atomicity profile; opening the store must require explicit requalification.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Device-service policy and management](../device-service-policy-and-management/README.md) — settles hardware outcomes and buffer custody.
- [Release, update, rollback, and state migration](../release-update-rollback-and-state-migration/README.md) — coordinates code/state transitions and retention.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [FSCQ](../../../30-sources/chen-et-al-2015-fscq.md).
2. [sDDF design](../../../30-sources/heiser-et-al-2026-sddf-design.md).
