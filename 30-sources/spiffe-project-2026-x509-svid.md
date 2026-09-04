---
title: "The X.509 SPIFFE Verifiable Identity Document"
kind: source
created: "2026-09-04"
authors:
  - "SPIFFE Project"
published: null
citation_key: "spiffe-project-2026-x509-svid"
container: "SPIFFE standards repository"
edition: "Pinned revision 99470b9abc825f14aa364dfa2c3b53b02ba5db5b"
isbn: null
doi: null
url: "https://github.com/spiffe/spiffe/blob/99470b9abc825f14aa364dfa2c3b53b02ba5db5b/standards/X509-SVID.md"
accessed: "2026-09-04"
tags:
  - authentication
  - spiffe
  - workload-identity
  - x509
aliases:
  - "X.509-SVID"
  - "SPIFFE X.509-SVID specification"
---

# The X.509 SPIFFE Verifiable Identity Document

## Reference

SPIFFE Project. “[The X.509 SPIFFE Verifiable Identity
Document](https://github.com/spiffe/spiffe/blob/99470b9abc825f14aa364dfa2c3b53b02ba5db5b/standards/X509-SVID.md).”
Living stable SPIFFE standard pinned at revision
`99470b9abc825f14aa364dfa2c3b53b02ba5db5b`, accessed 4 September
2026.

## Research question or contribution

The specification profiles X.509 certificates as SPIFFE Verifiable Identity
Documents and defines how a validator distinguishes workload leaf identities
from signing certificates, binds exactly one SPIFFE ID, validates certificate
paths, and consumes X.509 trust-bundle entries.

## Method

This is a stable interoperability specification rather than an experiment.
The review focused on URI SAN cardinality, leaf/signing separation, Basic
Constraints, Key Usage, Extended Key Usage, path and leaf validation, and
bundle representation. The exact repository revision was pinned so later
changes do not silently alter the evidence.

## Findings

- An X.509-SVID contains exactly one URI SAN and therefore exactly one SPIFFE
  ID; validators must reject certificates with more than one URI SAN.
- Only a leaf certificate may identify a caller or resource. A leaf has
  `cA=false`, must not assert `keyCertSign` or `cRLSign`, and must carry a
  non-root-path `spiffe` URI.
- Signing SVIDs are validation material rather than workload-authentication
  identities; they use CA constraints and `keyCertSign`.
- Validation composes standard RFC 5280 path validation with SPIFFE-specific
  leaf checks and a trust-domain bundle. A peer authenticates the SPIFFE
  identity only when it also proves possession of the private key corresponding
  to the validated leaf; the result is still not application authorization.
- URI name constraints could reduce a compromised CA's namespace, but support
  varies and the specification does not require them in this revision.

## Relevance

Atom's X.509 compatibility profile should enforce these constraints at both
issuance and relying-party validation, pin the exact bundle revision and trust
domain, and keep signing credentials from being accepted as workload leaves.
The native local identity handle remains preferable where both endpoints are
Atom-aware because it can keep the private key outside the managed heap.

## Limits

The specification defines certificate syntax and validation, not caller
attestation, registration policy, authorization, private-key confinement,
revocation service levels, transport security, or Atom's incarnation binding.
It is a living standard, so the pinned revision—not a moving branch—is the
evidence used here.

## Derived work

- [Workload identity issuer](../20-notes/authentication-and-authorization-components/workload-identity-issuer.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
