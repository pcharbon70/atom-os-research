---
title: "Restart, resynchronization, and presentation backpressure"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - backpressure
  - fault-tolerance
  - visual-computing
aliases: []
---

# Restart, resynchronization, and presentation backpressure

This study decomposes [Durable semantic actors and disposable presentation](../durable-semantic-actors-and-disposable-presentation.md).

Research question: How does a replacement presentation become current under
message loss, slow consumers, and resource exhaustion?

## Research basis and status

Crash-only software and microreboot research make restart depend on explicit
state placement and bounded recovery. Chromium shows process-level renderer
replacement, while asynchronous FRP work demonstrates one approach to
coalescing presentation work.
[1](../../../30-sources/candea-fox-2003-crash-only-software.md)
[2](../../../30-sources/candea-et-al-2004-microreboot.md)
[3](../../../30-sources/chromium-project-2026-multiprocess-graphics-and-accessibility.md)
[4](../../../30-sources/czaplicki-chong-2013-asynchronous-frp-guis.md)

Recovery deadlines and overload profiles remain unmeasured.

## Development

### Owned state and trust boundary

The recovery coordinator owns presentation dependency state, restart budgets,
and recovery reserve. Each subscriber owns a bounded queue and last accepted
revision. Models own durable outcomes and must not depend on frame delivery for
progress.

### Admission, transitions, and completion

Replacement closes old view, surface, focus, and input generations; obtains a
complete current semantic snapshot; allocates fresh leases; and publishes
readiness only after a first coherent frame or nonvisual equivalent. Under
load, superseded state updates coalesce, but command outcomes and resnapshot
markers remain lossless.

### Failure and adversarial behavior

Restart storms, poisoned state, hot publishers, slow accessibility consumers,
and exhausted GPU memory can starve recovery. Per-project accounting, maximum
snapshot size, reserved CPU/memory, cooldown, and degraded text presentation
bound the path. A failed replacement never revives predecessor grants.

### Alternatives and unresolved tradeoffs

Infinite queues preserve events until the system fails globally. Silent
dropping preserves latency but corrupts state. Latest-state coalescing plus
explicit continuity loss is preferred; which semantic events are
non-coalescible needs protocol-specific classification.

## Verification obligations

- Overproduce updates with slow visual and assistive consumers; memory stays
  bounded and both recover through declared snapshot semantics.
- Inject repeated renderer failures and prove restart budgets preserve the
  trusted recovery console and unrelated projects.
- Measure model-to-semantic, semantic-to-frame, and failure-to-usable-view
  latency separately under each exhausted resource.

## Connections

- [Internal-service index](README.md) — recovery and backpressure scope.
- [Atomic semantic streams](../semantics-first-accessible-ui-protocol/atomic-snapshot-delta-and-resynchronization.md) — continuity protocol.
- [Resource reserve](../cross-layer-placement-and-recovery-topology/resource-reserve-overload-and-fault-containment.md) — cross-layer guarantees.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — limitations.

## Sources

1. [Crash-only software](../../../30-sources/candea-fox-2003-crash-only-software.md).
2. [Microreboot](../../../30-sources/candea-et-al-2004-microreboot.md).
3. [Chromium UI process architecture](../../../30-sources/chromium-project-2026-multiprocess-graphics-and-accessibility.md).
4. [Asynchronous FRP for GUIs](../../../30-sources/czaplicki-chong-2013-asynchronous-frp-guis.md).
