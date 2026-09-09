---
title: "Configuration snapshots and secret lease bindings"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Configuration snapshots and secret lease bindings

This study decomposes [Application manifest, composition, and authority envelope](../application-manifest-composition-and-authority-envelope.md).

Research question: What configuration can be retained durably without retaining live authority or secret values?

## Research basis and status

NixOS separates immutable configuration generations from mutable activation effects; selecting an old generation does not undo domain state. [1](../../../30-sources/dolstra-et-al-2008-nixos.md).

The archived WASI design principles favor explicit imports and resource handles; correct host enforcement is still assumed. [2](../../../30-sources/wasi-project-2026-design-principles.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own validated immutable configuration values, their schema and source digests, and
logical secret requirements. Layer 4 owns secret material, authenticated binding
generations, lease issuance and revocation. A durable application record may name
why a credential is needed, never serialize a reusable credential as recovery state.

### Admission, transitions and completion

Resolve configuration at a named generation, validate cross-field constraints and
publish it to specific recipients. Fetch secret handles through separately
authorized leases. A rotation constructs a new binding, establishes which accepted
operations may finish on the old one, then retires old admission. Record nonsecret
version evidence for diagnostics and reproducible recovery.

### Failure and adversarial behavior

An environment-variable fallback or debug dump can bypass the declared secrecy
boundary. Missing secrets must produce a typed dependency condition, not an empty
value that changes business behavior. Reloading configuration while an invariant
turn executes can mix policy generations; pin the relevant snapshot for the decision
and recheck required current authority at the sink.

### Alternatives and unresolved tradeoffs

Full restart on configuration change is simple but can interrupt long workflows.
Live replacement is justified only with explicit per-field transition semantics.
Content addressing provides identity, not proof that a build or configuration
evaluator was hermetic.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Rotate a secret during an accepted request and during compensation; record the intended old/new lease behavior without disclosing values.
- Inject an invalid cross-field configuration and a secret-provider outage; old valid state or explicit refusal must remain identifiable.

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

1. [NixOS](../../../30-sources/dolstra-et-al-2008-nixos.md).
2. [WASI Design Principles](../../../30-sources/wasi-project-2026-design-principles.md).
