---
title: "Back to the Future: Fault-Tolerant Live Update with Time-Traveling State Transfer"
kind: source
created: "2026-09-10"
authors:
  - "Cristiano Giuffrida"
  - "Călin Iorgulescu"
  - "Anton Kuijsten"
  - "Andrew S. Tanenbaum"
published: 2013
citation_key: "giuffrida-et-al-2013-fault-tolerant-live-update"
container: "27th Large Installation System Administration Conference (LISA '13)"
edition: null
isbn: null
doi: null
url: "https://www.usenix.org/conference/lisa13/technical-sessions/presentation/giuffrida"
accessed: "2026-09-10"
tags:
  - dynamic-software-update
  - fault-tolerance
  - state-migration
aliases:
  - "Time-traveling state transfer"
---

# Back to the Future: Fault-Tolerant Live Update with Time-Traveling State Transfer

## Reference

Cristiano Giuffrida, Călin Iorgulescu, Anton Kuijsten, and Andrew S.
Tanenbaum. [Back to the Future: Fault-Tolerant Live Update with
Time-Traveling State
Transfer](https://www.usenix.org/conference/lisa13/technical-sessions/presentation/giuffrida).
LISA '13, USENIX Association, 2013.

## Research question or contribution

Can state transfer for live update be validated and recovered when the transfer
code itself crashes or corrupts candidate state?

## Method

The work isolates program versions in different processes, transfers state
through past, future, and reverse transformations, and evaluates failure
recovery plus time and memory overhead under its stated model.

## Findings

- State transfer is treated as a transaction whose candidate result can be
  checked before publication.
- Separating old and new versions permits failure of transfer code without
  destroying the running old state.
- Multi-version and reverse transformations provide additional validation
  paths instead of trusting one forward converter.
- The reported experiments tolerate arbitrary run-time and memory faults within
  the modeled state-transfer boundary with modest measured overhead.

## Relevance

The paper supports isolating migration workers, retaining the old generation,
and publishing only validated candidate state. It sharpens Atom OS changeset
work by making migration failure a first-class recoverable event.

## Limits

The guarantee is limited to the authors' state model and evaluated systems. It
does not validate application invariants, external effects, capability
delegation, BEAM semantics, or arbitrary schema evolution. Reverse
transformation is not proof that user-observed effects can be undone.

## Derived work

- [Live-tool internal services](../20-notes/visual-computing-synthesis-components/capability-scoped-live-tools-and-transactional-evolution/README.md).
- [Visual-computing internal-services research session](../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md).
