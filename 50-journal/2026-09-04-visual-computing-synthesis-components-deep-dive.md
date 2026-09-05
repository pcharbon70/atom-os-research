---
title: "2026-09-04 visual-computing synthesis components deep dive"
kind: journal
created: "2026-09-04"
tags:
  - accessibility
  - capability-security
  - human-computer-interaction
  - literature-review
  - research-method
  - visual-computing
aliases:
  - "Atom OS visual-computing component research session"
---

# 2026-09-04 visual-computing synthesis components deep dive

## Observations

This session expanded the seven directions in the [Atom OS visual-interface
synthesis](../20-notes/alan-kay-smalltalk-visual-interface-and-modern-desktop.md)
into detailed reports under the [visual-computing synthesis components
directory](../20-notes/visual-computing-synthesis-components/README.md).

The shared result is an unprivileged visual-computing service stratum, not a
new privileged desktop layer. It uses the existing hardware and architecture,
minimal privileged kernel, managed actor runtime, and OTP-like system-services
contracts, then adds user-owned projects, semantic projections, rendering,
trusted interaction, accessibility, multimodal adapters, and live authoring.

The strongest cross-component distinctions are:

- durable project and semantic identity is distinct from actor PIDs, kernel
  capability selectors, surface IDs, platform accessibility handles, and
  localized labels;
- the project store persists typed meaning, history, provider requirements,
  and authority intent, while current policy derives fresh live capabilities;
- one authoritative semantic graph can support structurally different,
  access-controlled projections, so consistency is defined by logical objects,
  typed actions, and observable model effects rather than identical trees;
- model and durable-effect truth is separated from semantic-view, renderer,
  compositor, focus, capture, and other reconstructible or ephemeral state;
- trusted input can mint a narrow generation-bound grant, but a raw event never
  implies ambient access and is never replayed after presentation restart;
- inspection, pure evaluation, tracing, staging, commit, secret access, and
  publication are separate powers; and
- replica convergence, causality, user intent, authorization, domain
  invariants, and external-effect safety are separate properties.

These are evidence-backed architectural proposals. No Atom OS visual service,
project store, semantic protocol, trusted-input broker, compositor, live-tool
service, accessibility adapter, or collaborative projection was implemented or
tested during this session.

## Environment

- Repository: `/home/ducky/code/atom-os-research`
- Research date: 2026-09-04
- Host time zone: America/Toronto
- Activity: peer-reviewed-paper, standards, official-documentation, article,
  and engineering-literature review; cross-source architecture synthesis;
  archive editing
- Architecture scope: the existing four mechanism/policy layers plus an
  unprivileged visual-computing and domain-application stratum
- Hardware, simulator, toolkit, compositor, or assistive-technology target:
  none selected
- Code, device, performance, accessibility, security, or user-study experiment:
  none performed
- Local artifacts: seven component reports, twenty-three new source notes, one
  component directory index, navigation and inquiry updates, and this evidence
  record

## Evidence

### Research question and operational standard

For every proposed aspect, the research asked:

> What implementable object, protocol, authority, failure, persistence, and
> recovery contract would preserve the desired visual-computing property while
> respecting Atom OS actor isolation and the current layer boundaries?

A recommendation was retained only when its report:

- states the exact responsibility and what remains outside the component;
- distinguishes historical precedent, demonstrated source behavior, current
  platform behavior, and Atom-specific proposal;
- names identities, generations, capabilities, durable outcomes, state
  transitions, and resynchronization rules precisely enough to test;
- separates semantic authority from its visual, assistive, voice, textual,
  programmatic, automation, and remote projections;
- identifies the enforcing layer and prevents a higher service from claiming a
  lower-layer guarantee it cannot supply;
- gives bounded behavior under crash, restart, stale messages, lost replies,
  revocation, overload, malformed input, and incompatible versions;
- compares alternatives and preserves negative evidence and scope limits;
- defines staged implementation work and experiments that could falsify the
  recommendation; and
