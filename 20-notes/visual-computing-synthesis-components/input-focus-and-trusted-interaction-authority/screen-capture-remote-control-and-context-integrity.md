---
title: "Screen capture, remote control, and context integrity"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - remote-desktop
  - screen-capture
  - trusted-path
aliases: []
---

# Screen capture, remote control, and context integrity

This study decomposes [Input, focus, and trusted-interaction authority](../input-focus-and-trusted-interaction-authority.md).

Research question: How are observation, input injection, clipboard access, and
remote administration separately scoped, visible, revocable, and auditable?

## Research basis and status

XDG portals separate session creation, device selection, screen sources,
clipboard enablement, and user approval. PipeWire portal access demonstrates
restricted object visibility and later permission removal. User-driven access
control motivates binding selection to authentic user interaction.
[1](../../../30-sources/xdg-desktop-portal-project-2026-interaction-sessions.md)
[2](../../../30-sources/roesner-et-al-2012-user-driven-access-control.md)

The Atom remote-seat, capture, and indicator protocols are unimplemented.

## Development

### Owned state and trust boundary

The broker owns separate capture and control facets, selected surfaces/projects,
input device classes, remote principal, session generation, clipboard option,
expiry, visibility indicator, and revocation status. A capture consumer never
receives control merely because it can see pixels.

### Admission, transitions, and completion

User or policy selects exact sources and devices in a trusted ceremony.
Starting creates a fresh session and restricted data/control endpoints.
Persistent authorization stores policy intent, not a reusable active session;
restore revalidates resources and issues a new generation. Revocation closes
streams and receiver permissions before reporting completion.

### Failure and adversarial behavior

Indicator spoofing, hidden windows, stale restore tokens, screen changes,
remote input after revocation, and clipboard expansion are expected. Trusted
indicators, one-use restoration, per-frame/source labels, event generations,
and independent permission enforcement constrain the path.

### Alternatives and unresolved tradeoffs

Whole-desktop sharing is simple but overdiscloses. Semantic-only sharing
protects pixels but cannot support all workflows. Separately selectable
semantic, surface, audio, clipboard, and control facets are preferred; covert
channels and remote secure-attention policy remain open.

## Verification obligations

- Start every combination of observation/control facets and attempt each
  omitted operation; no implicit upgrade is permitted.
- Revoke during active key, touch, clipboard, and frame transfer and prove all
  receivers reject later generation traffic.
- Change selected surface, workspace, principal, and policy under capture;
  context mismatch must stop or require explicit reauthorization.

## Connections

- [Internal-service index](README.md) — remote interaction boundary.
- [Projection filtering](../semantics-first-accessible-ui-protocol/projection-filtering-redaction-and-platform-adapters.md) — semantic disclosure.
- [Remote collaborative views](../plural-representations-and-cross-view-consistency/remote-collaborative-views-convergence-privacy-and-revocation.md) — collaboration semantics.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — provenance.

## Sources

1. [XDG portal interaction sessions](../../../30-sources/xdg-desktop-portal-project-2026-interaction-sessions.md).
2. [User-driven access control](../../../30-sources/roesner-et-al-2012-user-driven-access-control.md).
