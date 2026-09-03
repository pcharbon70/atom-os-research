---
title: "Compatibility manifest, BEAM loader, and verifier"
kind: note
created: "2026-09-03"
maturity: developing
tags:
  - beam
  - code-loading
  - compatibility
  - language-safety
  - virtual-machines
aliases:
  - "BEAM compatibility and loader component"
  - "BEAM verifier"
---

# Compatibility manifest, BEAM loader, and verifier

The best initial implementation is a **memory-safe, staged loader for one
machine-readable compatibility profile**, followed by a simple reference
interpreter. It should treat a BEAM file as hostile structured input, parse it
in a bounded private arena, distinguish container validity from instruction
validity and behavioral compatibility, lower only verified modules to an
immutable internal image, and publish that image in a separate atomic
transaction. A module with `-on_load` remains a candidate visible only to its
fresh initialization actor until that function returns `ok`; validation and
sealing alone do not make it current or callable.

The loader cannot truthfully promise a hostile-code sandbox merely because a
module is well formed. Current ERTS documentation and source treat loaded BEAM
code as trusted, and no complete formal semantics or proof covers the OTP 29
instruction set, BIFs, signals, code loading, and native surface. Atom OS should
therefore publish at least two admission profiles: a trusted compatibility
profile and a narrower restricted profile whose imports and dynamic features
are explicitly constrained.

## Question, scope, and operational standard

The question is:

> What exact evidence must a module provide before the runtime may treat its
> bytes as executable state under a declared BEAM/OTP profile?

This component owns:

- the compatibility-manifest schema and profile negotiation;
- bounded framing and parsing of supported BEAM container chunks;
- structural instruction, operand, control-flow, register, stack, and root-map
  validation;
- import, BIF, native, code-loading, and distribution-feature policy checks;
- lowering from external generic instructions to an immutable runtime IR;
- `-on_load` candidate isolation, fresh-actor execution, waiter handling, and
  rollback input to the publication component;
- module hashing, provenance, rejection evidence, and atomic publication input;
  and
- differential and negative conformance corpora.

It does not own compiler correctness, application type correctness, OTP
library policy, executable-page cache maintenance, or module retirement. Code
publication is completed with the execution component and kernel adapter.

An implementation meets the initial standard when:

1. Every accepted module names one exact profile; “BEAM compatible” alone is
   rejected as incomplete.
2. Every length, offset, count, allocation, decompression, and multiplication is
   checked against both input size and a staging quota.
3. Parsing cannot intern permanent atoms, install exports, create executable
   mappings, call BIFs, or mutate runtime-global indexes.
4. Every reachable instruction has valid operands, branch targets, register
   and stack state, live-root information, and an allowed import.
5. Rejection leaves the active code view and global runtime state unchanged.
6. Publication exposes either the complete old generation or the complete new
   generation. A candidate with `-on_load` becomes current only after the
   fresh initialization actor returns `ok`; failure unloads the candidate and
   preserves any prior current generation.
7. Supported and unsupported behaviors are executable test data, not prose
   alone.

## Compatibility is a vector, not a bit

A useful manifest must identify more than an OTP release:

```text
CompatibilityProfile {
  schema_version,
  reference_otp_release,
  reference_erts_release,
  compiler_profile,
  beam_container_profile,
  external_opcode_set,
  term_representation_profile,
  exception_and_stacktrace_profile,
  bifs_and_runtime_calls,
  signal_link_monitor_alias_priority_profile,
  timer_profile,
  code_loading_and_purge_profile,
  external_term_profile,
  distribution_flags,
  otp_library_set,
  native_extension_policy,
  resource_limits,
  conformance_suite_hashes,
}
```

The initial research baseline is OTP 29.0.6/ERTS 17.0.6 for current public
documentation. The archive's pinned source audit remains OTP 29.0.5 until the
newer tag is audited with the same rigor. That distinction must be present in
the manifest and test record; a patch-level documentation update is not
silently a source-level conformance claim.

Profiles are monotonic identifiers, not feature guesses. A module compiled for
a newer instruction or term profile is rejected even if its file suffix is
`.beam`. Current OTP policy promises a bounded forward loading window in some
directions and permits security/correctness changes, which is direct evidence
against a timeless binary ABI.

## Evidence, synthesis, and proposal

