---
title: "Which BEAM, ERTS, and OTP principles belong in a new kernel?"
kind: inquiry
created: "2026-08-28"
status: open
tags:
  - actor-model
  - beam
  - capabilities
  - erts
  - operating-systems
  - otp
  - systems-architecture
  - zig
aliases:
  - "Kernel placement of BEAM and OTP principles"
---

# Which BEAM, ERTS, and OTP principles belong in a new kernel?

## Why this matters

“An OS based on BEAM and OTP principles” does not yet specify a protection
boundary. BEAM is an instruction machine, ERTS is a hosted runtime, and OTP is
mostly library and operational policy. Copying all three into privileged code
would inherit a large trusted computing base; placing everything in one hosted
runtime would leave the host OS as the actual protection, resource, driver, and
recovery foundation.

The project needs a principled rule for what the kernel must enforce, what a
managed actor runtime can implement cheaply, and what OTP-like services should
decide in user space. That choice also determines whether compatibility with
upstream BEAM modules and OTP applications is central, partial, or unnecessary.

The base implementation language is no longer part of this inquiry. New kernel
and project-owned native code is Zig under the settled [language
decision](../20-notes/zig-as-the-kernel-implementation-language.md). The
inquiry may change layer placement, compatibility strategy, or mechanism design;
it does not compare implementation languages.

## Operational question

For each candidate mechanism—process identity, message delivery, scheduling,
memory ownership, failure notification, supervision, code loading,
distribution, drivers, persistence, and observability—determine the least
privileged layer that can implement it in the Zig-based system while meeting
all of these criteria:

1. **Containment:** a faulty or malicious component cannot read, modify, or
   indefinitely block resources outside its declared authority.
2. **Bounded overload:** CPU, memory, mailbox, storage, and device demand have
   enforceable limits and documented failure behavior.
3. **Responsiveness:** timers, cancellation, process exit, and high-priority
   system work meet an explicit latency target under allocation, messaging,
   native work, and interrupt load.
4. **Recovery:** actor, service, runtime-domain, driver, node, and machine
   failures produce distinguishable evidence and have bounded recovery paths.
5. **Lifecycle:** a version can be authenticated, prepared, published, migrated,
   rolled back, and recovered after power loss without exposing a half-updated
   system.
6. **Distribution:** remote authority is authenticated and scoped; partitions,
   loss, duplication, retry, ordering, and backpressure are explicit.
7. **Portability:** every required host or firmware service is named, and a
   reset-to-managed-code trace can be reproduced on at least two materially
   different targets.

A mechanism belongs in the kernel only if an experiment or threat analysis
shows that a less privileged layer cannot enforce the required boundary, or if
the mechanism is required before ordinary services can run. The inquiry is
resolved only after a prototype and measurements justify a layer placement for
the initial system, not when a document simply proposes one.

## Working hypotheses

### H1: protected domains and managed actors should be separate scales

The kernel should schedule and isolate a modest number of hardware-protected
domains. An ERTS-like runtime should schedule much cheaper managed actors
inside each admitted domain. This preserves process economics while containing
drivers, native extensions, and mutually untrusted applications.

Falsifier: if kernel-visible actors meet process-creation, context-switch,
message, memory, and latency goals without a prohibitive protection cost, the
second scheduler may be unnecessary. Conversely, if runtime scheduling cannot
honor domain budgets or cancellation, more actors may need kernel visibility.

### H2: bounded capability endpoints should underlie mailboxes

The kernel should provide bounded, capability-addressed asynchronous endpoints
with explicit overflow and cancellation semantics. A runtime can build Erlang-
style selective mailboxes and aliases above them.

Falsifier: if cross-layer buffering, copying, or scheduling makes the endpoint
unusable for cheap local actors, a shared-memory fast path or runtime-only local
mailbox may be necessary. It must still preserve charging and revocation when
crossing a protection domain.

### H3: supervision belongs above the kernel

The kernel should terminate domains, reclaim resources, and emit reliable
failure events. OTP-like restart strategies, intensity limits, dependency
ordering, and application lifecycle should be implemented by ordinary
supervisor services.

Falsifier: a boot or recovery scenario may require a minimal root-supervisor
contract before user services exist. Even then, application-specific restart
policy should not become an immutable kernel API.

### H4: versioned publication is a cross-layer primitive

ERTS's prepare-and-atomically-publish code-loading pattern should generalize to
kernel-visible service endpoints and system images. State transformation and
rollback policy remain outside the kernel, while the kernel supplies atomic
selection, quiescence evidence, and durable boot state.

Falsifier: if service indirection and quiescence impose unacceptable latency or
cannot survive power loss under the selected storage model, the update unit or
publication boundary must change.

### H5: principles-first is the architectural center

