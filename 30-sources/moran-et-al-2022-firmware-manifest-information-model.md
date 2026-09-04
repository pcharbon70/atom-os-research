---
title: "A manifest information model for firmware updates in Internet of Things (IoT) devices"
kind: source
created: "2026-09-04"
authors:
  - "Brendan Moran"
  - "Hannes Tschofenig"
  - "Henk Birkholz"
published: 2022
citation_key: "moran-et-al-2022-firmware-manifest-information-model"
container: "RFC 9124"
edition: "Informational"
isbn: null
doi: "10.17487/RFC9124"
url: "https://www.rfc-editor.org/rfc/rfc9124.html"
accessed: "2026-09-04"
tags:
  - firmware
  - manifests
  - software-update
  - suit
aliases:
  - "RFC 9124"
  - "SUIT manifest information model"
---

# A manifest information model for firmware updates in Internet of Things (IoT) devices

## Reference

Brendan Moran, Hannes Tschofenig, and Henk Birkholz. “[A Manifest Information
Model for Firmware Updates in Internet of Things (IoT)
Devices](https://www.rfc-editor.org/rfc/rfc9124.html).” RFC 9124, January 2022.
DOI [10.17487/RFC9124](https://doi.org/10.17487/RFC9124).

## Research question or contribution

RFC 9124 identifies the protected information a machine-processable firmware
manifest needs to reject expired, incompatible, misplaced, replaced,
unauthenticated, or rollback updates.

## Method

This is an informational IETF information model and threat analysis. It defines
sequence, vendor/class/component identifiers, precursor/dependency conditions,
expiry, payload type/digest/size, storage/processing instructions, signatures,
and delegation-chain elements.

## Findings

- Compatibility and authority apply to exact vendor, class, component,
  precursor, version, payload type, and storage location—not merely a digest.
- A nonwrapping monotonic sequence and protected high-water state distinguish
  release security order from the human-visible software version.
- The manifest must remain immutable between validation and use to avoid TOCTOU.
- Payload size, whole-image digest, dependency, and format information support
  fail-early resource and compatibility checks.
- Deliberately reinstalling older bytes can remain secure only under a newly
  authorized higher manifest sequence.

## Relevance

Atom's release plan should authenticate hardware/boot/runtime/BEAM/OTP/policy/
schema compatibility, target generation, dependencies, payload bounds, and the
intended inactive destination. Operational rollback must not lower the security
sequence.

## Limits

The information model does not define a wire encoding, repository protocol,
installer, state-migration transaction, health authority, or proof that signed
firmware is safe.

## Derived work

- [Update and release service](../20-notes/authentication-and-authorization-components/update-and-release-service.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
