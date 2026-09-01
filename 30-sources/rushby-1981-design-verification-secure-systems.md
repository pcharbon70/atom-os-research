---
title: "Design and verification of secure systems"
kind: source
created: "2026-08-31"
authors:
  - "John Rushby"
published: 1981
citation_key: "rushby-1981-design-verification-secure-systems"
container: "ACM SIGOPS Operating Systems Review 15(5)"
edition: null
isbn: null
doi: "10.1145/800216.806586"
url: "https://www.csl.sri.com/papers/sosp81/"
accessed: "2026-08-31"
tags:
  - formal-verification
  - isolation
  - operating-systems
  - separation-kernels
  - security
aliases:
  - "Rushby separation-kernel paper"
---

# Design and verification of secure systems

## Reference

John Rushby. “Design and Verification of Secure Systems.” Reprint of a
paper presented at the Eighth ACM Symposium on Operating Systems Principles,
Pacific Grove, California, December 14–16, 1981. *ACM SIGOPS Operating Systems
Review* 15(5): 12–21. DOI
[10.1145/800216.806586](https://doi.org/10.1145/800216.806586).
[Author record and PDF](https://www.csl.sri.com/papers/sosp81/).

## Research question or contribution

How can a secure system be decomposed so that the small kernel's isolation
claim is verified independently from the application-specific policies of
trusted services?

## Method

Rushby develops a conceptual system decomposition and sketches a formal state
machine for “proof of separability.” Multiple abstraction functions project a
shared concrete machine into the private abstract machine observed by each
regime. Six conditions constrain operations, input, output, and operation
selection; a companion paper, rather than this paper, develops the method in
full.

## Findings

- A secure system can be treated as a distributed collection of isolated
  components, some of which perform narrowly defined trusted functions. A
  separation kernel simulates the physical separation on one processor.
- The kernel's responsibility is separability, not enforcement of every
  application-specific security policy. Each trusted file, print,
  authentication, or mediation service must have its own policy and assurance
  argument.
- An operation executed for the active regime must look like a valid operation
  of that regime's private abstract machine and must not change the state
  observed by inactive regimes.
- Isolation covers more than memory accesses. Inputs, outputs, operation
  selection, I/O-device activity, and interrupts can alter or reveal state and
  therefore belong in the separability model.
- This decomposition separates the proof obligation for the kernel's
  multiplexing and isolation mechanisms from proofs for trusted components,
  while still requiring a system-level argument that the components jointly
  implement the intended policy.

## Relevance

The project's minimal privileged kernel should define failure domains as
independent abstract machines over CPU time, memory, kernel objects, interrupts,
and device access, with only explicitly authorised communication changing what
another domain can observe. BEAM execution, supervision, naming, persistence,
and distribution policies should remain separate user-level components whose
failures cannot mutate the kernel or sibling domains. Rushby's model also makes
interrupt and I/O mediation part of the isolation claim rather than an
implementation footnote. Capabilities can implement this project's explicit
authority edges, but that mechanism is a project synthesis, not a mechanism
specified by this paper.

## Limits

The paper is a foundational 1981 treatment aimed at high-assurance secure
systems, with a simple single-processor and single-active-regime model. It does
not present an implementation, performance evaluation, capability API,
multicore protocol, or recovery architecture. The formal development is only
sketched here and does not by itself prove a concrete kernel. Separability is
also not complete system security: authorised communication, trusted-service
logic, availability, timing channels, and hardware behaviour require separate
models and evidence.

## Derived work

- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
