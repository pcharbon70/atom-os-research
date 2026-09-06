---
title: "Machine check recovery for Linux on Itanium processors"
kind: source
created: "2026-09-05"
authors:
  - "Tony Luck"
published: 2003
citation_key: "luck-2003-machine-check-recovery-itanium"
container: "Proceedings of the Ottawa Linux Symposium 2003"
edition: null
isbn: null
doi: null
url: "https://www.kernel.org/doc/ols/2003/ols2003-pages-297-303.pdf"
accessed: "2026-09-05"
tags:
  - fault-containment
  - hardware-errors
  - linux
  - ras
aliases:
  - "Itanium machine-check recovery"
---

# Machine check recovery for Linux on Itanium processors

## Reference

Tony Luck. “Machine Check Recovery for Linux on Itanium Processors.”
*Proceedings of the Ottawa Linux Symposium 2003*, 2003. [Conference
paper](https://www.kernel.org/doc/ols/2003/ols2003-pages-297-303.pdf) and
[official proceedings index](https://kernel.org/doc/ols/2003/).

## Research question or contribution

When hardware or firmware reports that error propagation was constrained, what
additional operating-system knowledge is required to reconstruct state,
sacrifice an affected process, or stop the system?

## Method

The paper's platform machine-check model, processor rendezvous, TLB recovery,
memory-error cases, and limitations were read as a historical case study in
post-error classification and recovery.

## Findings

- Hardware and firmware can correct some errors transparently; lost data that
  cannot be reconstructed requires an operating-system decision.
- Recovery is source and object specific. Some translation-state failures can
  be reconstructed without application impact, while some memory failures can
  be contained only by terminating processes that own the affected data.
- Memory containing kernel code or state, unclear ownership, failure during
  recovery, and insufficient rendezvous evidence can force machine-wide
  termination.
- The handling sequence combines local architectural state with cross-CPU and
  memory-management knowledge. A machine-error label alone is insufficient.
- Sacrificing a process is a containment action whose safety depends on the
  lost data not already having corrupted shared kernel or external state.

## Relevance

The classifier should produce a requirement naming the exact object and
reconstruction/retirement obligations. The policy plane can continue only
after independently owned CPU, memory, translation, DMA, and domain-lifecycle
components return matching completion evidence. The case study supports a
conservative default when object ownership or propagation is unknown.

## Limits

The Itanium architecture and Linux implementation are historical and do not
define x86-64, Arm, or RISC-V recovery. The reported cases do not prove that a
modern device, interconnect, persistent store, or malicious workload is
contained. The paper is most valuable for its decision structure, not as a
current platform recipe.

## Derived work

- [Containment classifier and promotion](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/containment-classifier-and-promotion.md)
- [Escalation channel](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/escalation-channel.md)
