---
title: "Presentation Sessions, Semantic Views, and User Outcomes"
kind: note
created: "2026-09-05"
maturity: developing
tags:
  - accessibility
  - human-computer-interaction
  - presentation
  - visual-computing
aliases:
  - "Layer 5 presentation contract"
---

# Presentation Sessions, Semantic Views, and User Outcomes

## Executive decision

An application's durable domain model should be independent of every desktop,
window, renderer, toolkit, accessibility bridge, voice session, terminal,
automation client, or remote presentation. Layer 5 publishes **versioned
semantic projections** and accepts typed commands; presentation sessions are
generation-bound and reconstructible. A desktop or view can crash and restart
while the application's domain actors and workflows continue according to
declared policy.

Accessibility is a peer semantic projection, not metadata bolted onto pixels.
Visual, accessible, textual, voice, automation, and remote views may have
different structures while referring to stable logical objects, permitted
actions, revisions, and outcomes. A frame, focus state, animation completion,
or button disappearance is never proof that a domain effect committed.

## Question and operational standard

The component asks: **how can an application remain meaningful and correct when
its presentation is replaceable, plural, stale, or absent?**

It succeeds only if:

- domain state and workflows survive presentation restart;
- a complete semantic snapshot plus revisioned deltas can reconstruct a view;
- gaps, stale generations, or unsupported schemas trigger resynchronization;
- every interactive action returns through a typed domain command with target,
  observed revision, operation ID, and scoped authority;
- input/focus grants are validated by the trusted interaction path, not minted
  by application pixels;
- accessibility exposes the same permitted semantic action and resulting
  domain outcome as other views;
- sensitive fields are redacted before publication;
- view backpressure cannot stall invariant commits indefinitely;
- user-visible pending, committed, rejected, not-committed, terminated, and
  indeterminate states
  match durable domain outcomes; and
- headless and remote operation remain possible without pretending every
  application must progress while no user is present.

## Evidence and limits

[Asynchronous FRP](../../30-sources/czaplicki-chong-2013-asynchronous-frp-guis.md)
demonstrates compositional time-varying views and asynchronous tasks in an
early Elm design. Existing [Smalltalk MVC](../../30-sources/krasner-pope-1988-mvc-smalltalk-80.md)
and [multi-view research](../../30-sources/hosn-et-al-2001-single-application-model-multiple-views.md)
support model/view separation and several coordinated representations.

[WAI-ARIA](../../30-sources/w3c-2023-wai-aria-1-2.md) and [Core AAM](../../30-sources/w3c-2026-core-accessibility-api-mappings-1-2.md)
show that semantic roles, states, properties, relations, and actions can be
mapped into platform accessibility trees whose structure differs from the
render tree. These web standards inform the Atom OS protocol but are not its
complete schema or security model.

The detailed visual architecture remains in the [visual-computing component
research](../visual-computing-synthesis-components/README.md). No UI prototype
or accessibility user study validates this Layer 5 binding yet.

## Semantic publication object

```text
SemanticNode {
  logical_object_ref,
  semantic_type_and_schema,
  role,
  permitted_properties,
  redacted_value_or_summary,
  state,
  relationships[],
  available_actions[],
  ordering_and_grouping_hints,
  revision_or_frontier,
  policy_revision
}
```

The model publishes only what the caller's read capability permits. A
relationship targets another stable logical reference, not a widget pointer.
Localized text and presentation hints are replaceable projections, not domain
identity.

## Session protocol

```text
OpenSemanticView {
  domain_scope,
  projection_kind_and_versions,
  caller_and_tenant_binding,
  read_capability,
  locale_accessibility_and_modality_profile,
  requested_frontier | latest,
  session_generation,
  budget_and_deadline
}
```

The publisher returns `SemanticSnapshot {root_refs, nodes, frontier,
projection_generation, completeness}` followed by ordered or causally tagged
deltas. A delta applies only to its exact base/frontier and session generation.
Coalescing may skip intermediate presentational states but cannot fabricate a
domain revision.

