---
title: "What Visual-Computing Model Should Atom OS Adopt?"
kind: inquiry
created: "2026-09-04"
status: open
tags:
  - accessibility
  - capability-security
  - human-computer-interaction
  - live-programming
  - visual-computing
aliases:
  - "Atom OS visual UI contract"
  - "Capability-safe metamedium inquiry"
---

# What Visual-Computing Model Should Atom OS Adopt?

## Why this matters

Atom OS aims to preserve actor isolation, supervision, fault containment, and
distribution while building a complete operating system. A conventional
application-and-window desktop would fit those mechanisms, but it could miss
Alan Kay's stronger goal: a personal medium in which users can understand,
combine, and create the objects and tools behind the visible interface.

The opposite extreme—a globally mutable live image—would undermine
multi-principal security, independent recovery, bounded resources, and the
BEAM execution model. The open question is whether a user-programmable
metamedium can be reconstructed from isolated supervised actors and explicit
capabilities.

## Operational question

Can Atom OS make a durable user-owned project, rather than an application
package, the primary visual unit of work while satisfying all of these tests?

1. Non-expert users can inspect an unfamiliar object, relate a visible action
   to its symbolic behavior, modify it, and create a reusable tool.
2. Graphical, textual, programmatic, voice, and assistive views address stable
   semantic identities and equivalent operations.
3. Model actors survive bounded failures and restarts of renderers, the shell,
   the compositor, accessibility services, and editing tools.
4. Input, inspection, mutation, debugging, publication, and cross-project use
   each require explicit attenuable authority.
5. Presentation reconstruction cannot replay input, duplicate an external
   effect, or silently roll a durable model backward.
6. The compositor and secure-attention path remain small enough to audit and
   protect, while layout and desktop policy remain replaceable.
7. New media and editor types can be installed without adding privileged code
   or extending one central schema for every domain.
8. Latency, overload, accessibility, localization, distribution, and update
   behavior meet declared profiles under fault injection.

Failure of any security or semantic-integrity requirement rejects the current
design even if the interface appears live. Failure of the authorship tests
rejects the claim that it recovers Kay's metamedium rather than only a modern
desktop with scripting.

## Working hypotheses

- A project can be a durable, versioned capability graph of semantic model
  actors, histories, commands, media objects, editor providers, and
  collaborators.
- A versioned semantic UI protocol can be the common source for visual,
  assistive, automation, and remote views without prescribing one widget set.
- Rendering surfaces and GPU resources can be disposable leases derived from
  semantic view generations; model progress need not depend on their survival.
- A narrow compositor and input broker can enforce focus, secure attention,
  capture, clipboard, and drag-and-drop authority without owning application
  meaning.
- Live browsers, inspectors, editors, and debuggers can be ordinary supervised
  services if inspection and mutation rights are separately scoped and all
  persistent changes are staged, versioned, attributable, and reversible or
  compensatable.
- Direct manipulation and symbolic actor messages can address the same domain
  operations, allowing an action–image–symbol learning progression.
- A universal semantic *protocol family* is viable; a universal closed object
  taxonomy is not.

## Paths to explore

### Protocol models

- Define identities, generations, roles, values, relationships, actions,
  focus, selection, localization, update streams, and protocol negotiation for
  a semantic UI tree.
- Define project ownership, editor discovery, object handoff, embedding,
  provenance, capability attenuation, offline replicas, and deletion.
- Separate commands that request durable domain effects from ephemeral
  presentation actions and specify both outcome protocols.

### Prototypes

- Build one mixed-media project with text, table, graph, and simulation actors
  plus visual and screen-reader views.
- Implement two independently replaceable editors for one model type.
- Restart each UI service at every message transition and verify
  generation-bound reconstruction.
- Add a capability-scoped inspector and stage one live method or actor-module
  change with validation and rollback.

### Human evidence

- Compare a direct-only interface, a code-only interface, and an integrated
  action-image-symbol environment with novice and expert participants.
- Test explanation and transfer to a new task, not only speed and preference.
- Include keyboard-only, screen-reader, low-vision, motor-access, and localized
  workflows from the first study.

### Assurance

- Threat-model prompt spoofing, focus theft, input capture, stale surface and
  editor leases, unauthorized inspection, cross-project mutation, and
  resource-exhaustion attacks.
- Model-check view generations, event acknowledgement, compositor restart,
  authority revocation, and live-change commit/rollback state machines.
- Measure end-to-end action latency, semantic propagation, frame deadlines,
  overload behavior, and recovery bounds.

## Findings

The [historical and architectural
synthesis](../20-notes/alan-kay-smalltalk-visual-interface-and-modern-desktop.md)
finds that Kay's differentiating goal was semantic continuity and user
authorship, not the visible WIMP vocabulary alone. Smalltalk implemented a
powerful live environment but left its components in a shared failure and
authority domain. Modern desktops separated applications, compositors,
toolkits, persistence, and accessibility and thereby gained important
operational properties while making the application producer the normal author
of behavior.

The strongest current direction is a capability-safe metamedium: preserve
durable meaning in model actors and user-owned project graphs; make semantic
views primary; render through disposable workers and surfaces; and expose live
tools only through explicit authority and transactional change. No prototype
or human study yet verifies that this combination is usable, secure, or
performant.

## Outcome

Open. Resolution requires at minimum a protocol specification, executable
state models, a restartable mixed-media prototype, security tests, accessibility
testing, and a comparative learnability study. The [visual-computing
map](../10-maps/alan-kay-smalltalk-ui.md) routes the current evidence.
