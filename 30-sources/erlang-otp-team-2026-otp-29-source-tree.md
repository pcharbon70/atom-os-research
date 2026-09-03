---
title: "Erlang/OTP source tree at 5cf5f9725452"
kind: source
created: "2026-08-28"
authors:
  - "Erlang/OTP contributors"
published: "2026-08-03"
citation_key: "erlang-otp-source-5cf5f9725452"
container: "GitHub"
edition: "OTP-29.0.5; git revision 5cf5f9725452f4e1b6a4890e8ff0305d76924b98"
isbn: null
doi: null
url: "https://github.com/erlang/otp/tree/5cf5f9725452f4e1b6a4890e8ff0305d76924b98"
accessed: "2026-08-28"
tags:
  - beam
  - code-loading
  - erts
  - repository-audit
  - scheduling
  - virtual-machines
aliases:
  - "OTP 29 source audit"
---

# Erlang/OTP source tree at 5cf5f9725452

## Reference

Erlang/OTP contributors. *Erlang/OTP* source tree, tag OTP-29.0.5, revision
[`5cf5f9725452f4e1b6a4890e8ff0305d76924b98`](https://github.com/erlang/otp/commit/5cf5f9725452f4e1b6a4890e8ff0305d76924b98),
authored 2026-08-03. Accessed 2026-08-28. The repository and inspected source
headers use the Apache License 2.0.

## Research question or contribution

The audit asks which mechanisms current ERTS actually implements, how those
mechanisms depend on a host operating system, and which implementation facts
should or should not become requirements for a new kernel.

## Method

The official repository was cloned locally, the stable OTP-29.0.5 tag was
fetched, and the checkout was pinned to the full commit. Review concentrated on:

- `erts/emulator/beam/erl_vm.h`, `erl_process.*`, `erl_message.*`, `erl_gc.c`,
  `beam_load.c`, `code_ix.h`, and related scheduler, loader, table, and process
  structures;
- `erts/emulator/internal_doc/BeamAsm.md`, `GarbageCollection.md`,
  `CodeLoading.md`, and `AutomaticYieldingOfCCode.md`;
- Unix system and threading code below `erts/emulator/sys`;
- `erts/preloaded/src/erlang.erl`, the NIF and driver references,
  `lib/stdlib/src/supervisor.erl`, and `lib/kernel/src/code_server.erl`; and
- the matching system, reference, efficiency, and OTP design-principle
  documentation in the tree.

Tracked file counts and selected line totals were collected for orientation.
No generated binary, benchmark, or target-hardware trace was produced. Exact
commands are preserved in the [journal
entry](../50-journal/2026-08-28-beam-erts-and-otp-deep-dive.md).

## Findings

- `erl_vm.h` defines `CONTEXT_REDS` as 4,000 at this revision and the default
  initial combined heap-and-stack minimum, `H_DEFAULT_SIZE`, as 233 words.
  These are implementation constants, not language promises.
- The runtime implements normal, dirty CPU, and dirty I/O scheduler classes.
  Per-scheduler run queues, migration paths, thread progress, auxiliary work,
  timers, ports, and system tasks make scheduling substantially richer than a
  simple round-robin actor loop.
- The process representation connects registers, stack/heap storage, message
  queues, links, monitors, dictionaries, flags, scheduling state, resource
  accounting, and signal queues. A cheap language process is still a complex
  runtime object.
- Garbage collection is process-oriented, but the complete VM also manages
  shared binaries, literals, allocator arenas, code, atoms, tables, and other
  runtime-wide resources. Private language heaps do not eliminate shared
  implementation state.
- BeamAsm translates loaded BEAM instructions to native x86-64 or AArch64 code.
  It deliberately performs little optimization across instructions and reuses
  compiler register allocation, avoiding the runtime profiling and optimizer
  complexity of a tracing JIT. Unsupported architectures retain the
  interpreter path.
- Non-blocking code loading prepares a staged view, waits for thread progress,
  and publishes it by changing the active code index. `code_ix.h` defines three
  code indexes. Those three replicated access-structure generations must not be
  confused with the two module versions visible to Erlang code.
- Yieldable BIF/NIF machinery and the Yielding C Fun transformer exist because
  long native routines can occupy a scheduler and harm responsiveness. Dirty
  schedulers isolate classes of work but do not create a memory-protection
  boundary.
- The supervisor implementation supplies defaults of one-for-one, intensity
  one, and period five seconds. Excess restart intensity terminates the
  supervisor so that failure can propagate to its parent.
- The inspected Unix substrate uses POSIX threads and synchronization, clocks,
  memory mapping, files, sockets, event polling, dynamic loading, libc, and
  platform facilities including Linux `/proc` paths. Upstream ERTS is a hosted
  runtime whose OS contract is much larger than an interrupt, timer, and
  allocator shim.
- The tree contained 3,848 Erlang files, 599 C files, 464 headers, and 400
  Markdown files by tracked extension. Selected tracked C/header files under
  `erts/emulator/beam` totaled about 267,066 lines; selected system-port
  C/header files about 26,442 lines; and the direct Kernel and STDLIB Erlang
  sources about 238,492 lines. These numbers include optional, generated-style,
  test-adjacent, and platform code and are not a trusted-computing-base metric.

## Relevance

The source confirms that the attractive actor model is produced by a large,
carefully engineered runtime over substantial host services. It identifies
mechanisms worth adapting—safe-point accounting, process-local collection,
asynchronous signals, thread progress, staged publication, and yieldable native
work—while cautioning against treating ERTS itself as a small kernel.

It also sharpens the system boundary. A new kernel can either provide the host
contract required by ERTS, implement a selected compatible runtime, or adopt
the principles without compatibility. Those are materially different research
programs.

## Limits

This was a targeted static audit, not an exhaustive review of the Erlang/OTP
tree. The checkout was not configured or built, and no ERTS executable,
instruction trace, benchmark, scheduler trace, heap profile, port, NIF, or
fault-injection experiment was run. Line counts indicate scope only. Source
structures can change after OTP 29.0.5, and comments or internal documentation
are not public compatibility guarantees.

## Derived work

- [Managed actor runtime layer](../20-notes/managed-actor-runtime-layer.md)
- [Managed actor runtime map](../10-maps/managed-actor-runtime.md)
- [Managed-runtime contract inquiry](../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md)
- [BEAM, ERTS, and OTP principles for a new operating system](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md)
- [Minimal privileged kernel layer](../20-notes/minimal-privileged-kernel-layer.md)
- [BEAM, ERTS, and OTP map](../10-maps/beam-erts-and-otp.md)
- [Kernel-placement inquiry](../40-inquiries/which-beam-erts-and-otp-principles-belong-in-the-kernel.md)
- [2026-08-28 research journal](../50-journal/2026-08-28-beam-erts-and-otp-deep-dive.md)
