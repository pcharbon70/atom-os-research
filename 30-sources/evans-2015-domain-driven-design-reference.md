---
title: "Domain-Driven Design Reference: Definitions and Pattern Summaries"
kind: source
created: "2026-09-05"
authors:
  - "Eric Evans"
published: 2015
citation_key: "evans-2015-domain-driven-design-reference"
container: "Domain Language, Inc."
edition: null
isbn: null
doi: null
url: "https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf"
accessed: "2026-09-05"
tags:
  - application-architecture
  - domain-driven-design
  - domain-modeling
aliases:
  - "DDD Reference"
---

# Domain-Driven Design Reference: Definitions and Pattern Summaries

## Reference

Eric Evans. “[Domain-Driven Design Reference: Definitions and Pattern
Summaries](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf).”
Domain Language, Inc., 2015.

## Research question or contribution

The reference condenses the strategic and tactical patterns of domain-driven
design: ubiquitous language, bounded contexts and context maps, layered
architecture, entities, value objects, aggregates, services, domain events,
repositories, and factories.

## Method

This is an authorial pattern reference distilled from the larger DDD body of
practice, not a controlled comparative experiment. The complete reference was
read for boundary definitions and for the responsibilities assigned to domain,
application, presentation, and infrastructure code.

## Findings

- A bounded context makes explicit where one model and its language apply;
  relationships and translations between models must also be explicit.
- Entities retain identity across changing attributes. An aggregate is a
  consistency boundary whose root controls external references and invariant-
  preserving changes.
- Application code coordinates use cases, while domain objects and domain
  services express business rules. Infrastructure and presentation should not
  contaminate that model.
- A domain event records something meaningful that happened in the domain; it
  is not synonymous with every log, transport message, or telemetry record.

## Relevance

The reference supplies the vocabulary for Atom OS Layer 5. The synthesis keeps
its semantic boundaries separate from actor activation, supervision,
protected-domain, deployment, and tenant boundaries. Aggregate-per-actor is
therefore a candidate implementation profile rather than a rule inferred from
DDD.

## Limits

The patterns do not specify crash consistency, message delivery, distributed
transactions, capability security, resource enforcement, or empirical
performance. DDD terminology is also used inconsistently in industry; the
Atom OS reports define “application service” and “domain service” explicitly.

## Derived work

- [Applications and domain services layer](../20-notes/applications-and-domain-services-layer.md)
- [Bounded contexts, domain model, and application services](../20-notes/applications-and-domain-services-components/bounded-contexts-domain-model-and-application-services.md)
- [Applications and domain services map](../10-maps/applications-and-domain-services.md)
- [2026-09-05 applications deep dive](../50-journal/2026-09-05-applications-and-domain-services-deep-dive.md)
