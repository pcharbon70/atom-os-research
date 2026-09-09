---
title: "State reconstruction and root fallback"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# State reconstruction and root fallback

What state may a replacement trust, and where does recovery stop when its final independent controller fails?

## Research basis and status

CuriOS explicitly discusses damaged client state and non-transparent external effects after restart. [1](../../../30-sources/david-et-al-2008-curios.md), [2](../../../30-sources/goyal-et-al-2005-kdump.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../failure-boundaries-and-recovery-topology.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

Unprivileged recovery policy classifies ephemeral heap, validated client state, durable state, caches, shared memory, device state and external effects. The kernel supplies isolation, current authority and teardown evidence. It does not interpret service schemas or restore arbitrary managed heaps; BEAM garbage collection remains a runtime responsibility.

### Admission, transitions and completion

Create a replacement domain from an authorized fresh manifest, reconstruct only validated state under its protocol version, and reconcile ambiguous accepted operations before publication. Preserve exact custody of quarantined resources rather than presenting them as free replacement capacity. If independent root control, reserved slots or usable recovery execution is lost, follow the declared node/external fallback.

### Failure and adversarial behavior

Restoring an entire failed heap can restore the corruption that caused failure. Checksums show accidental change, not semantic validity. A second kernel or external controller can assist recovery only if its memory, entry and device assumptions survive; it is not an unconditional escape hatch.

### Alternatives and unresolved tradeoffs

Reconstructing state from narrow external records reduces inherited corruption but can increase latency and require application-specific repair. Transparent retry is safe only for protocols that prove its effect semantics. Otherwise expose uncertainty to clients rather than promise uninterrupted service.

## Verification obligations

Corrupt one client record, preserve an already committed external effect and lose the final recovery controller. Require scoped validation failures, no blind duplicate action and explicit node/external escalation. Distinguish recovered service availability from preservation of every client's session.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Sealed use facets and epoch sessions](../capability-spaces-and-authority/sealed-use-facets-and-epoch-sessions.md) — Lease enforcement relies on protected facets and closed sessions.
- [Charged reaper and resumable cursors](../teardown-revocation-and-safe-reclamation/charged-reaper-and-resumable-cursors.md) — A successor must continue the same teardown operation.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [CuriOS: Improving reliability through operating system structure](../../../30-sources/david-et-al-2008-curios.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Kdump: A kexec-based kernel crash dumping mechanism](../../../30-sources/goyal-et-al-2005-kdump.md) — comparative evidence; its methods and limits are recorded in the source note.
