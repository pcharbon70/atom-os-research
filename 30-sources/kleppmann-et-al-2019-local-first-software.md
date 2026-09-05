---
title: "Local-First Software: You Own Your Data, in Spite of the Cloud"
kind: source
created: "2026-09-04"
authors:
  - "Martin Kleppmann"
  - "Adam Wiggins"
  - "Peter van Hardenberg"
  - "Mark McGranaghan"
published: "2019-10"
citation_key: "kleppmann-et-al-2019-local-first-software"
container: "Proceedings of the 2019 ACM SIGPLAN International Symposium on New Ideas, New Paradigms, and Reflections on Programming and Software (Onward! '19)"
edition: null
isbn: "978-1-4503-6995-4"
doi: "10.1145/3359591.3359737"
url: "https://doi.org/10.1145/3359591.3359737"
accessed: "2026-09-04"
tags:
  - collaborative-computing
  - crdt
  - data-ownership
  - local-first
aliases:
  - "Local-first software"
---

# Local-First Software: You Own Your Data, in Spite of the Cloud

## Reference

Martin Kleppmann, Adam Wiggins, Peter van Hardenberg, and Mark McGranaghan.
“[Local-First Software: You Own Your Data, in Spite of the
Cloud](https://doi.org/10.1145/3359591.3359737).” *Onward! '19*, pages
154–178, October 2019. The authors' [HTML
edition](https://www.inkandswitch.com/essay/local-first/) and [paper](https://martin.kleppmann.com/papers/local-first.pdf)
were checked.

## Contribution

The paper defines seven ideals for software that combines local ownership and
offline responsiveness with multi-device access and collaboration. It surveys
storage and synchronization architectures, evaluates several prototypes, and
argues that the user's local copy should be primary rather than a cache beneath
an indispensable service provider.

## Method

The authors synthesize design principles from several years of prototype work
at Ink & Switch, compare common deployment models, and analyze CRDTs as a
candidate synchronization substrate. The work is an experience report and
architectural argument, not a controlled usability study or proof that all
application semantics can merge automatically.

## Findings

- Local operations can complete against an authoritative local replica rather
  than wait for a network round trip.
- Collaboration, multi-device use, privacy, long-term preservation, and user
  control need not require the cloud service to own the only authoritative
  copy.
- CRDTs can merge some concurrent data changes without a central sequencer,
  but data type, metadata growth, access control, and application semantics
  remain design concerns.
- Availability of bytes is not enough for longevity: usable software,
  interpretable schemas, migrations, and control over replicas also matter.
- The authors explicitly restrict the argument to user-created documents and
  personal data; centralized services such as banking have different
  authority and consistency requirements.

## Relevance

The local-first ideals give Atom OS an operational meaning for “user-owned
project”: locally usable durable state, exportable history and schema, optional
network assistance, and collaboration that does not silently transfer project
ownership to a provider. They also support separating replication rights from
ordinary object authority.

## Limits

The paper does not define an OS capability model, trusted input path, general
transaction protocol, or resolution rule for non-commutative external effects.
CRDT convergence does not establish authorization, semantic validity, or
intent preservation. Atom OS therefore cannot use “local-first” as a promise
that every actor state or effect is mergeable.

## Derived work

- [Alan Kay, Smalltalk, and visual computing map](../10-maps/alan-kay-smalltalk-ui.md)
- [Visual-computing model inquiry](../40-inquiries/what-visual-computing-model-should-atom-os-adopt.md)
