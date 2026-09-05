---
title: "Practical Access Control Management for Distributed Collaborative Editors"
kind: source
created: "2026-09-04"
authors:
  - "Asma Cherif"
  - "Abdessamad Imine"
  - "Michaël Rusinowitch"
published: "2014-12"
citation_key: "cherif-et-al-2014-access-control-collaborative-editors"
container: "Pervasive and Mobile Computing 15"
edition: null
isbn: null
doi: "10.1016/j.pmcj.2013.09.004"
url: "https://doi.org/10.1016/j.pmcj.2013.09.004"
accessed: "2026-09-04"
tags:
  - access-control
  - collaboration
  - consistency
  - distributed-systems
aliases:
  - "Access control for distributed editors"
---

# Practical Access Control Management for Distributed Collaborative Editors

## Reference

Asma Cherif, Abdessamad Imine, and Michaël Rusinowitch. “[Practical Access
Control Management for Distributed Collaborative
Editors](https://doi.org/10.1016/j.pmcj.2013.09.004).” *Pervasive and Mobile
Computing* 15, pages 62–86, December 2014.

## Contribution

The paper studies the interaction between replicated collaborative editing and
access-control policy. It shows why independently replicating document and
policy state can cause replicas to accept forbidden edits or reject permitted
ones and proposes an optimistic management approach with later repair.

## Method

The authors formalize document and policy replication, identify consistency
problems, propose algorithms and repair behavior, and evaluate an
implementation. Their permitted temporary inconsistency is part of the model,
not a suitable default for secrets or irreversible effects.

## Findings

- Content state and authorization state can advance on different causal paths,
  making a locally plausible decision globally stale.
- Convergence of document and policy replicas does not retroactively make an
  unauthorized disclosure safe.
- Optimistic acceptance improves availability only by permitting transient
  policy violations and requiring repair.
- Security-sensitive actions need a declared freshness or coordination
  profile rather than one universal offline rule.

## Relevance

Atom OS must bind a collaborative edit to the policy, relationship, object,
and revocation generations under which it was admitted. Offline edits without
current authority may be stored as private proposals, but must not become
published grants or irreversible effects through ordinary data merge.

## Limits

The paper's repair approach is unacceptable where data already escaped or an
effect cannot be compensated. It does not supply Atom OS capability issuance,
trusted interaction, project import, or provider-update semantics.

## Derived work

- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
