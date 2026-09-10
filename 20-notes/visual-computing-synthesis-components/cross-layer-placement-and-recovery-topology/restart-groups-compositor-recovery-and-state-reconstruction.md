---
title: "Restart groups, compositor recovery, and state reconstruction"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - compositor
  - fault-tolerance
  - visual-computing
aliases: []
---

# Restart groups, compositor recovery, and state reconstruction

This study decomposes [Cross-layer placement and recovery topology](../cross-layer-placement-and-recovery-topology.md).

Research question: Which services restart together, who holds recovery
authority, and how does composition return without restarting durable models?

## Research basis and status

Microreboot research requires explicit state separation and dependency-aware
recovery. Wayland separates surfaces/buffers from client meaning; Chromium
replaces failed renderers and GPU processes; Qubes separates application agents
from the trusted GUI domain.
[1](../../../30-sources/candea-et-al-2004-microreboot.md)
[2](../../../30-sources/wayland-project-2026-architecture-and-protocol.md)
[3](../../../30-sources/chromium-project-2026-multiprocess-graphics-and-accessibility.md)
[4](../../../30-sources/qubes-project-2026-gui-virtualization.md)

Actual shared-fate groups are not yet measured.

## Development

### Owned state and trust boundary

Recovery metadata names service instances, supervisors, external recovery
holders, dependency generations, resource accounts, restart budgets, and
readiness evidence. Project/model roots sit outside desktop supervision.
Compositor state, scene layout, surfaces, focus, and input grants are
reconstructible or ephemeral.

### Admission, transitions, and completion

Compositor failure first fences surfaces, buffers, focus, capture, and pending
presentation submissions. The replacement obtains current project/view
descriptors, rebuilds trusted shell and scene state, derives fresh device and
input facets, requests current semantic snapshots, and publishes readiness
after coherent output. Models continue unless their independent contract fails.

### Failure and adversarial behavior

Restart storms, poisoned snapshots, stale device queues, circular readiness,
and a failed service holding its own cleanup authority prevent recovery.
External revocation, typed readiness, bounded retries, dependency DAG checks,
and quarantine of repeated failures make the transition finite.

### Alternatives and unresolved tradeoffs

Restarting the entire desktop stack simplifies consistency but disrupts models
and effects. Preserving all compositor state couples recovery to corrupt data.
Rebuild from semantic/project truth is preferred; which shell preferences are
durable meaning versus presentation remains user-policy work.

## Verification obligations

- Crash every visual service before/after capability derivation, publication,
  frame submit, focus transfer, command admission, and teardown.
- Compare generated dependency manifests with observed restart propagation and
  eliminate hidden shared state.
- Preserve model progress during compositor, shell, renderer, adapter, and
  GPU restart while rejecting every stale resource.

## Connections

- [Internal-service index](README.md) — restart topology.
- [Presentation restart](../durable-semantic-actors-and-disposable-presentation/restart-resynchronization-and-presentation-backpressure.md) — view-level sequence.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — sources.

## Sources

1. [Microreboot](../../../30-sources/candea-et-al-2004-microreboot.md).
2. [Wayland architecture and protocol](../../../30-sources/wayland-project-2026-architecture-and-protocol.md).
3. [Chromium UI process architecture](../../../30-sources/chromium-project-2026-multiprocess-graphics-and-accessibility.md).
4. [Qubes GUI virtualization](../../../30-sources/qubes-project-2026-gui-virtualization.md).
