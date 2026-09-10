---
title: "Focus/capture leases and generation fencing"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - focus-management
  - input-routing
  - trusted-path
aliases: []
---

# Focus/capture leases and generation fencing

This study decomposes [Input, focus, and trusted-interaction authority](../input-focus-and-trusted-interaction-authority.md).

Research question: How are keyboard focus, pointer/touch capture, and gesture
ownership made explicit, bounded, and stale-safe?

## Research basis and status

Wayland uses compositor focus and event serials for sensitive interactive
operations. Chromium routes input through browser-owned frame identity, and
Qubes confines events to the focused application's domain.
[1](../../../30-sources/wayland-project-2026-architecture-and-protocol.md)
[2](../../../30-sources/chromium-project-2026-multiprocess-graphics-and-accessibility.md)
[3](../../../30-sources/qubes-project-2026-gui-virtualization.md)

The proposed lease state machines have not been model checked.

## Development

### Owned state and trust boundary

The broker owns per-seat focus generation, keyboard target, pointer/touch
capture records, gesture IDs, route reason, expiry, and compositor generation.
Semantic focus is an accessibility/view concept and cannot itself redirect
hardware events.

### Admission, transitions, and completion

Focus transfer validates current surface/view generations and trusted policy.
Capture derives from an admitted press or touch sequence and is limited to its
device contacts, target, operations, and deadline. Release, target death,
compositor restart, secure attention, or lease expiry closes capture before a
new route becomes active.

### Failure and adversarial behavior

Focus stealing, popup replacement, hidden capture, missing release, double
clicks across targets, and stale compositor replies can authorize the wrong
context. Broker serialization, current-scene evidence, explicit cancellation,
and receiver-side generations reject late or cross-target transitions.

### Alternatives and unresolved tradeoffs

Focus-follows-pointer reduces clicks but increases accidental authority.
Unbounded grabs simplify legacy interaction but permit denial of service.
Short explicit leases with visible trusted context are preferred; exact
gesture and accessibility accommodation profiles require user testing.

## Verification obligations

- Reproduce focus theft, rapid target replacement, hidden overlays, double
  click, drag, and missing-release schedules.
- Crash broker, compositor, and client before/after every transfer; old events
  and grants must not survive the generation transition.
- Perform equivalent tasks with pointer, keyboard, switch, screen reader,
  voice, and remote seats and test both access and principal comprehension.

## Connections

- [Internal-service index](README.md) — input authority context.
- [Semantic focus continuity](../semantics-first-accessible-ui-protocol/focus-selection-virtualization-and-consumer-continuity.md) — non-routing focus.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — sources.

## Sources

1. [Wayland architecture and protocol](../../../30-sources/wayland-project-2026-architecture-and-protocol.md).
2. [Chromium UI process architecture](../../../30-sources/chromium-project-2026-multiprocess-graphics-and-accessibility.md).
3. [Qubes GUI virtualization](../../../30-sources/qubes-project-2026-gui-virtualization.md).
