---
title: "Efficient data structures for tamper-evident logging"
kind: source
created: "2026-09-04"
authors:
  - "Scott A. Crosby"
  - "Dan S. Wallach"
published: 2009
citation_key: "crosby-wallach-2009-tamper-evident-logging"
container: "18th USENIX Security Symposium (USENIX Security 09)"
edition: null
isbn: null
doi: null
url: "https://www.usenix.org/conference/usenixsecurity09/technical-sessions/presentation/efficient-data-structures-tamper-evident"
accessed: "2026-09-04"
tags:
  - audit
  - logging
  - merkle-trees
  - security
aliases:
  - "Tamper-evident logging"
---

# Efficient data structures for tamper-evident logging

## Reference

Scott A. Crosby and Dan S. Wallach. “[Efficient Data Structures for
Tamper-Evident
Logging](https://www.usenix.org/conference/usenixsecurity09/technical-sessions/presentation/efficient-data-structures-tamper-evident).”
*18th USENIX Security Symposium*, 2009.

## Research question or contribution

The paper asks how clients and auditors can efficiently verify event inclusion,
append-only consistency, and authenticated searches when the log server itself
is untrusted.

## Method

The authors define audit semantics, design a tree-based authenticated data
structure, implement a prototype, and evaluate it on an 80-million-event
syslog trace. They compare proof size and throughput with linear hash-chain
approaches.

## Findings

- A challenged logger must prove both that an event remains present and that
  the current log is consistent with an earlier observed commitment.
- Tree-based proofs reduce inclusion and consistency evidence from linear to
  logarithmic size.
- The prototype produced kilobyte-scale proofs for the large trace and measured
  thousands of events per second, with higher throughput when signatures were
  offloaded.
- Authenticated search and agreed retention can coexist, but only under an
  explicit deletion policy and verifiable commitments.

## Relevance

Atom should separate a bounded local append path from asynchronous tree
construction, witness publication, search, and retention. A witness verifies
commitment continuity; it cannot certify that a compromised producer emitted
every required event or described the effect honestly.

## Limits

The workload and 2009 prototype do not predict Atom's performance, crash
behavior, privacy requirements, or distributed witness availability. The
scheme detects evidence inconsistencies under its audit model but does not
prevent an attack or reconstruct omitted events.

## Derived work

- [Audit and witness services](../20-notes/authentication-and-authorization-components/audit-and-witness-services.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
