---
title: "Application Manifest, Composition, and Authority Envelope"
kind: note
created: "2026-09-05"
maturity: developing
tags:
  - application-architecture
  - capability-security
  - lifecycle
  - service-manifests
aliases:
  - "Layer 5 application contract"
---

# Application Manifest, Composition, and Authority Envelope

## Executive decision

Every application generation should enter Atom OS through a **declarative,
typed manifest and one explicit composition root**. The manifest says what the
application is, which bounded contexts and protocols it provides, which
facilities it requires, which durable schemas it reads and writes, which
capabilities and budgets it requests, how it participates in lifecycle and
recovery, and what compatibility evidence accompanies it. It contains no
ambient filesystem, registry, network, device, secret, or administrator
authority.

Layer 4 parses, resolves, validates, reserves, and provisions this request. It
derives attenuated live handles and starts the immutable application generation
privately. The Layer 5 composition root receives those imports and connects
them to domain ports. Only Layer 4 can publish the ready generation, fence the
old one, enforce hard budgets, or revoke the resulting handles.

## Question and operational standard

The component asks: **how can an application describe and receive everything it
needs without ambient authority, self-publication, hidden dependencies, or a
second lifecycle manager?**

It succeeds only if:

- every required and provided interface is typed, versioned, and resolved
  before ordinary effects begin;
- a locator or dependency name never doubles as invocation authority;
- requested authority is narrower than the application's total possible API;
- one composition root sees the complete import graph, while ordinary domain
  code sees only per-use-case facets;
- artifact, manifest, schema, configuration, and compatibility digests are
  bound to one immutable generation;
- readiness evidence is externally verifiable and cannot be satisfied by one
  untrusted self-reported Boolean;
- all queues, actors, durable bytes, timers, external sessions, native work,
  and recovery reserve have explicit budgets;
- optional dependencies and degraded behavior are declared rather than
  discovered by exception;
- secrets arrive by short-lived handles and never as durable manifest values;
- prepare, publish, drain, retire, rollback, and quarantine are distinct; and
- Layer 5 declares lifecycle semantics without replacing Layer 4 orchestration.

## Evidence and limits

[TOSCA 2.0](../../30-sources/oasis-2025-tosca-2.md) demonstrates a typed graph
of nodes, requirements, capabilities, relationships, interfaces, and
operations, with parsing/resolution separated from orchestration. It is far
larger than Atom OS needs and does not provide capability security, bounded
execution, truthful readiness, or crash-atomic publication.

[OTP application documentation](../../30-sources/erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md)
supplies a practical precedent for application metadata, dependencies,
callbacks, and start/stop units. Existing OTP names and environment values are
not sufficient as a least-authority application contract. [NixOS](../../30-sources/dolstra-et-al-2008-nixos.md)
supports immutable closure and generation thinking, but mutable data and
activation effects remain outside the store switch.

[Parnas](../../30-sources/parnas-1972-decomposing-systems-into-modules.md)
supports hiding construction and adapter choices. [WASI design
principles](../../30-sources/wasi-project-2026-design-principles.md) support
explicit resource imports. Neither source proves that one manifest schema or
composition tool is secure; the application contract below is an Atom OS
synthesis.

## Manifest object

```text
ApplicationManifest {
  application_id,
  generation,
  artifact_digest,
  signer_and_provenance_requirements,
  beam_otp_compatibility_profile,
  bounded_contexts[],
  provided_protocols[],
  required_protocols[],
  durable_schemas[],
  configuration_schema,
  requested_capability_facets[],
  resource_budgets,
  supervision_declaration,
  protected_domain_profile,
  lifecycle_contract,
  readiness_evidence,
  degradation_policy,
  update_and_migration_matrix,
  observability_contract,
  audit_and_outcome_obligations,
  extension_points[]
}
```

The installed record is content-addressed and immutable. A deployment record
binds that content to site policy, tenant/realm, configuration snapshot,
approved dependencies, budget reservation, and granted imports. This keeps
reproducible application identity separate from one mutable installation.

### Required/provided interface descriptor

```text
PortRequirement {
  port_id,
  semantic_role,
  protocol_family,
  accepted_versions,
  required_outcome_profile,
  locality_constraints,
  tenant_binding,
  confidentiality_and_integrity_class,
  maximum_authority,
  availability_and_degradation_policy
}
```

