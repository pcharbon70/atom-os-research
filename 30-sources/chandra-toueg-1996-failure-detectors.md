---
title: "Unreliable failure detectors for reliable distributed systems"
kind: source
created: "2026-08-31"
authors:
  - "Tushar Deepak Chandra"
  - "Sam Toueg"
published: 1996
citation_key: "chandra-toueg-1996-failure-detectors"
container: "Journal of the ACM 43(2), 225–267"
edition: null
isbn: null
doi: "10.1145/226643.226647"
url: "https://doi.org/10.1145/226643.226647"
accessed: "2026-08-31"
tags:
  - distributed-systems
  - failure-detection
  - fault-containment
  - recovery
aliases:
  - "Unreliable failure detectors"
---

# Unreliable failure detectors for reliable distributed systems

## Reference

Tushar Deepak Chandra and Sam Toueg. “Unreliable Failure Detectors for Reliable
Distributed Systems.” *Journal of the ACM* 43(2), pages 225–267, 1996. DOI
[10.1145/226643.226647](https://doi.org/10.1145/226643.226647).

## Research question or contribution

What failure-detector properties are sufficient for reliable agreement in
asynchronous systems where timing alone cannot prove that a process crashed?

## Method

The paper formalizes classes of unreliable failure detectors in terms of
completeness and accuracy, then establishes which classes suffice for consensus
under different crash assumptions.

## Findings

- A timeout produces suspicion, not proof, in an asynchronous model.
- Completeness describes whether failed participants are eventually suspected;
  accuracy describes whether correct participants avoid suspicion.
- Useful algorithms can tolerate detectors that make mistakes, provided their
  eventual properties and system assumptions are explicit.

## Relevance

Local domain monitoring has the same epistemic distinction. A synchronous CPU
fault or completed external termination is definite; a missed heartbeat is a
liveness suspicion whose accuracy depends on reserved scheduling time, timer
semantics, and load assumptions. Fault records and supervisor policy must keep
these classes separate.

## Limits

This is distributed-systems theory about crash failures and consensus, not an
evaluation of local kernel watchdogs. A shared-kernel domain can corrupt shared
state or external devices before stopping, so it is not automatically the
fail-stop process assumed by the model.

## Derived work

- [Distribution gateway and remote actor semantics](../20-notes/managed-actor-runtime-components/distribution-gateway-and-remote-actor-semantics.md)
- [Failure translation and the OTP boundary](../20-notes/managed-actor-runtime-components/failure-translation-and-the-otp-boundary.md)
- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
