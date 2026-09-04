---
title: "Guide to computer security log management"
kind: source
created: "2026-09-04"
authors:
  - "Karen Kent"
  - "Murugiah Souppaya"
published: 2006
citation_key: "kent-souppaya-2006-log-management"
container: "NIST Special Publication 800-92"
edition: null
isbn: null
doi: "10.6028/NIST.SP.800-92"
url: "https://csrc.nist.gov/pubs/sp/800/92/final"
accessed: "2026-09-04"
tags:
  - audit
  - logging
  - nist
  - operations
aliases:
  - "NIST SP 800-92"
---

# Guide to computer security log management

## Reference

Karen Kent and Murugiah Souppaya. “[Guide to Computer Security Log
Management](https://doi.org/10.6028/NIST.SP.800-92).” NIST Special Publication
800-92, September 2006.

## Research question or contribution

The guide addresses the infrastructure and operational processes required to
generate, transmit, store, analyze, retain, and protect security logs across an
organization.

## Method

This is government operational guidance. It describes architectures, policies,
roles, failure modes, and planning practices rather than presenting a new
cryptographic construction or measured experiment.

## Findings

- Log generation, collection/storage, and monitoring can be separated into
  tiers with different trust and availability responsibilities.
- Local buffering and redundant collectors help during unreliable connectivity,
  but finite storage and log volume require explicit capacity policy.
- Confidentiality and availability matter alongside integrity because logs
  often contain sensitive data and are needed during incidents.
- Time synchronization, retention, disposal, access control, and operational
  review are part of log assurance.

## Relevance

Atom should isolate producer append, durable local spool, query, retention,
witnessing, and encryption-key authority. It should define behavior for audit
outages and spool exhaustion per action class rather than silently discarding
records or allowing all effects.

## Limits

The guide is old and intentionally high level. It does not define modern
forward-secure logging, transparency witnesses, privacy-preserving queries,
anti-rollback boot identities, or an atomic link between logs and external
effects.

## Derived work

- [Audit and witness services](../20-notes/authentication-and-authorization-components/audit-and-witness-services.md)
- [Authentication and authorization components deep dive](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
