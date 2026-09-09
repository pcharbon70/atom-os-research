---
title: "Quota accounts and charge transfer"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Quota accounts and charge transfer

Who pays for a shared object when the creator, users and cleanup owner differ?

## Research basis and status

Resource containers separate resource attribution from execution and protection entities. [1](../../../30-sources/banga-et-al-1999-resource-containers.md), [2](../../../30-sources/elkaduwe-et-al-2008-kernel-memory-isolation.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../typed-object-storage-and-explicit-memory.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

Each object has exactly one protected payer account at a time. Its lifetime group, authority holders and currently executing domain are independent relations. Charge covers indirect entries, pins, cursors and retained/quarantined backing, not merely the visible payload.

### Admission, transitions and completion

A charge transfer requires source MoveCharge authority, destination AcceptCharge authority, destination quota and the relevant object-lifetime authority. Reserve the destination amount, then atomically exchange the payer and accounting deltas without changing object identity or use rights. Concurrent close or resize must serialize against the recorded amount. After owner failure, retain the old account or explicitly accepted recovery account until physical obligations end.

### Failure and adversarial behavior

Automatically billing the current caller lets an unrelated client inherit earlier cleanup debt. Dropping a failed account while objects remain creates uncharged storage; moving charge must not transfer permissions by accident. Charging the same retained extent to two accounts can hide a leak even when global counters look conservative.

### Alternatives and unresolved tradeoffs

Always charging the creator is simple but poor for durable shared services. Negotiated transfer supports service evolution at the cost of a multi-party transaction. Neither approach permits forced acceptance merely because the destination is a supervisor.

## Verification obligations

Race transfer with closure, growth and destination exhaustion. Check that the sum of debits matches live plus retained physical and metadata charges, and that at every observable state there is exactly one payer. Verify that refusing a transfer cannot strand cleanup authority.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Quarantine custody and reuse release](../teardown-revocation-and-safe-reclamation/quarantine-custody-and-reuse-release.md) — The reaper proves eligibility; the allocator performs final reuse.
- [Product authority and durable detachment](../capability-spaces-and-authority/product-authority-and-durable-detachment.md) — Creation must attach the correct lifetime dependencies.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Resource containers: A new facility for resource management in server systems](../../../30-sources/banga-et-al-1999-resource-containers.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Kernel design for isolation and assurance of physical memory](../../../30-sources/elkaduwe-et-al-2008-kernel-memory-isolation.md) — comparative evidence; its methods and limits are recorded in the source note.