- remains `maturity: developing` because no Atom implementation was evaluated.

### Search and selection method

The parent synthesis supplied the seven-part decomposition. Three independent
evidence lanes examined project ownership and durability; semantic,
accessibility, multimodal, and collaborative views; and trusted input, live
tools, transactional change, and recovery. Searches covered HCI, programming
languages, hypermedia, accessibility standards, secure UI, capability systems,
distributed data, crash recovery, dynamic updating, tracing, and current
desktop protocols.

Search snippets and secondary summaries were used only for discovery. Detailed
claims were checked against primary papers, normative standards, official
project documentation, or first-party engineering material. Current living
documents were pinned by revision or access date. Blogs and practitioner
articles were retained where they described a distinctive implemented system
or design experience and their evidential limits were explicit.

### Component reports

1. [User-owned project graph and composition](../20-notes/visual-computing-synthesis-components/user-owned-project-graph-and-composition.md)
2. [Durable semantic actors and disposable presentation](../20-notes/visual-computing-synthesis-components/durable-semantic-actors-and-disposable-presentation.md)
3. [Semantics-first accessible UI protocol](../20-notes/visual-computing-synthesis-components/semantics-first-accessible-ui-protocol.md)
4. [Input, focus, and trusted-interaction authority](../20-notes/visual-computing-synthesis-components/input-focus-and-trusted-interaction-authority.md)
5. [Capability-scoped live tools and transactional evolution](../20-notes/visual-computing-synthesis-components/capability-scoped-live-tools-and-transactional-evolution.md)
6. [Cross-layer placement and recovery topology](../20-notes/visual-computing-synthesis-components/cross-layer-placement-and-recovery-topology.md)
7. [Plural representations and cross-view consistency](../20-notes/visual-computing-synthesis-components/plural-representations-and-cross-view-consistency.md)

### Strongest cross-component conclusions

1. **The project, not the package or window, is the durable unit.** Packages
   supply providers; they do not monopolize interpretation or ownership of the
   user's typed objects and history.
2. **Persistence does not preserve live authority.** Durable records can name
   a policy decision and delegation lineage, but reopening rechecks identity,
   policy, revocation, schema, and generation before deriving a new grant.
3. **Actor execution identity is not semantic identity.** A durable object can
   be served by successive actor activations; a restarted activation cannot
   inherit stale messages or authority merely by using the same logical name.
4. **One source of meaning is not one literal tree.** Platform adapters may
   merge, flatten, reorder, virtualize, redact, or localize. Equivalence is
   judged through stable logical references, permitted actions, and resulting
   model observations.
5. **Presentation recovery starts from current truth.** It requests a complete
   semantic snapshot, establishes fresh view/surface/focus generations, and
   discards old input. Unknown domain effects reconcile by operation ID rather
   than being inferred from frames or retried blindly.
6. **Input is a narrowly scoped authority source.** The trusted broker binds
   physical or assistive action to a target, operation, resource facet,
   generations, expiry, and use count. Focus or “recent gesture” alone is not a
   general capability.
7. **Live programming crosses explicit fences.** Inspection returns redacted
   semantic projections or immutable snapshots. Evaluation runs with declared
   imports and budgets. Publication is a typed, staged changeset with durable
   outcome and migration/compensation policy.
8. **Visual services consume existing lower contracts.** Hardware provides
   display/input mechanisms; the kernel provides isolation and capabilities;
   the runtime provides actors and messages; OTP-like services provide
   persistence, lifecycle, update, overload, telemetry, and audit policy.
9. **Collaboration has several independent correctness axes.** A converged
   replica may still violate intent, authorization, invariants, or effect
   safety. Each data type and command therefore declares its own policy.
10. **Recovery requires reserved paths, not only supervisors.** The minimum
    trusted display, input, revocation, project selection, and evidence path
    needs bounded resources independent of ordinary renderers and projects.

### Evidence gaps and falsifiers

