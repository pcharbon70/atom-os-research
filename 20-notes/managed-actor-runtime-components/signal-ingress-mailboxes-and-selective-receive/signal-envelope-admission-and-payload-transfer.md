---
title: "Signal envelope admission and payload transfer"
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

# Signal envelope admission and payload transfer

This study decomposes [Signal ingress, mailboxes and selective receive](../signal-ingress-mailboxes-and-selective-receive.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

Message-passing engineering separates signal transport from receiver-owned messages; resource attribution must survive asynchronous execution. [1](../../../30-sources/hogberg-2021-message-passing.md), [2](../../../30-sources/banga-et-al-1999-resource-containers.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Physical enqueue order, ordered signal delivery and selective mailbox placement are three separate contracts.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own a prepared envelope containing source/destination incarnations, signal kind, order-domain identity, payload storage, correlation and charge. The sender owns private construction; publication transfers cleanup responsibility to the destination-generation path.

### Admission, transitions and completion

Resolve and pin the destination, measure bounded payload requirements and reserve queue/fragment capacity before copying. Revalidate destination state at publication. After successful publication, the receiver or its exit cleanup owns the object even if the sender dies before returning; wakeup merely announces possible work.

### Failure and adversarial behavior

Rollback may release an unpublished fragment but cannot retract a node another worker can observe. A dead destination follows the selected language contract while releasing preparation resources. Compatible ordinary sends do not gain a silent quota-drop policy or a new delivery-completion return value.

### Alternatives and unresolved tradeoffs

Direct receiver-heap construction can avoid intermediate copying only under a proved exclusion protocol and measured benefit. Private off-heap preparation simplifies concurrent GC and has an explicit extra allocation cost. Decide separately from mailbox overload policy.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Kill sender immediately before and after publication and check exact charge transfer.
- Collect receiver while multiple senders build large payloads.
- Refuse admission at each resource boundary without leaving partially visible signals.

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

1. [A few notes on message passing](../../../30-sources/hogberg-2021-message-passing.md).
2. [Resource containers](../../../30-sources/banga-et-al-1999-resource-containers.md).
