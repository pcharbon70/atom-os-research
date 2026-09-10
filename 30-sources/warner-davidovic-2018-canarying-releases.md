---
title: "Canarying Releases"
kind: source
created: "2026-09-10"
authors:
  - "Alec Warner"
  - "Štěpán Davidovič"
published: 2018
citation_key: "warner-davidovic-2018-canarying-releases"
container: "The Site Reliability Workbook"
edition: "Chapter 16; online edition"
isbn: null
doi: null
url: "https://sre.google/workbook/canarying-releases/"
accessed: "2026-09-10"
tags:
  - system-services
  - reliability
  - service-architecture
aliases: []
---

# Canarying Releases

## Reference

Alec Warner and Štěpán Davidovič, with Alex Hidalgo, Betsy Beyer, Kyle Smith and Matt Duftler. [Canarying Releases](https://sre.google/workbook/canarying-releases/). The Site Reliability Workbook, chapter 16, 2018.

## Research question or contribution

How should limited rollout exposure inform expansion decisions?

## Method

First-party engineering chapter with a worked App Engine example; population, duration, attribution and asynchronous-pipeline sections were read.

## Findings

Version-specific, representative metrics reveal regressions hidden by aggregate traffic. Contemporaneous controls and absolute service indicators complement one another; asynchronous evaluation must cover complete work units.

## Relevance

Proposed Atom OS use: bounded effect-scoped cohorts and explicit Inconclusive outcomes when evidence is insufficient.

## Limits

Operational guidance, not a universal statistical test, security proof or evidence that state rollback is possible.

## Derived work

- [Internal-service study](../20-notes/otp-like-system-services-components/release-update-rollback-and-state-migration/canary-cohorts-attribution-and-inconclusive-evidence.md).
- [Research session](../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md).