The central gaps are executable protocol models; a first semantic schema and
compatibility profile; a project persistence and migration format; a measured
view-update and rendering budget; platform accessibility-adapter behavior;
secure-attention and input hardware assumptions; GPU and media-parser
containment; collaboration and revocation during offline operation; live-code
data/effect rollback; and comparative user evidence for action–image–symbol
authorship.

The synthesis is falsified by an implementation that:

- makes an application package the only interpreter of durable user data;
- serializes actor PIDs, kernel capabilities, focus tokens, or surface leases
  as reusable project authority;
- requires the model to restart or roll back whenever presentation restarts;
- accepts a semantic delta, action, frame, or input grant for a stale base or
  generation;
- treats accessibility metadata as permission or publishes private model
  state merely because it has an accessible representation;
- replays an unacknowledged gesture or reports an unknown external effect as
  safely failed;
- gives an inspector, evaluator, tracer, editor, or publisher a generic debug
  capability rather than the minimum operation facet;
- calls a code rollback a data rollback or claims to undo an already observed
  external effect without a compensating protocol;
- requires a new privileged kernel API for every new widget, media type, or
  project object; or
- calls replicas correct solely because their bytes converge.

### Evidence boundary

No cited experiment or user study was reproduced. Formal results apply only to
their stated models, and no external proof, security property, accessibility
conformance result, or production-recovery result transfers to Atom OS. The
reports specify hypotheses and evaluation programs rather than implementation
facts.

## Source manifest

### Newly introduced sources

- [An Approach to Persistent Programming](../30-sources/atkinson-et-al-1983-persistent-programming.md) — rooted, typed, execution-independent persistence and its authority and retention limits.
- [A Theory of Changes for Higher-Order Languages](../30-sources/cai-et-al-2014-theory-of-changes.md) — formal incremental-change correctness relative to an exact base state.
- [A Unifying Reference Framework for Multi-Target User Interfaces](../30-sources/calvary-et-al-2003-multi-target-user-interface-framework.md) — task, abstract, concrete, and final presentation layers for multi-target interfaces.
- [Access Control for Collaborative Editors](../30-sources/cherif-et-al-2014-access-control-collaborative-editors.md) — evidence that convergence and access policy must be composed explicitly.
- [Functional Reactive Animation](../30-sources/elliott-hudak-1997-functional-reactive-animation.md) — compositional behavior/event model for deriving presentation without imperative repaint identity.
- [Combinators for Bi-Directional Tree Transformations](../30-sources/foster-et-al-2007-bidirectional-tree-transformations.md) — round-trip laws and explicit limits for editable projections.
- [Automatically Generating Personalized User Interfaces with SUPPLE](../30-sources/gajos-et-al-2010-personalized-user-interfaces-supple.md) — evaluated model-driven adaptation plus scope and authoring-cost limits.
- [The Dexter Hypertext Reference Model](../30-sources/halasz-schwartz-1994-dexter-hypertext-reference-model.md) — separation of durable components and links from transient run-time presentation.
- [Single Application Model, Multiple Synchronized Views](../30-sources/hosn-et-al-2001-single-application-model-multiple-views.md) — common model driving coordinated visual and speech views.
- [Clickjacking: Attacks and Defenses](../30-sources/huang-et-al-2012-clickjacking-attacks-and-defenses.md) — empirical and architectural limits of untrusted visual context around consequential input.
- [A Conflict-Free Replicated JSON Datatype](../30-sources/kleppmann-beresford-2017-conflict-free-json.md) — structured replicated state and explicit datatype/concurrency boundaries.
- [Local-First Software](../30-sources/kleppmann-et-al-2019-local-first-software.md) — user ownership, offline availability, collaboration, and unresolved access/history problems.
- [Webstrates: Shareable Dynamic Media](../30-sources/klokmose-et-al-2015-webstrates-shareable-dynamic-media.md) — implemented shareable substrate with several editors, computation, and synchronized content.
- [Potluck: Dynamic Documents as Personal Software](../30-sources/litt-et-al-2022-potluck-dynamic-documents.md) — gradual enrichment of user-owned documents and representation-complexity limits.
- [Ten Myths of Multimodal Interaction](../30-sources/oviatt-1999-ten-myths-multimodal-interaction.md) — empirical synthesis showing complementary, sequential, task-dependent modalities.
- [Living in a Programming Environment](../30-sources/rein-et-al-2017-living-in-programming-environment.md) — qualitative evidence about continuous tool use and liveness in a mature environment.
- [Exploratory and Live, Programming and Coding](../30-sources/rein-et-al-2019-liveness-literature-study.md) — systematic liveness dimensions and terminology boundaries.
- [User-Driven Access Control](../30-sources/roesner-et-al-2012-user-driven-access-control.md) — precedent for binding authority to authentic user interaction rather than ambient application identity.
- [Conflict-Free Replicated Data Types](../30-sources/shapiro-et-al-2011-conflict-free-replicated-data-types.md) — formal convergence conditions and their limited semantic scope.
- [Mutatis Mutandis](../30-sources/stoyle-et-al-2005-safe-predictable-dynamic-updating.md) — type-directed dynamic update and the need for controlled state transformation.
- [Achieving Convergence, Causality Preservation, and Intention Preservation](../30-sources/sun-et-al-1998-cooperative-editing-consistency.md) — separates three collaborative-editing correctness properties.
- [Accessible Rich Internet Applications 1.2](../30-sources/w3c-2023-wai-aria-1-2.md) — normative role, state, relationship, action, focus, and accessibility-tree semantics.
- [Core Accessibility API Mappings 1.2](../30-sources/w3c-2026-core-accessibility-api-mappings-1-2.md) — current mapping evidence that one semantic authority need not produce identical platform trees.

