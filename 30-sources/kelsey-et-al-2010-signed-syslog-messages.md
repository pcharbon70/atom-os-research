---
title: "Signed syslog messages"
kind: source
created: "2026-09-04"
authors:
  - "John Kelsey"
  - "Jon Callas"
  - "Alexander Clemm"
published: 2010
citation_key: "kelsey-et-al-2010-signed-syslog-messages"
container: "RFC 5848"
edition: "Standards Track"
isbn: null
doi: "10.17487/RFC5848"
url: "https://www.rfc-editor.org/rfc/rfc5848.html"
accessed: "2026-09-04"
tags:
  - audit
  - logging
  - protocols
  - security
aliases:
  - "RFC 5848"
---

# Signed syslog messages

## Reference

John Kelsey, Jon Callas, and Alexander Clemm. “[Signed Syslog
Messages](https://www.rfc-editor.org/rfc/rfc5848.html).” RFC 5848, May 2010.
DOI [10.17487/RFC5848](https://doi.org/10.17487/RFC5848).

## Research question or contribution

RFC 5848 defines origin authentication, integrity, replay resistance,
sequencing, and missing-message detection for syslog across untrusted relays
and storage.

## Method

This is an IETF Standards Track protocol specification. The review used its
session identifiers, sequence windows, signature blocks, loss detection, and
collector-flooding analysis, not its dated cryptographic suite.

## Findings

- Per-origin sequencing and reboot/session identifiers are necessary to detect
  replay, reordering, truncation, and gaps across restarts.
- A signing key authenticates the producer but also lets a compromised producer
  fabricate new records; signatures do not establish truth or completeness.
- Aggregating signatures reduces cost but expands the window and amount of data
  affected by loss.
- Attackers can flood collectors or exploit verification cost, so audit
  admission and storage need explicit availability controls.

## Relevance

Atom audit producers should bind sequence numbers to an anti-rollback boot
epoch, make gaps explicit, and reserve bounded append capacity. Modern
algorithms and a forward-secure evolution scheme are required; the RFC's
protocol is evidence about semantics, not an implementation prescription.

## Limits

The mandatory cryptographic choices reflect 2010-era interoperability and
should not be copied. The protocol does not provide append-only Merkle
witnessing, local effect atomicity, confidentiality policy, or prevention of
producer omission.

## Derived work

- [Audit and witness services](../20-notes/authentication-and-authorization-components/audit-and-witness-services.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
