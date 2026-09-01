---
title: "seL4 design principles"
kind: source
created: "2026-08-31"
authors:
  - "Gernot Heiser"
published: "2020-03-11"
citation_key: "heiser-2020-sel4-design-principles"
container: "microkerneldude"
edition: null
isbn: null
doi: null
url: "https://microkerneldude.org/2020/03/11/sel4-design-principles/"
accessed: "2026-08-31"
tags:
  - capabilities
  - formal-verification
  - microkernels
  - operating-systems
  - sel4
aliases:
  - "Heiser's seL4 design principles"
---

# seL4 design principles

## Reference

Gernot Heiser. “seL4 Design Principles.” *microkerneldude*, March 11,
2020. [Canonical article](https://microkerneldude.org/2020/03/11/sel4-design-principles/).

## Research question or contribution

The article records the design principles and deliberate non-goals behind
seL4's API, including rationales that had previously remained largely tacit
knowledge among its designers.

## Method

This is a first-person retrospective by a lead seL4 researcher. It explains
design decisions and trade-offs by reference to seL4's development and
verification experience; it is not an empirical comparison or a new formal
proof.

## Findings

- Verification, minimality, policy freedom, performance, security, and not
  charging unused features are the stated API drivers. Ease of use, protection
  from an authorised designer's mistakes, and a uniform hardware abstraction
  are explicit non-goals of the kernel API.
- Verification pressure favours a non-concurrent kernel with no nested kernel
  exceptions, and makes re-verification cost part of the price of every API
  change.
- Minimality excludes device drivers other than the interrupt controller and
  timer. Memory-allocation policy, including management of kernel-object
  memory, belongs at user level.
- After boot, seL4 has no heap and performs no implicit memory allocation. A
  caller must explicitly supply untyped memory when an operation creates a
  kernel object.
- The hot IPC path is organised around short RPC round trips that restore the
  same logical kernel state. Capability transfer is treated as a colder,
  persistent state change; kernel-assisted long IPC was rejected because it
  adds checks and can introduce nested faults even when callers do not use it.
- Fine-grained capabilities support least authority, reduced-rights
  delegation, and revocation down a hierarchy without requiring the root
  authority to mediate every operation.

## Relevance

The article supplies a useful admission rule for this project's minimal
privileged layer: include a mechanism only when moving it out would prevent a
required property. Kernel-object memory must be explicit and capability
authorised; short control IPC should stay the optimised primitive; bulk
transport, device policy, BEAM execution, supervision, and friendly APIs should
be built above the privileged boundary. That split can keep the kernel small
without forcing the BEAM-compatible runtime to expose a bare microkernel API to
ordinary processes.

## Limits

This is a practitioner essay rather than a peer-reviewed paper, specification,
or proof. It describes seL4's goals and trade-offs as of 2020, not a universal
microkernel contract or evidence from BEAM workloads. Some statements, such as
the rough relationship between code size and verification effort, are design
heuristics rather than results established in this article. Its deliberate
kernel-API non-goals still require usable, policy-bearing layers elsewhere in a
complete operating system.

## Derived work

- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
