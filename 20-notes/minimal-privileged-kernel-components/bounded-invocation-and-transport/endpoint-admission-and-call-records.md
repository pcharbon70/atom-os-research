---
title: "Endpoint admission and call records"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Endpoint admission and call records

What must be reserved before a request can become an accepted service invocation?

## Research basis and status

Small protected-call guidance does not eliminate queue growth or receiver-capacity obligations. [1](../../../30-sources/heiser-2019-sel4-ipc-design.md), [2](../../../30-sources/shapiro-2003-synchronous-ipc-vulnerabilities.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../bounded-invocation-and-transport.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

An endpoint generation fixes payload bounds, funding mode, queue capacity, closure behavior and cancellation profile. A caller-funded CallRecord holds copied small arguments, exact peer generations, reservations, deadline, prospective transfer and terminal-outcome state. It is not an arbitrary BEAM mailbox or a kernel-managed bulk buffer.

### Admission, transitions and completion

Validate the caller's outbound gate and endpoint authority, reserve the call record and any receiver-consented slot, then queue a pending call. Acceptance atomically binds the receiver and reply token, commits any transfer, consumes shared passive admission and establishes a valid funding source. The receiver becomes Ready; actual execution still requires positive budget and current domain/thread gates.

### Failure and adversarial behavior

An endpoint with finite messages but unbounded pending reply or cancellation metadata remains unbounded. Capability copies of PassiveCallAdmission must refer to the same protected counter rather than multiplying uses. A rejected request must not deliver an argument pointer that the receiver later dereferences.

### Alternatives and unresolved tradeoffs

Server-funded endpoints reduce clients' ability to force handler termination, while passive endpoints provide causal time attribution with a stronger abort contract. Funding mode is immutable for the endpoint generation so callers can reason about failure consequences before admission.

## Verification obligations

Exhaust each reservation separately, queue multiple clients and race accept with endpoint close. Verify no receiver effect for NotAccepted, exactly one admission debit for acceptance and no execution without usable handler budget.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Exclusive binding, donation and migration](../scheduling-contexts-and-temporal-authority/exclusive-binding-donation-and-migration.md) — Call acceptance and donation share a commit boundary.
- [Recipient fences and service publication](../failure-boundaries-and-recovery-topology/recipient-fences-and-service-publication.md) — Replacement must preserve old call outcomes.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [How to (and how not to) use seL4 IPC](../../../30-sources/heiser-2019-sel4-ipc-design.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Vulnerabilities in synchronous IPC designs](../../../30-sources/shapiro-2003-synchronous-ipc-vulnerabilities.md) — comparative evidence; its methods and limits are recorded in the source note.
