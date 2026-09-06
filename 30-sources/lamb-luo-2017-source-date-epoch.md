---
title: "SOURCE_DATE_EPOCH specification"
kind: source
created: "2026-09-06"
authors: ["Chris Lamb","Ximin Luo"]
published: "2017-11-27"
citation_key: "lamb-luo-2017-source-date-epoch"
container: "Reproducible Builds"
edition: "Revision 1.1"
isbn: null
doi: null
url: "https://reproducible-builds.org/specs/source-date-epoch/"
accessed: "2026-09-05"
tags:
  - build-systems
  - reproducibility
aliases: []
---

# SOURCE_DATE_EPOCH specification

## Reference

Chris Lamb, Ximin Luo. [SOURCE_DATE_EPOCH specification](https://reproducible-builds.org/specs/source-date-epoch/). Reproducible Builds. 2017-11-27. Revision 1.1. Accessed 2026-09-05; source record created 2026-09-06.

## Research question or contribution

Evidence relevant to freestanding build and static images in the CLI-first operating-system proof of concept.

## Method

Read revision history and normative timestamp rules.

## Findings

The timestamp must be deterministic from source inputs, exported to subprocesses, and used instead of build-time clock values where applicable. The specification also defines timestamp clamping.

## Relevance

Informs the proposed requirement contract and its negative tests. This source does not establish that Atom implements or passes that contract.

## Limits

Controlling timestamps does not control compilers, link order, build paths, locale, dependency downloads or uninitialized data. It neither proves source correctness nor independently authenticates a compiler.

## Derived work

- [Freestanding build and static images](../20-notes/proof-of-concept-requirements/freestanding-build-and-static-images.md)