A provider satisfies a requirement only after graph compatibility, policy,
authority, budget, and generation checks. A registry match is candidate
discovery, not a grant.

## Composition root

The composition root receives the complete **wiring plan**, but not a reusable
union of every imported authority. Layer 4 either injects already attenuated
terminal facets directly into each private child or gives the root sealed,
one-shot installer facets that can transfer each import only to its declared
recipient. It:

1. verifies the manifest/deployment/generation binding presented by Layer 4;
2. validates the recipient and uses each one-shot installer to place a narrow
   domain port facet, without retaining the broader source handle;
3. constructs application services, aggregates, workflows, projections, and
   adapters in dependency order;
4. supplies tenant and context bindings explicitly;
5. refuses unexpected imports and returns unused installers;
6. starts components privately under the declared supervisor topology; and
7. emits readiness evidence describing exact initialized state and generations.

After wiring, Layer 4 revokes the installer generation and the root proves that
no broad source handle remains. It is not a global service locator. Ordinary
actors cannot ask it for arbitrary new capabilities. Runtime resource
acquisition goes through a typed broker request constrained by the admitted
manifest and current policy.

```mermaid
sequenceDiagram
    participant M as Layer 4 manifest controller
    participant B as Resource/identity brokers
    participant C as Layer 5 composition root
    participant A as Application actors
    participant R as Registry/publication service

    M->>M: verify artifact, graph, schemas, compatibility
    M->>B: reserve budgets and derive narrow imports
    B-->>M: recipient-bound terminal or one-shot installer facets
    M->>C: start privately with manifest + sealed wiring plan
    C->>A: construct actors; install each recipient facet once
    A-->>C: component readiness evidence
    C-->>M: readiness + proof installers consumed/returned
    M->>M: revoke installer generation
    M->>R: atomically publish admitted application generation
    R-->>A: public route generation active
```

## Authority envelope

Every import states:

- exact resource or broker facet;
- permitted operations and attenuation;
- application business-tenant reference, Layer 4-authenticated security-realm
  binding, and application generation;
- policy revision and revocation epoch;
- expiry, use count, or lease/fence where meaningful;
- resource account charged for invocation and completion;
- transfer/delegation rule;
- audit and outcome obligations; and
- teardown/reconciliation behavior.

The application may attenuate or delegate an import within policy. It cannot
amplify authority by combining a name with its own identity, resurrect an
expired handle from durable storage, or mint a trusted-path grant. Persistent
records retain authority intent and provenance only; reopening asks Layer 4 to
derive a fresh handle under current policy.

## Configuration and secrets

Configuration is a validated immutable snapshot with schema version,
provenance, tenant binding, generation, and redaction class. Code reads it
through typed accessors rather than arbitrary environment strings. Sensitive
values are references to Layer 4 secret leases, not manifest literals. The
application declares what happens when a lease expires or rotation fails:
reject new work, use an already established session until its limit, or enter a
specific degraded mode.

## Lifecycle participation

| Phase | Layer 5 responsibility | Layer 4 responsibility |
| --- | --- | --- |
| Validate | publish schemas, invariants, dependencies, requested authority, budgets, and compatibility evidence | authenticate artifact; validate graph, policy, and platform compatibility |
| Prepare | construct privately; open state read-only or shadow generation; run self-tests | reserve resources; derive handles; create domains; keep generation undiscoverable |
| Ready | return typed evidence for actual initialized dependencies and state | independently validate evidence and admission conditions |
| Publish | accept traffic only for the published generation | atomically publish registry route and fence prior admission |
| Drain | stop new domain admissions; finish, hand off, or expose accepted outcomes | close routes, enforce deadline, preserve outcome/recovery services |
| Retire | release imports after effects and leases reconcile | revoke, quiesce, reap, or quarantine resources |
| Rollback/repair | apply declared semantic rollback or roll-forward plan | orchestrate generation switch and retain evidence |

An application cannot declare itself “ready” merely because its root actor is
alive. Evidence may include recovered state frontier, required-provider
generations, compatibility checks, migration checkpoint, and ability to commit
one synthetic no-effect transaction within budget.

## Dependency and degradation semantics

