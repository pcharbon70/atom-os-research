---
title: "Headless boot, dependency cuts, and recovery console"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - boot
  - fault-tolerance
  - visual-computing
aliases: []
---

# Headless boot, dependency cuts, and recovery console

This study decomposes [Cross-layer placement and recovery topology](../cross-layer-placement-and-recovery-topology.md).

Research question: What minimal dependency cut can open durable projects,
diagnose failure, revoke authority, and recover service without the ordinary
desktop?

## Research basis and status

Crash-only and microreboot work make recovery paths explicit services rather
than exceptional afterthoughts. seL4 design principles support minimizing the
privileged base, and Chromium retains software rendering when GPU acceleration
is unavailable.
[1](../../../30-sources/candea-fox-2003-crash-only-software.md)
[2](../../../30-sources/candea-et-al-2004-microreboot.md)
[3](../../../30-sources/heiser-2020-sel4-design-principles.md)
[4](../../../30-sources/chromium-project-2026-multiprocess-graphics-and-accessibility.md)

This is full-system architecture research; it does not alter the current CLI
PoC scope or claim that the path boots.

## Development

### Owned state and trust boundary

The recovery root owns a statically auditable manifest for console I/O,
authentication, authority revocation, project enumeration, evidence access,
service restart, and safe shutdown. It does not depend on GPU, general
toolkits, package registries, network identity, or user project renderers.

### Admission, transitions, and completion

Boot establishes kernel mechanisms, trusted storage/evidence, minimal identity
and policy, and a serial/text console before optional visual services. A
software trusted display may be added only after its device/input dependencies
are explicit. Recovery actions use narrow facets and durable outcomes; ordinary
desktop readiness is not a prerequisite.

### Failure and adversarial behavior

Corrupt manifests, unavailable storage, exhausted memory, broken GPU,
compromised compositor, and authentication-service loss can create circular
recovery. Fixed bounds, offline credentials or recovery keys, reserved
resources, immutable fallback artifacts, and independent revocation cut those
cycles.

### Alternatives and unresolved tradeoffs

Using the normal desktop for recovery improves familiarity but shares its
failures. Firmware-only recovery lacks project semantics and audit. A bounded
text-first path with optional software graphics is preferred; physical
presence, accessibility, and credential-recovery policy remain open.

## Verification obligations

- Remove network, GPU, package registry, and ordinary project services; boot
  the recovery path and inspect/revoke/restart under declared bounds.
- Corrupt each recovery dependency and prove the system exposes the exact
  missing root rather than entering a silent loop.
- Exhaust CPU, memory, mailbox, storage, capability, and device resources while
  meeting the recovery-console deadline.

## Connections

- [Internal-service index](README.md) — recovery topology.
- [Resource reserve](resource-reserve-overload-and-fault-containment.md) — guaranteed capacity.
- [Proof-of-concept planning](../../../60-planning/01-proof-of-concept/README.md) — separate current implementation scope.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — evidence boundary.

## Sources

1. [Crash-only software](../../../30-sources/candea-fox-2003-crash-only-software.md).
2. [Microreboot](../../../30-sources/candea-et-al-2004-microreboot.md).
3. [seL4 design principles](../../../30-sources/heiser-2020-sel4-design-principles.md).
4. [Chromium UI process architecture](../../../30-sources/chromium-project-2026-multiprocess-graphics-and-accessibility.md).
