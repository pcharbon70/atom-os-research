---
title: "BEAM profile, loader, and conformance"
kind: note
created: "2026-09-06"
maturity: developing
tags:
  - operating-systems
  - proof-of-concept
  - requirements
aliases: []
---

# BEAM profile, loader, and conformance

Requirement R08, M3. “Runs compiled BEAM” must identify an actual compiler-produced workload, its complete dependency closure and the observable behaviors that the project interpreter implements.

## Evidence and compatibility trap

The [OTP 29.0.6 runtime documentation](../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md) distinguishes external BEAM instructions from runtime-specific internal operations and documents compatibility direction. Documentation alone is not a generated compatibility manifest.

A targeted reading of [OTP 29.0.6 gen.erl](../../30-sources/erlang-otp-team-2026-otp-29-0-6-generic-behaviour-call-protocol.md) finds that finite generic calls use aliases, monitors, cleanup and a final reply check; the local infinite-timeout path differs. Implementing only send/receive and a timer is insufficient for that finite-call path.

[Högberg's BEAM primer](../../30-sources/hogberg-2020-brief-introduction-to-beam.md) explains compiler/runtime conventions, registers and heap checks. It is an implementation tutorial, not the complete opcode or malformed-input specification.

## Proposed two-level profile

Keep a core execution profile separate from a selected OTP-library profile. Core fixtures should cover compiler-emitted terms, function calls, exceptions, copied send, selective receive, spawn/exit, links/monitors, timers and long-lived allocation with automatic tracing collection.

The OTP profile adds only explicitly selected modules and call paths. A project restart loop is OTP-inspired supervision, not proof that the upstream supervisor module runs unchanged. The [system-services reference](../../30-sources/erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md) includes shutdown, restart intensity and current behavior options that must enter the workload closure when exercised.

Pin the exact OTP release, compiler executable, compiler flags, upstream library modules, source tags and hashes. OTP 29.0.6 is a proposed oracle baseline, not a compiler installed or tested in this session. Align source inspection and generated fixtures rather than combining the archive's older 29.0.5 audit with newer behavior silently.

Generate a machine-readable manifest containing supported chunks, external opcode numbers/forms, imports and BIF arities, term forms/limits, exception classes, signal rules and library exports. Distinguish implemented, deliberately excluded and not yet tested. Record resource-induced differences separately from ordinary semantic mismatches.

Static import lists are necessary but insufficient: dynamic apply, callbacks, error paths, supervisor options and generated helper functions enlarge the executed closure. Trace representative success and failure paths on the oracle, inspect compiler output, and retain negative cases for unsupported dynamic targets.

## Loader boundary and failure behavior

The native runtime itself runs unprivileged, but its loader protects all actors sharing that runtime. Validate lengths, integer arithmetic, chunk layout, tables, instruction operands, register indices, control-flow destinations and references before publication. Declare accepted handling of unknown optional chunks rather than rejecting or trusting every unfamiliar chunk indiscriminately.

Stage atoms, code, literals and exports under a finite loading account. A malformed or unsupported module must not leave half-installed exports or uncharged global atoms. Define transactional rollback or a separately bounded retained-interning policy. Hash-based bundle identity does not replace parser validation.

Do not equate a syntactically valid module with hostile-code isolation: this profile trusts the interpreter's memory safety and does not establish an adversarial sandbox among actors sharing it.

## Acceptance and next exploration

Create the smallest compiler-produced counter/job workload first, then inspect its exact closure before setting implementation scope. Include deliberate unknown opcodes/imports, truncated chunks, oversized tables, invalid references and load failures after staged allocations.

Differential tests compare observable results and ordering constraints, not incidental scheduling order or raw process identifiers. Require every admitted case to pass on the hosted interpreter and then in the guest launched through the CLI. Record exclusions and intentional limit behavior.

The next artifact is a pinned compiler bundle and generated conformance manifest. No fixture corpus has yet been compiled or executed. AtomVM is excluded from both implementation and comparison gates.

## Connections

[Runtime adaptation](runtime-adapter-signals-and-native-services.md), [tracing GC](private-heaps-and-tracing-garbage-collection.md), and [integrated measurement](models-fault-injection-and-measurement.md) complete the M3 evidence boundary.
