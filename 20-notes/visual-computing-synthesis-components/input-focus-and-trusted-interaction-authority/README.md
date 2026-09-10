---
title: "Input, focus, and trusted-interaction authority: internal services"
kind: map
created: "2026-09-10"
tags:
  - input-routing
  - trusted-path
  - visual-computing
aliases: []
---

# Input, focus, and trusted-interaction authority: internal services

## Purpose

Separate device provenance, focus/capture state, cross-domain transfer,
protected ceremonies, and remote observation or control.

This directory decomposes [Input, focus, and trusted-interaction authority](../input-focus-and-trusted-interaction-authority.md).

## What belongs here

Keep broker state, grant boundaries, transition evidence, adversarial cases,
and unexecuted verification obligations here. Hardware and compositor
mechanisms are dependencies rather than implied implementation results. The
[session manifest](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md)
records provenance.

## Index

### Subdirectories

- None yet.

### Documents

- [Device normalization, event provenance, and seat routing](device-normalization-event-provenance-and-seat-routing.md) — Which device event occurred, on whose seat, and through which current path?
- [Focus/capture leases and generation fencing](focus-capture-leases-and-generation-fencing.md) — How are keyboard, pointer, touch, and gesture routes made explicit and stale-safe?
- [Drag/drop, clipboard, and format confinement](drag-drop-clipboard-and-format-confinement.md) — How does cross-domain data transfer remain user-directed and parser-confined?
- [Secure attention, confirmation, and global shortcuts](secure-attention-confirmation-and-global-shortcuts.md) — Which gestures cannot be spoofed or captured by ordinary clients?
- [Screen capture, remote control, and context integrity](screen-capture-remote-control-and-context-integrity.md) — How are observation and control separately scoped, visible, revocable, and auditable?

## Maintaining this index

Inventory every direct child. Keep the parent, trusted-interaction research,
component index, map, and inquiry synchronized when authority boundaries change.
