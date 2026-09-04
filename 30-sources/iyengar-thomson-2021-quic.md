---
title: "QUIC: A UDP-based multiplexed and secure transport"
kind: source
created: "2026-09-04"
authors:
  - "Jana Iyengar"
  - "Martin Thomson"
published: "2021-05-01"
citation_key: "iyengar-thomson-2021-quic"
container: "Internet Engineering Task Force"
edition: "RFC 9000"
isbn: null
doi: "10.17487/RFC9000"
url: "https://www.rfc-editor.org/rfc/rfc9000.html"
accessed: "2026-09-04"
tags:
  - flow-control
  - ietf
  - networking
  - protocols
  - quic
aliases:
  - "RFC 9000"
  - "QUIC transport"
---

# QUIC: A UDP-based multiplexed and secure transport

## Reference

Jana Iyengar and Martin Thomson, editors. “[QUIC: A UDP-Based Multiplexed and
Secure Transport](https://www.rfc-editor.org/rfc/rfc9000.html).” RFC 9000,
Internet Engineering Task Force, May 2021. DOI
[10.17487/RFC9000](https://doi.org/10.17487/RFC9000).

## Research question or contribution

RFC 9000 specifies QUIC version 1: a connection-oriented secure transport over
UDP with multiplexed streams, connection and stream flow control, low-latency
establishment, path migration, loss recovery hooks, and explicit close/reset
behavior. It shows which state and resource controls a modern user-space
transport endpoint must own without making transport success an application
commit guarantee.

## Method

This is an Internet Standards Track protocol specification produced through
IETF review, not a performance paper. The core transport document was read for
connection identity, streams, flow control, endpoint validation, migration,
errors, and termination. TLS integration and loss recovery are specified in
companion RFCs and are referenced but not reanalyzed as if they were part of
one implementation.

## Findings

- A QUIC connection is stateful and identified by protocol connection IDs
  rather than permanently by one network five-tuple. That supports NAT
  rebinding and controlled client migration, but requires authenticated
  validation before using a new path.
- Bidirectional and unidirectional streams are independently ordered. A lost
  packet carrying one stream need not impose application-visible ordering on
  another stream, although connection-level resources and congestion control
  remain shared.
- Credit limits bound both the data that may be outstanding and the number of
  streams a peer may create. Flow control is distinct at connection and stream
  scopes, and increasing credit is an explicit protocol action.
- QUIC authenticates packets and encrypts most protocol content through its TLS
  integration. Authentication of the connection does not define application
  authorization, capability delegation, or whether a message's requested
  effect is safe.
- Streams and connections have explicit normal, reset, timeout, error, and
  stateless-reset paths. Graceful close and abrupt loss are observably
  different, but neither can retrospectively determine an unacknowledged
  application commit.
- Zero-round-trip data is replayable in ways one-round-trip protected data is
  not. An application must classify which operations can safely be admitted
  before fresh handshake state is established.

## Relevance

Atom OS should implement network endpoints as generation-bound service objects
with separate connection, stream, buffer-credit, route, credential, and
admission state. Endpoint capabilities select local bind/connect/listen rights;
the identity service provides keys or handles; the protocol service validates
the peer; and the application still authorizes the operation. Each scope gets
a finite queue and teardown ledger so a dead owner cannot leave unbounded
streams, timers, or retransmission buffers.

QUIC is a useful first advanced transport profile because it makes multiplexing,
flow control, migration, and authenticated state explicit in user space. The
architecture should nevertheless begin with a smaller transport-independent
endpoint contract and a simpler UDP/TCP or loopback implementation, then add
QUIC without leaking its connection identifiers into the kernel ABI.

## Limits

RFC 9000 is a wire-level interoperability contract, not evidence that one QUIC
implementation is memory-safe, bounded, timing-safe, or resilient to hostile
traffic. Security depends on the companion TLS profile, cryptographic
implementation, randomness, key lifecycle, and anti-amplification behavior.
The RFC does not provide application-level exactly-once execution, service
discovery, authorization, durable request results, or sink fencing. Its
migration model is asymmetric in version 1, and an Atom OS profile must record
the exact extensions and versions it supports.

## Derived work

- [Network endpoint and protocol services](../20-notes/otp-like-system-services-components/network-endpoint-and-protocol-services.md)
- [Admission, overload, and service-resource governance](../20-notes/otp-like-system-services-components/admission-overload-and-service-resource-governance.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
