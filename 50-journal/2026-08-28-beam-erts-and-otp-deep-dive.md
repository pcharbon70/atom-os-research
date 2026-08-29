---
title: "2026-08-28 BEAM, ERTS, and OTP deep dive"
kind: journal
created: "2026-08-28"
tags:
  - beam
  - erts
  - literature-search
  - otp
  - repository-audit
  - research-session
aliases:
  - "BEAM and OTP source and literature audit"
---

# 2026-08-28 BEAM, ERTS, and OTP deep dive

## Observations

- “BEAM,” “ERTS,” and “OTP” need separate meanings in this archive. BEAM is the
  instruction machine, ERTS implements processes and runtime facilities, and
  OTP provides behaviours, supervision, applications, releases, and policy.
- The most promising OS inheritance is a combination of cheap isolated actors,
  asynchronous protocols, work-accounted safe points, local reclamation,
  explicit failure observation, hierarchical recovery, and versioned
  publication.
- Current Erlang/OTP deliberately relies on a host security and resource
  boundary. Loaded code and connected nodes are trusted; NIFs and drivers are
  native; mailboxes and process consumption are not bounded by default.
- ERTS's Unix implementation uses a broad POSIX and host-OS surface. Porting
  upstream ERTS, implementing BEAM compatibility, and designing a new inspired
  runtime are three different projects.
- Historical papers consistently qualify the attractive abstraction: runtime
  locks and allocators can constrain many-core scaling; global namespaces and
  recovery data constrain distributed scaling; and heap/message placement is a
  design trade-off rather than a consequence of actor semantics.
- Practitioner sources repeatedly identify mailbox backpressure, long native
  work, state migration, and misuse of “let it crash” as operational hazards.
  They were used as search leads, not independent proof.

## Environment

- Host: Linux Mint 22.1 (Xia), x86-64, Linux 6.8.0-51-generic.
- Git: 2.49.0.
- Python: 3.12.12.
- curl: 8.5.0.
- pdftotext: 24.02.0.
- The host's installed Erlang reported OTP release 27. It was not used as the
  audited runtime or as evidence about OTP 29 behavior.
- No kernel target, virtual machine monitor, board, interrupt trace, power
  instrument, or fault-injection harness was used.

## Evidence

### Official source acquisition and revision choice

The official repository was cloned to a temporary directory outside the
archive. The moving default branch initially resolved to a development commit
reporting OTP 30.0-rc0, so the audit was deliberately switched to the stable
release that matched the rendered manual:

```bash
git clone --depth=1 https://github.com/erlang/otp.git
git -C otp rev-parse HEAD
git -C otp fetch --depth=1 origin tag OTP-29.0.5
git -C otp checkout --detach OTP-29.0.5
git -C otp show -s --format='%H%n%aI%n%an%n%s' HEAD
cat otp/OTP_VERSION
```

Pinned result:

```text
5cf5f9725452f4e1b6a4890e8ff0305d76924b98
2026-08-03T11:34:26+02:00
Erlang/OTP
Updated OTP version
29.0.5
```

The source audit read these primary areas directly:

```text
system/doc/reference_manual/ref_man_processes.md
system/doc/reference_manual/code_loading.md
system/doc/reference_manual/distributed.md
system/doc/design_principles/design_principles.md
system/doc/design_principles/sup_princ.md
system/doc/design_principles/release_handling.md
system/doc/design_principles/secure_coding.md
erts/doc/guides/communication.md
erts/emulator/internal_doc/BeamAsm.md
erts/emulator/internal_doc/GarbageCollection.md
erts/emulator/internal_doc/CodeLoading.md
erts/emulator/internal_doc/AutomaticYieldingOfCCode.md
erts/emulator/beam/erl_vm.h
erts/emulator/beam/erl_process.c
erts/emulator/beam/erl_process.h
erts/emulator/beam/erl_message.c
erts/emulator/beam/erl_message.h
erts/emulator/beam/erl_gc.c
erts/emulator/beam/beam_load.c
erts/emulator/beam/code_ix.h
erts/emulator/sys/common/*
erts/emulator/sys/unix/*
erts/preloaded/src/erlang.erl
lib/stdlib/src/supervisor.erl
lib/kernel/src/code_server.erl
```

Targeted searches covered reductions, scheduler types, process priorities,
run queues, aliases, signal ordering, queue storage, heap defaults, shared
binaries and tables, loader phases, code indexes, supervisor defaults, NIF and
driver guidance, trust, sandboxing, distribution cookies and TLS, system calls,
POSIX threads, clocks, mmap, dynamic loading, files, sockets, event polling,
and `/proc`.

Two implementation constants found at this revision were:

```text
erts/emulator/beam/erl_vm.h: CONTEXT_REDS = 4000
erts/emulator/beam/erl_vm.h: H_DEFAULT_SIZE = 233 words
erts/emulator/beam/code_ix.h: ERTS_NUM_CODE_IX = 3
```

Orientation counts from tracked files:

```text
3,848 .erl files
599 .c files
464 .h files
400 .md files
267,066 lines in selected tracked erts/emulator/beam C and header files
26,442 lines in selected erts/emulator/sys C and header files
238,492 lines in direct Kernel and STDLIB Erlang sources
```

These totals are not a trusted-computing-base or maintainability measure. They
include optional platforms, generated-style code, and many responsibilities
that a new system might omit or move.

No checkout build was attempted. This research pass audited source structure
and documentation rather than producing a local OTP 29 executable.

### Documentation reading

