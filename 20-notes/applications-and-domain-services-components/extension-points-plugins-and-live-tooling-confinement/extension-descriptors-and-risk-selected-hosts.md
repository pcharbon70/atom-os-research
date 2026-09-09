---
title: "Extension descriptors and risk-selected hosts"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Extension descriptors and risk-selected hosts

This study decomposes [Extension points, plugins, and live-tooling confinement](../extension-points-plugins-and-live-tooling-confinement.md).

Research question: Which execution boundary is justified for a particular extension?

## Research basis and status

The archived WASI design principles favor explicit imports and resource handles; correct host enforcement is still assumed. [1](../../../30-sources/wasi-project-2026-design-principles.md).

Wedge demonstrates reduced-privilege compartments in Linux applications; it does not validate Atom OS isolation costs. [2](../../../30-sources/bittau-et-al-2008-wedge.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own extension-point meaning, artifact identity, declared inputs and outputs, trust
class, state profile and requested budgets. Layer 4 authenticates artifacts and
provisions enforcement. A signed package proves provenance under a trust policy, not
safe behavior or entitlement to all application data.

### Admission, transitions and completion

Classify reviewed bounded rules, trusted callbacks, isolated managed code, portable
modules and native or device-related code separately. Select a host from mutual
trust, accessible secrets, native risk and required resource isolation. Install
explicit imports into an immutable extension generation before opening invocation
admission.

### Failure and adversarial behavior

A same-runtime actor can isolate ordinary process failure while sharing a
compromised runtime's memory and powers. Untrusted code cannot be declared confined
simply because it is BEAM-compatible. Portable bytecode still depends on host calls,
engine correctness and resource control. A supposedly pure function may loop or
allocate without bound.

### Alternatives and unresolved tradeoffs

In-process rules are justified only for a reviewed total and conservatively
cost-bounded subset or immutable data. Budgeted workers suit larger trusted
computations; distrustful authors or unsafe code require an independently enforced
boundary. Exact costs remain unmeasured.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Exercise every admitted code class with infinite computation, oversized output and denied imports; record the actual enforcement layer.
- Attempt cross-extension and cross-tenant access inside shared versus separate hosts; do not infer isolation from a supervisor tree.

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

1. [WASI Design Principles](../../../30-sources/wasi-project-2026-design-principles.md).
2. [Wedge](../../../30-sources/bittau-et-al-2008-wedge.md).
