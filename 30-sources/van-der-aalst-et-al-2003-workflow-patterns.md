---
title: "Workflow Patterns"
kind: source
created: "2026-09-05"
authors:
  - "W. M. P. van der Aalst"
  - "A. H. M. ter Hofstede"
  - "B. Kiepuszewski"
  - "A. P. Barros"
published: 2003
citation_key: "van-der-aalst-et-al-2003-workflow-patterns"
container: "Distributed and Parallel Databases 14(1)"
edition: null
isbn: null
doi: "10.1023/A:1022883727209"
url: "https://doi.org/10.1023/A:1022883727209"
accessed: "2026-09-05"
tags:
  - business-processes
  - workflow
  - workflow-patterns
aliases:
  - "Control-flow workflow patterns"
---

# Workflow Patterns

## Reference

W. M. P. van der Aalst, A. H. M. ter Hofstede, B. Kiepuszewski, and A. P.
Barros. “[Workflow Patterns](https://doi.org/10.1023/A:1022883727209).”
*Distributed and Parallel Databases* 14, no. 1, 2003, pages 5–51.

## Research question or contribution

The paper develops a vocabulary of recurring control-flow structures and uses
it to compare the expressive support of workflow products and languages.

## Method

The authors derive and define patterns for sequence, branching, joining,
multiple instances, cancellation, and related structures, then evaluate
commercial workflow systems against them.

## Findings

- Workflow requirements extend far beyond a linear list of retrying tasks.
- Choice, synchronization, cancellation, and multiple-instance behavior need
  precise semantics.
- Products that appear similar can differ materially in supported control
  behavior.

## Relevance

Layer 5 process managers should expose a small, explicit, testable set of
control semantics rather than encode hidden branches in callbacks. The
patterns inform workflow modeling; durability, authority, and business
compensation remain separate contracts.

## Limits

The study reflects workflow systems of its period and focuses on control flow.
It does not define actor recovery, capability grants, durable timers,
idempotency, or external-effect outcomes.

## Derived work

- [Workflows, process managers, timers, and compensation](../20-notes/applications-and-domain-services-components/workflows-process-managers-timers-and-compensation.md)
- [Semantic observability, testing, and assurance](../20-notes/applications-and-domain-services-components/semantic-observability-testing-and-assurance.md)
