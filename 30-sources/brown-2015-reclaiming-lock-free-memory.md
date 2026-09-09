---
title: "Reclaiming memory for lock-free data structures: there has to be a better way"
kind: source
created: "2026-09-09"
authors: ["Trevor Brown"]
published: 2015
citation_key: "brown-2015-reclaiming-lock-free-memory"
container: "PODC 2015; author full version"
edition: "Full version, arXiv:1712.01044v1 (2017)"
isbn: null
doi: "10.48550/arXiv.1712.01044"
url: "https://arxiv.org/abs/1712.01044"
accessed: "2026-09-09"
tags: [capabilities, kernel-internal-services, microkernels]
aliases: []
---

# Reclaiming memory for lock-free data structures: there has to be a better way

## Reference

Trevor Brown. [Reclaiming memory for lock-free data structures: there has to be a better way](https://arxiv.org/abs/1712.01044). PODC 2015; author full version; 2015. Full version, arXiv:1712.01044v1 (2017). Accessed 2026-09-09. DOI: [10.48550/arXiv.1712.01044](https://doi.org/10.48550/arXiv.1712.01044).

## Research question or contribution

Can reclamation tolerate stalled participants without invalidating interrupted operations?

## Method

Read the full-version system model, reclamation comparison and DEBRA+ neutralization/recovery sections, especially sections 3 and 5. The arXiv record identifies the original PODC 2015 publication.

## Findings

Stalled participants can prevent epoch-based reclamation. DEBRA+ uses operating-system signal guarantees and tailored recovery to neutralize eligible operations. Its interruption scheme depends on restartable work; the paper explicitly identifies the difficulty of interrupting lock holders.

## Relevance

Separate software-reference protection from legal kernel checkpoints. A remote interrupt is not itself evidence that an activation can safely be abandoned.

## Limits

The algorithm assumes a hosted signaling contract and structured operations. Its bounds and experiments do not establish Atom's privileged stop protocol, hardware drainage, or performance. The DOI identifies the accessed full version, not the conference edition.

## Derived work

- [Lifetime groups and activation pins](../20-notes/minimal-privileged-kernel-components/typed-object-storage-and-explicit-memory/lifetime-groups-and-activation-pins.md) — proposed contract constrained by this evidence.
- [Kernel activation checkpoints](../20-notes/minimal-privileged-kernel-components/protection-domains-threads-and-address-spaces/kernel-activation-checkpoints.md) — proposed contract constrained by this evidence.
- [Software and hardware quiescence join](../20-notes/minimal-privileged-kernel-components/teardown-revocation-and-safe-reclamation/software-and-hardware-quiescence-join.md) — proposed contract constrained by this evidence.
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md) — selective architectural context.
