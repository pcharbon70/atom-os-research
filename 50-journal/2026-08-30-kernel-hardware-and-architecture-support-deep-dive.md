---
title: "2026-08-30 kernel hardware and architecture support deep dive"
kind: journal
created: "2026-08-30"
tags:
  - architecture-support
  - literature-review
  - operating-systems
  - research-session
aliases:
  - "Kernel architecture support research session"
---

# 2026-08-30 kernel hardware and architecture support deep dive

## Observations

The session re-scoped “hardware and architecture support” to privileged kernel
mechanisms. Physical-component comparison, board design, SoC/peripheral surveys,
firmware engineering, and concrete device protocols were excluded.

The evidence converged on a semantic-component design rather than an opaque
HAL. The recurring issue was completion: a local instruction or metadata
update is often only the beginning of a state transition involving other CPUs,
translation caches, instruction caches, interrupt controllers, devices, or an
IOMMU. Generational handles and explicit quiescence epochs appear applicable
across these boundaries, but that synthesis remains unimplemented.

## Environment

- Research archive: `atom-os-research`
- Session date: 2026-08-30
- Method: primary-paper and official-documentation review plus cross-source
  synthesis
- Hardware or simulator target: none selected or exercised
- Source-code implementation: none
- Local empirical experiment: none
- Scope: kernel privilege/architecture boundary only

## Evidence

### Search and selection method

The search began from kernel responsibilities—entry/context, translation,
ordering/cache, interrupts, time, CPUs, protected I/O, and fault capture—rather
than from a processor or board shopping list. Sources were selected when they
provided at least one of:

- a primary operating-system architecture and evaluation;
- a formal or verified model relevant to a proposed contract;
- a demonstrated failure mode at an architecture boundary;
- current official architecture semantics; or
- current mature-kernel documentation for a low-level interface split.

Search results and abstracts were used to locate sources, not as evidence for
detailed claims. The linked papers/manuals or their official full-text pages
were read for the claims recorded in their individual source notes.

### Primary architecture and assurance works

- Elphinstone and Heiser, L4 lessons, SOSP 2013:
  <https://eecs582.github.io/readings/l3-20years.pdf>
- Engler, Kaashoek, and O'Toole, Exokernel, SOSP 1995:
  <https://pdos.csail.mit.edu/6.828/2008/readings/engler95exokernel.pdf>
- Ford and colleagues, Flux OSKit, SOSP 1997:
  <https://www-old.cs.utah.edu/flux/papers/oskit-sosp97.html>
- Gu and colleagues, CertiKOS, OSDI 2016:
  <https://www.usenix.org/conference/osdi16/technical-sessions/presentation/gu>
- Klein and colleagues, comprehensive seL4 verification, TOCS 2014:
  <https://sel4.systems/Research/pdfs/comprehensive-formal-verification-os-microkernel.pdf>
- Baumann and colleagues, Multikernel, SOSP 2009:
  <https://barrelfish.org/publications/barrelfish_sosp09.pdf>

### Delegation and protected-I/O works

- Belay and colleagues, Dune, OSDI 2012:
  <https://www.usenix.org/conference/osdi12/technical-sessions/presentation/belay>
- Peter and colleagues, Arrakis, OSDI 2014:
  <https://www.usenix.org/conference/osdi14/technical-sessions/presentation/peter>
- Haecki and colleagues, CleanQ:
  <https://arxiv.org/abs/1911.08773>
- Markettos and colleagues, Thunderclap, NDSS 2019:
  <https://thunderclap.io/wp-content/uploads/2024/01/thunderclap-paper-ndss2019.pdf>

### Memory, translation, and context works

- Stecklina and Prescher, LazyFP:
  <https://arxiv.org/abs/1806.07480>
- Simner and colleagues, relaxed virtual memory in Armv8-A:
  <https://www.cl.cam.ac.uk/~pes20/RelaxedVM-Arm/>
- Simner and colleagues, Arm instruction fetch:
  <https://www.cl.cam.ac.uk/~pes20/iflat/>
- Sewell and colleagues, x86-TSO:
  <https://www.cl.cam.ac.uk/~pes20/weakmemory/cacm.pdf>
- Pulte and colleagues, simplifying Arm concurrency:
  <https://www.cl.cam.ac.uk/~pes20/armv8-mca/>
- Achermann and colleagues, least-privilege memory protection:
  <https://arxiv.org/abs/1908.08707>

### Current official technical documentation

- Linux low-level entry, IRQ, time, barrier, cache/TLB, CPU-hotplug, and DMA
  documentation, rooted at:
  <https://www.kernel.org/doc/html/latest/core-api/index.html>
- Intel 64 and IA-32 manuals, revision 092 landing page:
  <https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html>
- Arm A-profile architecture reference manual:
  <https://developer.arm.com/documentation/ddi0487/latest/>
- RISC-V ratified privileged architecture, release 20260120:
  <https://docs.riscv.org/reference/isa/priv/priv-index.html>

The full evidence extraction is preserved in the linked [source-note
index](../30-sources/README.md). The synthesis is [Kernel hardware and
architecture support
layer](../20-notes/kernel-hardware-and-architecture-support-layer.md).

### Evidence boundary

This was a literature session. It did not boot code, inspect generated
assembly, run memory-model litmus tests, measure latency, exercise an emulator,
or test real interrupt, cache, timer, CPU-start, IOMMU, or fault behavior.
Consequently:

- architecture-manual statements are normative for their pinned version but
  do not prove an implementation;
- paper results apply to their evaluated systems and workloads;
- mature Linux interfaces are precedent, not automatically the minimal design;
- formal-verification results apply within their stated models and assumptions;
  and
- the eleven-component decomposition and recommendations are cross-source
  synthesis, not reported conclusions of any one source.

## Threads

- [Kernel hardware and architecture support
  layer](../20-notes/kernel-hardware-and-architecture-support-layer.md) develops
  the eleven components, lifecycles, tradeoffs, and phased verification plan.
- [Kernel architecture support
  map](../10-maps/kernel-hardware-and-architecture-support.md) provides reading
  trails through the evidence.
- [Kernel hardware-contract
  inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md)
  records the falsifiable criteria and remaining decisions.

## Follow-ups

1. Specify object authority, context safety, failure, and completion in a
   machine-checkable interface vocabulary.
2. Model mapping, code publication, interrupt, CPU, and DMA state machines and
   search for stale-generation and premature-reclamation traces.
3. Select one virtual ISA target only after the semantic baseline is explicit;
   selection is a later implementation experiment, not a physical-board
   research task.
4. Pin the exact architecture/manual, compiler, emulator, and firmware profile
   when implementation begins.
5. Define runtime-derived latency and event-semantics requirements before
   optimizing architecture paths.

Continue unresolved work in the [contract inquiry](../40-inquiries/what-contract-should-the-kernel-hardware-and-architecture-layer-provide.md).
