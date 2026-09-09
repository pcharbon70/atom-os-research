---
title: "How to (and how not to) use seL4 IPC"
kind: source
created: "2026-09-09"
authors: ["Gernot Heiser"]
published: 2019
citation_key: "heiser-2019-sel4-ipc-design"
container: "microkerneldude"
edition: "Updated 2021-01-30"
isbn: null
doi: null
url: "https://microkerneldude.org/2019/03/07/how-to-and-how-not-to-use-sel4-ipc/"
accessed: "2026-09-09"
tags: [capabilities, kernel-internal-services, microkernels]
aliases: []
---

# How to (and how not to) use seL4 IPC

## Reference

Gernot Heiser. [How to (and how not to) use seL4 IPC](https://microkerneldude.org/2019/03/07/how-to-and-how-not-to-use-sel4-ipc/). microkerneldude; 2019. Updated 2021-01-30. Accessed 2026-09-09.

## Research question or contribution

Which communication responsibilities should a minimal privileged IPC mechanism own?

## Method

Read the complete article, including its correction on passive-server queue depth.

## Findings

Heiser advocates small cross-domain function calls, notifications for synchronization and shared buffers for bulk transfer. The corrected article allows many queued clients for passive servers; the single-client queue argument does not apply universally.

## Relevance

Keep invocation, event coalescing and buffer ownership separate. Queue capacity and passive-server cancellation still require explicit admission contracts.

## Limits

This is first-person engineering guidance, not a general latency or security proof. Its advice against cross-core IPC and its suggested payload size are design preferences, not accepted Atom limits. Statements about MCS development describe the article's historical context.

## Derived work

- [Endpoint admission and call records](../20-notes/minimal-privileged-kernel-components/bounded-invocation-and-transport/endpoint-admission-and-call-records.md) — proposed contract constrained by this evidence.
- [Notifications and sticky event state](../20-notes/minimal-privileged-kernel-components/bounded-invocation-and-transport/notifications-and-sticky-event-state.md) — proposed contract constrained by this evidence.
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md) — selective architectural context.