| Status | Claim |
| --- | --- |
| Current implementation evidence | The [OTP 29 managed-runtime documentation](../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md) distinguishes external generic instructions, loader-selected forms, public code semantics, and mutable internal implementation. |
| Current source evidence | The [pinned OTP source audit](../../30-sources/erlang-otp-team-2026-otp-29-source-tree.md) shows a mature but large native loader and generated operation machinery; it is a behavioral oracle, not a malicious-module sandbox. |
| Reported evidence | [Proof-carrying code](../../30-sources/necula-1997-proof-carrying-code.md) separates producer complexity from a smaller policy-specific checker. |
| Reported evidence | [Secure Virtual Architecture](../../30-sources/criswell-et-al-2007-secure-virtual-architecture.md) and [translation validation](../../30-sources/sewell-et-al-2013-translation-validation.md) support checking concrete low-level artifacts at a narrow trust boundary. |
| Synthesis | Structural validity, profile compatibility, authorization, and semantic correctness are distinct claims and need distinct evidence. |
| Project proposal | Implement an independent staged parser/verifier and reference interpreter before reusing or translating current ERTS-specific instruction representations. |
| Unverified | Completeness of the proposed validator, full OTP 29 behavioral coverage, restricted-profile soundness, and parser performance on the chosen implementation language. |

## Threat model and admission profiles

### Trusted OTP-compatible profile

This profile accepts modules from an authenticated deployment pipeline after
structural and compatibility validation. It can expose the broad BIF and code
surface needed by selected OTP libraries. Like current ERTS, it does not claim
that a deliberately malicious valid module cannot exploit a runtime bug or
resource path. Kernel containment limits the result to that runtime domain.

### Restricted untrusted profile

This stronger profile should begin much smaller:

- no in-process NIFs, linked drivers, raw code patching, or arbitrary on-load
  hooks;
- allowlisted BIF/import set with explicit cost and safe-point rules;
- bounded atoms, literals, code, stack, terms, mailboxes, timers, and tables;
- constrained external-term decoding and no implicit atom creation;
- no dynamic module loading or distribution unless separately authorized;
- verifier-known GC/safe-point state at every allocation or call boundary; and
- service access only through opaque runtime-broker handles.

Even this is a proposal, not a proven sandbox. The restricted profile becomes
a security boundary only after its runtime calls, interpreter, collector, and
resource enforcement are reviewed or verified as one system.

### Future certified profile

PCC, typed assembly, mailbox types, and capability-aware languages suggest a
future profile where a compiler supplies checkable facts about root maps,
immutability, unique transfer, mailbox protocol, or resource bounds. The
consumer must still validate the certificate against the exact profile and
concrete module hash. A compiler signature proves provenance, not the claimed
property.

## Staged loading pipeline

```text
UntrustedBytes
  -> FramedContainer
  -> ParsedPrivateModule
  -> StructurallyValidModule
  -> ProfileValidModule
  -> AuthorizedModule
  -> ImmutableRuntimeImage
  -> SealedGeneration
  -> PublishedGeneration
```

### 1. Framing

Verify the outer identifier and total bounded size before trusting any chunk.
Walk the EA-IFF-derived chunk directory with checked addition, alignment, and
non-overlap rules. Reject duplicate singleton chunks, unsupported compressed
forms, impossible padding, unknown mandatory chunks, and any declared region
outside the actual buffer.

Debug and documentation chunks are opaque and changeable. The compatibility
profile either ignores them under a size limit, preserves them as nonexecuting
metadata, or rejects them; the loader never treats their layout as stable
unless the profile says so.

### 2. Private parse

Build temporary symbols, atoms, literals, imports, exports, labels, and
instruction records in a staging arena charged to the load operation. Atom
names are validated and deduplicated in staging; permanent atom-table insertion
waits until the publication transaction has reserved and accepted the full
set.

Compressed literals and external terms use depth, node-count, integer-size,
binary-size, and output-ratio limits. A small input must not expand into an
unbounded staging allocation.

### 3. Instruction and control-flow validation

Decode only opcodes declared by the external profile. Verify operand tags and
ranges, label uniqueness, branch targets at instruction boundaries, function
entry structure, exception regions, stack-frame allocation/deallocation, and
fall-through rules.

A forward data-flow pass computes conservative initialized X/Y registers,
stack depth, catch/try state, and live roots at calls, allocations, BIFs, and
safe points. When the validator cannot establish a required invariant, it
rejects rather than relying on the interpreter to fail safely later.

### 4. Imports and effects

Resolve each import against a versioned runtime-call descriptor:

```text
RuntimeCallDescriptor {
  module, function, arity,
  profile_version,
  may_allocate,
  may_gc,
  may_yield,
  may_block,
  may_send,
  required_authority,
  cost_model,
  native_trust_class,
}
```

