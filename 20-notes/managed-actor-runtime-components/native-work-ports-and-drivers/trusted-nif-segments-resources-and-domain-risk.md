---
title: "Trusted NIF segments, resources and domain risk"
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

# Trusted NIF segments, resources and domain risk

This study decomposes [Native work, ports and drivers](../native-work-ports-and-drivers.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

NIF scheduling class is per function/segment; dirty scheduling changes availability, not memory containment. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md), [2](../../../30-sources/erlang-otp-team-2026-yielding-c-code-contracts.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Protected service domains are the default native boundary. Regular and dirty NIFs remain inside the runtime memory-failure domain.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own an admitted module manifest covering each name/arity entry, permitted regular/dirty CPU/dirty I/O transitions, callbacks, resource types and upgrade/destructor behavior. Every admitted native function belongs to the runtime trusted computing base.

### Admission, transitions and completion

Validate each initial ErlNifFunc class and each scheduled continuation class. Root and charge resource wrappers, bound worker pools and retain module/resource lifetime through callbacks and destructors. A killed actor can stop managed execution while dirty work continues to hold its native or heap-related state.

### Failure and adversarial behavior

A wild pointer compromises all actors in the runtime regardless of dirty class. A module-wide safe/dirty label misses functions and dynamic transitions. An arbitrary scheduled name/arity is not necessarily an exported entry, so audit the continuation graph rather than only exported symbols.

### Alternatives and unresolved tradeoffs

Isolated services are preferred where their protocol can supply the required behavior. A trusted compatibility lane may be justified for specific libraries, but requires an explicit deployment risk decision and cannot advertise per-actor native fault isolation.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Alternate permitted CPU/I/O segments and reject unauthorized class transitions.
- Kill an actor during dirty work and delay resource destruction safely.
- Inject a native memory fault in a controlled test model and require runtime-domain—not actor-only—failure classification.

Record the exact profile, tested revision, schedule/input bounds and resource
observations before claiming this contract holds. A semantic pass does not
establish latency or corruption containment.

## Connections

- [Component service index](README.md) — sibling responsibilities and shared boundaries.
- [I/O ownership and terminal completion](../timers-events-and-asynchronous-io-integration/asynchronous-operation-records-and-buffer-completion.md) — a contract this service must compose with.
- [Failure projection without unsafe retry](../failure-translation-and-the-otp-boundary/service-loss-uncertainty-and-supervisor-handoff.md) — a contract this service must compose with.
- [Open runtime inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — unresolved design and evidence.
- [Research session](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — source manifest and reading limitations.

## Sources

1. [OTP 29.0.6 managed-runtime documentation](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md).
2. [Automatic Yielding of C Code](../../../30-sources/erlang-otp-team-2026-yielding-c-code-contracts.md).
