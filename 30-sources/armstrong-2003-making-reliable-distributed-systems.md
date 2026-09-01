---
title: "Making reliable distributed systems in the presence of software errors"
kind: source
created: "2026-08-28"
authors:
  - "Joe Armstrong"
published: 2003
citation_key: "armstrong-2003-reliable-distributed-systems"
container: "Royal Institute of Technology"
edition: "Doctoral dissertation; TRITA-IMIT-LECS AVH 03:09; SICS Dissertation Series 34"
isbn: null
doi: null
url: "https://erlang.org/download/armstrong_thesis_2003.pdf"
accessed: "2026-08-28"
tags:
  - actor-model
  - erlang
  - fault-tolerance
  - otp
  - supervision
aliases:
  - "Armstrong thesis"
---

# Making reliable distributed systems in the presence of software errors

## Reference

Joe Armstrong. *[Making reliable distributed systems in the presence of
software errors](https://erlang.org/download/armstrong_thesis_2003.pdf)*.
Doctoral dissertation, Royal Institute of Technology, Stockholm, 2003.
TRITA-IMIT-LECS AVH 03:09; SICS Dissertation Series 34. Accessed 2026-08-28.

## Research question or contribution

The thesis asks how systems can remain reliable when their component programs
contain software errors. It develops the Erlang concurrency model and OTP
design methodology as a combined answer, then relates them to commercial
telecommunications systems.

## Method

Armstrong derives language and library requirements, describes Erlang and OTP
mechanisms, presents programming rules and patterns, and uses case studies from
industrial systems including the Ericsson AXD301. It is a design dissertation
with historical and industrial evidence, not a controlled fault-injection
comparison against alternative kernels.

## Findings

- The proposed concurrency-oriented programming model treats processes as
  self-contained virtual machines with strong isolation, private state,
  unforgeable identities, message-only interaction, unreliable delivery, and a
  way to detect another process's failure and reason.
- Strong isolation and asynchronous messaging are linked: a sender cannot rely
  on the receiver being present or on immediate acknowledgement. Reliable
  protocol behavior must be built from explicit replies, timeouts, and recovery
  rather than inferred from a send operation.
- The thesis identifies six system needs: concurrency, error encapsulation,
  fault detection, fault identification, live code upgrade, and stable storage.
  Erlang processes and signals cover only part of that set; libraries and
  external system facilities are also required.
- Workers and supervisors separate application work from generic correction.
  A component should fail when it cannot safely repair its own state, while a
  distinct process decides whether and how to restart it.
- “Let it crash” is conditional. Errors the programmer expects and understands
  should normally be handled. Termination is appropriate when continued local
  action would be less reliable than clean reconstruction under supervision.
- The thesis argues that many services traditionally associated with an OS can
  be implemented in the language runtime and OTP layer, leaving lower layers to
  supply drivers and hardware access.

## Relevance

This is the clearest foundational statement of the reliability principles the
project wants to preserve. It supports cheap isolated components, explicit
failure signals, hierarchy, restart policy outside the failed component,
dynamic change, and durable state as a coherent systems model.

It also suggests an evaluation standard: calling an actor runtime an operating
system is meaningful only if the complete system covers stable storage,
hardware and driver failures, whole-runtime failure, and the operational path
from diagnosis to recovery.

## Limits

The dissertation predates multicore ERTS, BeamAsm, current OTP security
guidance, modern cloud deployments, and many later runtime changes. Its
“unforgeable” process identifiers and strong-isolation model are conceptual,
not a current hostile-code security guarantee: official OTP 29 documentation
assumes loaded code and connected nodes are trusted. The industrial case
studies show that the methodology can support reliable products, but they do
not isolate the causal contribution of each language or OTP feature.

The claim that OTP can act as an application operating system is a design
argument, not evidence that ERTS replaces boot, hardware protection, drivers,
durable filesystems, secure updates, or a kernel on modern machines.

## Derived work

- [BEAM, ERTS, and OTP principles for a new operating system](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md)
- [BEAM, ERTS, and OTP map](../10-maps/beam-erts-and-otp.md)
- [Kernel-placement inquiry](../40-inquiries/which-beam-erts-and-otp-principles-belong-in-the-kernel.md)
- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [Minimal privileged kernel map](../10-maps/minimal-privileged-kernel.md)
- [Minimal privileged-kernel contract inquiry](../40-inquiries/what-contract-should-the-minimal-privileged-kernel-provide.md)
