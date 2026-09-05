---
title: "Online, Asynchronous Schema Change in F1"
kind: source
created: "2026-09-05"
authors:
  - "Ian Rae"
  - "Eric Rollins"
  - "Jeff Shute"
  - "Sukhdeep S. Sodhi"
  - "Radek Vingralek"
published: 2013
citation_key: "rae-et-al-2013-online-schema-change-f1"
container: "Proceedings of the VLDB Endowment 6(11)"
edition: null
isbn: null
doi: "10.14778/2536222.2536230"
url: "https://research.google/pubs/online-asynchronous-schema-change-in-f1/"
accessed: "2026-09-05"
tags:
  - database-systems
  - online-migration
  - schema-evolution
aliases:
  - "F1 online schema change"
---

# Online, Asynchronous Schema Change in F1

## Reference

Ian Rae, Eric Rollins, Jeff Shute, Sukhdeep S. Sodhi, and Radek Vingralek.
“[Online, Asynchronous Schema Change in
F1](https://doi.org/10.14778/2536222.2536230).” *Proceedings of the VLDB
Endowment* 6, no. 11, 2013, pages 1045–1056.

## Research question or contribution

The paper develops an online schema-change protocol for a globally distributed
database with shared data, stateless servers, no global membership, and
temporarily mixed schema versions.

## Method

The authors formalize schema-change correctness, show common changes can
corrupt data, decompose them into compatible intermediate stages, implement
the protocol in F1, and report operational findings.

## Findings

- Abrupt schema replacement during mixed-version operation can cause anomalies
  and corruption.
- Safe changes can be constructed as ordered intermediate schemas under the
  stated one-version-behind bound.
- Formal modeling found subtle problems, including two production bugs.

## Relevance

Atom OS application migrations should declare compatible intermediate states,
reader/writer matrices, checkpoints, and irreversible boundaries. Layer 4 can
stage and publish generations; Layer 5 owns semantic transforms and invariant
checks.

## Limits

F1's shared-data, stateless-server, and one-version-lag assumptions are
specific. The protocol does not make external effects reversible or prove
arbitrary actor-state upgrades safe.

## Derived work

- [Application evolution, schema compatibility, and migration](../20-notes/applications-and-domain-services-components/application-evolution-schema-compatibility-and-migration.md)
- [Durable state, journals, snapshots, and projections](../20-notes/applications-and-domain-services-components/durable-state-journals-snapshots-and-projections.md)
