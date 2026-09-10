---
title: "2026-09-10 visual-computing internal services deep dive"
kind: journal
created: "2026-09-10"
tags:
  - accessibility
  - capability-security
  - human-computer-interaction
  - literature-review
  - research-method
  - visual-computing
aliases:
  - "Atom OS visual-computing internal-service research session"
---

# 2026-09-10 visual-computing internal services deep dive

## Observations

This session decomposed all seven reports in the [visual-computing synthesis
component directory](../20-notes/visual-computing-synthesis-components/README.md)
into 34 internal-service studies. The count follows distinct state, authority,
failure, and completion boundaries rather than a uniform quota.

The result retains durable meaning in user-owned project and model records;
treats semantic projections as reconstructible; makes rendering resources
disposable leases; derives narrow authority from trusted interaction; splits
live tooling into observation, evaluation, control, commit, and publication
powers; and judges plural representations by task outcomes rather than
identical pixels or tree shapes.

The decomposition makes five boundaries explicit:

- project manifests are not process snapshots and do not persist bearer authority;
- semantic publication, platform accessibility adaptation, and hardware input
  focus are separate state machines;
- clipboard, drag/drop, capture, and remote control are explicit sessions;
- migration validation does not prove domain invariants or reverse external
  effects; and
- visual recovery depends on externally held revocation and resource reserve.

No Atom OS project format, semantic protocol, compositor, input broker,
accessibility adapter, live tool, multimodal manager, or visual recovery path
was implemented or tested.

## Environment

- Repository: /home/ducky/code/atom-os-research
- Research date: 2026-09-10
- Host time zone: America/Toronto
- Activity: scientific-paper, standards, official-documentation, project-
  architecture, and first-party engineering-article review
- Scope: full visual-computing architecture, explicitly excluding PoC and QEMU
- Selected toolkit, display server, GPU API, or accessibility backend: none
- Local experiment, benchmark, model check, security test, accessibility test,
  or participant study: none
- Artifacts: seven directory indexes, 34 studies, five new source notes,
  connected navigation, and this evidence record

## Evidence

### Research question and operational standard

For each parent component, the research asked which independently owned state,
authority, transition, failure, and completion responsibilities must exist for
the contract to be implementable and falsifiable.

A responsibility became a separate study when its authoritative state,
privilege or disclosure boundary, restart lifecycle, terminal outcome,
overload policy, compatibility profile, or qualification method differed.
Every study identifies owned state, source limits, transitions, adversarial
behavior, alternatives, and unexecuted falsifiers. All remain developing
because no Atom implementation was evaluated.

### Search and selection method

The 2026-09-04 sessions supplied the historical, HCI, capability, persistence,
accessibility, collaboration, dynamic-update, and desktop-protocol foundation.
This session re-read those notes and searched scientific literature, official
project documentation, and first-party engineering articles for missing
internal boundaries.

Searches covered cross-process accessibility trees and updates; secure GUI
composition and clipboard transfer; sandbox-mediated remote input, capture,
and clipboard; renderer/GPU/accessibility recovery; and fault-tolerant live
state migration. Snippets were discovery aids only. Retained claims were
checked against primary papers or first-party architecture documentation.

### Decomposition by component

1. [User-owned project graph](../20-notes/visual-computing-synthesis-components/user-owned-project-graph-and-composition/README.md) — manifest/history, provider binding, authority rehydration, collaboration, and portability.
2. [Durable semantic actors](../20-notes/visual-computing-synthesis-components/durable-semantic-actors-and-disposable-presentation/README.md) — model activation, semantic publication, rendering leases, and reconstruction.
3. [Semantics-first accessible UI](../20-notes/visual-computing-synthesis-components/semantics-first-accessible-ui-protocol/README.md) — vocabulary, ordered updates, actions, adapters, and consumer continuity.
4. [Trusted interaction](../20-notes/visual-computing-synthesis-components/input-focus-and-trusted-interaction-authority/README.md) — event provenance, focus/capture, transfer, secure attention, and remote sessions.
5. [Capability-scoped live tools](../20-notes/visual-computing-synthesis-components/capability-scoped-live-tools-and-transactional-evolution/README.md) — inspection, evaluation, debugging, changesets, and release.
6. [Recovery topology](../20-notes/visual-computing-synthesis-components/cross-layer-placement-and-recovery-topology/README.md) — placement, fencing, headless recovery, restart groups, and reserves.
7. [Plural representations](../20-notes/visual-computing-synthesis-components/plural-representations-and-cross-view-consistency/README.md) — provider contracts, equivalence, bidirectional edits, multimodality, and collaboration.

### Strongest cross-component conclusions

1. Durable, activation, and presentation identities need separate lifecycles.
2. Every cached tree needs snapshot-plus-cursor continuity and explicit resync.
3. Accessibility semantics originate before rendering and adapters are lossy.
4. Discoverable actions do not grant authority or establish durable outcomes.
5. Focus does not imply clipboard, capture, remote-control, or confirmation rights.
6. Cross-domain transfer has separate offer, conversion, receipt, and effect outcomes.
7. Inspection, evaluation, tracing, debugging, commit, and publication are distinct powers.
8. Code rollback, data restore, compensation, and forward repair are distinct.
9. Cross-view conformance compares essential tasks and model outcomes, not pixels.
10. Recovery requires authority and resources outside the failed component.

