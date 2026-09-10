---
title: "Configuration, workload identity, and secrets: internal services"
kind: map
created: "2026-09-10"
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Configuration, workload identity, and secrets: internal services

## Purpose

Separate immutable configuration construction, actual adoption, attested caller
binding and credential lifetime.

This directory decomposes [Configuration, workload identity, and secrets](../configuration-workload-identity-and-secrets.md).
These are logical responsibilities, not a requirement for one process per study.

## What belongs here

Keep owned state, authority, transition evidence, failure cases, alternatives
and unexecuted verification obligations here. This is full-system Layer 4
architecture research, not a PoC, QEMU profile or implementation plan. Layers
2–3 supply enforcement and managed execution; Layer 5 supplies domain meaning.
The [session manifest](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) records provenance.

## Index

### Subdirectories

- None yet.

### Documents

- [Configuration snapshot schema and source precedence](configuration-snapshot-schema-and-source-precedence.md) — How can a complete configuration be reproducible without embedding secrets or mutable operational state?
- [Configuration acknowledgement, adoption, and rollout](configuration-acknowledgement-adoption-and-rollout.md) — How can a controller distinguish a valid candidate from the configuration actually in use?
- [Workload attestation and credential-authority binding](workload-attestation-and-credential-authority-binding.md) — How does the broker identify its caller without trusting a self-declared service name?
- [Credential rotation, secret confinement, and issuer outage](credential-rotation-secret-confinement-and-issuer-outage.md) — What remains valid when credentials rotate or issuance becomes unavailable?

## Maintaining this index

Inventory every direct child. Keep the parent report, component index, topic
map and inquiry connected when responsibilities change. Decompose according
to distinct state, authority and completion needs, not a fixed document quota.
Writing these studies does not validate their proposed guarantees.
