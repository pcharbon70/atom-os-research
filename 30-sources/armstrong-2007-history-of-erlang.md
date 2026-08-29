---
title: "A History of Erlang"
kind: source
created: "2026-08-28"
authors:
  - "Joe Armstrong"
published: "2007-06-09"
citation_key: "armstrong-2007-history-erlang"
container: "Proceedings of the third ACM SIGPLAN conference on History of programming languages"
edition: null
isbn: null
doi: "10.1145/1238844.1238850"
url: "https://doi.org/10.1145/1238844.1238850"
accessed: "2026-08-28"
tags:
  - actor-model
  - erlang
  - fault-tolerance
  - programming-language-history
aliases:
  - "History of Erlang"
---

# A History of Erlang

## Reference

Joe Armstrong. “[A History of
Erlang](https://doi.org/10.1145/1238844.1238850).” *Proceedings of the Third ACM
SIGPLAN Conference on History of Programming Languages (HOPL III)*, 2007,
pages 6-1–6-26. DOI 10.1145/1238844.1238850.

## Contribution

The paper traces Erlang from Ericsson's experiments in telecommunications
languages through its process model, VM implementations, open-source release,
and OTP practices. It explains why concurrency, protocols, fault tolerance,
live change, and long-running systems shaped the language.

## Method

This is a retrospective first-person history by a principal designer. It
combines project records, implementation history, design rationale, examples,
and lessons learned. It is primary evidence for intent and evolution, but not
an independent performance or reliability evaluation.

## Findings

- Erlang was designed around large concurrent systems that must run for long
  periods and evolve in service. Lightweight processes, no ordinary shared
  mutable state, asynchronous messages, links, and live code change emerged
  from that target rather than being isolated language features.
- The model places protocols and connections between components ahead of the
  sequential language used inside a component. This makes the concurrency
  architecture and failure relationships primary design artifacts.
- Rapid prototypes and feedback from real users shaped the language. Several
  execution engines were replaced as requirements became clearer, supporting a
  principle-first rather than implementation-first research strategy.
- The paper is candid about shortcomings: atoms are not garbage-collected;
  foreign-code isolation is difficult; mailbox flooding and CPU consumption can
  weaken process isolation; and distributed Erlang historically offered an
  all-or-nothing security model.
- The author argues that process protocols deserve more explicit notation and
  analysis. Message passing alone does not guarantee a correct protocol.

## Relevance

The history reinforces that the transferable value is a systems method:
isolate state, make protocols explicit, expose failure, and design operations
and change into the system. It also supplies negative lessons directly relevant
to a kernel. Resource exhaustion, global tables, foreign code, and ambient
cluster trust need architectural remedies rather than optimistic supervision.

The evolution from prototypes through several VMs also supports comparing an
ERTS port, a compatible VM, and a clean-slate runtime before fixing the kernel
ABI around one implementation.

## Limits

The paper ends in 2007. Its implementation and deployment details are
historical, and later OTP releases have changed schedulers, garbage collection,
distribution options, code generation, tooling, and mitigations. A designer's
retrospective can overrepresent the coherence of decisions after the fact. Use
current official documentation and source for present behavior.

## Derived work

- [BEAM, ERTS, and OTP principles for a new operating system](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md)
- [BEAM, ERTS, and OTP map](../10-maps/beam-erts-and-otp.md)
- [Kernel-placement inquiry](../40-inquiries/which-beam-erts-and-otp-principles-belong-in-the-kernel.md)
