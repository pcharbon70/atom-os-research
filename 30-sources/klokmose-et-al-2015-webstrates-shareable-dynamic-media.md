---
title: "Webstrates: Shareable Dynamic Media"
kind: source
created: "2026-09-04"
authors:
  - "Clemens Nylandsted Klokmose"
  - "James R. Eagan"
  - "Siemen Baader"
  - "Wendy E. Mackay"
  - "Michel Beaudouin-Lafon"
published: "2015"
citation_key: "klokmose-et-al-2015-webstrates-shareable-dynamic-media"
container: "Proceedings of the 28th Annual ACM Symposium on User Interface Software & Technology (UIST '15)"
edition: null
isbn: "978-1-4503-3779-3"
doi: "10.1145/2807442.2807446"
url: "https://doi.org/10.1145/2807442.2807446"
accessed: "2026-09-04"
tags:
  - collaborative-computing
  - dynamic-media
  - end-user-programming
  - visual-computing
aliases:
  - "Webstrates"
---

# Webstrates: Shareable Dynamic Media

## Reference

Clemens Nylandsted Klokmose, James R. Eagan, Siemen Baader, Wendy E.
Mackay, and Michel Beaudouin-Lafon. “[Webstrates: Shareable Dynamic
Media](https://doi.org/10.1145/2807442.2807446).” *Proceedings of UIST
'15*, 2015. The open [author manuscript](https://pure.au.dk/ws/files/91047333/webstrates.pdf)
was read in addition to the bibliographic record.

## Contribution

The paper introduces *shareable dynamic media*: malleable substrates that
combine content, computation, and interaction and may act as documents,
applications, or both. Webstrates changes a web page from a client-side copy
of server-owned behavior into a persistent, synchronized substrate that users
can compose, share, personalize, and alter at run time.

## Method

The authors describe the system architecture, use the system to co-author the
paper, report a second multi-device presentation case study, build three
additional prototypes, and evaluate synchronization and system behavior. This
is a research-system demonstration and systems evaluation, not a controlled
longitudinal study of broad end-user adoption or a security proof.

## Findings

- A substrate can hold content, computation, and interaction while one
  substrate gives structure or meaning to another.
- Persisting and synchronizing client-side document changes supports several
  users and several personalized editors over the same shared material.
- Separating a shared substrate from the particular transclusion and editor
  used to present it enables multiple simultaneous representations.
- The case studies demonstrate composition across devices and run-time
  extension without a fixed application boundary.
- Web technology supplies portability and a familiar implementation base, but
  the prototype inherits browser, server, DOM, operational-transformation,
  access-control, and availability assumptions that are not intrinsic to the
  dynamic-media idea.

## Relevance

Webstrates is direct post-Smalltalk evidence that a document/application
boundary can be replaced by user-malleable, shared computational objects. For
Atom OS it supports project-owned composition and provider-independent views,
while also warning against equating a shared mutable DOM with the durable
semantic model or authority graph.

## Limits

The prototype centralizes synchronization and gives the shared DOM a large
semantic and failure role. It does not demonstrate capability confinement,
offline-first ownership, deterministic conflict resolution for arbitrary
program state, accessible semantic equivalence, or recovery from a compromised
renderer. Its positive examples establish feasibility, not the correct Atom OS
trust boundary.

## Derived work

- [Alan Kay's Smalltalk visual interface and the modern desktop](../20-notes/alan-kay-smalltalk-visual-interface-and-modern-desktop.md)
- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
