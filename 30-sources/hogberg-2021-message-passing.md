---
title: "A few notes on message passing"
kind: source
created: "2026-09-02"
authors:
  - "John Högberg"
published: "2021-03-19"
citation_key: "hogberg-2021-message-passing"
container: "Erlang/OTP Blog"
edition: null
isbn: null
doi: null
url: "https://www.erlang.org/blog/message-passing/"
accessed: "2026-09-02"
tags:
  - erlang
  - erts
  - mailboxes
  - message-passing
  - selective-receive
aliases:
  - "Erlang message passing notes"
---

# A few notes on message passing

## Reference

John Högberg. “[A few notes on message
passing](https://www.erlang.org/blog/message-passing/).” *Erlang/OTP Blog*,
2021-03-19. Accessed 2026-09-02.

## Contribution

This official engineering article explains the distinction between signals,
signal queues, message queues, message copying, and selective receive in the
then-current ERTS implementation. It also identifies the exact ordering
guarantee on which links, monitors, and request/reply idioms rely.

## Method

The author develops small Erlang examples and an implementation-level account
of sending and receiving. The article describes OTP 24-era optimization work;
current public semantics were checked separately against OTP 29 documentation.

## Findings

- ERTS continuously accepts many signal types. A `receive` expression searches
  messages already transferred to a process’s message queue rather than being
  the primitive that first accepts a signal.
- Signals sent from one entity to one destination retain sender order. Signals
  from different senders do not have a global arrival order.
- Ordinary local message payloads are copied for the recipient. The design
  spends bandwidth to keep most collection process-local and pauses short;
  large binaries and other special terms qualify the simple copy model.
- On-heap and off-heap queued messages trade ordinary send cost against
  receiver contention and the cost of scanning messages during garbage
  collection.
- Selective receive scans in arrival order until a pattern matches. Unique
  references let the compiler start some searches later in the queue, but the
  general search can still be linear in skipped backlog.
- A broken distribution connection leaves ambiguity about whether a remote
  request was processed before the connection failed.

## Relevance

The article gives the managed runtime a precise semantic floor: preserve
per-sender signal order, do not promise a cross-sender total order, charge
selective-receive scanning as work, and expose queue memory independently of
live actor heap memory. It also supports correlation references and revocable
aliases as both protocol and backlog-management tools.

## Limits

This is a maintainer explanation, not a peer-reviewed performance evaluation.
Several details describe OTP 24-era internals and may change without changing
the language contract. The paper does not define admission control, mailbox
bounds, hostile-sender isolation, or a kernel/runtime interface.

## Derived work

- [Managed actor runtime layer](../20-notes/managed-actor-runtime-layer.md)
- [Signal ingress, mailboxes, and selective receive](../20-notes/managed-actor-runtime-components/signal-ingress-mailboxes-and-selective-receive.md)
- [Managed actor runtime map](../10-maps/managed-actor-runtime.md)
- [Managed-runtime contract inquiry](../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md)
- [2026-09-02 research journal](../50-journal/2026-09-02-managed-actor-runtime-deep-dive.md)
- [2026-09-03 component research journal](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md)
