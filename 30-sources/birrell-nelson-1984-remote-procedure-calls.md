---
title: "Implementing remote procedure calls"
kind: source
created: "2026-09-03"
authors:
  - "Andrew D. Birrell"
  - "Bruce Jay Nelson"
published: 1984
citation_key: "birrell-nelson-1984-rpc"
container: "ACM Transactions on Computer Systems"
edition: "2(1), 39-59"
isbn: null
doi: "10.1145/2080.357392"
url: "https://doi.org/10.1145/2080.357392"
accessed: "2026-09-03"
tags:
  - distributed-systems
  - failure-semantics
  - networking
  - remote-procedure-call
aliases:
  - "Birrell-Nelson RPC"
---

# Implementing remote procedure calls

## Reference

Andrew D. Birrell and Bruce Jay Nelson. “[Implementing Remote Procedure
Calls](https://doi.org/10.1145/2080.357392).” *ACM Transactions on Computer
Systems* 2(1), pages 39–59, 1984.

## Research question or contribution

The paper develops a practical RPC mechanism and makes explicit the binding,
packet, retransmission, duplicate-suppression, exception, and performance
issues hidden by a local-call-like programming interface.

## Method

The authors describe the Cedar RPC design and implementation, including call
identifiers, acknowledgements, retransmission, transport choices, and binding,
then measure local-network operation costs.

## Findings

- Request identifiers and duplicate suppression can avoid repeated execution
  within retained protocol state, but state loss and failures still leave
  ambiguous outcomes.
- Retransmission improves availability; it cannot generally prove that a
  timed-out remote effect did or did not occur.
- Binding and incarnation information are part of correctness, not only route
  discovery.

## Relevance

The ambiguity applies equally to actor gateway requests. Atom OS should expose
`NotAccepted`, `Completed`, or `Indeterminate`, bind correlation to a session
and service incarnation, and leave stronger exactly-once effects to durable
idempotency or transaction protocols.

## Limits

The Cedar implementation and network measurements are historical and its RPC
surface is not Erlang distribution. The enduring contribution here is the
failure-semantics analysis, not its wire format or performance.

## Derived work

- [Distribution gateway and remote actor semantics](../20-notes/managed-actor-runtime-components/distribution-gateway-and-remote-actor-semantics.md)
- [Failure translation and the OTP boundary](../20-notes/managed-actor-runtime-components/failure-translation-and-the-otp-boundary.md)
- [2026-09-03 component research journal](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md)
- [OTP-like system services layer](../20-notes/otp-like-system-services-layer.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
- [OTP-like system-services contract inquiry](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
- [2026-09-03 OTP-like system services deep dive](../50-journal/2026-09-03-otp-like-system-services-deep-dive.md)
