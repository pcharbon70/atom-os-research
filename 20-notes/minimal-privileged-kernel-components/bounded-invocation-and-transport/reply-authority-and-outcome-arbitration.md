---
title: "Reply authority and outcome arbitration"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Reply authority and outcome arbitration

What can a caller safely conclude when reply, cancellation and failure race?

## Research basis and status

Synchronous IPC vulnerability analysis motivates treating blocking and timeout behavior as part of the security boundary. [1](../../../30-sources/shapiro-2003-synchronous-ipc-vulnerabilities.md), [2](../../../30-sources/sel4-foundation-2026-reference-manual.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../bounded-invocation-and-transport.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

A ReplyToken is single-use, non-transferable and bound to the exact call, receiver thread and endpoint generations. The call outcome distinguishes MechanismRejected, NotAccepted, ReplyReceived and AcceptedNoReply. These are transport facts; they do not establish durable application commit or exactly-once external action.

### Admission, transitions and completion

All terminal contenders compete for one protected outcome selection. Rejection happens before pending admission; NotAccepted requires that handler acceptance never occurred. Once acceptance wins, cancellation without a reply selects AcceptedNoReply. Reply publication selects ReplyReceived and enters drainage rather than immediately reusing the receiver. Subsequent contenders may assist cleanup but cannot rewrite the selected outcome.

### Failure and adversarial behavior

A server can perform a device write and crash before replying. Returning NotAccepted in that case invites an unsafe retry. Reusing a reply token or accepting it from another receiver can also target a later call if generations are omitted. A lost outcome notification does not undo the selected result.

### Alternatives and unresolved tradeoffs

A single linearizable arbitration word is attractive, but payload copying and capability transfer need a compatible commit protocol. Exposing a queryable call identity supports reconciliation at the cost of retaining bounded outcome records. Retention expiry must not silently convert uncertainty into non-acceptance.

## Verification obligations

Enumerate reply-versus-timeout, caller death, callee death and endpoint-close interleavings. Require one terminal tag, no reply reuse and correct transfer/outcome consistency. Demonstrate that an externally committed operation can still legitimately produce AcceptedNoReply.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Exclusive binding, donation and migration](../scheduling-contexts-and-temporal-authority/exclusive-binding-donation-and-migration.md) — Call acceptance and donation share a commit boundary.
- [Recipient fences and service publication](../failure-boundaries-and-recovery-topology/recipient-fences-and-service-publication.md) — Replacement must preserve old call outcomes.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Vulnerabilities in synchronous IPC designs](../../../30-sources/shapiro-2003-synchronous-ipc-vulnerabilities.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [seL4 reference manual, version 16.0.0](../../../30-sources/sel4-foundation-2026-reference-manual.md) — comparative evidence; its methods and limits are recorded in the source note.
