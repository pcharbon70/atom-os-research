---
title: "Context translation and anti-corruption boundaries"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Context translation and anti-corruption boundaries

This study decomposes [Bounded contexts, domain model, and application services](../bounded-contexts-domain-model-and-application-services.md).

Research question: When does changing representation require a new domain decision rather than a field mapping?

## Research basis and status

Cockburn places technology adapters outside semantic ports; the pattern does not guarantee effect safety. [1](../../../30-sources/cockburn-2005-hexagonal-architecture.md).

Cambria demonstrates schema lenses but explicitly leaves semantic reassignment and missing external data beyond mechanical translation. [2](../../../30-sources/litt-et-al-2020-cambria.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own a versioned relationship between two bounded contexts, source and target
vocabularies, loss declarations, correlation links and translation limits. The
translator receives only the two named ports. It does not own either context's
invariants or gain authority because it can map identifiers.

### Admission, transitions and completion

Decode in the source schema, construct a bounded intermediate value, and validate
the target meaning. Preserve the initiating operation's provenance; create a
distinct target operation with a durable causal binding when translation requests a
new effect. Reject missing facts or unsupported critical meanings instead of
inventing defaults. The target performs its own current authorization and invariant
checks.

### Failure and adversarial behavior

Mapping a displayed assignee name to a user-record name field can accidentally
request an identity edit instead of reassignment. Bidirectional conversion cannot
manufacture permission or recover lost distinctions. Translator retries must
retrieve the same target-operation binding; otherwise a restarted adapter becomes a
duplicate-command factory.

### Alternatives and unresolved tradeoffs

A mechanical lens is suitable for proven representation changes. An anti-corruption
service is warranted when concepts differ. A shared schema may eliminate translation
but couples model ownership and release cadence; select it only where that coupling
is intentional.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Round-trip fields with unknown variants and lossy mappings; either preserve promised meaning or report loss explicitly.
- Test reassignment versus renaming with identical visible strings; target action and authority must remain distinct.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Invariant catalog and coordination selection](../invariants-transactions-and-concurrency-policy/invariant-catalog-and-coordination-selection.md) — a cross-component contract this service must preserve.
- [Operation identity and honest outcome ledgers](../typed-commands-queries-events-and-protocol-contracts/operation-identity-and-honest-outcome-ledgers.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [Hexagonal Architecture](../../../30-sources/cockburn-2005-hexagonal-architecture.md).
2. [Project Cambria](../../../30-sources/litt-et-al-2020-cambria.md).