Edges distinguish build-time, prepare-time, continuing, optional, and
effect-only dependencies. Each continuing dependency declares:

- whether existing work may finish during outage;
- whether new work is rejected, queued within a bound, or served read-only;
- staleness and cache rules;
- reconnection and route-generation validation;
- whether failure escalates the whole application or one bounded context; and
- which semantic SLI exposes degradation.

A dependency cycle is rejected unless a deliberately modeled bootstrap
protocol breaks it. Hidden runtime discovery that creates an undeclared cycle
is a conformance failure.

## Overload and failure behavior

The manifest names queue capacities, command classes, deadlines, concurrency,
heap/mailbox ceilings, persistent growth, adapter sessions, timers, extension
budgets, and recovery reserve. Layer 5 chooses which semantic work can shed or
degrade; Layer 4 enforces the ceilings.

On composition-root crash before publication, Layer 4 revokes the installer
generation and discards private state or resumes only from a declared
preparation checkpoint. After publication, the root is not a permanent
authority concentration: child actors retain only their narrow imports, all
one-shot installers and broad derivation handles are gone, and an independent
supervisor can replace the root. Any handle whose safe ownership is unclear is
revoked or quarantined.

## Alternatives considered

| Alternative | Strength | Decision |
| --- | --- | --- |
| Ambient global registry and configuration | convenient dynamic lookup | rejected: hides dependency and turns names into deputy-controlled authority |
| DI container accessible everywhere | flexible late binding | rejected as a service locator; keep one bounded composition root |
| OTP `.app` metadata unchanged | proven, simple compatibility | retain through an adapter profile, but require stronger typed authority, budget, readiness, and migration contracts |
| TOSCA-compatible full language | rich topology vocabulary | reject for trusted core; borrow graph discipline in a small pinned schema |
| Application publishes itself | simple startup | rejected: readiness, authority, and atomic generation publication require independent Layer 4 control |
| Secrets embedded in bundle or environment | easy deployment | rejected: durable leakage and weak rotation/revocation semantics |

## Staged implementation and verification

1. Define a canonical encoded manifest with unknown-critical-field rejection
   and content digest.
2. Build parser and pure graph resolver separately from the effectful planner.
3. Implement one composition root receiving a synthetic capability bundle and
   prove ordinary actors cannot reach the global broker.
4. Add private preparation, independent readiness verification, atomic route
   publication, drain, and retirement.
5. Generate invalid graphs, capability escalations, budget overflows, stale
   generations, dependency cycles, and mismatched schemas property-wise.
6. Crash before and after every reservation, handle derivation, actor start,
   readiness record, publication, admission closure, and teardown transition.
7. Compare the declared dependency/recovery graph with observed message and
   authority edges; any hidden edge fails conformance.

The design is falsified if a child can acquire undeclared ambient authority,
if a name alone authorizes a resource, if readiness is self-certified without
external evidence, if an application can publish itself, or if retirement
depends on the failed application releasing its own authority correctly.

## Connections

- [Applications and domain services layer](../applications-and-domain-services-layer.md) —
  integrates this contract with the other Layer 5 components.
- [Service-domain bootstrap and manifest controller](../otp-like-system-services-components/service-domain-bootstrap-and-manifest-controller.md) —
  implements the Layer 4 validation, reservation, preparation, and publication
  side of this boundary.
- [Application lifecycle and dependency orchestration](../otp-like-system-services-components/application-lifecycle-and-dependency-orchestration.md) —
  owns system-level orchestration.
- [Authentication and authorization architecture](../authentication-and-authorization-across-the-five-layer-architecture.md) —
  supplies policy, identity, grants, and revocation.

## Sources

- [TOSCA 2.0](../../30-sources/oasis-2025-tosca-2.md)
- [OTP system-services documentation](../../30-sources/erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md)
- [NixOS](../../30-sources/dolstra-et-al-2008-nixos.md)
- [On the Criteria To Be Used in Decomposing Systems into Modules](../../30-sources/parnas-1972-decomposing-systems-into-modules.md)
- [WASI Design Principles](../../30-sources/wasi-project-2026-design-principles.md)
- [Capability Myths Demolished](../../30-sources/miller-et-al-2003-capability-myths.md)
- [The Confused Deputy](../../30-sources/hardy-1988-confused-deputy.md)
