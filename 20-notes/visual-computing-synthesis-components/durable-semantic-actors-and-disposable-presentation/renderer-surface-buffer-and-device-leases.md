---
title: "Renderer, surface, buffer, and device leases"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - compositor
  - resource-management
  - visual-computing
aliases: []
---

# Renderer, surface, buffer, and device leases

This study decomposes [Durable semantic actors and disposable presentation](../durable-semantic-actors-and-disposable-presentation.md).

Research question: Which rendering resources are disposable leases, and how
are stale ownership, buffer reuse, and device reset fenced?

## Research basis and status

Wayland separates client buffers and surfaces from compositor ownership.
Nitpicker demonstrates a small trusted compositor boundary, and Chromium
documents renderer/GPU-process separation plus software fallback.
[1](../../../30-sources/wayland-project-2026-architecture-and-protocol.md)
[2](../../../30-sources/feske-helmuth-2005-nitpicker.md)
[3](../../../30-sources/chromium-project-2026-multiprocess-graphics-and-accessibility.md)

No Atom display or GPU lease implementation exists.

## Development

### Owned state and trust boundary

The compositor owns surface generations, scene placement, accepted frame
sequence, and presentation acknowledgement. Renderer domains own only leased
buffers and derived caches. A device service owns queue, memory-mapping, reset,
and fault generations. No surface or buffer handle names semantic state.

### Admission, transitions, and completion

A view generation requests a bounded surface lease. Buffer allocation charges
the project account and binds renderer, surface, device, format, size, and
expiry. Submit checks every generation and damage bound; presentation returns
an acknowledgement or discard reason. Release is idempotent, while forced
reclamation advances generations before reuse.

### Failure and adversarial behavior

Stale frames, oversized damage, aliasing, use-after-revoke, GPU hangs, and
malformed command streams are expected. Device parsing remains isolated;
receiver-side checks reject old queues and buffers; compositor survival does
not depend on a renderer releasing its own resources; a CPU path preserves
minimal display after device loss.

### Alternatives and unresolved tradeoffs

Shared in-process graphics reduces copying but merges trust and failure.
Copy-only composition is simpler but costly. Lease-backed shared buffers with
explicit ownership transitions are preferred; zero-copy eligibility and GPU
reset granularity remain hardware-profile questions.

## Verification obligations

- Reuse every surface, buffer, and queue identifier after restart and submit
  old frames; none may become current.
- Crash renderer, compositor, and device service at every ownership transition
  and account for all pages and capabilities.
- Hang and reset the GPU under load, then restore a bounded software recovery
  display without restarting model actors.

## Connections

- [Internal-service index](README.md) — reconstructible presentation state.
- [Device-service policy](../../otp-like-system-services-components/device-service-policy-and-management/README.md) — lower device lifecycle.
- [Recovery topology](../cross-layer-placement-and-recovery-topology/README.md) — independent recovery holders.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — provenance.

## Sources

1. [Wayland architecture and protocol](../../../30-sources/wayland-project-2026-architecture-and-protocol.md).
2. [Nitpicker](../../../30-sources/feske-helmuth-2005-nitpicker.md).
3. [Chromium UI process architecture](../../../30-sources/chromium-project-2026-multiprocess-graphics-and-accessibility.md).
