---
title: "Remote collaborative views, convergence, privacy, and revocation"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - collaborative-computing
  - privacy
  - visual-computing
aliases: []
---

# Remote collaborative views, convergence, privacy, and revocation

This study decomposes [Plural representations and cross-view consistency](../plural-representations-and-cross-view-consistency.md).

Research question: How can remote representations collaborate without
conflating replicated data, projected disclosure, user presence, or authority?

## Research basis and status

Local-first work motivates offline ownership; CRDTs define convergence within
declared datatypes; collaborative access-control research shows authorization
must be composed separately. XDG portal sessions provide a contemporary
example of separately requested observation and control channels.
[1](../../../30-sources/kleppmann-et-al-2019-local-first-software.md)
[2](../../../30-sources/shapiro-et-al-2011-conflict-free-replicated-data-types.md)
[3](../../../30-sources/cherif-et-al-2014-access-control-collaborative-editors.md)
[4](../../../30-sources/xdg-desktop-portal-project-2026-interaction-sessions.md)

No Atom remote-view protocol or privacy evaluation exists.

## Development

### Owned state and trust boundary

Each remote view owns a filtered semantic projection, subscription revision,
presence identity, cursor/selection state, latency budget, and display
capabilities. Project collaboration owns replicated values and membership;
trusted interaction separately owns remote control grants.

### Admission, transitions, and completion

Authenticate the peer and project, select a disclosure policy, then atomically
return a filtered snapshot and stream cursor. Presence and selections are
ephemeral and bounded. Edits enter through typed model commands or declared
replica policy; remote-control input requires a separate visible session.
Revocation closes publication and control paths independently.

### Failure and adversarial behavior

Offline revocation, traffic analysis, redacted-structure leakage, stale
presence, duplicate commands, and convergent-but-invalid edits threaten the
model. Authority epochs, filtered subgraphs, batching, operation IDs, type
validation, and explicit conflicts preserve distinct properties.

### Alternatives and unresolved tradeoffs

Pixel streaming minimizes semantic protocol work but leaks presentation and
limits accessibility. Full project replication improves local capability but
widens disclosure. Selectable semantic, pixel, value-replica, and control
profiles are preferred; metadata leakage and long-offline policy remain open.

## Verification obligations

- Revoke observation, collaboration, and control independently during offline
  and active sessions; no data merge may restore authority.
- Compare filtered graph, traffic, timing, counts, presence, and error channels
  for excluded-object leakage.
- Drop and duplicate remote updates and commands; recover-HOOD consumers resynchronize
  while admitted effects reconcile by operation ID.

## Connections

- [Internal-service index](README.md) — remote representation scope.
- [Project collaboration](../user-owned-project-graph-and-composition/collaboration-replica-membership-and-conflict.md) — durable replica policy.
- [Remote interaction authority](../input-focus-and-trusted-interaction-authority/screen-capture-remote-control-and-context-integrity.md) — separate control.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — evidence limits.

## Sources

1. [Local-first software](../../../30-sources/kleppmann-et-al-2019-local-first-software.md).
2. [Conflict-free replicated data types](../../../30-sources/shapiro-et-al-2011-conflict-free-replicated-data-types.md).
3. [Access control for collaborative editors](../../../30-sources/cherif-et-al-2014-access-control-collaborative-editors.md).
4. [XDG portal interaction sessions](../../../30-sources/xdg-desktop-portal-project-2026-interaction-sessions.md).
