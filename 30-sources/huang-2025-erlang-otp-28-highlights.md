---
title: "Erlang/OTP 28 Highlights"
kind: source
created: "2026-09-03"
authors:
  - "Isabell Huang"
published: "2025-05-20"
citation_key: "huang-2025-erlang-otp-28-highlights"
container: "Erlang/OTP Blog"
edition: null
isbn: null
doi: null
url: "https://www.erlang.org/blog/highlights-otp-28/"
accessed: "2026-09-03"
tags:
  - erlang
  - mailboxes
  - otp
  - overload-control
  - priority-messages
aliases:
  - "OTP 28 highlights"
---

# Erlang/OTP 28 Highlights

## Reference

Isabell Huang. “[Erlang/OTP 28
Highlights](https://www.erlang.org/blog/highlights-otp-28/).” *Erlang/OTP
Blog*, 2025-05-20. Accessed 2026-09-03.

## Contribution

This official release article surveys selected Erlang/OTP 28 features. The
system-services research uses its priority-message section as maintainer
evidence that control information delivered through an ordinary overloaded
mailbox can arrive too late to govern that overload.

## Method

The author explains release features with small examples and links to the
corresponding EEPs and manuals. The priority-message discussion uses Logger's
queue-length polling as a motivating implementation case. It does not present
a controlled overload evaluation or publish benchmark artifacts.

## Findings

- Ordinary messages normally enter at the end of a process mailbox. A message
  reporting that a mailbox is already long can therefore sit behind the
  backlog it is intended to report.
- The article identifies Logger's queue-length polling and message-shedding
  path as a concrete case that would benefit from prompt queue-state
  notification.
- OTP 28 priority messages are opt-in at the receiver. A process creates and
  distributes a priority-enabled alias; a sender using that alias plus the
  `priority` send option can place a message before ordinary messages, while an
  ordinary send to the same alias remains ordinary.
- Priority messages retain their arrival order relative to other priority
  messages. The article says existing signal-delivery order remains intact if
  signals arrive, while the priority mechanism changes where resulting
  messages are inserted relative to ordinary messages.
- Deactivating the alias removes that priority-send route. Broken-link exit
  signals and monitor notifications instead opt into priority handling through
  priority options on link and monitor creation.

## Relevance

The Logger example supports a separate, bounded control path for overload,
supervision, cancellation, teardown, and lease renewal. It is evidence that
merely sending control information into the same FIFO backlog as ordinary work
can make the control loop ineffective.

Priority delivery is a useful runtime mechanism, but the Atom OS proposal adds
service-layer policy: narrow authority to use the control path, finite reserved
capacity, per-class admission, accounting, and an explicit response when that
capacity is exhausted. Those additions are architectural proposals, not claims
made by the article.

## Limits

This is a maintainer release overview, not a normative specification,
peer-reviewed study, or complete account of Logger. The statement that
priority messages impose no performance penalty is not accompanied by a
benchmark method, workloads, measurements, or tail-latency data. The article
does not establish bounded memory, fair service between priority classes,
starvation freedom, admission control, or resource reservation. Current OTP 29
documentation remains the compatibility authority, and any Atom OS control
queue requires independent overload and adversarial testing.

## Derived work

- [OTP-like system services layer](../20-notes/otp-like-system-services-layer.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
- [OTP-like system-services contract inquiry](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
- [2026-09-03 OTP-like system services deep dive](../50-journal/2026-09-03-otp-like-system-services-deep-dive.md)
