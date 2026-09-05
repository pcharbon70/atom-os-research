---
title: "User-Driven Access Control: Rethinking Permission Granting in Modern Operating Systems"
kind: source
created: "2026-09-04"
authors:
  - "Franziska Roesner"
  - "Tadayoshi Kohno"
  - "Alexander Moshchuk"
  - "Bryan Parno"
  - "Helen J. Wang"
  - "Crispin Cowan"
published: "2012-05"
citation_key: "roesner-et-al-2012-user-driven-access-control"
container: "2012 IEEE Symposium on Security and Privacy"
edition: null
isbn: null
doi: "10.1109/SP.2012.24"
url: "https://doi.org/10.1109/SP.2012.24"
accessed: "2026-09-04"
tags:
  - access-control
  - trusted-interaction
  - usable-security
  - user-intent
aliases:
  - "User-driven access control"
---

# User-Driven Access Control: Rethinking Permission Granting in Modern Operating Systems

## Reference

Franziska Roesner, Tadayoshi Kohno, Alexander Moshchuk, Bryan Parno, Helen J.
Wang, and Crispin Cowan. “[User-Driven Access Control: Rethinking Permission
Granting in Modern Operating Systems](https://doi.org/10.1109/SP.2012.24).”
*2012 IEEE Symposium on Security and Privacy*, pages 224–238, May 2012. The
[author manuscript](https://www.ieee-security.org/TC/SP2012/papers/4681a224.pdf)
was read.

## Contribution

The paper develops user-driven access control: permission is derived from an
authentic user action already meaningful in the application's context instead
of an install-time manifest or disconnected prompt. Access-control gadgets
expose trusted resource-specific interaction that an application can embed but
cannot forge.

## Method

The authors analyze permission failures on contemporary client platforms,
design and prototype access-control gadgets and related mechanisms, and report
two user studies with 139 and 186 participants. The prototypes cover selected
user-owned resources and do not constitute a complete desktop authority model.

## Findings

- Users' ordinary resource-selection actions can convey narrower intent than
  broad install-time grants or repeated prompts.
- A trusted principal must bind the visible resource, authentic interaction,
  requesting application, and resulting authority; application-drawn pixels
  alone cannot do so.
- Permission can be least-privilege and less disruptive when it is coupled to
  an action such as selecting a file or device target.
- User action is evidence of a particular intent, not blanket authority for
  future unrelated uses.
- Embedding trusted gadgets creates layout, spoofing, lifecycle, revocation,
  and accessibility challenges that require system mediation.

## Relevance

Atom OS should mint short-lived, audience-bound capabilities from brokered
focus, selection, drag/drop, clipboard, capture, and secure-confirmation
gestures. The event delivered to a view is evidence; the capability returned
by the trusted broker authorizes only the named resource and operation.

## Limits

The paper predates current compositor protocols and does not cover voice,
multi-user collaboration, remote desktops, restart generations, or every form
of continuous sensor use. Its user studies establish comparative expectations
for selected tasks, not universal understanding of capability semantics.

## Derived work

- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
