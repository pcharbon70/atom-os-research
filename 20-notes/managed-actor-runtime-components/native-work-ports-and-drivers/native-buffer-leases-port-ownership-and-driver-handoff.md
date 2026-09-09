---
title: "Native buffer leases, port ownership and driver handoff"
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

# Native buffer leases, port ownership and driver handoff

This study decomposes [Native work, ports and drivers](../native-work-ports-and-drivers.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

CleanQ specifies buffer ownership; port compatibility additionally requires actor-facing ordering and ownership mechanics. [1](../../../30-sources/haecki-et-al-2019-cleanq.md), [2](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Protected service domains are the default native boundary. Regular and dirty NIFs remain inside the runtime memory-failure domain.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own buffer lease generations, port owner identity, command sequence and service/device incarnation bindings. The device manager—not the dead driver—owns authoritative reset/quiescence evidence. Actor GC only releases its reference; it cannot prove a device stopped DMA.

### Admission, transitions and completion

Reserve command and buffer capacity before publication. Serialize port ownership changes with command routing and exit notifications. Transfer or copy buffers under an explicit permission protocol; release them after the original operation returns ownership and any required device quiescence completes.

### Failure and adversarial behavior

Actor death, service restart and device reset are different events. A port can be closed while residual requests remain charged. Shared reply metadata is hostile input: check length, offset and lease generation before constructing terms or granting access.

### Alternatives and unresolved tradeoffs

Copying messages to service-owned buffers is a safe comparison baseline. Shared leases reduce copies but increase retained memory, revocation and device-protection obligations. A universal generic native daemon can combine unrelated fault and authority domains.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Change port owner while ordered commands and an exit signal are pending.
- Crash a driver with an outstanding buffer and withhold quiescence evidence.
- Return a descriptor outside its granted region and verify rejection without term construction.

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

1. [CleanQ](../../../30-sources/haecki-et-al-2019-cleanq.md).
2. [OTP 29.0.6 managed-runtime documentation](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md).