### Evidence gaps and falsifiers

The largest gaps are a versioned project/export format; executable generation
models; a canonical semantic snapshot/delta/action profile; real
AT-SPI/UIA/screen-reader results; a hardware secure-attention profile; bounded
data converters; a changeset implementation; representative workloads; and
participant evidence for accessibility, comprehension, authorship, and transfer.

The architecture is falsified by persisted live capabilities or presentation
handles; package-owned opaque data; silent semantic continuity loss; roles
treated as permission; focus treated as transfer or control authority; rich
untrusted parsing in broadly trusted services; blind retry after unknown
effects; tool-facet amplification; convergence presented as intent
preservation; or loss of revocation and recovery under project exhaustion.

### Evidence boundary

Formal results retain their authors' models. Project documentation establishes
intended or implemented architecture, not independent security. First-party
engineering articles provide constraints and experience, not universal
behavior. Existing browser, Wayland, Qubes, Android, and capability-system
mechanisms are precedents rather than selected Atom OS dependencies. No
compatibility, performance, security, accessibility, usability, or recovery
result has transferred to Atom OS.

## Source manifest

### Newly introduced sources

- [AccessKit architecture and engineering notes](../30-sources/accesskit-project-2026-architecture-and-engineering.md) — semantic nodes, atomic updates, adapter boundaries, subtrees, and memory trade-offs.
- [Chromium multi-process graphics and accessibility](../30-sources/chromium-project-2026-multiprocess-graphics-and-accessibility.md) — renderer, GPU, input, accessibility cache, fallback, and crash-replacement precedent.
- [Fault-tolerant live update](../30-sources/giuffrida-et-al-2013-fault-tolerant-live-update.md) — isolated versions, migration validation, and recovery from transfer faults.
- [Qubes OS GUI virtualization](../30-sources/qubes-project-2026-gui-virtualization.md) — isolated composition, input routing, origin markers, and explicit clipboard transfer.
- [XDG Desktop Portal interaction sessions](../30-sources/xdg-desktop-portal-project-2026-interaction-sessions.md) — user-mediated remote input, capture, clipboard, restore, and revocation.

### Reused sources

