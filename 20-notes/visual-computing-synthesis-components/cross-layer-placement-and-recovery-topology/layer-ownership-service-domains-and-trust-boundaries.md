---
title: "Layer ownership, service domains, and trust boundaries"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - system-architecture
  - trust-boundary
  - visual-computing
aliases: []
---

# Layer ownership, service domains, and trust boundaries

This study decomposes [Cross-layer placement and recovery topology](../cross-layer-placement-and-recovery-topology.md).

Research question: Which layer can actually enforce each display, input,
semantic, lifecycle, resource, and domain guarantee?

## Research basis and status

L4 and seL4 design experience supports small privileged mechanism and
user-space policy. Nitpicker demonstrates a small user-space trusted GUI
server, while Chromium and Qubes show practical process/domain splits with
different TCB trade-offs.
[1](../../../30-sources/elphinstone-heiser-2013-l4-lessons.md)
[2](../../../30-sources/heiser-2020-sel4-design-principles.md)
[3](../../../30-sources/feske-helmuth-2005-nitpicker.md)
[4](../../../30-sources/chromium-project-2026-multiprocess-graphics-and-accessibility.md)
[5](../../../30-sources/qubes-project-2026-gui-virtualization.md)

The topology is proposed and has no measured Atom TCB.

## Development

### Owned state and trust boundary

Hardware support owns architectural mechanisms; the kernel owns isolation,
capabilities, mappings, IPC, budgets, revocation, and teardown; the managed
runtime owns actors/messages; system services own lifecycle, persistence,
devices, update, audit, and recovery policy. Visual services own semantic
publication, adapters, rendering, composition, input brokering, and tools.
Applications own domain invariants and effects.

### Admission, transitions, and completion

Every cross-layer request names an enforcing object, caller facet, resource
account, generation, and outcome contract. A service may be highly trusted
without entering the kernel. Lower layers expose generic mechanisms; new
widgets, media, roles, and project schemas require no privileged parser.

### Failure and adversarial behavior

Hidden host dependencies, shared libraries, omniscient brokers, and duplicated
policy can invalidate the topology. Dependency manifests enumerate actual
services and privileges; fault injection verifies claimed isolation; audits
distinguish policy decision from enforcement point and semantic completion.

### Alternatives and unresolved tradeoffs

A monolithic desktop simplifies calls but couples compromise and restart. A
kernel GUI reduces switching but freezes policy and enlarges privilege. Narrow
protected user-space services are preferred; exact domain co-location should
follow measured cost and shared fate, not conceptual diagrams.

## Verification obligations

- Compromise each renderer, adapter, shell, tool, model, compositor, and broker
  independently and enumerate reachable data, devices, and capabilities.
- Generate the manifest dependency graph and compare it with observed restart
  propagation under fault injection.
- Add a new media type and toolkit without privileged-code or kernel-ABI change.

## Connections

- [Internal-service index](README.md) — topology decomposition.
- [Minimal privileged kernel](../../minimal-privileged-kernel-layer.md) — enforcement boundary.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — evidence limits.

## Sources

1. [L4 lessons](../../../30-sources/elphinstone-heiser-2013-l4-lessons.md).
2. [seL4 design principles](../../../30-sources/heiser-2020-sel4-design-principles.md).
3. [Nitpicker](../../../30-sources/feske-helmuth-2005-nitpicker.md).
4. [Chromium UI process architecture](../../../30-sources/chromium-project-2026-multiprocess-graphics-and-accessibility.md).
5. [Qubes GUI virtualization](../../../30-sources/qubes-project-2026-gui-virtualization.md).