The descriptor is both a verifier fact and a scheduler/collector contract. A
call incorrectly marked nonallocating can invalidate root safety; a supposedly
bounded call that never yields can invalidate responsiveness. Therefore
descriptors are generated with implementation bindings and tested, not copied
manually into separate tables.

### 5. Immutable lowering

Lower external generic instructions into a simple, typed runtime IR. Resolve
labels and imports to generation-relative indexes, but retain source offsets
and original hashes for diagnostics. The IR is immutable after validation.
Interpreter dispatch may use decoded records or threaded indexes; neither form
is part of the public compatibility profile.

### 6. Publication

Reserve permanent atoms, code/literal memory, export entries, and generation
metadata before committing any. Construct a complete staging index and seal the
module image. A module without `-on_load` can then switch one active index or
root pointer atomically through the code-publication protocol.

A module with `-on_load` follows a gated transaction:

```text
SealedCandidate
  -> PendingOnLoad
  -> OnLoadRunning(fresh_actor, candidate_only)
  -> OnLoadReturnedOk -> PublishedCurrent
  -> OnLoadFailedOrRaised -> CandidateUnloaded
```

The initialization function runs in a freshly spawned actor that terminates
when the call returns. Candidate code is callable by that actor for the
initialization only; ordinary external callers cannot observe it as current.
If a prior generation is current, it remains callable throughout. On a first
load, external callers suspend in a bounded, accounted waiter set until the
initialization finishes. Only an exact `ok` result commits the candidate. Any
other result or exception unloads it; waiting callers then receive the selected
reference behavior and a previous current generation remains current.

Rollback restores runtime code state, not arbitrary external effects performed
by `-on_load`. The compatibility manifest therefore declares whether
initialization may load a trusted NIF or call services, which authority it
receives, and how timeout or runtime failure is reported. The restricted
untrusted profile can reject such effects or `-on_load` entirely.

Failure before the active-root switch releases staging. Failure after a normal
switch or successful on-load commit is a failure of a complete new generation.

## Validation invariants

- Every decoded byte belongs to exactly one bounded chunk or declared padding.
- Every control-flow edge targets a valid instruction boundary in the same
  module or an allowed import/export descriptor.
- Every read register and stack slot is initialized on every reaching path.
- Every possible GC or yield point has a complete and consistent root/state
  description.
- Literal graphs are acyclic or cyclic only where the term profile explicitly
  supports the encoded representation; no staging pointer enters the image.
- All atoms, imports, exports, funs, lambdas, and line metadata fit profile
  limits before global reservation.
- An immutable module image contains no raw kernel capability or ambient host
  pointer.
- Publication is all or nothing and generation-specific.
- A pending on-load candidate is unreachable to ordinary callers; its fresh
  actor cannot publish the candidate by any path other than an `ok` terminal.
- On-load failure leaves the previous current generation and export view
  unchanged, and first-load waiters cannot observe a partial candidate.

## Failure, security, and resource analysis

- **Parser memory safety:** implement in a memory-safe subset/language where
  practical, retain checked arithmetic, fuzz native decompression/crypto
  dependencies separately, and run loading in the unprivileged runtime domain.
- **Permanent-state exhaustion:** reserve atom/code/export budgets before
  publication; rejection cannot leave immortal atoms behind.
- **Algorithmic complexity:** cap nesting, labels, functions, imports, literal
  nodes, CFG edges, and validation iterations; charge work to the loader
  account and yield between bounded units.
- **TOCTOU:** hash and parse immutable input pages or copy into staging; the
  bytes validated are exactly the bytes lowered.
- **Confused profile:** include profile and module hashes in the immutable
  generation and crash evidence; never infer a profile from the loader binary
  alone.
- **Verifier bug:** differential negative corpora, independent structural
  checker in tests, and kernel containment reduce consequences but do not prove
  absence.
- **On-load side effects:** rollback can unload code but cannot undo an
  arbitrary NIF, service, or external effect; restrict authority, record the
  operation phase, and never describe failure as transactional external
  rollback.

## Alternatives and trade-offs

### Reuse the current ERTS loader

This maximizes near-term compatibility and is valuable as an oracle. It also
imports a large C trust base whose accepted-code model is not hostile. A staged
rehost may begin there, but the independent parser remains the target if
restricted code is a goal.

### Translate BEAM to WebAssembly

WebAssembly supplies strong structured validation precedent, but BEAM terms,
process-local GC, signals, exceptions, tail calls, BIFs, selective receive, and
hot code are not represented automatically. Translation can be a backend
experiment; it is not evidence that the source profile has been validated.

### Ahead-of-time native-only images

