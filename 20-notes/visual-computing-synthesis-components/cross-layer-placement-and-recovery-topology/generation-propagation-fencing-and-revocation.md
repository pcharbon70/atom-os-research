---
title: "Generation propagation, fencing, and revocation"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - capability-security
  - fault-tolerance
  - visual-computing
aliases: []
---

# Generation propagation, fencing, and revocation

This study decomposes [Cross-layer placement and recovery topology](../cross-layer-placement-and-recovery-topology.md).

Research question: How do object, activation, view, surface, device, input,
policy, and grant generations compose without one reused identifier reviving
stale work?

## Research basis and status

Capability research requires receiver-side authority enforcement. Orleans
separates logical actor identity from activation, while Chromium frame
identity combines renderer and local route. Wayland and Qubes retain trusted
routing outside clients.
[1](../../../30-sources/miller-et-al-2003-capability-myths.md)
[2](../../../30-sources/bernstein-et-al-2014-orleans.md)
[3](../../../30-sources/chromium-project-2026-multiprocess-graphics-and-accessibility.md)
[4](../../../30-sources/wayland-project-2026-architecture-and-protocol.md)

No end-to-end generation algebra has been modeled for Atom.

## Development

### Owned state and trust boundary

Each authority owns its own monotonic lifecycle: durable object, actor
activation, semantic publisher view, publisher, adapter, surface, compositor,
device queue, seat focus, capture, policy, and grant. Composite references
carry only the generations needed by the receiving sink; human-readable names
and numeric slots never substitute for them.

### Admission, transitions, and completion

Derivation records the parent generations and a delegation ceiling.
Replacement advances the relevant owner before resource reuse and withdraws
published readiness. Receivers compare current local state and reject with
fencing evidence. Revocation completion requires sinks or an enclosing
isolation boundary to make old authority unusable.

### Failure and adversarial behavior

Wraparound, rollback from backup, split coordinators, missed invalidation,
numeric reuse, and delayed DMA/messages can revive stale operations. Width and
persistence rules prevent wrap; epochs bind restore lineage; lower isolation
revokes mappings and queues; protocol caches treat lost continuity as resync.

### Alternatives and unresolved tradeoffs

One global epoch is simple but invalidates unrelated work and centralizes
availability. Independent generations are precise but easy to omit. Typed
composite references plus automated conformance generation are preferred; the
minimum reference shapes remain to be specified.

## Verification obligations

- Reuse every logical ID, PID, selector, surface, buffer, queue, and protocol
  sequence after restart; submit all captured stale records.
- Crash and revoke each owner during delegation and resource handoff; prove
  receiver-side state closes the old path.
- Model-check dependency cycles and show independent generations cannot produce
  a mutually waiting recovery state.

## Connections

- [Internal-service index](README.md) — end-to-end recovery topology.
- [Focus/capture fencing](../input-focus-and-trusted-interaction-authority/focus-capture-leases-and-generation-fencing.md) — input specialization.
- [Renderer leases](../durable-semantic-actors-and-disposable-presentation/renderer-surface-buffer-and-device-leases.md) — presentation specialization.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — provenance.

## Sources

1. [Capability myths demolished](../../../30-sources/miller-et-al-2003-capability-myths.md).
2. [Orleans](../../../30-sources/bernstein-et-al-2014-orleans.md).
3. [Chromium UI process architecture](../../../30-sources/chromium-project-2026-multiprocess-graphics-and-accessibility.md).
4. [Wayland architecture and protocol](../../../30-sources/wayland-project-2026-architecture-and-protocol.md).
