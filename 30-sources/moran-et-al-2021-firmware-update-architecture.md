---
title: "A firmware update architecture for Internet of Things"
kind: source
created: "2026-09-04"
authors:
  - "Brendan Moran"
  - "Hannes Tschofenig"
  - "David Brown"
  - "Milosch Meriac"
published: 2021
citation_key: "moran-et-al-2021-firmware-update-architecture"
container: "RFC 9019"
edition: "Informational"
isbn: null
doi: "10.17487/RFC9019"
url: "https://www.rfc-editor.org/rfc/rfc9019.html"
accessed: "2026-09-04"
tags:
  - embedded-systems
  - firmware
  - software-update
  - suit
aliases:
  - "RFC 9019"
  - "SUIT architecture"
---

# A firmware update architecture for Internet of Things

## Reference

Brendan Moran, Hannes Tschofenig, David Brown, and Milosch Meriac. “[A Firmware
Update Architecture for Internet of
Things](https://www.rfc-editor.org/rfc/rfc9019.html).” RFC 9019, April 2021.
DOI [10.17487/RFC9019](https://doi.org/10.17487/RFC9019).

## Research question or contribution

RFC 9019 defines stakeholders and functions for secure, reliable firmware
updates on constrained devices and motivates protected, transport-independent
manifests.

## Method

This is an informational IETF architecture. It separates author, device/network
operator, trust provisioning, status tracking, consumer, server, and bootloader
responsibilities and analyzes device classes and update flows.

## Findings

- Authoring an image, deciding deployment, transferring bytes, verifying a
  manifest, installing, booting, and reporting status are different powers.
- Trust anchors constrain what a key may authorize and their stores must resist
  unauthorized insertion, deletion, and modification.
- A firmware verifier performs security checks before invocation; in secure-
  boot MCU deployments this is commonly the bootloader. Recovery strategies
  are needed for interrupted or failed updates.
- Heterogeneous multi-component updates, dependencies, energy/resources, and
  automatic remote operation complicate safe activation.

## Relevance

Atom should separate release signers from node installers and keep a small boot
verifier below the Layer-4 updater. Quiescence, dependency closure, trial
activation, and recovery remain explicit even after a manifest is authentic.

## Limits

The RFC is informational and IoT-oriented. It does not select a manifest
encoding, repository security protocol, transactional installer, health model,
or Atom-specific kernel/runtime/BEAM compatibility contract.

## Derived work

- [Update and release service](../20-notes/authentication-and-authorization-components/update-and-release-service.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
