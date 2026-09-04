---
title: "A formal analysis of the FIDO2 protocols"
kind: source
created: "2026-09-04"
authors:
  - "Jingjing Guan"
  - "Hui Li"
  - "Haisong Ye"
  - "Ziming Zhao"
published: 2022
citation_key: "guan-et-al-2022-formal-analysis-fido2"
container: "Computer Security — ESORICS 2022, LNCS 13556, 3–21"
edition: null
isbn: null
doi: "10.1007/978-3-031-17143-7_1"
url: "https://cactilab.github.io/assets/pdf/jingjing2022fido2.pdf"
accessed: "2026-09-04"
tags:
  - authentication
  - fido2
  - formal-analysis
  - protocol-security
aliases:
  - "Formal FIDO2 analysis"
---

# A formal analysis of the FIDO2 protocols

## Reference

Jingjing Guan, Hui Li, Haisong Ye, and Ziming Zhao. “[A Formal Analysis of the
FIDO2 Protocols](https://doi.org/10.1007/978-3-031-17143-7_1).” *ESORICS
2022*, LNCS 13556, pages 3–21.

## Research question or contribution

The paper models WebAuthn and CTAP2 together in ProVerif to identify the
assumptions needed for confidentiality, authentication, and privacy goals and
to test multiple authenticator and transaction-authorization modes.

## Method

The authors formalize the complete ceremony, publish a verification front end,
and analyze client-side and server-side authenticators, PIN/token handling,
registration, assertion, rebinding, and parallel sessions.

## Findings

- End-to-end properties can fail even when the WebAuthn and CTAP components
  look safe in isolation; the binding between client and authenticator matters.
- Under the analyzed CTAP2 generation, unauthenticated key agreement in the
  client-PIN path weakens strong authentication properties.
- The model identifies authenticator-rebinding and parallel-session attacks
  under stated scenarios and proposes protocol changes.

## Relevance

Atom OS should model its exact native-login and step-up ceremony—including the
authenticator transport, trusted UI, session issuer, parallel requests, reset,
and credential rebinding—rather than cite FIDO2 conformance as an end-to-end
proof. Every challenge must bind the requester, target, operation, boot epoch,
and intended grant.

## Limits

The analysis targets an earlier CTAP2/WebAuthn generation and a symbolic model;
current CTAP 2.2 and WebAuthn Level 3 require a fresh comparison before assuming
the same attacks remain. Model omissions and implementation defects remain
outside the result.

## Derived work

- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
- [Authentication and authorization map](../10-maps/authentication-and-authorization.md)
- [System-wide authentication and authorization inquiry](../40-inquiries/what-contract-should-system-wide-authentication-and-authorization-provide.md)
