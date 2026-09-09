---
title: "Signal dispatch, priority and alias admission"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - actor-model
  - beam
  - managed-runtime
  - system-architecture
aliases: []
---

# Signal dispatch, priority and alias admission

This study decomposes [Signal ingress, mailboxes and selective receive](../signal-ingress-mailboxes-and-selective-receive.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

OTP distinguishes signal receipt from priority-message placement; aliases constrain insertion without canceling the source operation. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md), [2](../../../30-sources/hogberg-2021-message-passing.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Physical enqueue order, ordered signal delivery and selective mailbox placement are three separate contracts.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own the receiver-side signal dispatcher, priority/ordinary mailbox partitions and bounded control-work cursor. Relation managers own relation state; this service applies their generation-checked signal effects in the required order.

### Admission, transitions and completion

Process ordered ingress before classifying mailbox placement. A priority-alias message may be placed ahead of an earlier ordinary message only after the corresponding signals have arrived in order. Recheck alias activity at insertion. Link, monitor, exit and timer signals retain their typed semantics rather than being blindly converted to message tuples.

### Failure and adversarial behavior

A deactivated alias rejects an in-flight reply not yet inserted but cannot remove previously queued messages. Unbounded priority traffic can starve ordinary messages even when ingress is correct; reserve accounting and policy must make that risk visible without inventing stronger compatible fairness.

### Alternatives and unresolved tradeoffs

A single combined mailbox with a partition boundary can simplify scans; separate lists can simplify priority insertion but require cursor rules across both. Keep placement semantics stable while changing the representation.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Deliver ordinary then priority signals from one sender; preserve receipt order while allowing documented placement.
- Deactivate an alias at each boundary from send to mailbox insertion.
- Mix exit/control bursts with ordinary traffic and measure bounded dispatcher work and starvation.

Record the exact profile, tested revision, schedule/input bounds and resource
observations before claiming this contract holds. A semantic pass does not
establish latency or corruption containment.

## Connections

- [Component service index](README.md) — sibling responsibilities and shared boundaries.
- [Relation state ownership](../actor-identity-lifecycle-and-process-state/links-monitors-aliases-and-name-registration.md) — a contract this service must compose with.
- [Payload lifetime and adoption](../terms-private-heaps-shared-binaries-and-tracing-collection/shared-binary-literal-and-fragment-lifetimes.md) — a contract this service must compose with.
- [Open runtime inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — unresolved design and evidence.
- [Research session](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — source manifest and reading limitations.

## Sources

1. [OTP 29.0.6 managed-runtime documentation](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md).
2. [A few notes on message passing](../../../30-sources/hogberg-2021-message-passing.md).
