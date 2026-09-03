---
title: "RISC-V supervisor binary interface specification"
kind: source
created: "2026-09-02"
authors:
  - "RISC-V Platform Runtime Services Task Group"
published: "2025-07-16"
citation_key: "risc-v-international-2025-supervisor-binary-interface"
container: "RISC-V Ratified Specifications Library"
edition: "Version 3.0, ratified"
isbn: null
doi: null
url: "https://docs.riscv.org/reference/sbi/v3.0/index.html"
accessed: "2026-09-02"
tags:
  - cpu-lifecycle
  - firmware
  - instruction-fetch
  - interrupts
  - risc-v
  - tlb
aliases:
  - "RISC-V SBI 3.0"
---

# RISC-V supervisor binary interface specification

## Reference

RISC-V Platform Runtime Services Task Group. *RISC-V Supervisor Binary
Interface Specification*, version 3.0, ratified 2025-07-16.
[Official specification](https://docs.riscv.org/reference/sbi/v3.0/index.html).

## Research question or contribution

Which machine-mode services can a RISC-V supervisor invoke through a portable,
versioned firmware boundary, and what does that boundary say about timer
programming, hart lifecycle, IPIs, and remote translation/instruction-fetch
synchronization?

## Method

This is a normative interface specification. The analysis focuses on the TIME,
Hart State Management (HSM), IPI, remote-fence, and error contracts rather than
treating an SBI implementation as part of the supervisor kernel.

## Findings

- The RFENCE extension provides remote `FENCE.I`, `SFENCE.VMA`, ASID-scoped
  `SFENCE.VMA`, and hypervisor-fence requests over explicit hart sets and
  optional address ranges.
- Calls can reject invalid harts, addresses, ASIDs, or unsupported operations,
  and can return a general failure. A supervisor therefore cannot treat a
  firmware request as an infallible local instruction.
- The IPI extension separately sends supervisor software interrupts. The
  distinction permits a direct supervisor-owned shootdown implementation or a
  delegated firmware implementation behind one semantic backend.
- The TIME extension programs the next timer event using an absolute time
  value. It is a higher-privilege service boundary, not ownership of a kernel
  software timer queue. In SBI 3.0, `sbi_set_timer` is specified to return
  `SBI_SUCCESS`; extension discovery, firmware latency, interrupt masking, and
  the supervisor's own channel state remain separate obligations.
- HSM separates a start request from the target hart reaching `STARTED`; its
  state vocabulary includes pending states. `hart_start` supplies an entry
  address and opaque value, while successful `hart_stop` is a target-hart
  operation that does not return. These semantics require an OS-side
  incarnation/cookie handshake and separate confirmation before a hart becomes
  schedulable or reclaimable.
- The specification describes a request interface; a kernel still needs to
  define which returned state constitutes protection completion and how failed
  or unavailable harts affect reclamation.

## Relevance

A RISC-V backend should declare whether it owns inter-hart coordination or
depends on SBI RFENCE. Firmware success is admitted as completion only under a
pinned platform profile whose SBI implementation provides the required
semantics; errors remain explicit and keep affected mappings or code pinned.
TIME should back one typed absolute deadline channel, and HSM should remain the
fallible platform step inside the logical-CPU transaction rather than defining
kernel membership by itself.

## Limits

SBI is an interface, not evidence that every firmware implementation is
correct, timely, or resilient to a failed hart. It does not define the
capability checks, address-space lifecycle, scheduling interlock, or recovery
policy required by this project.

## Derived work

- [Address translation and protection transitions](../20-notes/kernel-hardware-and-architecture-components/address-translation-and-protection-transitions.md)
- [Ordering, coherence, and code publication](../20-notes/kernel-hardware-and-architecture-components/ordering-coherence-and-code-publication.md)
- [Raw time and deadline programming](../20-notes/kernel-hardware-and-architecture-components/raw-time-and-deadline-programming.md)
- [Logical-CPU coordination and lifecycle](../20-notes/kernel-hardware-and-architecture-components/logical-cpu-coordination-and-lifecycle.md)
