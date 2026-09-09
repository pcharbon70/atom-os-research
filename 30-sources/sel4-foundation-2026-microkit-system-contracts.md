---
title: "Microkit User Manual (v2.3.0)"
kind: source
created: "2026-09-09"
authors: ["seL4 Foundation"]
published: null
citation_key: "sel4-foundation-2026-microkit-system-contracts"
container: "Microkit documentation"
edition: "2.3.0, as displayed at access"
isbn: null
doi: null
url: "https://docs.sel4.systems/projects/microkit/manual/latest/"
accessed: "2026-09-09"
tags: [capabilities, kernel-internal-services, microkernels]
aliases: []
---

# Microkit User Manual (v2.3.0)

## Reference

seL4 Foundation. [Microkit User Manual (v2.3.0)](https://docs.sel4.systems/projects/microkit/manual/latest/). Microkit documentation; publication date not stated. 2.3.0, as displayed at access. Accessed 2026-09-09.

## Research question or contribution

Which static configuration restrictions simplify protected service composition?

## Method

Read protection domains, initialization, notifications, protected procedures, scheduling configuration and system-description constraints.

## Findings

Microkit uses statically described protection domains. Protected calls go to a higher-priority domain, restricting call cycles. A domain finishes its own init before handling other entry points, but may handle events while another domain is still initializing. The manual requires protected procedures to finish in bounded time while explicitly relying on callee trust rather than the proposed future static enforcement.

## Relevance

Compare static acyclic deployment against Atom's proposed dynamic admission, bootstrap handoff and failure topology. Initialization eligibility needs a checked protocol, not a presumed global barrier.

## Limits

These are framework contracts, not universal microkernel requirements. The URL tracks latest documentation; the observed version is recorded here. Atom does not adopt Microkit's fixed configuration limits or recovery semantics.

## Derived work

- [One-way root handoff and abort](../20-notes/minimal-privileged-kernel-components/bootstrap-and-root-authority-handoff/one-way-root-handoff-and-abort.md) — proposed contract constrained by this evidence.
- [Domain roots and membership](../20-notes/minimal-privileged-kernel-components/protection-domains-threads-and-address-spaces/domain-roots-and-membership.md) — proposed contract constrained by this evidence.
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md) — selective architectural context.
