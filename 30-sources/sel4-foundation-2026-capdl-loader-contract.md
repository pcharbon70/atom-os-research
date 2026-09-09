---
title: "capDL Loader"
kind: source
created: "2026-09-09"
authors: ["seL4 Foundation"]
published: null
citation_key: "sel4-foundation-2026-capdl-loader-contract"
container: "seL4 documentation"
edition: null
isbn: null
doi: null
url: "https://docs.sel4.systems/projects/capdl/c-loader-app.html"
accessed: "2026-09-09"
tags: [capabilities, kernel-internal-services, microkernels]
aliases: []
---

# capDL Loader

## Reference

seL4 Foundation. [capDL Loader](https://docs.sel4.systems/projects/capdl/c-loader-app.html). seL4 documentation; publication date not stated. Accessed 2026-09-09.

## Research question or contribution

Where does declarative initialization assurance stop?

## Method

Read the loader overview, functional-correctness scope, assumptions and retained-capability discussion.

## Findings

The loader constructs a system from a declarative description. Its documented correctness argument concerns a model, not verification of the complete C implementation; additional functionality is outside that argument. Remaining loader capabilities are rendered inert by terminating the loader.

## Relevance

Separate manifest validation, construction correctness and elimination of usable bootstrap authority. Each needs its own evidence in Atom OS.

## Limits

A successfully parsed model need not encode the intended security policy. A model-level theorem neither verifies an Atom loader nor covers extensions without a corresponding argument.

## Derived work

- [Manifest decoding and policy validation](../20-notes/minimal-privileged-kernel-components/bootstrap-and-root-authority-handoff/manifest-decoding-and-policy-validation.md) — proposed contract constrained by this evidence.
- [Private object construction transaction](../20-notes/minimal-privileged-kernel-components/bootstrap-and-root-authority-handoff/private-object-construction-transaction.md) — proposed contract constrained by this evidence.
- [One-way root handoff and abort](../20-notes/minimal-privileged-kernel-components/bootstrap-and-root-authority-handoff/one-way-root-handoff-and-abort.md) — proposed contract constrained by this evidence.
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md) — selective architectural context.