### Reused sources

- [Android Protected Confirmation](../30-sources/android-project-2026-protected-confirmation.md) — protected rendering/input ceremony and message-bound one-shot confirmation.
- [Apple desktop UI framework and design documentation](../30-sources/apple-2026-desktop-ui-frameworks.md) — current application, view, state, sandbox, and accessibility boundaries.
- [Orleans](../30-sources/bernstein-et-al-2014-orleans.md) — stable logical actor identity over replaceable activations.
- [Implementing Remote Procedure Calls](../30-sources/birrell-nelson-1984-remote-procedure-calls.md) — delivery ambiguity and operation-identity limits across failure.
- [Microreboot](../30-sources/candea-et-al-2004-microreboot.md) — fine-grained restart dependent on explicit state placement and retry discipline.
- [Crash-Only Software](../30-sources/candea-fox-2003-crash-only-software.md) — ordinary restart lifecycle and the need for bounded recovery paths.
- [Dynamic Instrumentation of Production Systems](../30-sources/cantrill-et-al-2004-dtrace.md) — typed probes, verifier-bounded tracing, aggregation, and per-consumer state.
- [FSCQ](../30-sources/chen-et-al-2015-fscq.md) — crash-consistency specification and proof precedent for persistent recovery claims.
- [NixOS](../30-sources/dolstra-et-al-2008-nixos.md) — immutable deployment generations and rollback precedent.
- [From L3 to seL4](../30-sources/elphinstone-heiser-2013-l4-lessons.md) — minimal mechanism and user-space policy placement.
- [A Conversation with Alan Kay](../30-sources/feldman-kay-2004-conversation-alan-kay.md) — later metamedium critique and explicit meta-level boundary.
- [Nitpicker](../30-sources/feske-helmuth-2005-nitpicker.md) — small secure GUI, input routing, labelling, and quota precedent.
- [Sagas](../30-sources/garcia-molina-salem-1987-sagas.md) — compensation and partial-progress semantics for long-running effects.
- [Smalltalk-80: The Interactive Programming Environment](../30-sources/goldberg-1984-smalltalk-80-interactive-environment.md) — integrated project, browser, inspector, debugger, source, and change-history precedent.
- [The Confused Deputy](../30-sources/hardy-1988-confused-deputy.md) — why ambient authority and authority-bearing names are unsafe.
- [seL4 design principles for a high-assurance system](../30-sources/heiser-2020-sel4-design-principles.md) — small privileged mechanism and explicit assurance-boundary guidance.
- [Direct Manipulation Interfaces](../30-sources/hutchins-et-al-1985-direct-manipulation-interfaces.md) — semantic/articulatory distance and the abstraction limits of direct action.
- [Personal Dynamic Media](../30-sources/kay-goldberg-1977-personal-dynamic-media.md) — dynamic documents, personal ownership, simulation, and user-created tools.
- [RIFL](../30-sources/lee-et-al-2015-rifl.md) — durable result tracking and retry reconciliation precedent.
- [Windows desktop UI architecture documentation](../30-sources/microsoft-2026-desktop-ui-architecture.md) — current composition, toolkit, GPU, lifecycle, isolation, and automation boundaries.
- [Capability Myths Demolished](../30-sources/miller-et-al-2003-capability-myths.md) — authority as reachable references and delegation rather than names alone.
- [ARIES](../30-sources/mohan-et-al-1992-aries.md) — logged transactional recovery and precise committed-outcome reasoning.
- [Practical Dynamic Software Updating for C](../30-sources/neamtiu-et-al-2006-practical-dynamic-software-updating.md) — implemented update points and state transformation with explicit limits.
- [Live Objects All The Way Down](../30-sources/pimas-et-al-2023-live-objects-all-the-way-down.md) — reflective liveness case studies and metacircular-system trade-offs.
- [The Protection of Information in Computer Systems](../30-sources/saltzer-schroeder-1975-protection-information.md) — economy, least privilege, complete mediation, and usable-protection principles.
- [End-to-End Arguments in System Design](../30-sources/saltzer-et-al-1984-end-to-end-arguments.md) — placement of correctness checks at the endpoint that can state the requirement.
- [The Update Framework](../30-sources/samuel-et-al-2010-tuf.md) — role-separated update trust and rollback/freeze resistance.
- [EROS](../30-sources/shapiro-et-al-1999-eros.md) — durable capability-oriented object-system precedent and its scope limits.
- [in-toto](../30-sources/torres-arias-et-al-2019-in-toto.md) — attributable software-supply-chain steps and artifact provenance.
- [Web Content Accessibility Guidelines 2.2](../30-sources/w3c-2024-wcag-2-2.md) — current testable accessibility baseline and semantic interaction requirements.
- [Wayland architecture and protocol](../30-sources/wayland-project-2026-architecture-and-protocol.md) — client buffer, surface, compositor, seat, and input-routing boundary.
- [User interaction design for secure systems](../30-sources/yee-2002-user-interaction-design-secure-systems.md) — trusted-path, authentic-party, and explicit-authorization interaction principles.

## Threads

- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [What visual-computing model should Atom OS adopt?](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
- [BEAM, ERTS, and OTP principles for a new operating system](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md)
- [Authentication and authorization across the five-layer architecture](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)

## Follow-ups

- Define a versioned semantic protocol profile and executable state models for
  snapshots, deltas, actions, generations, resynchronization, and redaction.
- Build a local project store and two independent providers for one object type;
  remove the original provider and prove continued semantic access and export.
- Implement presentation restart with stale-frame, stale-focus, input-replay,
  and ambiguous-effect fault injection at every protocol transition.
- Prototype a protected input broker and secure prompt path with assistive input
  included in the trusted ceremony.
- Specify a live changeset format and distinguish code rollback, data migration,
  external-effect compensation, and indeterminate outcomes in tests.
- Evaluate visual, textual, screen-reader, voice, and remote projections for
  observational equivalence, real usability, privacy, latency, and overload.
