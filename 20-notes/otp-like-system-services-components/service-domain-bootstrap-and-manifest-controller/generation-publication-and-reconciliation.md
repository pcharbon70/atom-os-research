---
title: "Generation publication and reconciliation"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Generation publication and reconciliation

This study decomposes [Service-domain bootstrap and manifest controller](../service-domain-bootstrap-and-manifest-controller.md).

Research question: What does one public generation switch guarantee when services continue executing independently?

## Research basis and status

Anvil proves conditional convergence in its model; NixOS separates profile selection
from effectful activation. [1](../../../30-sources/sun-et-al-2024-anvil.md) [2](../../../30-sources/dolstra-et-al-2008-nixos.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The controller owns desired and observed revisions, readiness attestations and the
proposed registry root. The registry owns the actual publication linearization
point. Running services retain their own execution and effect state; a root pointer
cannot synchronize all their instructions.

### Admission, transitions and completion

Prepare a complete immutable binding table. Recheck dependency, configuration and
authority generations immediately before conditional publication. Log the stable
publication operation, then reobserve its result after reply loss. Cross-service
operations requiring coherent activation carry the shared generation and are fenced
on mismatch.

### Failure and adversarial behavior

Publication conflict requires replanning, not overwriting a newer root. A crash
after publication must discover the committed root rather than duplicate
preparation. Persistent instability permits bounded backoff or escalation;
convergence is conditional on stable inputs and fair adapter progress.

### Alternatives and unresolved tradeoffs

Per-service publication reduces peak private memory but exposes mixed graphs unless
consumers tolerate it explicitly. One root is preferable for coherent local
activation; multi-cell publication needs separate coordination. A convergence
property supplies no boot deadline.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Lose the publication reply and verify recovery identifies exactly one selected table.
- Change a dependency after readiness and require revalidation; then stabilize inputs and check eventual reconciliation rather than an endless safe loop.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Application lifecycle and dependency orchestration](../application-lifecycle-and-dependency-orchestration/README.md) — coordinates readiness, publication and drain.
- [Naming, registry, and local discovery](../naming-registry-and-local-discovery/README.md) — publishes current bindings and watch revisions.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [Anvil](../../../30-sources/sun-et-al-2024-anvil.md).
2. [NixOS](../../../30-sources/dolstra-et-al-2008-nixos.md).
