---
title: "Recovery escrow and reserve admission"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Recovery escrow and reserve admission

How can a successor recover a domain when both the child and its replaceable supervisor are unusable?

## Research basis and status

Explicit resource attribution provides the accounting foundation; independently escrowed recovery authority is an Atom proposal. [1](../../../30-sources/banga-et-al-1999-resource-containers.md), [2](../../../30-sources/elkaduwe-et-al-2008-kernel-memory-isolation.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../failure-boundaries-and-recovery-topology.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

RecoveryEscrow holds predeposited attenuated lifecycle facets, replacement templates, slots and resource reservations. It is derived independently of the child and replaceable supervisor and controlled by a narrow RecoveryControl. It excludes ambient root authority and does not store a policy for arbitrary restart.

### Admission, transitions and completion

At deployment admission, prove that the escrow can instantiate the named successor with protected destination slots, scheduling capacity and a live fault/cleanup path. Reserve enough for the declared simultaneous failure set. Issue only the current sealed lease-use and authorized target facets; a successor must not recover its own power by reading the dead supervisor's capability table.

### Failure and adversarial behavior

A reserve whose anchor closes when the supervisor dies is not escrow. Sufficient bytes without usable slot capacity or time budget can still make takeover impossible. Repeated failed replacements must not silently consume unbounded reserved memory or duplicate authority.

### Alternatives and unresolved tradeoffs

Predepositing exact successor resources provides predictable failure behavior but limits dynamic replacement. A trusted resource service can provision more flexibly only if it is outside the protected failure scope and its own capacity/availability assumptions are recorded.

## Verification obligations

Destroy the old supervisor's capability table, exhaust every child account and then attempt takeover. Verify that only precommitted authority is issued, that failed attempts remain accounted and that reserve exhaustion yields explicit escalation rather than ambient privilege reconstruction.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Sealed use facets and epoch sessions](../capability-spaces-and-authority/sealed-use-facets-and-epoch-sessions.md) — Lease enforcement relies on protected facets and closed sessions.
- [Charged reaper and resumable cursors](../teardown-revocation-and-safe-reclamation/charged-reaper-and-resumable-cursors.md) — A successor must continue the same teardown operation.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Resource containers: A new facility for resource management in server systems](../../../30-sources/banga-et-al-1999-resource-containers.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Kernel design for isolation and assurance of physical memory](../../../30-sources/elkaduwe-et-al-2008-kernel-memory-isolation.md) — comparative evidence; its methods and limits are recorded in the source note.
