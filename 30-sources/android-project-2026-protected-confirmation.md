---
title: "Android Protected Confirmation"
kind: source
created: "2026-09-04"
authors:
  - "Android Open Source Project"
published: null
citation_key: "android-project-2026-protected-confirmation"
container: "Android Open Source Project documentation"
edition: null
isbn: null
doi: null
url: "https://source.android.com/docs/security/features/protected-confirmation"
accessed: "2026-09-04"
tags:
  - android
  - hardware-security
  - trusted-path
  - user-interface
aliases:
  - "ConfirmationUI"
---

# Android Protected Confirmation

## Reference

Android Open Source Project. “[Android Protected
Confirmation](https://source.android.com/docs/security/features/protected-confirmation).”
Last updated 16 July 2026. See also the first-party [implementation
guide](https://source.android.com/docs/security/features/protected-confirmation/implementation)
for the rendering, input, and interruption requirements used below.

## Research question or contribution

The documentation describes a hardware-protected Trusted UI and KeyMint
integration that lets a user confirm a displayed message and produces a
cryptographic confirmation token for a critical transaction.

## Method

These are first-party architecture and implementation documents for supported
Android devices, not a peer-reviewed security proof or an evaluation of Atom.
The review focused on protected rendering/input, message binding, interruption,
and the boundary between ordinary Android and TEE components.

## Findings

- ConfirmationUI and a KeyMint extension reside in a TEE on the documented
  profile and bind approval to the prompted message.
- Protected input/output must be treated atomically; overlays, incomplete
  rendering, unsafe streaming, or interruption abort confirmation.
- A key can require a trusted-confirmation token before an operation.
- The guarantee depends on device/TEE/firmware support and does not imply the
  user understood or freely approved the transaction.

## Relevance

Atom can use this as an implementation precedent for full-render-before-arm,
abort-on-route-change, and an operation-bound confirmation receipt. The Atom
broker still needs its own hardware profile, canonical schemas, accessibility,
multi-seat handling, and independent verification.

## Limits

The claims are platform documentation and assume a trustworthy TEE, display,
input path, KeyMint implementation, and manufacturer integration. They do not
define general authentication, authorization, remote administration, or user-
comprehension properties.

## Derived work

- [Trusted-interaction broker](../20-notes/authentication-and-authorization-components/trusted-interaction-broker.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