```mermaid
sequenceDiagram
    participant V as View/desktop session
    participant P as Semantic projection
    participant A as Application service/aggregate
    participant O as Durable outcome service

    V->>P: open view with read facet and session generation
    P-->>V: complete snapshot + frontier
    P-->>V: revisioned deltas
    V->>A: typed action + broker client-action ID + observed revision + grant
    A->>O: atomically bind action ID/digest to operation ID and admit
    O-->>A: accepted responsibility + operation ID
    A-->>V: AcceptedPending(operation ID)
    A->>O: commit/query durable semantic outcome
    O-->>A: committed or indeterminate evidence
    A-->>V: terminal outcome + new revision
    Note over V,P: fresh snapshot includes visible unresolved operation IDs; never replay raw input
```

## Action envelope

```text
SemanticAction {
  logical_target,
  action_kind,
  action_schema_version,
  observed_revision_or_frontier,
  projection_and_session_generation,
  input_route_and_policy_generation,
  security_realm_binding_id_and_generation,
  client_action_id,
  operation_id | null,
  deadline,
  user_or_automation_grant,
  parameters
}
```

The application revalidates all fields at the domain/effect boundary. The
presentation cannot infer write authority from read access, focus, visibility,
or a recent raw gesture. Trusted input services may issue a narrow one-shot or
bounded grant; Layer 5 consumes it for the named action.

The input broker assigns a non-reusable `client_action_id` before delivery and
retains it for the advertised reconciliation window. The application-admission
boundary, not the disposable view, atomically binds that ID and request digest
to a durable `operation_id` before delegating effectful work. Repeated admission
with the same pair recovers the binding; a different digest fails closed.
Authorized fresh snapshots expose unresolved operation IDs relevant to the
caller, so a replacement view can reconcile even when the admission reply was
lost. `operation_id` is null only on the initial admission request and is never
invented as the view's sole recovery handle.

## User-visible outcome model

| Domain outcome | Required presentation behavior |
| --- | --- |
| Rejected before admission | keep prior truth; explain stable reason without implying work began |
| Expired before admission | show that no responsibility was accepted; require current intent before retry |
| Accepted pending | show durable pending identity and safe close/reopen behavior |
| Committed | update from authoritative revision/receipt, not optimistic animation alone |
| Not committed | allow retry according to policy with same or new operation identity as specified |
| Terminated/compensated | show surviving visible effects and compensation status honestly |
| Indeterminate | preserve operation identity, prevent blind duplicate action, offer status/repair path |
| Fenced/stale | refresh snapshot/grant and ask user to reconsider changed context |

Optimistic UI is allowed only as explicitly provisional state. It cannot erase
the pending indicator until authoritative outcome evidence arrives.

## Presentation restart

1. Close the old view, surface, focus, capture, and trusted-input generations.
2. Do not replay queued raw input or infer commands from old frames.
3. Start a fresh session and request a complete current semantic snapshot.
4. Reconcile operations from the snapshot's unresolved-operation set or by the
   broker-retained client-action-ID to durable-operation-ID binding.
5. Recreate local selection, navigation, and layout only where their persisted
   state is safe and compatible.
6. Re-establish focus and sensitive ceremonies under current policy.
7. Resume deltas from the new frontier.

Application policy may pause actions that require an interactive user or may
continue background workflows. The architecture makes that choice explicit;
it does not force model death with desktop death.

## Multiple views and consistency

Views are equivalent when they preserve the same permitted logical objects,
actions, and observable domain results—not when their widget/accessibility/
voice trees are identical. Each adapter may flatten, group, virtualize,
localize, summarize, or redact as required.

Cross-view coordination uses logical references and revisions. A selection or
edit initiated in one view becomes a semantic command or ephemeral view-state
event; other views observe the resulting model change, not an imitation of the
originating widget action.

## Privacy, authority, and hostile presentation

