---
title: "Device normalization, event provenance, and seat routing"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - input-routing
  - trusted-path
  - visual-computing
aliases: []
---

# Device normalization, event provenance, and seat routing

This study decomposes [Input, focus, and trusted-interaction authority](../input-focus-and-trusted-interaction-authority.md).

Research question: Which physical or assistive event occurred, on whose seat,
through which current device and broker generations?

## Research basis and status

Wayland groups devices into seats and routes compositor-selected input.
Nitpicker demonstrates trusted routing above isolated clients, while Qubes
prevents one application domain from injecting events into another.
[1](../../../30-sources/wayland-project-2026-architecture-and-protocol.md)
[2](../../../30-sources/feske-helmuth-2005-nitpicker.md)
[3](../../../30-sources/qubes-project-2026-gui-virtualization.md)

Atom event provenance and multi-seat profiles are unimplemented.

## Development

### Owned state and trust boundary

Device services own hardware decoding, device identity, reset generation, and
normalized events. The input broker owns seat membership, ordered seat
sequence, broker incarnation, route class, and trusted/untrusted origin. A raw
event does not name a semantic action or carry project authority.

### Admission, transitions, and completion

Device attach authenticates the driver endpoint and publishes capabilities
before joining a seat. Each event binds device and seat generations, monotonic
sequence, timestamp domain, modality, physical state, and integrity metadata.
The broker orders routing decisions against focus/capture state and
acknowledges only admitted events.

### Failure and adversarial behavior

Device reset, delayed releases, synthetic-event loops, malformed reports,
clock discontinuity, and seat reassignment can create stuck or misrouted input.
Reset advances generation, synthesizes explicit cancellation rather than a
fresh gesture, and closes affected captures and confirmations.

### Alternatives and unresolved tradeoffs

Applications decoding devices gain flexibility but destroy the trusted
provenance boundary. Treating every remote or assistive event as physical hides
different trust assumptions. A common event envelope with explicit origin
profiles is preferred; timestamp and ordering rules across devices remain open.

## Verification obligations

- Reset, detach, and reattach devices between press and release; no late event
  may complete a new gesture.
- Inject synthetic, remote, assistive, and physical events with identical
  payloads and verify policy can distinguish their provenance.
- Flood malformed and high-rate motion while secure attention remains ordered
  and within its declared latency bound.

## Connections

- [Internal-service index](README.md) — trusted-input responsibilities.
- [Focus and capture leases](focus-capture-leases-and-generation-fencing.md) — routing state.
- [Device-service policy](../../otp-like-system-services-components/device-service-policy-and-management/README.md) — lower driver lifecycle.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — evidence boundary.

## Sources

1. [Wayland architecture and protocol](../../../30-sources/wayland-project-2026-architecture-and-protocol.md).
2. [Nitpicker](../../../30-sources/feske-helmuth-2005-nitpicker.md).
3. [Qubes GUI virtualization](../../../30-sources/qubes-project-2026-gui-virtualization.md).
