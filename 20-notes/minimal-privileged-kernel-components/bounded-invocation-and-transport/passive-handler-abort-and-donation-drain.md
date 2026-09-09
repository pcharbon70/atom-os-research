---
title: "Passive handler abort and donation drain"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Passive handler abort and donation drain

How may caller-funded work be terminated without returning a scheduling context that is still executing elsewhere?

## Research basis and status

The seL4 manual warns that a callee can retain donated time by never replying; donation alone is not a return guarantee. [1](../../../30-sources/sel4-foundation-2026-reference-manual.md), [2](../../../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../bounded-invocation-and-transport.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

PassiveCallAdmission includes a shared finite count, cleanup credit and server-consented immutable PassiveAbortPolicy. The active handler records its call identity and donation chain. The default post-accept failure scope is domain-fatal; thread-local CALL_ABORTED requires a trusted profile for an isolated reconstructible worker.

### Admission, transitions and completion

On accepted-call failure, install ABORT_PENDING and a no-entry gate before attempting drain. The generic policy starts domain closing and requires the domain-stop checkpoint conditions; only the trusted isolated-worker profile may use terminal thread-local abort. Close borrowed descendant authority and drain nested calls before returning the unique donated scheduling context to a still-valid predecessor or unbound custody. The success path likewise passes through REPLY_DRAINING before the active-call tag clears.

### Failure and adversarial behavior

Returning donated budget immediately on timeout can let caller and callee spend the same context concurrently. Arbitrary stack cancellation can abandon locks or partially mutated service state. A server-funded handler has no incoming donation to return and may continue on its own budget while borrowed call-scoped products close.

### Alternatives and unresolved tradeoffs

Always server-funded execution avoids this particular donation dependency but changes attribution and overload policy. Passive execution is appropriate only where the server deliberately consents to the conditional failure authority of clients, sessions and endpoint closure.

## Verification obligations

Cancel at every nested call depth, suspend or kill predecessors, and exhaust cleanup reserve. Verify one scheduling-context owner, non-reuse of aborting handlers and no thread-local cancellation without the declared profile. Check success drainage as rigorously as failure drainage.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Exclusive binding, donation and migration](../scheduling-contexts-and-temporal-authority/exclusive-binding-donation-and-migration.md) — Call acceptance and donation share a commit boundary.
- [Recipient fences and service publication](../failure-boundaries-and-recovery-topology/recipient-fences-and-service-publication.md) — Replacement must preserve old call outcomes.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [seL4 reference manual, version 16.0.0](../../../30-sources/sel4-foundation-2026-reference-manual.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Scheduling-context capabilities: A principled, light-weight operating-system mechanism for managing time](../../../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md) — comparative evidence; its methods and limits are recorded in the source note.
