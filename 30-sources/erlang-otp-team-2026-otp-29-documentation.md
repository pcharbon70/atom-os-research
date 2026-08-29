---
title: "Erlang/OTP 29.0.5 system documentation"
kind: source
created: "2026-08-28"
authors:
  - "Erlang/OTP contributors"
published: 2026
citation_key: "erlang-otp-docs-29.0.5"
container: "Erlang/OTP System Documentation"
edition: "OTP 29.0.5; ERTS 17.0.5"
isbn: null
doi: null
url: "https://www.erlang.org/doc/"
accessed: "2026-08-28"
tags:
  - beam
  - code-loading
  - erts
  - fault-tolerance
  - otp
  - scheduling
  - source-documentation
aliases:
  - "OTP 29 documentation"
---

# Erlang/OTP 29.0.5 system documentation

## Reference

Erlang/OTP contributors. *Erlang/OTP System Documentation*, OTP 29.0.5,
ERTS 17.0.5. [Documentation root](https://www.erlang.org/doc/). Accessed
2026-08-28.

The reading centered on [code
loading](https://www.erlang.org/doc/system/code_loading.html),
[processes](https://www.erlang.org/doc/system/ref_man_processes.html),
[scheduling](https://www.erlang.org/doc/system/eff_guide_processes.html),
[garbage collection](https://www.erlang.org/doc/apps/erts/GarbageCollection.html),
[communication](https://www.erlang.org/doc/apps/erts/communication.html), [OTP
design principles](https://www.erlang.org/doc/system/design_principles.html),
[supervision](https://www.erlang.org/doc/system/sup_princ.html), [release
handling](https://www.erlang.org/doc/system/release_handling.html),
[distribution](https://www.erlang.org/doc/system/distributed.html), and [secure
coding](https://www.erlang.org/doc/system/secure_coding.html). The matching
Markdown sources at tag OTP-29.0.5 were also read in the official repository.

## Research question or contribution

The documentation defines the current public semantics and supported
operational model that are often collectively called “BEAM.” This reading asks
which behavior belongs to the language, ERTS, or OTP; which behavior is an
implementation choice; and where the documented trust and resource boundaries
fall short of a kernel boundary.

## Method

The rendered OTP 29.0.5 manual was checked against the corresponding files in
the pinned OTP-29.0.5 source checkout. The review followed processes and
signals through scheduling, memory, native work, code change, supervision,
releases, distribution, and deployment security. Claims described as
implementation-dependent in the manual remain qualified here.

## Findings

### Processes and signals

- Erlang processes are lightweight, dynamically sized execution units. They
  interact with processes and ports through asynchronous signals; ordinary
  messages are the most common signal type.
- Signal reception can happen independently of executing a receive expression.
  Request/reply operations that appear synchronous can be implemented as two
  asynchronous signals.
- The ordering guarantee is per sender-destination pair. Signal arrival time is
  unspecified, and a distribution-channel failure can prevent signals from
  arriving.
- Links are bidirectional failure relationships; monitors provide one-way
  observation. Termination carries a reason and directly visible Erlang
  resources are released as the process exits.
- A process alias can act as a revocable reply target. Deactivating it lets the
  runtime discard a late response instead of adding it to a mailbox.
- Selective receive finds the first matching queued message. Its cost can grow
  with the number of messages scanned. Mailbox capacity and producer
  backpressure remain application or deployment concerns.
- Message data is normally copied between local process heaps, with exceptions
  such as reference-counted binaries and literals. The process option for
  on-heap versus off-heap message data trades faster ordinary delivery against
  better behavior when queues may become large.

OTP 28 introduced priority-message reception, so ordering statements must now
distinguish signal delivery from how accepted priority and ordinary messages
are arranged in the mailbox. This is one example of why scheduler and mailbox
behavior must be pinned to a release.

### Scheduling and native work

- ERTS uses reductions as an implementation-level approximation of work and
  pre-empts a process after its budget. The precise scheduling behavior is not
  a language guarantee and may change between releases.
- Processes have low, normal, high, and max priorities. Round-robin behavior
  applies within a priority, but higher-priority work can delay lower-priority
  work; the system does not automatically solve every priority-inversion case.
- ERTS normally starts scheduler threads based on available logical processors.
  Per-scheduler run queues and migration balance managed work, while the host
  OS ultimately schedules those native threads on CPUs unless explicit binding
  is configured.
- Dirty CPU and dirty I/O schedulers isolate lengthy native work from normal
  schedulers. They do not make arbitrary native code safe: a badly behaved or
  misclassified NIF can still delay other work, process suspension, garbage
  collection, or termination.
- Ordinary NIF work should complete in roughly a millisecond or less. Longer
  operations need yielding, dirty schedulers, or an external port/process
  design.

### Memory

- Each process has a private heap and uses generational copying collection.
  Stack and heap share a process allocation and grow toward one another.
- Independent heaps keep most garbage collection local and let process
  termination reclaim private memory cheaply.
- Large binaries and several runtime structures are shared. ETS,
  persistent_term, the atom table, code, allocators, and native resources mean
  that “share nothing” describes ordinary Erlang state semantics, not every
  ERTS implementation structure.
- Atoms are not garbage-collected and the atom table is bounded. Inputs that
  can create atoms therefore create a system-wide exhaustion risk.
- Default Erlang/OTP does not prevent a process from consuming enough resources
  to stop the whole runtime. Heap limits and other safeguards must be selected
  deliberately.

### Code loading and OTP lifecycle

- ERTS can retain current and old versions of a module. Fully qualified calls
  select the current version, while local calls and return addresses can keep a
  process executing old code.
- Loading a third version requires the oldest version to be purged. Processes
  that still refer to the oldest code can be terminated during purge.
- Hot loading changes executable code; state conversion remains an application
  responsibility. OTP behaviours expose system messages and code-change
  callbacks, while applications, release files, boot scripts, appup/relup
  instructions, and release handling supply a wider operational workflow.
- OTP supervision separates workers from generic restart policy. The standard
  strategies encode different dependency assumptions, while restart intensity
  limits prevent an endless local restart loop and propagate repeated failure
  upward.

### Trust and distribution

- Erlang is memory-safe for ordinary language code, but the deployment model
  assumes every loaded module is fully trusted. There is no built-in sandbox
  for untrusted Erlang code, and malicious loaded code can compromise the
  runtime.
- Native extensions and drivers enter the runtime's native trust boundary.
  Language-process supervision cannot contain arbitrary memory corruption or a
  complete VM crash.
- All nodes admitted to standard Erlang distribution are trusted with broad
  access to one another. The default cookie is meant to avoid accidental
  cluster mixing, not provide strong authentication. Untrusted networks need
  TLS with client-certificate verification and careful node-discovery policy.
- Default EPMD can reveal node names and ports to unauthenticated queries.

## Relevance

The manual supplies the current semantic baseline against which an inspired
kernel should be compared. It supports asynchronous signaling, explicit
failure observation, local collection, work accounting, supervision, and
versioned publication as valuable principles. It also makes clear that
resource bounds, hardware protection, hostile-code containment, durable
recovery, and authenticated authority are not supplied by ordinary Erlang
process isolation.

## Limits

This is documentation evidence, not a timing or fault-injection experiment.
Some scheduler, allocator, queue, and distribution behavior is deliberately
implementation-dependent. The web manual can advance after this access date;
the source-tree note pins implementation claims to OTP 29.0.5. Application
guidance describes supported behavior but does not establish hard real-time,
security-certification, or kernel-suitability results.

## Derived work

- [BEAM, ERTS, and OTP principles for a new operating system](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md)
- [BEAM, ERTS, and OTP map](../10-maps/beam-erts-and-otp.md)
- [Kernel-placement inquiry](../40-inquiries/which-beam-erts-and-otp-principles-belong-in-the-kernel.md)
- [2026-08-28 research journal](../50-journal/2026-08-28-beam-erts-and-otp-deep-dive.md)
