---
title: "The Update Framework Specification version 1.0.36"
kind: source
created: "2026-09-04"
authors:
  - "Justin Cappos"
  - "Trishank Karthik Kuppusamy"
  - "Joshua Lock"
  - "Marina Moore"
  - "Lukas Pühringer"
published: null
citation_key: "tuf-project-2026-specification-1-0-36"
container: "The Update Framework specification"
edition: "Version 1.0.36"
isbn: null
doi: null
url: "https://theupdateframework.github.io/specification/v1.0.36/index.html"
accessed: "2026-09-04"
tags:
  - anti-rollback
  - software-update
  - supply-chain-security
  - tuf
aliases:
  - "TUF specification 1.0.36"
---

# The Update Framework Specification version 1.0.36

## Reference

Justin Cappos, Trishank Karthik Kuppusamy, Joshua Lock, Marina Moore, and Lukas
Pühringer, editors. “[The Update Framework Specification Version
1.0.36](https://theupdateframework.github.io/specification/v1.0.36/index.html).”
Last modified 5 August 2026.

## Research question or contribution

The specification defines role-separated signed metadata and a precise client
workflow for securely obtaining target files despite mirror/network attack and
limited signing-key compromise.

## Method

This is the current normative TUF specification. The review covered root,
targets, snapshot, timestamp, threshold/delegation, consistent-snapshot, client
workflow, rollback/freeze/mix-and-match defenses, and resource-bound
requirements.

## Findings

- Root, targets, snapshot, and timestamp roles separate trust; each can use
  multiple keys and a signature threshold, while root keys should remain
  offline.
- Root updates are sequential and must be authenticated under the old and new
  trusted state before the client persists a new root.
- Timestamp and snapshot version/hash relations detect freeze, rollback, fast-
  forward, and mix-and-match behavior under the stated clock and key
  assumptions.
- Clients must bound downloaded bytes, root updates, and delegated-role visits
  to resist endless-data and delegation attacks.
- TUF deliberately stops after securely obtaining verified target bytes; the
  application owns installation and situation-specific error policy.

## Relevance

Atom should profile this workflow for all signed release artifacts and preserve
the boundary between verification and typed inactive-slot installation. Root
high-water state, exact resource bounds, algorithms, time, and offline recovery
need an Atom-specific POUF-like profile.

## Limits

The specification cannot provide update availability against an on-path
attacker, does not validate software correctness or supply-chain provenance,
and does not define activation, state migration, health, rollback safety, or
recovery after root-threshold compromise.

## Derived work

- [Update and release service](../20-notes/authentication-and-authorization-components/update-and-release-service.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
