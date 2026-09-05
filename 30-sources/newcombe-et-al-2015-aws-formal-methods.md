---
title: "How Amazon Web Services Uses Formal Methods"
kind: source
created: "2026-09-05"
authors:
  - "Chris Newcombe"
  - "Tim Rath"
  - "Fan Zhang"
  - "Bogdan Munteanu"
  - "Marc Brooker"
  - "Michael Deardeuff"
published: 2015
citation_key: "newcombe-et-al-2015-aws-formal-methods"
container: "Communications of the ACM 58(4)"
edition: null
isbn: null
doi: "10.1145/2699417"
url: "https://www.amazon.science/publications/how-amazon-web-services-uses-formal-methods"
accessed: "2026-09-05"
tags:
  - distributed-systems
  - formal-methods
  - model-checking
aliases:
  - "AWS formal methods"
---

# How Amazon Web Services Uses Formal Methods

## Reference

Chris Newcombe, Tim Rath, Fan Zhang, Bogdan Munteanu, Marc Brooker, and Michael
Deardeuff. “[How Amazon Web Services Uses Formal
Methods](https://doi.org/10.1145/2699417).” *Communications of the ACM* 58, no.
4, 2015, pages 66–73.

## Research question or contribution

The article reports how teams used TLA+ specifications and model checking to
reason about critical distributed algorithms and system designs at AWS.

## Method

The authors describe several industrial case studies, errors found, modeling
practice, and adoption experience. This is first-party observational evidence,
not an independent controlled experiment.

## Findings

- Small executable specifications exposed subtle design errors not found by
  conventional testing or review in the reported systems.
- Modeling helped teams clarify safety and liveness properties before code was
  complete.
- The practical value depended on selecting the right abstraction and
  properties rather than modeling every implementation detail.

## Relevance

High-consequence Layer 5 outcomes, workflows, migrations, and conflict policies
should have executable state models and checked invariants before implementation
fault injection.

## Limits

The model is not the code, and omitted assumptions or properties can hide real
failures. The evidence is first-party and does not quantify benefits across
ordinary application teams.

## Derived work

- [Semantic observability, testing, and assurance](../20-notes/applications-and-domain-services-components/semantic-observability-testing-and-assurance.md)
