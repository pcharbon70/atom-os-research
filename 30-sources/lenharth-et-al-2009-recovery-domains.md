---
title: "Recovery domains: An organizing principle for recoverable operating systems"
kind: source
created: "2026-09-05"
authors:
  - "Andrew Lenharth"
  - "Vikram Adve"
  - "Samuel T. King"
published: 2009
citation_key: "lenharth-et-al-2009-recovery-domains"
container: "ASPLOS XIV"
edition: null
isbn: null
doi: "10.1145/1508244.1508251"
url: "https://llvm.org/pubs/2009-03-ASPLOS-Recovery.html"
accessed: "2026-09-05"
tags:
  - fault-containment
  - operating-systems
  - recovery
aliases:
  - "Akeso recovery domains"
---

# Recovery domains: An organizing principle for recoverable operating systems

## Reference

Andrew Lenharth, Vikram Adve, and Samuel T. King. “Recovery Domains: An
Organizing Principle for Recoverable Operating Systems.” *ASPLOS XIV*, pages
49–60, 2009. DOI
[10.1145/1508244.1508251](https://doi.org/10.1145/1508244.1508251).
[Author project page](https://llvm.org/pubs/2009-03-ASPLOS-Recovery.html) and
[paper](https://llvm.org/pubs/2009-03-ASPLOS-Recovery.pdf).

## Research question or contribution

Can a multithreaded commodity kernel roll back only the request whose execution
encountered a run-time safety check instead of rebooting or restarting an
entire static component?

## Method

The Akeso prototype instruments Linux 2.4.22 and 2.6.27, groups request-local
state into dynamic recovery domains, logs selected changes, and evaluates
recovery from injected faults in core kernel paths.

## Findings

- Recovery scope can follow a dynamic request rather than a static component,
  reducing collateral impact when all effects of that request are identified.
- Multithreaded shared state and output commit are the hard boundaries: state
  observed or modified outside the recovery domain cannot simply be rolled
  back without coordination.
- Compiler instrumentation and small kernel changes can establish useful
  rollback points for selected checked failures, and the prototype recovered
  from cases that would otherwise be fatal in its evaluated configurations.
- Runtime checks detect particular software faults. They do not establish that
  corrupted hardware, DMA, firmware, or an external effect remained inside the
  request.
- A recovery region needs an explicit commit boundary; after externally
  visible output, “retry the request” may duplicate or contradict effects.

## Relevance

Atom's classifier can use a request/domain scope only when the capture evidence
and object ledgers prove that all affected state and outputs are inside that
scope. `ContainmentRequirement` should name those dependencies and carry an
`external_effect_status` of none, committed, or indeterminate. Unknown scope or
output commit forces widening, not optimistic rollback.

## Limits

The evaluation targets injected software errors in historical Linux kernels,
not machine checks or arbitrary state corruption. Instrumentation coverage and
the correctness of recovery handlers remain assumptions. The paper
demonstrates that narrow recovery is possible under explicit boundaries, not
that every kernel or hardware fault is request-local.

## Derived work

- [Containment classifier and promotion](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/containment-classifier-and-promotion.md)
- [Escalation channel](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/escalation-channel.md)
