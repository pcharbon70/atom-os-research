---
title: "Making retries safe with idempotent APIs"
kind: source
created: "2026-09-09"
authors:
  - "Malcolm Featonby"
published: "2021-01-15"
citation_key: "featonby-2021-idempotent-apis"
container: "Amazon Builders' Library"
edition: null
isbn: null
doi: null
url: "https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/"
accessed: "2026-09-09"
tags:
  - application-architecture
  - distributed-systems
aliases: []
---

# Making retries safe with idempotent APIs

## Reference

Malcolm Featonby. “[Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/).”
Amazon Builders' Library, 2021-01-15.

Date evidence: [AWS announcement, 15 January 2021](https://aws.amazon.com/about-aws/whats-new/2021/01/new-abl-article-making-retries-safe-with-idempotent-APIs/).

## Research question or contribution

How should an API represent a caller's repeated intent?

## Method

Read the first-party article's identity, atomicity, response, late-arrival and parameter-mismatch sections. Publication date follows AWS's launch announcement.

## Findings

The design uses caller request IDs, atomic mutation/result recording, parameter validation and resource-aware retention. Repeated responses preserve meaning while resource status may change.

## Relevance

Atom OS inference: keep one logical execution with advancing pending status, and reject expired identities rather than silently re-admitting forgotten requests. User-session loss needs a durable client-action binding beyond transport retries.

## Limits

This is practitioner experience, not a universal guarantee. The endpoint must implement its advertised behavior; the article supplies no indefinite retry promise.

## Derived work

- [Operation identity and honest outcome ledgers](../20-notes/applications-and-domain-services-components/typed-commands-queries-events-and-protocol-contracts/operation-identity-and-honest-outcome-ledgers.md).
- [Effect reconciliation and unqueryable repair](../20-notes/applications-and-domain-services-components/external-effects-ports-adapters-and-reconciliation/effect-reconciliation-and-unqueryable-repair.md).
- [Application internal-services research session](../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md).
