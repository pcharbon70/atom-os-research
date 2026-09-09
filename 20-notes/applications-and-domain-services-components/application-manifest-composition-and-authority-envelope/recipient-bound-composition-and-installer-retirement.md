---
title: "Recipient-bound composition and installer retirement"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Recipient-bound composition and installer retirement

This study decomposes [Application manifest, composition, and authority envelope](../application-manifest-composition-and-authority-envelope.md).

Research question: How can composition wire the whole application without retaining the union of its powers?

## Research basis and status

The archived WASI design principles favor explicit imports and resource handles; correct host enforcement is still assumed. [1](../../../30-sources/wasi-project-2026-design-principles.md).

Wedge demonstrates reduced-privilege compartments in Linux applications; it does not validate Atom OS isolation costs. [2](../../../30-sources/bittau-et-al-2008-wedge.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own a wiring inventory containing recipient identity, port slot, contract digest,
installer generation and installation receipt. Layer 4 derives and delivers terminal
facets or sealed recipient-bound installers. The composition root can inspect
structure without possessing reusable database, secret and external-effect handles
for every child.

### Admission, transitions and completion

Prepare children privately; request installation into exact recipient generations;
verify receipt and port compatibility; return unused installers; then request
installer retirement. Application startup code does not turn a wiring description
into a service locator. Replacement children require a fresh authorized installation
transaction, not copying stale capability bytes from a saved heap.

### Failure and adversarial behavior

If the root crashes halfway through, Layer 4 revokes the installer generation and
either discards the private graph or resumes from authenticated receipts. A
compromised recipient may misuse its own imports, but must not redeem another
child's installer. Retirement closes future installation; it does not
retrospectively undo already accepted effects.

### Alternatives and unresolved tradeoffs

Direct facet delivery offers a smaller deputy surface than handing broad powers to
the root for later attenuation. Sealed installers support more flexible
initialization but add recipient-authentication, replay and teardown obligations.
Keeping the root permanently privileged is not justified by graph visibility.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Replay an installer into a replacement actor, another tenant and a different port slot; each must fail before access.
- Crash after each installation receipt and after retirement; enumerate remaining reachable authority and accepted responsibilities.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Business-tenant bindings and realm reassignment](../cross-layer-placement-tenancy-overload-and-recovery-topology/business-tenant-bindings-and-realm-reassignment.md) — a cross-component contract this service must preserve.
- [Workflow-generation handoff and publication fences](../application-evolution-schema-compatibility-and-migration/workflow-generation-handoff-and-publication-fences.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [WASI Design Principles](../../../30-sources/wasi-project-2026-design-principles.md).
2. [Wedge](../../../30-sources/bittau-et-al-2008-wedge.md).
