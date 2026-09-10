---
title: "XDG Desktop Portal Interaction, Capture, and Clipboard Sessions"
kind: source
created: "2026-09-10"
authors:
  - "XDG Desktop Portal Project"
published: null
citation_key: "xdg-desktop-portal-project-2026-interaction-sessions"
container: "XDG Desktop Portal documentation"
edition: null
isbn: null
doi: null
url: "https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.RemoteDesktop.html"
accessed: "2026-09-10"
tags:
  - clipboard
  - input-routing
  - remote-desktop
  - screen-capture
aliases:
  - "XDG portal interaction sessions"
---

# XDG Desktop Portal Interaction, Capture, and Clipboard Sessions

## Reference

XDG Desktop Portal Project. [Remote
Desktop](https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.RemoteDesktop.html),
[Clipboard](https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.Clipboard.html),
[ScreenCast](https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.ScreenCast.html),
and [Input
Capture](https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.InputCapture.html)
interface documentation. Accessed 2026-09-10.

## Research question or contribution

How can sandboxed clients request user-mediated, session-scoped remote input,
screen capture, and clipboard access through a desktop broker?

## Method

These are normative first-party interface documents. The review compares
session creation, user selection, device/resource scoping, transfer records,
restore tokens, and cross-interface composition. It does not assess all portal
backend implementations.

## Findings

- Remote-control sessions separate creation, device selection, user-visible
  start, active event transport, and stop.
- Keyboard, pointer, touchscreen, screen streams, and clipboard access are
  separately selected and combined through one session rather than ambiently
  exposed to a sandbox.
- Restore tokens are replaceable, may fail when resources or permission change,
  and do not eliminate fresh policy checks.
- Clipboard ownership advertises formats, transfers data on demand, and uses
  serials plus explicit completion for write requests.
- Event injection and capture are permitted only while the corresponding
  session and device grant are active.

## Relevance

The interfaces provide deployed engineering precedent for composable grants,
session generations, explicit transfer completion, brokered device selection,
and revocable remote-control/capture profiles.

## Limits

Portal object paths and restore tokens are desktop API handles, not durable Atom
capabilities. Backend trust, prompt integrity, data-format parsing, accessibility,
and post-grant policy vary by desktop. The documentation does not guarantee
complete revocation of already disclosed pixels or clipboard bytes.

## Derived work

- [Trusted-interaction internal services](../20-notes/visual-computing-synthesis-components/input-focus-and-trusted-interaction-authority/README.md).
- [Visual-computing internal-services research session](../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md).
