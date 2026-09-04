---
title: "FIDO Metadata Service"
kind: source
created: "2026-09-04"
authors:
  - "Billy Jack"
  - "Rolf Lindemann"
published: 2026
citation_key: "fido-alliance-2026-metadata-service"
container: "FIDO Alliance Proposed Standard"
edition: "Version 3.1.1"
isbn: null
doi: null
url: "https://fidoalliance.org/specs/mds/fido-metadata-service-v3.1.1-ps-20260105.html"
accessed: "2026-09-04"
tags:
  - authentication
  - fido2
  - metadata
  - passkeys
aliases:
  - "FIDO MDS 3.1.1"
---

# FIDO Metadata Service

## Reference

Billy Jack and Rolf Lindemann, editors. “[FIDO Metadata
Service](https://fidoalliance.org/specs/mds/fido-metadata-service-v3.1.1-ps-20260105.html).”
FIDO Alliance Proposed Standard 3.1.1, 5 January 2026.

## Research question or contribution

The specification defines a signed metadata BLOB through which relying parties
can obtain authenticator attestation trust anchors, model characteristics,
certification facts, firmware versions, and changing security status.

## Method

This is a normative proposed standard. The review examined BLOB signature and
sequence processing, AAGUID/model records, status reports, trust anchors,
refresh behavior, and the limits stated for certification and multi-device
keys.

## Findings

- Relying parties authenticate the metadata BLOB and choose how often to
  refresh/cache it; update cadence is therefore a security and availability
  policy.
- Status reports can identify revoked authenticators, user-verification bypass,
  key compromise, or an available update and associate status with versions.
- Metadata describes capabilities and trust anchors but the relying party still
  decides whether a model is acceptable.
- The specification says authenticator certification does not cover the
  security characteristics of multi-device keys.

## Relevance

Atom's credential registrar can record the exact signed metadata revision and
status that informed enrollment/use, reduce assurance on new warnings, and
avoid treating synchronized and device-bound credentials as equivalent.

## Limits

This is a proposed standard and depends on FIDO/vendor truth, signing-key
security, update availability, and correct mapping from a concrete
authenticator to metadata. It does not prove the authenticator, client,
synchronization provider, or account recovery secure.

## Derived work

- [Credential registrar and inventory](../20-notes/authentication-and-authorization-components/credential-registrar-and-inventory.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
