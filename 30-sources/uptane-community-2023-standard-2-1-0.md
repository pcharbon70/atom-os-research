---
title: "Uptane Standard for Design and Implementation version 2.1.0"
kind: source
created: "2026-09-04"
authors:
  - "Uptane Community"
published: 2023
citation_key: "uptane-community-2023-standard-2-1-0"
container: "Uptane Standard"
edition: "Version 2.1.0"
isbn: null
doi: null
url: "https://uptane.org/docs/2.1.0/standard/uptane-standard"
accessed: "2026-09-04"
tags:
  - embedded-systems
  - software-update
  - supply-chain-security
  - tuf
aliases:
  - "Uptane 2.1.0"
---

# Uptane Standard for Design and Implementation version 2.1.0

## Reference

Uptane Community. “[Uptane Standard for Design and Implementation Version
2.1.0](https://uptane.org/docs/2.1.0/standard/uptane-standard).” Released 27
June 2023.

## Research question or contribution

Uptane adapts TUF-style role-separated metadata to connected units that may be
resource-constrained, intermittently connected, safety critical, and exposed
to repository or network compromise.

## Method

This is a normative implementation standard. It specifies repository roles,
Director and Image repository interaction, version manifests, full and partial
verification, secure time, metadata ordering, and attack mitigations.

## Findings

- Root, targets, snapshot, and timestamp roles separate trust and support
  threshold and delegated authority.
- Director and Image repositories let a client compare device-specific
  assignment with artifact metadata and resist mix-and-match behavior.
- Inventory and version reports are security inputs, not merely operations
  telemetry.
- Freeze, rollback, mix-and-match, arbitrary-package, endless-data, and key-
  compromise threats require different metadata and client checks.

## Relevance

Atom should bind a release plan to the exact device/service inventory,
compatible state schema, boot and policy epochs, artifact digests, and
activation cohort. The Uptane split is a useful precedent for checking both
artifact authorization and target-specific assignment under intermittent
connectivity.

## Limits

The standard targets automotive deployments and intentionally permits
deployment-specific formats and choices. It assumes other controls for some
on-device and supply-chain threats and does not specify Atom's actor quiescence,
state transfer, health criteria, or recovery semantics.

## Derived work

- [Update and release service](../20-notes/authentication-and-authorization-components/update-and-release-service.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