They reduce load-time translation but complicate target portability,
publication, stack maps, exception metadata, signatures, and compiler trust.
The platform requirement is compiled BEAM execution, so retaining the verified
portable image and interpreter is the safer first oracle.

## Implementation program

### Stage 0: executable profile

- Serialize the manifest schema canonically and version it.
- Extract external opcodes and runtime-call descriptors from the pinned OTP
  toolchain and current source audit.
- Classify every supported feature as normative compatibility, current ERTS
  implementation, Atom OS extension, or unsupported.

Exit condition: two runtimes can reject or accept a fixture using only the
profile and module, and every unsupported feature has a stable reason code.

### Stage 1: parser and structural verifier

- Implement bounded chunk parsing, literal decoding, instruction decoding, and
  CFG/state validation.
- Build a corpus from all modules shipped with the reference release plus
  representative Erlang, Elixir, and Gleam applications.
- Add coverage-guided mutation and hand-built boundary cases.

Exit condition: the valid corpus loads and negative inputs cannot crash,
overrun, allocate beyond quota, or mutate active code state.

### Stage 2: reference interpreter and differential oracle

- Execute the immutable IR with precise roots and explicit safe points.
- Differentially compare values, exceptions, stack traces, messages, timers,
  links, monitors, successful/failing `-on_load`, first-load caller suspension,
  code loading, and resource-limit outcomes.
- Retain minimized divergences as permanent fixtures.

Exit condition: the declared core profile passes a published conformance suite
against the pinned reference runtime.

### Stage 3: restricted profile and certificates

- Build a closed import set and effect/cost descriptors.
- Model and fuzz untrusted resource behavior.
- Experiment with certified root, immutability, or mailbox facts only after the
  ordinary validator is stable.

## Verification and measurements

- Fuzz chunk sizes, offsets, counts, compression, ETF terms, labels, operand
  tags, live counts, imports, stack frames, and exception regions.
- Force loader yield/failure at every bounded unit and confirm rollback.
- Load and replace modules while all schedulers call them; check complete old
  or new generation observation.
- Race successful, non-`ok`, exceptional, stalled, and native-loading
  `-on_load` functions with first load, replacement, callers, loader failure,
  and domain teardown; verify candidate isolation and prior-current rollback.
- Run GC at every verifier/interpreter allocation point and validate roots.
- Compare peak staging bytes, validation time, publication time, and rejection
  latency against module size and CFG complexity.
- Red-team the restricted profile with permanent-atom creation, huge integers,
  deep terms, self-modifying/native paths, nonyielding calls, and diagnostic
  exfiltration.

## Supported decisions and open questions

Evidence strongly supports versioned profiles, private staging, checked
framing, an immutable intermediate image, an explicit import boundary, and
atomic publication. It does not supply a complete BEAM formal semantics or
prove that the restricted profile is safe.

Open decisions include the implementation language, exact internal IR,
handling of optional/unknown chunks, certificate format, whether compiler
validators can provide independently checkable hints, and the boundary between
trusted deployment provenance and hostile-module policy. These decisions must
not delay the minimum structural verifier and interpreter.

## Connections

- [Managed actor runtime layer](../managed-actor-runtime-layer.md) — defines the
  broader compatibility target.
- [Runtime-domain bootstrap and kernel adapter](runtime-domain-bootstrap-and-kernel-adapter.md) —
  supplies immutable image and publication authority without exposing kernel
  handles.
- [Terms, private heaps, shared binaries, and tracing collection](terms-private-heaps-shared-binaries-and-tracing-collection.md) —
  consumes root and term invariants established at load time.
- [Code execution, safe points, and version publication](code-execution-safe-points-and-version-publication.md) —
  executes and optionally lowers the verified image.
- [Ordering, coherence, and code publication](../kernel-hardware-and-architecture-components/ordering-coherence-and-code-publication.md) —
  supplies the architecture-level visibility transaction for native code.

## Sources

- [OTP 29.0.6 managed-runtime documentation](../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md)
- [OTP 29 source tree](../../30-sources/erlang-otp-team-2026-otp-29-source-tree.md)
- [Proof-carrying code](../../30-sources/necula-1997-proof-carrying-code.md)
- [Secure Virtual Architecture](../../30-sources/criswell-et-al-2007-secure-virtual-architecture.md)
- [Translation validation for a verified OS kernel](../../30-sources/sewell-et-al-2013-translation-validation.md)
- [A brief introduction to BEAM](../../30-sources/hogberg-2020-brief-introduction-to-beam.md)
- [Mailbox types](../../30-sources/fowler-et-al-2023-mailbox-types.md)
