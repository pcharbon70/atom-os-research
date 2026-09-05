---
title: "Recommendation for block cipher modes of operation: GCM and GMAC"
kind: source
created: "2026-09-05"
authors:
  - "Morris Dworkin"
published: 2007
citation_key: "dworkin-2007-gcm-gmac"
container: "NIST Special Publication 800-38D"
edition: "SP 800-38D"
isbn: null
doi: "10.6028/NIST.SP.800-38D"
url: "https://doi.org/10.6028/NIST.SP.800-38D"
accessed: "2026-09-05"
tags:
  - authenticated-encryption
  - cryptography
  - diagnostics
  - security
aliases:
  - "NIST SP 800-38D"
---

# Recommendation for block cipher modes of operation: GCM and GMAC

## Reference

Morris Dworkin. *Recommendation for Block Cipher Modes of Operation:
Galois/Counter Mode (GCM) and GMAC*. NIST Special Publication 800-38D, 2007.
DOI [10.6028/NIST.SP.800-38D](https://doi.org/10.6028/NIST.SP.800-38D).

## Research question or contribution

Which properties and nonce obligations arise when crash evidence is protected
with an authenticated-encryption construction?

## Method

The standard's authenticated-encryption interface, additional authenticated
data, tag, IV uniqueness, and replay discussion were read as cryptographic
requirements. The document is not treated as a command to select GCM before an
Atom target and key lifecycle are defined.

## Findings

- Authenticated encryption can provide confidentiality for plaintext and
  integrity/authenticity for both ciphertext and additional metadata.
- Security critically depends on IV uniqueness for a given key; fatal-path
  concurrency, reboot, and counter rollback can therefore destroy security if
  nonce allocation is improvised after failure.
- A tag detects modification with a bounded forgery probability but says
  nothing about whether the record is the newest valid record.
- Replay detection is a surrounding protocol responsibility, not a consequence
  of successful tag verification alone.
- Key storage, algorithm selection, implementation integrity, and failure
  behavior remain outside the mode definition.

## Relevance

Atom should pre-provision any crash-export key and nonce/sequence allocation
while healthy, authenticate immutable header fields as associated data, and
never block the minimal local seal on encryption. A protected raw capsule may
be encrypted during post-seal custody transfer; if safe nonce continuity or a
key is unavailable, the system should retain protected local evidence and
report the missing property rather than export plaintext automatically.

## Limits

NIST has announced revision work for SP 800-38D. The publication specifies a
mode, not a key-management, crash-consistency, platform-root, or diagnostic
authorization system. Atom should specify required security properties and
permit a reviewed profile rather than make one algorithm part of the kernel
ABI.

## Derived work

- [Crash-safe sink](../20-notes/kernel-hardware-and-architecture-components/architecture-faults-and-diagnostics/crash-safe-sink.md)
