---
title: "Drag/drop, clipboard, and format confinement"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - capability-security
  - clipboard
  - trusted-path
aliases: []
---

# Drag/drop, clipboard, and format confinement

This study decomposes [Input, focus, and trusted-interaction authority](../input-focus-and-trusted-interaction-authority.md).

Research question: How can user-directed cross-domain transfer avoid ambient
clipboard access, confused deputies, parser compromise, and ambiguous receipt?

## Research basis and status

Wayland couples selection/data transfer to compositor-mediated serials. Qubes
uses explicit user keystrokes for cross-domain clipboard transfer. XDG portals
provide session-scoped clipboard ownership and serialized transfers for
sandboxed remote/input sessions.
[1](../../../30-sources/wayland-project-2026-architecture-and-protocol.md)
[2](../../../30-sources/qubes-project-2026-gui-virtualization.md)
[3](../../../30-sources/xdg-desktop-portal-project-2026-interaction-sessions.md)

No Atom transfer format or confinement test exists.

## Development

### Owned state and trust boundary

The transfer broker owns source/destination identities, offered formats,
disclosure class, user gesture evidence, byte/object quotas, expiry, and
transfer operation ID. Sources own original content; destinations select a
format. Parsers and converters run in isolated domains with no unrelated
project authority.

### Admission, transitions, and completion

Drag begins from a current capture and creates a preview-only offer. Drop binds
the visible target and one selected object/format to a one-use grant. Clipboard
ownership is explicit and read access is requested per session. Transfer
completion records bytes/object digest and destination admission separately
from source read success.

### Failure and adversarial behavior

Clipboard polling, format bombs, parser exploits, misleading previews,
destination replacement, and crash after receiving bytes can leak or duplicate
state. Lazy disclosure, MIME/schema allowlists, bounded converters, target
generation checks, and durable operation status constrain the path.

### Alternatives and unresolved tradeoffs

A global clipboard is convenient but ambient. Copying only plain text is safer
but destroys rich semantics. Typed object transfer with deliberately selected
degradation is preferred; history retention, previews, and cross-device
encryption profiles remain open.

## Verification obligations

- Attempt clipboard polling and reads outside an active grant; disclose no
  content or format metadata.
- Fuzz every supported format and converter under memory, CPU, recursion, and
  output-expansion bounds.
- Crash source, broker, converter, and destination at every transition and
  reconcile receipt without repeating a user-visible effect.

## Connections

- [Internal-service index](README.md) — cross-domain input authority.
- [Project authority rehydration](../user-owned-project-graph-and-composition/authority-intent-rehydration-and-revocation.md) — target object facets.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — provenance.

## Sources

1. [Wayland architecture and protocol](../../../30-sources/wayland-project-2026-architecture-and-protocol.md).
2. [Qubes GUI virtualization](../../../30-sources/qubes-project-2026-gui-virtualization.md).
3. [XDG portal interaction sessions](../../../30-sources/xdg-desktop-portal-project-2026-interaction-sessions.md).