The clean-slate system should not make BEAM bytecode compatibility a kernel
requirement. A port of upstream ERTS and a narrow BEAM-compatible runtime are
comparison prototypes that quantify ecosystem reuse and compatibility costs.

Falsifier: if reusing ERTS produces a sufficiently small, auditable substrate
and meets protection, recovery, and timing requirements with materially less
total complexity than a new runtime, an ERTS-centered architecture may be the
better foundation.

## Paths to explore

### Compatibility alternatives

| Path | First artifact | Evidence needed before preference |
| --- | --- | --- |
| Upstream ERTS port | Minimal Zig kernel/compatibility substrate that boots a pinned OTP release and contains upstream C ERTS behind an explicit boundary | Complete host-contract inventory, trusted-code size, C ABI and build census, driver isolation, dual-scheduler behavior, memory floor, OTP test-suite results |
| Selected BEAM compatibility | Zig loader and native actor runtime for a declared opcode/BIF/OTP profile | Versioned compatibility matrix, negative tests, exception and signal semantics, hot-loading behavior, tooling and library coverage |
| Principles-first runtime | Zig substrate for bounded actors, capabilities, supervision-friendly failures, and versioned services with no BEAM promise | Compiler/tool path, process and message economics, diagnostics, service libraries, comparison against equivalent OTP workload |

### Minimum experiments

All new kernel and project-owned native code in these experiments is Zig. C is
limited to named upstream, vendor, or compatibility components.

1. Implement a bounded endpoint with send and receive capabilities, byte and
   message quotas, credits, revocable reply authority, and structured drop or
   refusal evidence.
2. Run reduction-accounted actors inside a kernel-scheduled protection domain.
   Measure throughput and tail latency under timer, interrupt, garbage
   collection, native worker, and priority stress.
3. Crash ordinary actors, the actor runtime, and an isolated driver. Confirm
   cleanup of memory, capabilities, endpoints, interrupt subscriptions, and DMA
   buffers, and preserve the exit reason outside the failed domain.
4. Publish a new service version atomically while messages and timers are in
   flight. Test state conversion, incompatible code, lingering callers,
   rollback, and simulated power failure.
5. Connect two nodes with cryptographic identities and delegated endpoint
   capabilities. Inject loss, delay, duplication, partition, restart, and a
   compromised peer.
6. Trace reset to the first managed actor on one emulator and one physical
   target. Inventory firmware, privilege state, memory maps, clocks, allocator,
   interrupts, storage, console, and network dependencies.
7. Port one identical supervision workload to pinned OTP 29, AtomVM, a narrow
   compatible runtime, and the principles-first runtime. Record semantic gaps
   before comparing performance.

### Source and implementation follow-up

- Audit current ERTS start-up and Unix-host calls systematically instead of by
  targeted search.
- Pin and inspect Tyn, GRiSP Metal/RTEMS, historical LING, and any maintained
  bare-metal BEAM work. Reproduce one boot claim before using it as evidence.
- Read current research on capability kernels, language-based protection,
  real-time garbage collection, restartable drivers, crash-only software,
  transactional update, and verified IPC alongside the BEAM/OTP lineage.
- Derive protocol tests from OTP links, monitors, aliases, selective receive,
  supervisor intensity, and code-version transitions without assuming their
  exact APIs.
- Pin the Zig toolchain and test its freestanding ABI, C integration, generated
  code, safety modes, and scalar/FPU/SIMD context assumptions on the first
  target. These tests refine the implementation policy rather than reopen the
  language choice.

## Findings

The initial [operating-system synthesis](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md)
supports the working hypotheses but does not resolve them:

- The official architecture separates the instruction machine from process
  runtime and recovery libraries, supporting a layered kernel design.
- ERTS demonstrates cheap processes, process-local collection, reduction-based
  pre-emption, explicit failure signals, and non-blocking version publication.
- Official security guidance confirms that loaded code, native extensions, and
  connected nodes are trusted; ordinary process isolation is not a hostile-code
  boundary.
- Historical measurements show that mailbox pressure, runtime-wide locks,
  memory structures, global names, and global recovery data can defeat simple
  “share nothing” and “scale out” narratives.
- OTP supervision provides a strong recovery-policy model, but it cannot by
  itself survive complete runtime, driver, power, storage, or correlated
  failures.
- No prototype in this archive yet measures the proposed two-level scheduler,
  bounded capability endpoint, driver domain, or transactional update path.
- Zig is now the fixed base language for implementing those prototypes; this is
  a project decision rather than a result claimed by the BEAM/OTP evidence.

## Outcome

Open. The present preferred direction is a small capability kernel, an
ERTS-inspired managed actor layer, and OTP-inspired user-space services, with
BEAM compatibility treated as an experimental choice. The kernel and new
native components are implemented in Zig. The first bounded endpoint and
failure-containment prototypes should be allowed to overturn the proposed
decomposition, but not silently substitute another base language.
