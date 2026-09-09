---
title: "Extension invocation and domain-proposal validation"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Extension invocation and domain-proposal validation

This study decomposes [Extension points, plugins, and live-tooling confinement](../extension-points-plugins-and-live-tooling-confinement.md).

Research question: How can extensions influence behavior without becoming aggregate writers?

## Research basis and status

Cockburn places technology adapters outside semantic ports; the pattern does not guarantee effect safety. [1](../../../30-sources/cockburn-2005-hexagonal-architecture.md).

Liskov and Wing treat substitution as preservation of behavioral properties, beyond compatible representation. [2](../../../30-sources/liskov-wing-1994-behavioral-subtyping.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own invocation ID, extension generation, host revision, copied input, deadline and
output schema. The extension returns bounded data or proposed typed commands. Host
domain validation owns meaning and invariants; Layer 4 supplies scoped authority and
runtime resource enforcement.

### Admission, transitions and completion

Admit only after reserving input, computation, result and teardown budgets. Execute
outside the aggregate invariant turn unless the narrow total-rule profile applies.
Validate the result's generation, digest, size and host revision, then make a fresh
domain decision. Returned pointers, PIDs, live capability bytes and executable
payloads are not accepted as ordinary domain values.

### Failure and adversarial behavior

A valid-looking result may arrive after the host changed state or the extension was
revoked. Discard pure stale output, but reconcile any separately accepted effect.
Nested calls must consume the initiating budget and obey depth limits; a plugin
cannot escape accounting by spawning helpers.

### Alternatives and unresolved tradeoffs

Typed proposals preserve a clear domain boundary but can constrain extension
expressiveness. Direct mutation is more flexible only by treating the extension as
trusted aggregate code with the corresponding failure scope. The research default is
explicit proposals, not implicit trust escalation.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Change the aggregate revision while an extension computes; reject or revalidate the stale proposal.
- Return deeply nested data and forged handle-like values; output validation must remain bounded and confer no authority.

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

1. [Hexagonal Architecture](../../../30-sources/cockburn-2005-hexagonal-architecture.md).
2. [Behavioral subtyping](../../../30-sources/liskov-wing-1994-behavioral-subtyping.md).
