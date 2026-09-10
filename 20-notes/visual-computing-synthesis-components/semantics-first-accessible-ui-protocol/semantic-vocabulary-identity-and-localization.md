---
title: "Semantic vocabulary, identity, and localization"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - accessibility
  - localization
  - semantic-ui
aliases: []
---

# Semantic vocabulary, identity, and localization

This study decomposes [Semantics-first accessible UI protocol](../semantics-first-accessible-ui-protocol.md).

Research question: What stable semantic meaning survives locale, toolkit,
platform adapter, view reconstruction, and object reactivation?

## Research basis and status

WAI-ARIA defines roles, states, properties, and relationships; Core-AAM exposes
the lossy mappings to platform APIs. AccessKit supplies an implemented
cross-platform node/action schema but explicitly retains specification gaps.
[1](../../../30-sources/w3c-2023-wai-aria-1-2.md)
[2](../../../30-sources/w3c-2026-core-accessibility-api-mappings-1-2.md)
[3](../../../30-sources/accesskit-project-2026-architecture-and-engineering.md)

The Atom OS core vocabulary and compatibility profile are not frozen.

## Development

### Owned state and trust boundary

The vocabulary registry owns namespaced role IDs, version ranges, required
properties, supported actions, relation schemas, typed values, and fallback
roles. Logical object identity and lifecycle generation are distinct from
view-local node IDs. Localized messages carry stable message IDs and typed
arguments; rendered strings never become durable identity.

### Admission, transitions, and completion

Publishers negotiate a vocabulary profile before a snapshot. Unknown custom
roles declare a known base role and may lose extension semantics in older
consumers. Locale or direction changes produce a new semantic revision while
preserving logical targets, selections, pending operation IDs, and action
meaning.

### Failure and adversarial behavior

Incorrect roles can promise actions that do not exist; translated labels can
collide; unbounded extension metadata can exhaust adapters. Validators enforce
role invariants, length and nesting bounds, namespace ownership, and semantic
action schemas before publication. Fallback is explicit, never invented from
pixels.

### Alternatives and unresolved tradeoffs

A closed universal taxonomy is interoperable but cannot express new media. An
untyped property bag is extensible but unverifiable. A small versioned core
plus namespaced, base-role-compatible extensions is preferred; the initial
core and deprecation lifetime remain research questions.

## Verification obligations

- Switch locale, script direction, and adapter during a pending action; identity
  and outcome correlation must remain stable.
- Fuzz incompatible custom roles and missing required properties; consumers
  must reject or use declared fallback without semantic invention.
- Test equivalent tasks through real screen readers, voice, keyboard, and
  visual clients; schema validation alone cannot pass.

## Connections

- [Internal-service index](README.md) — sibling protocol responsibilities.
- [Plural representation contracts](../plural-representations-and-cross-view-consistency/provider-registration-negotiation-and-representation-contracts.md) — extension negotiation.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — evidence.

## Sources

1. [WAI-ARIA 1.2](../../../30-sources/w3c-2023-wai-aria-1-2.md).
2. [Core-AAM 1.2](../../../30-sources/w3c-2026-core-accessibility-api-mappings-1-2.md).
3. [AccessKit architecture](../../../30-sources/accesskit-project-2026-architecture-and-engineering.md).
