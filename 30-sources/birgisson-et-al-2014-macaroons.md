---
title: "Macaroons: cookies with contextual caveats for decentralized authorization in the cloud"
kind: source
created: "2026-09-04"
authors:
  - "Arnar Birgisson"
  - "Joe Gibbs Politz"
  - "Úlfar Erlingsson"
  - "Ankur Taly"
  - "Michael Vrable"
  - "Mark Lentczner"
published: 2014
citation_key: "birgisson-et-al-2014-macaroons"
container: "Network and Distributed System Security Symposium 2014"
edition: null
isbn: "1-891562-35-5"
doi: "10.14722/ndss.2014.23212"
url: "https://www.ndss-symposium.org/wp-content/uploads/2017/09/04_3_1.pdf"
accessed: "2026-09-04"
tags:
  - authorization
  - delegation
  - distributed-systems
  - macaroons
aliases:
  - "Macaroons"
---

# Macaroons: cookies with contextual caveats for decentralized authorization in the cloud

## Reference

Arnar Birgisson, Joe Gibbs Politz, Úlfar Erlingsson, Ankur Taly, Michael
Vrable, and Mark Lentczner. “[Macaroons: Cookies with Contextual Caveats for
Decentralized Authorization in the Cloud](https://doi.org/10.14722/ndss.2014.23212).”
NDSS 2014.

## Research question or contribution

The paper introduces efficient HMAC-based authorization credentials that a
holder can attenuate and delegate by adding first-party or third-party caveats
without contacting the original issuer for each delegation.

## Method

The authors define the chained-MAC construction and caveat semantics, analyze
security and expressiveness, implement several service integrations, and
measure cryptographic and request-processing costs.

## Findings

- A derived macaroon can only add restrictions; caveats can constrain action,
  resource, time, location, request context, or required third-party discharge.
- Third-party caveats permit an independent service to supply fresh evidence
  without revealing its proof to the original delegator.
- Macaroons are restricted bearer credentials: possession normally enables use
  unless a caveat additionally binds the request to a holder or channel.
- Caveat interpretation is part of the verifier’s trusted code, and delegation
  remains only as safe as attenuation, key protection, discharge binding, and
  context validation.

## Relevance

Macaroon-like attenuation is useful at Atom OS distribution gateways and for
explicitly delegated, disconnected workflows. It should not replace local
kernel capabilities. Any portable token profile must require audience,
resource, action, expiry, nonce or request binding, delegation-depth, and
revocation-epoch caveats, and should be sender-constrained for sensitive use.

## Limits

The construction does not provide identity proofing, holder-of-key by default,
global revocation, trusted clocks, policy consistency, or a safe caveat
language. Bearer replay and verifier disagreement remain serious hazards. The
paper’s workloads and performance figures do not establish suitability for an
OS kernel or every network topology.

## Derived work

- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
- [Authentication and authorization map](../10-maps/authentication-and-authorization.md)
- [System-wide authentication and authorization inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