- Projection happens after read authorization and field-level redaction.
- Hidden or off-screen content is not implicitly available to a renderer.
- Accessibility adapters receive semantic read/action facets, not arbitrary
  application memory.
- Screen capture, clipboard, drag/drop, automation, and remote presentation are
  distinct grants.
- A hostile view can misrepresent data to its own user; trusted confirmation
  for consequential effects uses a protected path outside that view.
- View-supplied labels, object IDs, and trace context are untrusted inputs.

## Backpressure and responsiveness

Snapshot and delta size, node count, update rate, fan-out, localization work,
renderer work, and session count have budgets. Projections may coalesce
intermediate changes or force snapshot resync. They may not block domain commit
waiting for every view.

Interactive commands carry end-to-end deadlines and admission classes.
Rendering/animation drops before semantic outcome, audit, or reconciliation.
Under overload the application can offer a read-only or simplified semantic
view with explicit freshness rather than a frozen or falsely current UI.

## Alternatives considered

| Alternative | Decision |
| --- | --- |
| UI widget tree is the application model | reject; ties durable meaning to one toolkit/session |
| Restart application whenever desktop crashes | reject as an architectural necessity; allow only explicit app policy |
| Persist raw input and replay after restart | reject; target, context, policy, and user intent may be stale |
| Accessibility is generated from pixels | reject; publish typed semantics and map them to each platform |
| One literal tree for all modalities | reject; preserve logical equivalence, not structural identity |
| Optimistic completion without outcome receipt | reject for consequential effects; display as provisional only |
| Presentation has direct storage/device access | reject; use domain and Layer 4 ports with narrow capabilities |

## Staged implementation and verification

1. Define a small semantic schema with stable object references, roles,
   properties, actions, revision/frontier, and redaction.
2. Build two structurally different views over one model actor.
3. Restart each view and the desktop between every command/outcome transition.
4. Drop, duplicate, reorder, and gap deltas; require snapshot resync.
5. Test visual and accessibility actions for identical permitted domain results.
6. Inject stale focus, session, object revision, policy, and grant generations.
7. Lose a command reply after commit and verify the new view reconciles by
   operation ID rather than repeating raw input.
8. Measure semantic-to-presentation latency and overload degradation separately
   from domain commit latency.

The design is falsified if a presentation restart loses domain truth, if a
frame or focus state is accepted as commit evidence, if hidden fields reach an
unauthorized adapter, or if two permitted views produce contradictory domain
outcomes for the same action.

## Connections

- [Applications and domain services layer](../applications-and-domain-services-layer.md)
- [Visual-computing synthesis components](../visual-computing-synthesis-components/README.md)
- [Semantics-first accessible UI protocol](../visual-computing-synthesis-components/semantics-first-accessible-ui-protocol.md)
- [Durable semantic actors and disposable presentation](../visual-computing-synthesis-components/durable-semantic-actors-and-disposable-presentation.md)
- [Input, focus, and trusted-interaction authority](../visual-computing-synthesis-components/input-focus-and-trusted-interaction-authority.md)

## Sources

- [Asynchronous Functional Reactive Programming for GUIs](../../30-sources/czaplicki-chong-2013-asynchronous-frp-guis.md)
- [Smalltalk-80 MVC](../../30-sources/krasner-pope-1988-mvc-smalltalk-80.md)
- [Single Application Model, Multiple Synchronized Views](../../30-sources/hosn-et-al-2001-single-application-model-multiple-views.md)
- [WAI-ARIA 1.2](../../30-sources/w3c-2023-wai-aria-1-2.md)
- [Core Accessibility API Mappings 1.2](../../30-sources/w3c-2026-core-accessibility-api-mappings-1-2.md)
- [Multi-Target User Interfaces](../../30-sources/calvary-et-al-2003-multi-target-user-interface-framework.md)
- [User-Driven Access Control](../../30-sources/roesner-et-al-2012-user-driven-access-control.md)
