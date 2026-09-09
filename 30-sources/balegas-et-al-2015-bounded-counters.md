---
title: "Extending Eventually Consistent Cloud Databases for Enforcing Numeric Invariants"
kind: source
created: "2026-09-09"
authors:
  - "Valter Balegas"
  - "Diogo Serra"
  - "Sérgio Duarte"
  - "Carla Ferreira"
  - "Marc Shapiro"
  - "Rodrigo Rodrigues"
  - "Nuno Preguiça"
published: 2015
citation_key: "balegas-et-al-2015-bounded-counters"
container: "34th IEEE Symposium on Reliable Distributed Systems (SRDS 2015), 31–36"
edition: null
isbn: null
doi: "10.1109/SRDS.2015.32"
url: "https://perso.lip6.fr/Marc.Shapiro/papers/2015/numeric-invariants-SRDS-2015.pdf"
accessed: "2026-09-09"
tags:
  - application-architecture
  - distributed-systems
aliases: []
---

# Extending Eventually Consistent Cloud Databases for Enforcing Numeric Invariants

## Reference

Valter Balegas, Diogo Serra, Sérgio Duarte, Carla Ferreira, Marc Shapiro, Rodrigo Rodrigues, Nuno Preguiça. “[Extending Eventually Consistent Cloud Databases for Enforcing Numeric Invariants](https://perso.lip6.fr/Marc.Shapiro/papers/2015/numeric-invariants-SRDS-2015.pdf).”
34th IEEE Symposium on Reliable Distributed Systems (SRDS 2015), 31–36, 2015. DOI: [10.1109/SRDS.2015.32](https://doi.org/10.1109/SRDS.2015.32).

Bibliography verified against the [authors' institutional record](https://novaresearch.unl.pt/en/publications/extending-eventually-consistent-cloud-databases-for-enforcing-num/).

## Research question or contribution

Can replicated numerical bounds survive independent local updates?

## Method

Read the conference paper's system model, counter algorithm, middleware and evaluation setup. The author-hosted six-page version and the institutional bibliographic record identify seven authors; the earlier arXiv version has a different author list.

## Findings

Rights are distributed and consumed locally; transfer and merge conserve the bound. Local conditional writes serialize each replica's updates. The Riak experiment compares weak and strong counter baselines.

## Relevance

Atom OS inference: separate numerical rights from authentication, and require an explicit replica-generation and anti-rollback contract before allowing offline scarce-resource spending. Prototype cloning, lost transfer replies and backup restoration are decisive adversarial cases.

## Limits

The model assumes crash failures with persistent state intact. Unreachable allocations become unavailable; they are not safely recreated by timeout. The evaluation does not establish malicious-replica safety or Atom OS performance.

## Derived work

- [Escrow rights conservation and transfer](../20-notes/applications-and-domain-services-components/invariants-transactions-and-concurrency-policy/escrow-rights-conservation-and-transfer.md).
- [Offline scarce rights and online effect gates](../20-notes/applications-and-domain-services-components/offline-collaboration-replication-and-conflict-semantics/offline-scarce-rights-and-online-effect-gates.md).
- [Application internal-services research session](../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md).
