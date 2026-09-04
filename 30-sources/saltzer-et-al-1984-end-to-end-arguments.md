---
title: "End-to-end arguments in system design"
kind: source
created: "2026-09-04"
authors:
  - "Jerome H. Saltzer"
  - "David P. Reed"
  - "David D. Clark"
published: "1984-11-01"
citation_key: "saltzer-et-al-1984-end-to-end-arguments"
container: "ACM Transactions on Computer Systems"
edition: "Volume 2, issue 4, pages 277–288"
isbn: null
doi: "10.1145/357401.357402"
url: "https://doi.org/10.1145/357401.357402"
accessed: "2026-09-04"
tags:
  - distributed-systems
  - networking
  - protocol-design
  - reliability
aliases:
  - "End-to-end arguments"
---

# End-to-end arguments in system design

## Reference

Jerome H. Saltzer, David P. Reed, and David D. Clark. “[End-to-End Arguments
in System
Design](https://groups.csail.mit.edu/ana/Publications/PubPDFs/End-to-End%20Arguments%20in%20System%20Design.pdf).”
*ACM Transactions on Computer Systems* 2, no. 4, pages 277–288, November 1984.
DOI [10.1145/357401.357402](https://doi.org/10.1145/357401.357402).

## Research question or contribution

The paper gives a placement test for reliability, security, and correctness
functions in layered systems. If a function can be implemented completely only
with application knowledge at the endpoints, a lower layer cannot by itself
provide that guarantee. A lower implementation may still be valuable as a
performance optimization or to reduce the frequency of end-to-end recovery.

## Method

The authors reason through case studies: reliable file transfer, delivery
acknowledgement, duplicate suppression, encryption, transaction recovery, and
other system functions. This is a design argument supported by accumulated
systems experience, not an experiment comparing one universal protocol stack.
It structures trade-offs rather than prescribing that all functions always be
moved upward.

## Findings

- Correct file transfer cannot be proved solely by reliable packets because
  faults can arise while reading, buffering, copying, processing, or writing
  at either endpoint. An application-level content check is still required.
- A transport acknowledgement can show arrival at a host or protocol endpoint;
  it cannot show that the requested application effect committed. The useful
  acknowledgement for effectful operations is the target application's
  explicit “done,” “not done,” or otherwise qualified result.
- Suppressing duplicate packets below the application can reduce work, but an
  application that versions objects or makes requests idempotent may need a
  different duplicate policy. Crash and retry can also reintroduce duplicates
  above a perfect transport.
- Encryption inside a lower communication layer can leave plaintext exposed
  at the final host and cannot alone establish the peer or operation semantics
  the application intends. End-to-end authentication and authorization remain
  necessary.
- The argument does not ban lower-layer reliability. Hop-local checks, retry,
  flow control, encryption, or caching can be justified by performance when
  their incomplete guarantee is not mistaken for end-to-end correctness.

## Relevance

Atom OS network services should expose what the transport actually knows:
local rejection, bytes accepted for transmission, authenticated session state,
stream acknowledgement, peer close, or loss. They must not translate those
facts into “the remote service committed the operation.” Effectful protocols
carry a stable operation ID and obtain a service-level outcome from the
authoritative endpoint; if that outcome is lost, the client reconciles rather
than blindly retrying.

The same rule applies to durable state and audit. A WAL commit proves only the
effects enclosed by its transaction, and a telemetry exporter acknowledgement
does not prove that a protected audit record is durably retained by an
independent verifier. Atom OS can still use reliable streams, checksums,
authenticated encryption, and bounded retry as useful lower mechanisms while
keeping their guarantee labels precise.

## Limits

The paper predates modern encrypted transports, zero-copy networking,
large-scale service meshes, and capability kernels. It provides no wire
protocol, algorithm, quantitative placement rule, or Byzantine threat model.
Some functions are cheaper or safer when partly duplicated across layers, and
strictly following a slogan instead of evaluating cost and failure scope would
misapply the work. Atom OS must measure where a lower optimization belongs
while retaining endpoint-level correctness.

## Derived work

- [Durable state, transactions, and outcome recovery](../20-notes/otp-like-system-services-components/durable-state-transactions-and-outcome-recovery.md)
- [Network endpoint and protocol services](../20-notes/otp-like-system-services-components/network-endpoint-and-protocol-services.md)
- [Observability, audit, alarms, and operator control](../20-notes/otp-like-system-services-components/observability-audit-alarms-and-operator-control.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