- [An approach to persistent programming](../30-sources/atkinson-et-al-1983-persistent-programming.md) — typed durable roots.
- [Android Protected Confirmation](../30-sources/android-project-2026-protected-confirmation.md) — operation-bound protected input and display.
- [Orleans](../30-sources/bernstein-et-al-2014-orleans.md) — logical identity over replaceable activations.
- [Implementing remote procedure calls](../30-sources/birrell-nelson-1984-remote-procedure-calls.md) — delivery and reply ambiguity.
- [A theory of changes](../30-sources/cai-et-al-2014-theory-of-changes.md) — incremental change relative to an exact base.
- [CAMELEON framework](../30-sources/calvary-et-al-2003-multi-target-user-interface-framework.md) — task, abstract, concrete, and final presentation.
- [Crash-only software](../30-sources/candea-fox-2003-crash-only-software.md) — bounded restart lifecycle.
- [Microreboot](../30-sources/candea-et-al-2004-microreboot.md) — fine-grained recovery and state placement.
- [DTrace](../30-sources/cantrill-et-al-2004-dtrace.md) — typed probes, verification, and aggregation.
- [FSCQ](../30-sources/chen-et-al-2015-fscq.md) — precise crash-consistency specification.
- [Access control for collaborative editors](../30-sources/cherif-et-al-2014-access-control-collaborative-editors.md) — authorization separate from convergence.
- [Hexagonal architecture](../30-sources/cockburn-2005-hexagonal-architecture.md) — semantic ports and replaceable adapters.
- [Asynchronous FRP for GUIs](../30-sources/czaplicki-chong-2013-asynchronous-frp-guis.md) — asynchronous presentation.
- [NixOS](../30-sources/dolstra-et-al-2008-nixos.md) — immutable closures and activation generations.
- [L4 lessons](../30-sources/elphinstone-heiser-2013-l4-lessons.md) — privileged mechanism and user-space policy.
- [Functional reactive animation](../30-sources/elliott-hudak-1997-functional-reactive-animation.md) — declarative presentation.
- [Nitpicker](../30-sources/feske-helmuth-2005-nitpicker.md) — minimal trusted compositor/input boundary.
- [Bidirectional tree transformations](../30-sources/foster-et-al-2007-bidirectional-tree-transformations.md) — round-trip laws and complements.
- [SUPPLE](../30-sources/gajos-et-al-2010-personalized-user-interfaces-supple.md) — evaluated model-driven adaptation.
- [Sagas](../30-sources/garcia-molina-salem-1987-sagas.md) — compensation distinct from rollback.
- [Smalltalk-80 interactive environment](../30-sources/goldberg-1984-smalltalk-80-interactive-environment.md) — integrated browsers, inspectors, and history.
- [Dexter hypertext reference model](../30-sources/halasz-schwartz-1994-dexter-hypertext-reference-model.md) — durable structures separate from presentation.
- [seL4 design principles](../30-sources/heiser-2020-sel4-design-principles.md) — minimal privilege and assurance boundaries.
- [Single application model, multiple views](../30-sources/hosn-et-al-2001-single-application-model-multiple-views.md) — synchronized visual and speech views.
- [Direct manipulation interfaces](../30-sources/hutchins-et-al-1985-direct-manipulation-interfaces.md) — semantic distance and directness limits.
- [Personal dynamic media](../30-sources/kay-goldberg-1977-personal-dynamic-media.md) — user-owned media and authorship.
- [Conflict-free replicated JSON](../30-sources/kleppmann-beresford-2017-conflict-free-json.md) — structured convergent data.
- [Local-first software](../30-sources/kleppmann-et-al-2019-local-first-software.md) — offline ownership and access/history gaps.
- [Webstrates](../30-sources/klokmose-et-al-2015-webstrates-shareable-dynamic-media.md) — shared durable content with multiple tools.
- [Recovery domains](../30-sources/lenharth-et-al-2009-recovery-domains.md) — explicit failure and recovery scope.
- [RIFL](../30-sources/lee-et-al-2015-rifl.md) — durable request identity and result lookup.
- [Project Cambria](../30-sources/litt-et-al-2020-cambria.md) — schema lenses and translation limits.
- [Potluck](../30-sources/litt-et-al-2022-potluck-dynamic-documents.md) — personal-software enrichment and complexity.
- [Scheduling-context capabilities](../30-sources/lyons-et-al-2018-scheduling-context-capabilities.md) — temporal accounting and delegation.
- [Capability myths demolished](../30-sources/miller-et-al-2003-capability-myths.md) — authority as reachable references.
- [ARIES](../30-sources/mohan-et-al-1992-aries.md) — durable recovery and committed outcomes.
- [Practical dynamic software updating](../30-sources/neamtiu-et-al-2006-practical-dynamic-software-updating.md) — update points and state transformation.
- [Ten myths of multimodal interaction](../30-sources/oviatt-1999-ten-myths-multimodal-interaction.md) — complementary context-dependent modalities.
- [Capability-based OS design](../30-sources/parmer-2016-capability-based-os-design.md) — capability authority boundaries.
- [Living in a programming environment](../30-sources/rein-et-al-2017-living-in-programming-environment.md) — continuous tools and remote-object limits.
- [Liveness literature study](../30-sources/rein-et-al-2019-liveness-literature-study.md) — liveness dimensions.
- [User-driven access control](../30-sources/roesner-et-al-2012-user-driven-access-control.md) — interaction-bound authority.
- [The Update Framework](../30-sources/samuel-et-al-2010-tuf.md) — role-separated update trust.
- [Conflict-free replicated data types](../30-sources/shapiro-et-al-2011-conflict-free-replicated-data-types.md) — convergence and its scoped semantics.
- [Mutatis Mutandis](../30-sources/stoyle-et-al-2005-safe-predictable-dynamic-updating.md) — controlled safe update points.
- [Cooperative-editing consistency](../30-sources/sun-et-al-1998-cooperative-editing-consistency.md) — convergence, causality, and intention.
- [in-toto](../30-sources/torres-arias-et-al-2019-in-toto.md) — attributable supply-chain steps.
- [WAI-ARIA 1.2](../30-sources/w3c-2023-wai-aria-1-2.md) — roles, states, relationships, and actions.
- [WCAG 2.2](../30-sources/w3c-2024-wcag-2-2.md) — accessibility and operability criteria.
- [Core-AAM 1.2](../30-sources/w3c-2026-core-accessibility-api-mappings-1-2.md) — platform mapping differences.
- [Canarying releases](../30-sources/warner-davidovic-2018-canarying-releases.md) — cohort attribution and inconclusive rollout.
- [WASI design principles](../30-sources/wasi-project-2026-design-principles.md) — explicit portable imports.
- [Wayland architecture](../30-sources/wayland-project-2026-architecture-and-protocol.md) — surfaces, buffers, focus, and input routing.
- [User interaction design for secure systems](../30-sources/yee-2002-user-interaction-design-secure-systems.md) — trusted path and explicit authorization.

## Threads

- [Visual-computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [Open visual-computing inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
- [Visual-computing component index](../20-notes/visual-computing-synthesis-components/README.md)
- [Earlier component session](2026-09-04-visual-computing-synthesis-components-deep-dive.md)

## Follow-ups

- Define a versioned project/export format and executable generation models.
- Specify a canonical semantic snapshot/delta/action compatibility profile.
- Build real AT-SPI/UIA adapters and test actual assistive technologies.
- Prototype trusted input, transfer, secure-attention, and remote sessions.
- Implement changeset migration with injected failure and unknown effects.
- Evaluate a mixed-media project across visual, nonvisual, multimodal, and
  collaborative tasks under restart, overload, and revocation.
