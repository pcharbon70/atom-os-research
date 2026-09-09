---
title: "Live-tool facets and staged change authority"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Live-tool facets and staged change authority

This study decomposes [Extension points, plugins, and live-tooling confinement](../extension-points-plugins-and-live-tooling-confinement.md).

Research question: How can inspection and live programming coexist without a universal debugger capability?

## Research basis and status

Wedge demonstrates reduced-privilege compartments in Linux applications; it does not validate Atom OS isolation costs. [1](../../../30-sources/bittau-et-al-2008-wedge.md).

Proteus relates update safety to code, data and update points; type safety is weaker than domain or effect safety. [2](../../../30-sources/stoyle-et-al-2005-safe-predictable-dynamic-updating.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own semantic inspection, trace, pure evaluation, staged changesets and domain
validation interfaces. Keep separate facets for reading redacted state, preparing
edits, migrating shadow data, publishing generations and repairing effects. Layer 4
owns grant derivation and release publication.

### Admission, transitions and completion

An inspector receives copied snapshots or bounded probes. An editor produces a
changeset against exact base generation and schema. Validation runs without
production effect imports. A separately authorized publisher checks evidence and
asks Layer 4 to activate a generation. Repair authority names one operation and
allowed amendment, not every adapter.

### Failure and adversarial behavior

A tool that can evaluate arbitrary code in the host heap can bypass read redaction
and mutation policy. Calling a tool developer-only does not reduce that authority.
Traces may disclose secrets; staging may consume excessive shadow storage; both need
independent limits and audit.

### Alternatives and unresolved tradeoffs

A powerful trusted debugger remains a possible explicit recovery profile, with a
much larger acknowledged trust boundary. Routine application tools should use
narrower semantic APIs. Safe language-level updating informs staging but does not
establish state, workflow or external-effect reversibility.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Give a tool inspect-only access and attempt mutation, secret traversal, publication and effect dispatch; each must be denied.
- Validate a changeset, change its base generation, then publish; stale validation evidence must not authorize activation.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Recipient-bound composition and installer retirement](../application-manifest-composition-and-authority-envelope/recipient-bound-composition-and-installer-retirement.md) — a cross-component contract this service must preserve.
- [Placement contracts and independent boundary selection](../cross-layer-placement-tenancy-overload-and-recovery-topology/placement-contracts-and-independent-boundary-selection.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [Wedge](../../../30-sources/bittau-et-al-2008-wedge.md).
2. [Mutatis Mutandis](../../../30-sources/stoyle-et-al-2005-safe-predictable-dynamic-updating.md).
