---
title: "xDS REST and gRPC protocol"
kind: source
created: "2026-09-04"
authors:
  - "Envoy project"
published: null
citation_key: "envoy-project-2026-xds-protocol"
container: "Envoy documentation"
edition: "Envoy 1.40.0-dev documentation"
isbn: null
doi: null
url: "https://www.envoyproxy.io/docs/envoy/latest/api-docs/xds_protocol.html"
accessed: "2026-09-04"
tags:
  - configuration
  - control-planes
  - protocols
  - reconciliation
  - versioning
aliases:
  - "Envoy xDS configuration protocol"
---

# xDS REST and gRPC protocol

## Reference

Envoy project. “[xDS REST and gRPC
protocol](https://www.envoyproxy.io/docs/envoy/latest/api-docs/xds_protocol.html).”
Envoy 1.40.0-dev documentation, accessed 2026-09-04.

## Research question or contribution

The xDS protocol specifies how a control plane sends versioned configuration
resources to long-running data-plane clients, how clients acknowledge or
reject candidates, and how stream restarts and resource deletion are handled.
It supplies concrete practitioner evidence for separating configuration
receipt, validation, acknowledgement, and actual activation.

## Method

The current protocol document was read for state-of-the-world and delta
variants, version and nonce behavior, ACK/NACK meaning, reconnection, and
resource consistency. No Envoy binary or control plane was run. The page is
living development documentation, so the displayed edition and access date
are part of the record.

## Findings

- Responses carry a resource version and a stream-local nonce. Version
  identifies configuration state; nonce correlates a particular response and
  is not a globally durable configuration identifier.
- A client ACK says the response was valid and that it intends to apply the
  configuration. It does not prove that every dependent subsystem has already
  made the new version active.
- A NACK carries rejection detail while the client retains its last accepted
  valid configuration. Failure to adopt a new candidate need not destroy the
  previous working generation.
- State-of-the-world responses describe a complete resource set for a type;
  delta streams describe additions, changes, and removals and therefore need
  explicit client state and resynchronization behavior.
- Ordering across resource types is a control-plane problem. Correct rollout
  may require dependency sequencing or a transaction-like aggregate rather
  than independently updating references and referents.
- Reconnection loses stream-local response state. The client must advertise
  the versions it actually holds; neither side may infer activation from an
  old transport acknowledgement.

## Relevance

Atom OS should publish a typed immutable `ConfigSnapshot` and distinguish at
least `received`, `validated`, `prepared`, and `active`. An acknowledgement
records the candidate a service can accept, while the service reports its
active digest only after reaching a declared safe point. The configuration
controller can retain the last valid snapshot after a rejection and can use a
coordination barrier when several services truly require simultaneous
semantic activation.

The nonce/version distinction also reinforces the repository's generation
model: a session token correlates one exchange, while a content digest and
monotonic activation revision identify durable configuration state. Neither
credential rotation nor a config stream is itself an authorization decision.

## Limits

xDS is designed for Envoy's network-proxy resources and accepts a large,
evolving API surface. It is not a proof of atomic multi-service activation,
bounded memory, secrecy, or safe device configuration. ACK is intentionally
weaker than completed application, and transport recovery still depends on
the implementation. Atom OS should reuse the semantic distinctions, not the
full protocol or its deployment assumptions.

## Derived work

- [Configuration, workload identity, and secrets](../20-notes/otp-like-system-services-components/configuration-workload-identity-and-secrets.md)
- [Application lifecycle and dependency orchestration](../20-notes/otp-like-system-services-components/application-lifecycle-and-dependency-orchestration.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
