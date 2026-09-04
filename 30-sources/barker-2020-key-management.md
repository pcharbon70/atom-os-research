---
title: "Recommendation for key management: Part 1 – General"
kind: source
created: "2026-09-04"
authors:
  - "Elaine Barker"
published: 2020
citation_key: "barker-2020-key-management"
container: "NIST Special Publication 800-57 Part 1 Revision 5"
edition: "Revision 5"
isbn: null
doi: "10.6028/NIST.SP.800-57pt1r5"
url: "https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final"
accessed: "2026-09-04"
tags:
  - cryptography
  - key-management
  - nist
  - secrets
aliases:
  - "NIST SP 800-57 Part 1 Rev. 5"
---

# Recommendation for key management: Part 1 – General

## Reference

Elaine Barker. “[Recommendation for Key Management: Part 1 –
General](https://doi.org/10.6028/NIST.SP.800-57pt1r5).” NIST Special
Publication 800-57 Part 1 Revision 5, May 2020.

## Research question or contribution

The publication defines cryptographic key types, security services, lifecycle
states, protection requirements, metadata, compromise handling, inventory,
and institutional practices for key management.

## Method

This is NIST technical guidance based on cryptographic and operational practice. It
classifies keying material by purpose and lifecycle and gives requirements and
recommendations; it does not evaluate a particular key service or hardware
module.

## Findings

- Key type and authorized use matter: signing, authentication, encryption,
  key agreement, derivation, and wrapping powers should not be conflated.
- Metadata—identity, owner, purpose, algorithm, status, validity and usage
  periods, and associations—needs protection as well as the key bytes.
- Generation, registration, activation, rotation, deactivation, compromise,
  archival, recovery, and destruction are distinct lifecycle events.
- A compromise-recovery plan and inventory are necessary because key loss,
  exposure, and expiration have different consequences.

## Relevance

Atom's key and secret service should expose opaque handles with narrow
operation facets, protected metadata, explicit lifecycle transitions, and
auditable rotation/destruction. Recovery policy must distinguish replacing an
authentication key from recovering a data-encryption key because the latter
is decryption authority.

## Limits

SP 800-57 is general guidance and assumes a larger organizational setting. It
does not define an IPC interface, guarantee non-exportability, solve side
channels, or select a hardware root and cryptographic profile for Atom.

## Derived work

- [Key and secret service](../20-notes/authentication-and-authorization-components/key-and-secret-service.md)
- [Recovery coordinator](../20-notes/authentication-and-authorization-components/recovery-coordinator.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
