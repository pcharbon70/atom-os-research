---
title: "TOSCA Version 2.0"
kind: source
created: "2026-09-04"
authors:
  - "Chris Lauwers"
  - "Calin Curescu"
published: "2025-07-22"
citation_key: "oasis-2025-tosca-2"
container: "OASIS Standard"
edition: "TOSCA Version 2.0"
isbn: null
doi: null
url: "https://docs.oasis-open.org/tosca/TOSCA/v2.0/os/TOSCA-v2.0-os.md"
accessed: "2026-09-04"
tags:
  - dependency-graphs
  - lifecycle
  - orchestration
  - service-manifests
  - standards
aliases:
  - "TOSCA 2.0"
---

# TOSCA Version 2.0

## Reference

Chris Lauwers and Calin Curescu, editors. “[TOSCA Version
2.0](https://docs.oasis-open.org/tosca/TOSCA/v2.0/os/TOSCA-v2.0-os.md).”
OASIS Standard, 22 July 2025.

## Research question or contribution

TOSCA defines a typed, model-driven language for service components,
requirements, capabilities, relationships, operations, artifacts, policies,
and lifecycle orchestration. Version 2.0 also describes how old and new
representation graphs can guide creation, modification, deletion, update, and
upgrade.

## Method

The authoritative Markdown OASIS Standard was read for graph validation,
parser/resolver/orchestrator separation, dependency traversal, lifecycle
change, type/version behavior, and stated security limits. This is a broad
interoperability language. Atom OS uses its graph lessons, not its entire YAML
surface or cloud platform assumptions.

## Findings

- A processor parses templates into normalized typed nodes, then a resolver
  constructs a representation graph and fulfills requirements. Circular
  dependencies are errors, and every mandatory nonoptional requirement must be
  satisfied before the representation is accepted.
- Node types distinguish properties, observed attributes, requirements,
  capabilities, interfaces, and operations. Relationships are first-class
  rather than implicit name conventions.
- The orchestrator continuously turns representation state into external
  implementations and reflects observed changes back into the model. The
  processor that validates a model and the executor that performs effects are
  therefore separable roles.
- For change, nodes and relationships are classified as unchanged, modified,
  obsolete, or novel. Obsolete work is traversed in reverse dependency order;
  new or modified work is traversed in dependency order, with eligible nodes
  operated in parallel.
- A profile must define which relationships actually impose dependency and
  which operations implement create, change, or delete. A generic graph does
  not invent safe domain-specific lifecycle semantics.

## Relevance

Atom OS should adopt a deliberately smaller binary or term-encoded manifest
schema with the same separation of parser, resolver, planner, and executor. A
node declares artifact and configuration digests, required and provided
interfaces, delegated capability facets, resource and recovery budgets,
readiness criteria, supervision, update profile, and evidence sinks. The
resolver rejects an incomplete or cyclic graph before any capability is
derived or service started.

Lifecycle edges should remain typed: a service can require another service's
interface without necessarily requiring synchronized start, continuing health,
or reverse-order drain. Old/new graph comparison yields an explicit plan, but
publication still occurs only after Atom OS readiness and authority checks;
irreversible external effects remain outside generic rollback.

## Limits

TOSCA is intentionally domain-independent, and parts of its functional
architecture are non-prescriptive. An implementation need not support every
possible lifecycle phase. The standard does not provide capability security,
crash consistency, bounded execution, truthful readiness, exactly-once effects,
or safe compensation. Its large extensible language would be excessive for an
early trusted service bootstrap. Atom OS should borrow the typed-graph
discipline while keeping a small pinned profile.

## Derived work

- [Service-domain bootstrap and manifest controller](../20-notes/otp-like-system-services-components/service-domain-bootstrap-and-manifest-controller.md)
- [Application lifecycle and dependency orchestration](../20-notes/otp-like-system-services-components/application-lifecycle-and-dependency-orchestration.md)
- [Release, update, rollback, and state migration](../20-notes/otp-like-system-services-components/release-update-rollback-and-state-migration.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
