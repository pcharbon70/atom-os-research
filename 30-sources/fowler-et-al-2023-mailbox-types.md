---
title: "Special delivery: Programming with mailbox types"
kind: source
created: "2026-09-03"
authors:
  - "Simon Fowler"
  - "Duncan Paul Attard"
  - "Franciszek Sowul"
  - "Simon J. Gay"
  - "Phil Trinder"
published: 2023
citation_key: "fowler-et-al-2023-mailbox-types"
container: "Proceedings of the ACM on Programming Languages"
edition: "7(ICFP), Article 191, 78-107"
isbn: null
doi: "10.1145/3607832"
url: "https://doi.org/10.1145/3607832"
accessed: "2026-09-03"
tags:
  - actor-model
  - mailboxes
  - message-passing
  - type-systems
aliases:
  - "Mailbox types"
---

# Special delivery: Programming with mailbox types

## Reference

Simon Fowler, Duncan Paul Attard, Franciszek Sowul, Simon J. Gay, and Phil
Trinder. “[Special Delivery: Programming with Mailbox
Types](https://doi.org/10.1145/3607832).” *Proceedings of the ACM on
Programming Languages* 7(ICFP), Article 191, pages 78–107, 2023. [Extended
version](https://arxiv.org/abs/2306.12935).

## Research question or contribution

The paper develops mailbox types for statically describing the messages an
actor may receive and the protocols that connect senders and receivers, aiming
to reject communication mismatches, forgotten replies, and selected
self-deadlocks before execution.

## Method

The authors define the type system and operational model, prove key properties,
and implement the approach in a programming-language prototype with examples
and evaluation.

## Findings

- Actor-local mailboxes can receive stronger protocol guarantees when message
  capabilities and mailbox usage are statically tracked.
- Types can exclude classes of unexpected messages, forgotten replies, and
  self-deadlocks that an untyped mailbox discovers only at runtime. The result
  does not rule out general inter-process deadlock.
- The guarantees depend on adopting the language/type discipline; they do not
  describe arbitrary existing BEAM modules.

## Relevance

Mailbox types are a promising optional certified profile for future Atom OS
languages or generated service interfaces. The baseline BEAM-compatible
runtime must still implement dynamic selective receive, unknown terms, and
runtime failure semantics. Certificates may enable specialized queues only
when the loader verifies their assumptions.

## Limits

The paper is a language-safety result, not evidence for queue throughput,
memory bounds, overload behavior, or distributed failure semantics. It cannot
be silently imposed on untyped compiled BEAM code.

## Derived work

- [Signal ingress, mailboxes, and selective receive](../20-notes/managed-actor-runtime-components/signal-ingress-mailboxes-and-selective-receive.md)
- [Compatibility manifest, BEAM loader, and verifier](../20-notes/managed-actor-runtime-components/compatibility-manifest-beam-loader-and-verifier.md)
- [2026-09-03 component research journal](../50-journal/2026-09-03-managed-actor-runtime-components-deep-dive.md)
