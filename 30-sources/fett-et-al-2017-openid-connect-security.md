---
title: "The Web SSO standard OpenID Connect: In-depth formal security analysis and security guidelines"
kind: source
created: "2026-09-04"
authors:
  - "Daniel Fett"
  - "Ralf Küsters"
  - "Guido Schmitz"
published: 2017
citation_key: "fett-et-al-2017-openid-connect-security"
container: "2017 IEEE 30th Computer Security Foundations Symposium (CSF)"
edition: null
isbn: null
doi: "10.1109/CSF.2017.20"
url: "https://doi.org/10.1109/CSF.2017.20"
accessed: "2026-09-04"
tags:
  - authentication
  - federation
  - formal-methods
  - openid-connect
aliases:
  - "Formal security analysis of OpenID Connect"
---

# The Web SSO standard OpenID Connect: In-depth formal security analysis and security guidelines

## Reference

Daniel Fett, Ralf Küsters, and Guido Schmitz. “[The Web SSO Standard OpenID
Connect: In-Depth Formal Security Analysis and Security
Guidelines](https://doi.org/10.1109/CSF.2017.20).” *2017 IEEE 30th Computer
Security Foundations Symposium*, pages 189–202, 2017. DOI
[10.1109/CSF.2017.20](https://doi.org/10.1109/CSF.2017.20).

## Research question or contribution

The paper asks whether OpenID Connect provides authentication, authorization,
and session-integrity properties in a detailed web model, including discovery,
dynamic registration, multiple flows, and malicious identity providers.

## Method

The authors formalize OpenID Connect in their web infrastructure model,
discover attacks, derive security guidelines and specification changes, and
prove the target properties for the repaired model under stated assumptions.
The detailed review also used the authors' [full
version](https://arxiv.org/abs/1704.08539), while the bibliographic record and
DOI above identify the abridged CSF proceedings paper.

## Findings

- Federation security depends on the composition of redirects, issuer and
  endpoint metadata, state and nonce correlation, token validation, and web
  origins; validating one signed token is insufficient.
- Mix-up and malicious-endpoint behavior can cross trust boundaries when an RP
  fails to bind a response to the expected issuer and flow.
- Authentication, authorization, and session integrity are distinct properties
  requiring different checks.
- The proof applies only when relying parties and providers implement the
  modeled mitigations and when web, TLS, and cryptographic assumptions hold.

## Relevance

Atom's federation gateway should terminate remote protocols in a confined
parser domain, pin issuer-specific metadata, bind every response to a request
record, and emit typed evidence for local policy. It should never pass a remote
token through as a kernel capability or let federated logout mutate local
session generations without local validation.

## Limits

The analysis covers the modeled OpenID Connect ecosystem at publication time.
It is not a proof of current implementations, native OS login, OAuth extensions
added later, certificate-bound tokens, or Atom's proposed gateway.

## Derived work

- [Session service](../20-notes/authentication-and-authorization-components/session-service.md)
- [Federation gateway](../20-notes/authentication-and-authorization-components/federation-gateway.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
