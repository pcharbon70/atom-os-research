---
title: "Logical purge, fun invalidation and literal reclamation"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - actor-model
  - beam
  - managed-runtime
  - system-architecture
aliases: []
---

# Logical purge, fun invalidation and literal reclamation

This study decomposes [Code execution, safe points and version publication](../code-execution-safe-points-and-version-publication.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

The pinned parent audit separates direct old-code references from fun/literal retention; cheap shared literal access can require later global reclamation work. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md), [2](../../../30-sources/erlang-otp-team-2026-thread-progress-contracts.md), [3](../../../30-sources/larsson-2019-persistent-term.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Language execution and code-version visibility belong to the runtime; executable-page publication consumes the lower kernel's complete W^X and instruction-fetch contract.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own logical old-code eligibility, unloaded fun state, literal-copy queues and physically retired code generations. Direct execution references include instruction and continuation state. Indirect holders can retain storage without keeping the module logically callable.

### Admission, transitions and completion

Check direct old-code use for soft purge; hard-purge policy terminates direct users as required. Invalidate old fun invocation according to the profile, then retire execution visibility. Drain literal references by copying or releasing them and wait for all qualified native/software readers before freeing pages.

### Failure and adversarial behavior

Fun-only or literal-only holders must not by themselves fail soft purge or be killed by hard purge under the selected OTP baseline. Conversely, ignoring a saved native continuation can free executing code. Advancing a thread epoch cannot reclaim storage still leased to unmanaged native code.

### Alternatives and unresolved tradeoffs

Conservative physical retention improves safety but needs explicit memory limits and progress diagnostics. Treating every retained literal as a logical purge blocker is simpler but incompatible. Keep logical result and physical reclaim status as separate observables.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Compare direct-frame, fun-only and literal-only holders during soft and hard purge.
- Invoke an old local fun after successful purge and verify the reference exception.
- Delay a native reader while literal copies complete; retain only resources still legitimately referenced.

Record the exact profile, tested revision, schedule/input bounds and resource
observations before claiming this contract holds. A semantic pass does not
establish latency or corruption containment.

## Connections

- [Component service index](README.md) — sibling responsibilities and shared boundaries.
- [Verified instruction and root obligations](../compatibility-manifest-beam-loader-and-verifier/control-flow-root-and-operand-verifier.md) — a contract this service must compose with.
- [Retained literal ownership](../terms-private-heaps-shared-binaries-and-tracing-collection/shared-binary-literal-and-fragment-lifetimes.md) — a contract this service must compose with.
- [Open runtime inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — unresolved design and evidence.
- [Research session](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — source manifest and reading limitations.

## Sources

1. [OTP 29.0.6 managed-runtime documentation](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md).
2. [Thread Progress](../../../30-sources/erlang-otp-team-2026-thread-progress-contracts.md).
3. [Clever use of persistent_term](../../../30-sources/larsson-2019-persistent-term.md).