The user-supplied [documentation root](https://www.erlang.org/doc/) and [code
loading chapter](https://www.erlang.org/doc/system/code_loading.html) were read
first. The rendered site reported OTP 29.0.5 and ERTS 17.0.5. The matching
source Markdown was used for process, scheduling, memory, communication,
supervision, release, distribution, and security claims so that documentation
and implementation were pinned to the same release.

The official [BEAM
primer](../30-sources/hogberg-2020-brief-introduction-to-beam.md) established
the BEAM/ERTS terminology. The official [JIT
history](../30-sources/gustavsson-2020-road-to-the-jit.md) supplied the
implementation lineage and motivation for BeamAsm. [The BEAM
Book](../30-sources/stenman-2025-beam-book.md) was used as a secondary source
map and checked against current primary material.

### Research-paper acquisition

Five complete papers or theses were downloaded to the temporary research
directory and converted with pdftotext. Their SHA-256 values were:

```text
da585b914eb07350e2d6f727db5eb0fb1551f49fc1270f7d4dc079f2c8c1ab7a  armstrong-2003.pdf
1ebed44a2e76d2568ac5af39f86db3973e2f051f54e3311412ad0d6b790b6642  armstrong-2007.pdf
2ade5e5cedbe6e8992fdb1fc35af1c9bcde632161d6f9fde7ab4b1dc3672c4ad  sagonas-wilhelmsson-2006.pdf
a4827e7edaebfb59e1336fe591189958ea767a33d57edd7e33b3c5920f6515b6  zhang-2011.pdf
46e67de70d2ed40efbc2d4ffdd773e91c53221eef1d953fa1c499a66d97b2399  trinder-et-al-2017.pdf
```

The complete works were read for the claims retained in their source notes:

- [Armstrong's 2003
  dissertation](../30-sources/armstrong-2003-making-reliable-distributed-systems.md)
- [Armstrong's 2007 Erlang
  history](../30-sources/armstrong-2007-history-of-erlang.md)
- [Sagonas and Wilhelmsson on message-passing memory
  management](../30-sources/sagonas-wilhelmsson-2006-efficient-memory-management.md)
- [Zhang on many-core Erlang VM
  scalability](../30-sources/zhang-2011-erlang-vm-many-core-scalability.md)
- [Trinder et al. on reliable distributed
  scaling](../30-sources/trinder-et-al-2017-scaling-reliably.md)

DOI, author, venue, and publication metadata were checked through publisher or
repository records and Crossref where available. Historical results were not
silently projected onto current OTP 29.

### Articles, blogs, mailing lists, projects, and forums

Searches combined BEAM, ERTS, Erlang VM, OTP, scheduler, reductions, garbage
collection, message passing, mailboxes, backpressure, supervision, code loading,
hot upgrade, distribution, scalability, security, bare metal, unikernel,
microkernel, LING, GRiSP, and NIF failure. Official documentation and primary
papers supplied technical claims; community material supplied terminology,
failure reports, and implementation leads.

Contextual sources screened but not used as independent proof included:

- an Erlang Questions [scheduler-discussion
  thread](https://erlang.org/pipermail/erlang-questions/2016-March/088222.html),
  where an OTP engineer points readers to source and Zhang's now-historical
  thesis;
- an Erlang Questions [backpressure
  thread](https://erlang.org/pipermail/erlang-questions/2014-November/081850.html)
  describing a many-producer, one-consumer mailbox exhausting memory and the
  need for an explicit flow-control protocol;
- the Erlang Forums [Tyn
  announcement](https://erlangforums.com/t/tyn-a-rust-microkernel-that-runs-beam-on-bare-metal-no-linux/5577)
  and the [Tyn kernel repository](https://github.com/tyn-os/kernel), which claim
  an unmodified ERTS/BEAM environment over a small Rust microkernel on KVM/QEMU
  and AWS Nitro; these claims were not reproduced or source-audited here;
- [GRiSP software](https://www.grisp.org/software) and its GRiSP Metal work,
  which demonstrate an embedded BEAM arrangement over RTEMS and motivate a
  precise distinction between “direct to BEAM” and “without any substrate”;
- historical LING/Erlang-on-Xen material, useful as a compatibility and project-
  lifecycle caution but not treated as current implementation evidence; and
- practitioner comparisons of BEAM with other VMs and posts about supervision,
  native extensions, and hot upgrades. They were retained only where a claim
  could be checked against official documentation or primary source.

No forum anecdote was used to establish performance, safety, compatibility, or
production readiness.

## Threads

- [The durable synthesis](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md)
  proposes the current layered architecture and records its confidence limits.
- [The topic map](../10-maps/beam-erts-and-otp.md) organizes current semantics,
  implementation, reliability, memory, and scaling trails.
- [The open inquiry](../40-inquiries/which-beam-erts-and-otp-principles-belong-in-the-kernel.md)
  turns the synthesis into testable placement decisions.
- [The AtomVM map](../10-maps/atomvm-foundation.md) remains a concrete compact-
  VM comparison case rather than the project's prescribed implementation.

## Follow-ups

- Audit and build pinned OTP 29.0.5, then capture scheduler, mailbox, garbage-
  collection, code-loading, NIF, and distribution traces under controlled
  workloads.
- Produce a systematic reset-to-ERTS host-contract inventory for one current
  bare-metal or RTOS-backed project, beginning with Tyn or GRiSP.
- Extend the literature search into capability kernels, language-based systems,
  restartable drivers, real-time managed runtimes, crash-only software, and
  transactional update systems.
- Implement the bounded endpoint and two-level scheduling experiments in the
  open inquiry before selecting BEAM compatibility or a final kernel/runtime
  boundary.
