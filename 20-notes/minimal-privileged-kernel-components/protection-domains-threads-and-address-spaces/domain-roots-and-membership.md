---
title: "Domain roots and membership"
kind: note
created: "2026-09-09"
maturity: developing
tags: [capabilities, kernel-internal-services, microkernels, system-architecture]
aliases: []
---

# Domain roots and membership

What state makes one protection domain a well-defined containment boundary?

## Research basis and status

Microkit demonstrates one static domain configuration; it does not supply Atom's dynamic domain lifecycle. [1](../../../30-sources/sel4-foundation-2026-microkit-system-contracts.md), [2](../../../30-sources/sel4-foundation-2026-reference-manual.md)

The contract below is an Atom OS architectural proposal refining the [parent component](../protection-domains-threads-and-address-spaces.md). It is not an implemented service, a transferred proof, or a milestone plan.

## Development

### Owned state and trust boundary

A domain owns exclusive CSpace and VSpace roots, a bounded membership ledger, fixed admission gates, execution-participant state and fault/recovery references. Payer accounts and lifetime groups are separate objects. BEAM processes and their tracing collectors remain unprivileged runtime entities rather than entries in the domain thread ledger.

### Admission, transitions and completion

Create the domain from explicitly supplied roots and membership capacity. Attach a thread only through the relationship gate, recording the thread generation and all future cleanup obligations before eligibility. Shared frames are explicit relationships, not shared roots. If multiple domains deliberately share a root, represent them as one correlated stop group rather than claiming independent containment.

### Failure and adversarial behavior

A thread that can enter the address space without appearing in the ledger defeats whole-domain stop. A stale thread identifier must not attach a replacement incarnation. Sharing a capability root can let one alleged domain alter another's authority even if their administrative labels differ.

### Alternatives and unresolved tradeoffs

Static membership reduces concurrency obligations but restricts runtime service evolution. Dynamic membership is reasonable only with bounded capacity and atomic close-versus-attach semantics. A domain object should not grow into a service registry, actor scheduler or supervisor strategy table.

## Verification obligations

Attempt duplicate-root attachment, stale-generation membership and concurrent thread creation during closing. Check that every execution-eligible thread belongs to the frozen set and that intentionally shared roots are reported as correlated failure scope.

These are unexecuted falsification cases. Acceptance requires a versioned model or implementation, explicit participant/resource bounds and recorded results; literature support alone does not satisfy them.

## Connections

- [Component service index](README.md) — the complete local decomposition and shared composition obligations.
- [Passive handler abort and donation drain](../bounded-invocation-and-transport/passive-handler-abort-and-donation-drain.md) — Accepted passive handlers require a valid stop/checkpoint path.
- [Software and hardware quiescence join](../teardown-revocation-and-safe-reclamation/software-and-hardware-quiescence-join.md) — Execution stop is only one condition of final reclamation.
- [Minimal-kernel inquiry](../../../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md) — open cross-service assurance questions.
- [Research session](../../../50-journal/2026-09-09-minimal-kernel-internal-services-deep-dive.md) — reading scope, limitations and source provenance.

## Sources

1. [Microkit User Manual (v2.3.0)](../../../30-sources/sel4-foundation-2026-microkit-system-contracts.md) — comparative evidence; its methods and limits are recorded in the source note.
2. [seL4 reference manual, version 16.0.0](../../../30-sources/sel4-foundation-2026-reference-manual.md) — comparative evidence; its methods and limits are recorded in the source note.
