---
title: "Root gates and close linearization"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Root gates and close linearization

How can a domain stop acquiring new work without first walking every object it owns?

## Research basis and status

Split logical removal and delayed reclamation is a useful concurrency precedent, not a complete domain-stop mechanism. [1](../../../30-sources/mckenney-slingwine-1998-read-copy-update.md), [2](../../../30-sources/blackham-et-al-2011-timing-analysis-protected-kernel.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../protection-domains-threads-and-address-spaces.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

Four preinstalled root gates cover execution, relationships, outbound calls and epoch sessions. Their storage and closure publication are fixed at domain creation. Child objects carry stable links to the relevant gates, so closing need not discover them before refusing new admission.

### Admission, transitions and completion

The CLOSING transition atomically freezes membership and closes all four gates before starting the bounded participant stop protocol. Each creation, migration, invocation and session operation must identify which gate it checks and where that check competes with close. Operations admitted earlier remain in their own ledgers and drain later; closing cannot retroactively report them as never accepted.

### Failure and adversarial behavior

A lazy object walk leaves a window in which new threads or calls extend the graph faster than cleanup progresses. Updating gates independently can expose an inconsistent halfway state. A shortcut fast path that checks only the object's local flag bypasses the domain boundary.

### Alternatives and unresolved tradeoffs

One packed state word can simplify the linearization proof, but it does not by itself protect compound membership data. A short lock-based transition may be clearer. Constant work is a claim about fixed gate publication, not elapsed global stop time or unlimited CPU notification.

## Verification obligations

Enumerate every operation that extends execution or relationships and race its admission with close. Verify either a fully recorded pre-close effect or a post-close rejection. Stress a large object graph and confirm close publication does not scale with descendant count.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Passive handler abort and donation drain](../bounded-invocation-and-transport/passive-handler-abort-and-donation-drain.md) — Accepted passive handlers require a valid stop/checkpoint path.
- [Software and hardware quiescence join](../teardown-revocation-and-safe-reclamation/software-and-hardware-quiescence-join.md) — Execution stop is only one condition of final reclamation.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Read-copy update: Using execution history to solve concurrency problems](../../../30-sources/mckenney-slingwine-1998-read-copy-update.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [Timing analysis of a protected operating system kernel](../../../30-sources/blackham-et-al-2011-timing-analysis-protected-kernel.md) — comparative evidence; its methods and limits are recorded in the source note.
