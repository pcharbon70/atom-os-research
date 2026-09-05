---
title: "WASI Design Principles"
kind: source
created: "2026-09-05"
authors:
  - "WebAssembly/WASI Subgroup"
published: null
citation_key: "wasi-project-2026-design-principles"
container: "WebAssembly/WASI repository"
edition: null
isbn: null
doi: null
url: "https://github.com/WebAssembly/WASI/blob/main/docs/DesignPrinciples.md"
accessed: "2026-09-05"
tags:
  - capability-security
  - plugins
  - wasi
aliases:
  - "WASI capability design"
---

# WASI Design Principles

## Reference

WebAssembly/WASI Subgroup. “[WASI Design
Principles](https://github.com/WebAssembly/WASI/blob/main/docs/DesignPrinciples.md).”
Living project documentation, accessed 5 September 2026.

## Research question or contribution

The document states principles for portable system interfaces whose external
resources are represented by explicit capability handles rather than ambient
global namespaces.

## Method

The current first-party design document was read for capability, handle,
linking, portability, and host-boundary claims. It records project intent, not
an independent security evaluation.

## Findings

- External resources should be supplied explicitly as unforgeable handles.
- A host or linker can refuse or interpose imports, enabling attenuation and
  virtualization.
- Portable APIs should avoid assuming one operating system's global namespace
  or process model.

## Relevance

Atom OS extension hosts can borrow explicit-import discipline and narrow
versioned resource facets. WASI is an optional compatibility/sandbox profile;
it does not replace the primary BEAM compatibility environment or lower-layer
protected domains.

## Limits

Living documentation can change and was pinned by access date only. Correct
host implementation is assumed, and handles do not alone enforce CPU, memory,
bandwidth, side-channel, or semantic limits.

## Derived work

- [Extension points, plugins, and live-tooling confinement](../20-notes/applications-and-domain-services-components/extension-points-plugins-and-live-tooling-confinement.md)
- [Application manifest, composition, and authority envelope](../20-notes/applications-and-domain-services-components/application-manifest-composition-and-authority-envelope.md)
