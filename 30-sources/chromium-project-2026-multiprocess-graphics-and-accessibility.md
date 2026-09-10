---
title: "Chromium Multi-Process Graphics and Accessibility Architecture"
kind: source
created: "2026-09-10"
authors:
  - "Chromium Project"
published: null
citation_key: "chromium-project-2026-multiprocess-graphics-and-accessibility"
container: "Chromium design documentation"
edition: null
isbn: null
doi: null
url: "https://www.chromium.org/developers/design-documents/multi-process-architecture/"
accessed: "2026-09-10"
tags:
  - accessibility
  - compositor
  - fault-isolation
  - user-interface
aliases:
  - "Chromium UI process architecture"
---

# Chromium Multi-Process Graphics and Accessibility Architecture

## Reference

Chromium Project. [Multi-process
architecture](https://www.chromium.org/developers/design-documents/multi-process-architecture/),
[accessibility technical
documentation](https://www.chromium.org/developers/design-documents/accessibility/),
and [GPU-accelerated
compositing](https://www.chromium.org/developers/design-documents/gpu-accelerated-compositing-in-chrome/).
Accessed 2026-09-10.

## Research question or contribution

How does a production browser divide untrusted document rendering, privileged
UI, accessibility projection, input routing, and GPU access across processes?

## Method

The source set is first-party design documentation. It reports architecture and
implementation rationale, including historical paths; it is not a current
conformance matrix or independent security proof.

## Findings

- Renderer processes are isolated because rendering engines can crash or be
  compromised; the browser retains routing and lifecycle state and can replace
  a failed renderer.
- Frame identity is composite: a routing identifier is unique only within its
  renderer process and must be paired with the hosting process identity.
- The browser routes input and maintains the cross-process frame tree, while a
  dedicated GPU process mediates access to native graphics APIs.
- Accessibility semantics originate in renderer-owned document state but are
  cached in the browser process so platform assistive APIs need not enter the
  sandboxed renderer.
- Software rendering remains a fallback, demonstrating that device acceleration
  is an implementation profile rather than semantic ownership.

## Relevance

The design provides a mature precedent for disposable renderers, compound
generation-aware identities, retained semantic projections, privileged input
routing, GPU mediation, and independent software fallback.

## Limits

Chromium's browser process remains a large trusted coordinator, its documents
describe evolving implementations, and web-origin policy is not Atom OS
capability policy. Renderer restart does not by itself prove durable application
meaning or exactly-once domain effects.

## Derived work

- [Durable semantic actors and disposable presentation](../20-notes/visual-computing-synthesis-components/durable-semantic-actors-and-disposable-presentation/README.md).
- [Cross-layer placement and recovery topology](../20-notes/visual-computing-synthesis-components/cross-layer-placement-and-recovery-topology/README.md).
- [Visual-computing internal-services research session](../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md).
