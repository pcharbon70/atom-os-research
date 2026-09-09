---
title: "Recipient fences and service publication"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Recipient fences and service publication

Where must an epoch be checked to prevent a stale manager from changing a recovered service?

## Research basis and status

Recovery experiments show that restarting execution does not automatically restore correct interactions with preserved state. [1](../../../30-sources/david-et-al-2008-curios.md), [2](../../../30-sources/chandra-toueg-1996-failure-detectors.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../failure-boundaries-and-recovery-topology.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

Each mutation recipient owns its commit-time fence or a session whose authority closes at takeover. The service registry owns a user-space service epoch and publication condition. Kernel domain generations identify execution objects; they must not be substituted for service protocol identities.

### Admission, transitions and completion

Require current recovery authority and target authority for repair or registry mutations. Publish a replacement only after its configured health and old-incarnation containment requirements are met, using compare-and-swap against the expected old service epoch and fence. Existing calls retain the old endpoint/call identities; clients establish new sessions explicitly after observing failure or replacement.

### Failure and adversarial behavior

Checking a fence only when a connection opens leaves queued stale operations usable after takeover. Redirecting old pending calls to the new service erases acceptance history and may repeat side effects. An external recipient that cannot fence, deduplicate or reconcile remains outside the local recovery guarantee.

### Alternatives and unresolved tradeoffs

Per-operation fence checks provide direct semantics but require protocol support. Revocable sessions can amortize checks if already-admitted operations have defined commit behavior. A local registry cannot make a remote system honor an epoch merely by including it in a message.

## Verification obligations

Pause a registry or state-repair request before commit, advance the lease and attempt publication. Require stale failure and a single replacement epoch. Keep an accepted old call pending through publication and verify that its outcome is not rewritten as a fresh NotAccepted request.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Sealed use facets and epoch sessions](../capability-spaces-and-authority/sealed-use-facets-and-epoch-sessions.md) — Lease enforcement relies on protected facets and closed sessions.
- [Charged reaper and resumable cursors](../teardown-revocation-and-safe-reclamation/charged-reaper-and-resumable-cursors.md) — A successor must continue the same teardown operation.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [CuriOS: Improving reliability through operating system structure](../../../30-sources/david-et-al-2008-curios.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Unreliable failure detectors for reliable distributed systems](../../../30-sources/chandra-toueg-1996-failure-detectors.md) — comparative evidence; its methods and limits are recorded in the source note.
