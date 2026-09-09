---
title: "Capability-based OS Design"
kind: source
created: "2026-09-09"
authors: ["Gabe Parmer"]
published: 2016
citation_key: "parmer-2016-capability-based-os-design"
container: "Systems Research @ GWU"
edition: null
isbn: null
doi: null
url: "https://www2.seas.gwu.edu/~parmer/posts/2016-04-06-capability-based-design.html"
accessed: "2026-09-09"
tags: [capabilities, kernel-internal-services, microkernels]
aliases: []
---

# Capability-based OS Design

## Reference

Gabe Parmer. [Capability-based OS Design](https://www2.seas.gwu.edu/~parmer/posts/2016-04-06-capability-based-design.html). Systems Research @ GWU; 2016. Accessed 2026-09-09.

## Research question or contribution

Must recursive delegation policy reside inside the privileged kernel?

## Method

Read capability creation/destruction and Composite resource-table design, including consent, revocation cost and user-level policy alternatives.

## Findings

Delegation needs receiver consent as well as sender authority. Recursive revocation has work proportional to the affected delegation structure. Composite instead exposes controlled resource-table mutation, leaving delegation policy to trusted user-level components.

## Relevance

Evaluate stable kernel closure anchors against a smaller table-mutation substrate. Receiver-selected slots make capability-space capacity part of admission.

## Limits

The article describes a design viewpoint and alternatives, not a comparative scalability proof. Moving policy outside the kernel relocates trust and failure dependencies; it does not eliminate them.

## Derived work

- [Slot mutation and consented transfer](../20-notes/minimal-privileged-kernel-components/capability-spaces-and-authority/slot-mutation-and-consented-transfer.md) — proposed contract constrained by this evidence.
- [Lineage and one-way revocation anchors](../20-notes/minimal-privileged-kernel-components/capability-spaces-and-authority/lineage-and-one-way-revocation-anchors.md) — proposed contract constrained by this evidence.
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md) — selective architectural context.
