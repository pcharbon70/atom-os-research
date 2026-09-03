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
decide in user space. Running compiled BEAM code is now a fixed platform
requirement. The remaining compatibility questions concern the pinned initial
profile, OTP coverage, implementation strategy, and how the kernel supports it
without absorbing managed-runtime policy.

## Operational question

For each candidate mechanism—process identity, message delivery, scheduling,
memory ownership, failure notification, supervision, code loading,
distribution, drivers, persistence, and observability—determine the least
privileged layer that can implement it while meeting all of these criteria:

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

### H5: BEAM compatibility belongs in the managed runtime

The platform must execute compiled BEAM code with automatic process-local
tracing collection, but the BEAM instruction set and term heap should remain a
managed-runtime contract rather than a kernel ABI. The kernel should provision
and account for runtime-domain memory in batches, while the runtime performs
ordinary term allocation, root tracing, reclamation, and process scheduling
without a privilege transition.

Falsifier: if conformance or resource evidence shows that a required memory or
execution invariant cannot be enforced without a new kernel primitive, add the
smallest policy-neutral primitive. Do not move BEAM heap tracing or collector
policy into privileged code merely because one runtime implementation expects
host services.

## Paths to explore

### Compatibility alternatives

| Path | First artifact | Evidence needed before preference |
| --- | --- | --- |
| Upstream ERTS port | Minimal kernel/compatibility substrate that boots a pinned OTP release | Complete host-contract inventory, trusted-code size, driver isolation, dual-scheduler behavior, memory floor, OTP test-suite results |
| New BEAM-compatible runtime | Loader and actor runtime for a declared opcode/BIF/OTP profile | Versioned compatibility matrix, allocation and GC conformance, negative tests, exception and signal semantics, hot-loading behavior, tooling and library coverage |
| Principles-only runtime control | Bounded actors, capabilities, supervision-friendly failures, and versioned services with no BEAM promise | Research comparison only; it cannot satisfy the platform compatibility requirement |

### Minimum experiments

1. Implement a bounded endpoint with send and receive capabilities, byte and
   message quotas, credits, revocable reply authority, and structured drop or
   refusal evidence.
2. Run reduction-accounted actors inside a kernel-scheduled protection domain.
   Measure throughput and tail latency under timer, interrupt, garbage
   collection, native worker, and priority stress. Verify that process-local
   collection does not require a kernel transition or stop unrelated runtime
   processes.
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
7. Port one identical supervision workload to pinned OTP 29, AtomVM, and the
   candidate compatible runtime. Exercise long-lived allocation and
   reclamation, explicit collection requests, process memory reporting,
   messages, shared binaries, exceptions, and code loading before comparing
   performance. A principles-only runtime may remain a research control.

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

## Findings

The initial [operating-system synthesis](../20-notes/beam-erts-and-otp-principles-for-a-new-operating-system.md)
supports the working hypotheses but does not resolve them:

- The official architecture separates the instruction machine from process
  runtime and recovery libraries, supporting a layered kernel design.
- ERTS demonstrates cheap processes, process-local collection, reduction-based
  pre-emption, explicit failure signals, and non-blocking version publication.
- A process-exit-only arena cannot run general long-lived compiled BEAM code
  within bounded memory because BEAM code does not explicitly free unreachable
  terms. Automatic process-local tracing collection is therefore an adopted
  compatibility constraint, not an optional optimization.
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

The focused [managed actor runtime
research](../20-notes/managed-actor-runtime-layer.md) strengthens the third-layer
placement and opens a dedicated [runtime contract
inquiry](what-contract-should-the-managed-actor-runtime-provide.md):

- the runtime, not the kernel, should own the compatibility manifest, BEAM
  loader, actor state, term heaps, tracing collector, signal/mailbox semantics,
  reductions, tables, timers, code versions, and actor-level tracing;
- kernel time and domain accounts enforce real CPU and memory authority while
  reductions distribute admitted time among actors;
- scientific alternatives such as Orca zero-copy collection depend on stronger
  type-system guarantees than ordinary BEAM provides; and
- ports or protected service domains are the default native boundary because
  dirty NIF scheduling does not contain memory corruption.

## Outcome

Open. The present direction is a small capability kernel, a BEAM-compatible
managed actor layer with automatic process-local tracing collection, and
OTP-inspired user-space services. Compatibility is fixed; the exact initial
BEAM/OTP profile and the choice between a pinned ERTS port and a new compatible
runtime remain experimental. The first bounded endpoint, collector, and
failure-containment prototypes may revise layer interfaces but may not be
reported as compatible without conformance evidence.
