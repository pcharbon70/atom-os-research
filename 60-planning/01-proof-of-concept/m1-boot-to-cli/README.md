---
title: "M1 — Boot to CLI"
kind: map
created: "2026-09-08"
tags:
  - archive-navigation
  - boot
  - cli
  - directory-index
  - implementation-planning
  - m1
  - proof-of-concept
aliases:
  - "M1 milestone definition"
---

# M1 — Boot to CLI

## Purpose

M1 delivers the first usable Atom OS image: boot it and reach an interactive
`atom>` prompt implemented by a native user-mode program. `help`, `version`,
and `uptime` must operate through a real kernel interface, with bounded input
and continuing timer progress. A printed banner, a privileged monitor, or a
program hosted inside another guest OS is not this milestone.

This is the first delivery, not the completed proof of concept. M1 establishes
the boot, memory, privilege, console, and time foundation that
[M2](../m2-protected-service-nucleus/README.md) extends into independently
recoverable services. Compiled BEAM and tracing GC arrive in
[M3](../m3-project-beam-runtime/README.md), then the combined system is evaluated
in [M4](../m4-integrated-recovery-and-resource-campaign/README.md).

## What belongs here

M1 includes the actual kernel entry path, conservative page initialization,
static image admission, kernel/user transitions, exception handling, minimal
console/time syscalls, serial transport, and native CLI. The initial QEMU
fixture stays one Intel x86-64 CPU, 128 MiB, serial-only, and without a writable
data disk or network interface.

The CLI is not a POSIX shell, general REPL, package manager, or desktop. It
does not promise pipelines, scripts, arbitrary file execution, human login,
BEAM execution, multiple independently recoverable services, or durable state.
Keep commands for those unavailable mechanisms absent rather than returning
simulated results. A debug-only privileged monitor must remain distinct from
the delivered interface.

## Planning and delivery state

This milestone now has a draft phased implementation plan. The detailed outcome,
artifact IDs and acceptance criteria below remain authoritative. All tasks are
unchecked, implementation has not started, and every acceptance case is not run.
Open decisions must be resolved before dependent execution; writing or reviewing
a plan neither closes a delivery gate nor authorizes implementation or publication.

## Authoritative inputs

The following inputs bind the delivery to the existing research and predecessor:

- [M0 — Boot inputs](../m0-boot-inputs/README.md) — the reproducible fixture, build, handoff, image, interface, and test-harness contract.
- [Readiness assessment](../../../20-notes/proof-of-concept-research-readiness.md) — first-delivery criteria and the difference between M1 and the completed PoC.
- [Target/handoff, R01](../../../20-notes/proof-of-concept-requirements/target-firmware-and-boot-handoff.md) and [native images, R02](../../../20-notes/proof-of-concept-requirements/freestanding-build-and-static-images.md) — validated entry and static image installation.
- [Privilege/memory, R03](../../../20-notes/proof-of-concept-requirements/privilege-entry-memory-and-user-return.md) — kernel-owned context, user-buffer checks, and negative protection tests.
- [Serial CLI, R04](../../../20-notes/proof-of-concept-requirements/serial-console-and-minimal-cli.md) and [time, R05](../../../20-notes/proof-of-concept-requirements/time-preemption-and-cpu-budgets.md) — bounded byte transport, parser behavior, and timer progress.
- [Measurement, R13](../../../20-notes/proof-of-concept-requirements/models-fault-injection-and-measurement.md) — guest evidence and unattended acceptance.
- [T7500 target profile](../../../20-notes/proof-of-concept-requirements/dell-precision-t7500-target-and-minimal-qemu-profile.md), [parent stream](../README.md), and [planning convention](../../README.md) — platform scope and planning/evidence rules.

## Entry decisions and dependencies

Accepted M0 virtual/build inputs are the basis of M1, not optional background
reading. Reproduce their checks and bind the exact revision used. Changes to
the loader, compiler, image format, entry mechanism, or fixture require the
corresponding M0 record and tests to change together. Provisional bring-up may
explore an open choice, but cannot be labelled accepted M1 evidence.

Before declaring this delivery, resolve console framing/capacity, overflow
behavior, enabled CPU register state, exception-stack ownership, validated
return, clock source/units, interrupt routing, and bounded input/output waits.
The CLI study proposes a 256-byte input limit; that remains a proposed profile
value until selected and tested. No new CPU feature, syscall instruction,
timer mode, or numeric response bound is selected by this definition.

Independent domain budgets, general object lifecycle, and service replacement
belong to M2. Their absence does not excuse disabled interrupts or an unbounded
kernel loop while M1 waits for serial input. Define a finite diagnostic
halt/reset policy for initial CLI faults rather than inventing a supervisor.

## What the running system must do

The boot path establishes the selected x86 entry environment, validates the
handoff, reserves firmware and image memory, initializes kernel-owned
descriptors/stacks/exception state, and constructs a protected native image.
The kernel admits the CLI only after lengths, destinations, permissions, entry
point, and enabled-state policy pass validation. Unknown or conflicting memory
must never become allocator capacity by guesswork.

The CLI runs at ring 3, and kernel mechanisms run at ring 0. CLI code, data,
and stack have deliberate permissions and bounded memory. Kernel memory, page
tables, firmware ranges, and device access are not made user-accessible merely
to simplify loading. Guard and zero-fill rules must be demonstrated.

Entry preserves every enabled state component under the chosen policy. User
return validates its context, address-space identity, PC, stack, and permitted
privilege/interrupt state. Every exposed syscall checks its operation, length,
direction, and complete user-buffer range before acting. A malformed request
must not partially change privileged state.

The command loop owns line editing, parsing, dispatch, and response formatting
in user space. It exposes exactly the first-delivery command set:

| Command | Required visible result |
| --- | --- |
| `help` | Actual implemented commands and accepted syntax, followed by a new prompt. |
| `version` | Identifiers bound to the executed kernel, CLI, and target profile rather than a fabricated version string. |
| `uptime` | Monotonic elapsed time in a declared unit, read through the kernel interface and advancing across idle periods. |

Blank lines, invalid commands/arguments, CR/LF/CRLF, editing at an empty line,
control bytes, and overlong lines need defined outcomes. Overflow must not
execute a truncated command prefix; discard/resynchronize according to the
selected byte contract and accept a subsequent valid line. Input and output
storage, formatting, and work per privileged entry remain bounded.

## Required artifacts

These deliver the coverage table's boot image, serial path, trap/MMU/timer
tests, and first command environment. M0 specifies their inputs; M1 supplies
working guest implementations and observed behavior.

| ID | Artifact | Required result |
| --- | --- | --- |
| M1-A01 | Kernel boot and normalized memory snapshot | An identifiable Atom kernel reaches controlled ring-0 execution with validated reservations, features, stack/exception state, and bounded boot failure diagnostics. |
| M1-A02 | Native image admission and protected memory | A bounded loader plus page-accounting/mapping implementation installs the selected native subset, zeroes user memory, applies permissions, and rejects malformed images without leaving runnable partial state. |
| M1-A03 | Entry, exception, and console/time ABI implementation | Kernel-owned contexts, validated ring-3 return, enabled-register-state handling, range-safe copies, and defined bad-operation/fault results. |
| M1-A04 | Serial and elapsed-time mechanisms | Bounded byte transport, specified readiness/waits/backpressure, monotonic time reads, and timer delivery that continues while input is idle or output is saturated. |
| M1-A05 | Native CLI image | The real user-mode prompt, three commands, bounded parser/editor/formatter, defined errors, and no simulated later services. |
| M1-A06 | Reproducible delivery and evidence bundle | Bootable image/bundle, associated symbols and manifests, executable M0 harness adapted to the real guest, transcripts, privilege traces, negative-test fixtures/results, and clean-build comparisons. |

## Integration acceptance

These cases run against the actual guest image, using M0's finite host watchdog
and declared fixture. Hosted parser tests are useful supporting evidence but
cannot replace the guest tests. Where only one user domain exists, a negative
test image can replace the CLI for a separate boot; tests need not introduce
M2's complete service graph prematurely.

| ID | Acceptance case | Artifacts | Passing evidence |
| --- | --- | --- | --- |
| M1-T01 | Clean boot and real privilege transition | A01–A03, A05, A06 | Rebuilt image reaches `atom>`; a debugger/trace establishes CLI CPL 3 and handler CPL 0 with the expected address space. |
| M1-T02 | Interactive command round trip | A03–A06 | Harness submits all three commands, checks actual build/time results and syntax, and observes return to the prompt after each command. |
| M1-T03 | Parser bounds and resynchronization | A04–A06 | Blank/control/editing inputs, invalid arguments, exact-limit and overlong lines produce specified bounded results; a subsequent valid command works with no memory growth or corruption beyond the declared bounds. |
| M1-T04 | Idle and backpressure progress | A03–A06 | Timer observations continue through input waits, serial floods, and transmit stalls; no lost-wakeup state or indefinite interrupt-disabled kernel loop appears. Host timeouts and guest-time observations are reported separately. |
| M1-T05 | Protection and invalid user requests | A02, A03, A06 | Test images attempt kernel access, privileged operations, text writes/data execution, stack overflow, invalid syscall arguments, and cross-page buffers. Each is rejected or follows the declared fault policy without altering protected canaries. |
| M1-T06 | Image admission and context integrity | A01–A03, A06 | Invalid entry/segments, truncated or unsupported images, and unsafe return state cannot publish executable contexts. Initial data/BSS and stack alignment are correct; interrupted enabled registers are preserved without exposing privileged state. |
| M1-T07 | CLI fault and harness failure handling | A03–A06 | Deliberate CLI faults leave bounded diagnostics and reach the selected initial halt/reset result. Boot failures and hangs fail the harness; an unexpected reboot loop cannot look like successful recovery. |
| M1-T08 | Repeated clean delivery | A01–A06 | Independent clean builds reproduce the executed identities or document allowed nondeterminism; unattended runs reproduce command and negative-test outcomes with retained artifacts. |

Each test records its fixture, expected result, actual result, output artifact,
and any limitation. A timer interrupt observed once is not evidence of budget
isolation; that becomes an M2 requirement. Conversely, future M2 work cannot
be used to waive M1's existing timer, protection, and bounded-wait obligations.

## Physical T7500 follow-on

After virtual acceptance and installed-unit/boot-media qualification, repeat
the single-CPU CLI checks on the T7500 with verified serial/debug access and
the selected physical firmware path. Keep additional CPUs unstarted or safely
parked; do not require their physical removal or SMP merely to test the CLI.
Record actual device/firmware differences instead of treating q35 as a board
replica. This checkpoint can follow M1 before M2–M4 finish or SMP begins.

Virtual M1 evidence supports the virtual fixture only. Keep physical execution
as a separate qualification result and leave it open until performed; a claim
of working on the T7500 requires its own evidence. Nothing in this definition
authorizes overwriting a disk, flashing firmware, or changing persistent BIOS
settings. Resolve the precise test media and permissions before those actions.

## Evidence and milestone exit

M1 exits for its declared fixture only when the real kernel/user-mode CLI and
all required acceptance cases pass with reproducible evidence. A missing
privilege trace, fake command result, unbounded console wait, unsafe image
publication, or untested protection failure is a reason to stop or revise,
not a cosmetic limitation. Required failures remain failures even if the
prompt is visible.

Keep run records in dated [journal evidence](../../../50-journal/README.md),
with exact artifact identities in [assets](../../../assets/README.md) or the
selected implementation repository, linked to the acceptance case IDs.

The M2 handoff is an immutable build/run bundle, tested entry/memory/console/
time interfaces, parser and bad-image fixtures, raw traces, and a list of
remaining limitations. M2 replaces the initial halt/reset-only child-failure
policy with independent CLI/service recovery and adds real inspection/control
commands. M1 completion must not be reported as compiled-BEAM capability or
overall PoC completion.

## Ordered phases

4 phases separate independently verifiable outcomes; their section/task/sub-task
counts follow the work rather than a quota. All are draft/not started, with no
execution evidence. Review dependencies and resolve decisions before execution.

| Phase | Integrated outcome | Entry dependency | State / evidence |
| --- | --- | --- | --- |
| [Phase 1 — Kernel entry and memory foundation](phase-01-kernel-entry-and-memory-foundation.md) | Bring up the real ring-0 kernel and validated boot-memory state on the M0 fixture, with bounded diagnostics and no host OS inside the guest. | m0-p03-handoff | Draft; not started; tests not run |
| [Phase 2 — Protected images and user transitions](phase-02-protected-images-and-user-transitions.md) | Install validated native images and demonstrate safe ring-3 execution, traps, and return with kernel-owned context and protected memory. | m1-p01-handoff | Draft; not started; tests not run |
| [Phase 3 — Serial CLI and virtual acceptance](phase-03-serial-cli-and-virtual-acceptance.md) | Deliver the native user-mode atom prompt with real commands, bounded serial behavior, advancing time, and the complete virtual M1 evidence bundle. | m1-p02-handoff | Draft; not started; tests not run |
| [Phase 4 — Physical T7500 qualification](phase-04-physical-t7500-qualification.md) | Repeat the single-CPU CLI qualification on the observed T7500 without confusing emulator evidence with physical support. | m1-p03-handoff | Draft; not started; tests not run |

Work within each phase follows its task dependencies. The serial order provides
a conservative baseline, not authorization for parallel agents. Independent
experiments may be proposed separately; their results cannot bypass a gate.

Phase 3 closes virtual M1 when all required virtual cases pass. Phase 4 is the
separate physical qualification branch and may run alongside later virtual
milestones after its own safety prerequisites. An open physical gate is not a
physical pass and is not an SMP prerequisite for M2.

## Decision register

The entry choices above remain open. Each row names its resolution task,
evaluation criteria and blocked work; responsible individuals are unassigned.
M0-D01 owns the initial implementation repository and toolchain selection.

| Decision ID | Choice and criteria | Resolution task and phase | Responsible role | Blocks | State |
| --- | --- | --- | --- | --- | --- |
| M1-D01 | Reconcile M0 entry/feature/register policies with the implementation; assign exception-stack and reserved-memory ownership before admitting any user image. | [m1-p01-decisions](phase-01-kernel-entry-and-memory-foundation.md) | Unassigned implementer/reviewer; assign before dependent execution | Remaining Phase 1 work and its dependent gates | Open; no decision evidence |
| M1-D02 | Freeze image permissions, state preservation, syscall buffer rules, and return validation against M0; restricted FP/SIMD remains explicit rather than full ABI support. | [m1-p02-decisions](phase-02-protected-images-and-user-transitions.md) | Unassigned implementer/reviewer; assign before dependent execution | Remaining Phase 2 work and its dependent gates | Open; no decision evidence |
| M1-D03 | Select framing, line limit, overflow resynchronization, timer source/units, interrupts/waits, and finite output behavior before acceptance; the proposed 256-byte limit is not automatically selected. | [m1-p03-decisions](phase-03-serial-cli-and-virtual-acceptance.md) | Unassigned implementer/reviewer; assign before dependent execution | Remaining Phase 3 work and its dependent gates | Open; no decision evidence |
| M1-D04 | Select safe boot media, actual firmware path, serial/debug transport, test boundaries, and explicit permission for any media or persistent-device writes. | [m1-p04-decisions](phase-04-physical-t7500-qualification.md) | Unassigned implementer/reviewer; assign before dependent execution | Remaining Phase 4 work and its dependent gates | Open; no decision evidence |

## Gate-to-phase and artifact mapping

Rows map contributions, not automatic acceptance. The phase task tables give
stable implementation IDs; the integration task exercises the mapped cases
and the handoff task records evidence. Shared cases retain their full definition
above and close only after all required environments and dependent portions pass.

| Phase gate | Artifact contributions | Acceptance coverage | Owning tasks | Entry dependency | Evidence / state |
| --- | --- | --- | --- | --- | --- |
| [M1-P01](phase-01-kernel-entry-and-memory-foundation.md) | M1-A01, M1-A06 | M1-T06, M1-T07, M1-T08 | m1-p01-decisions, m1-p01-memory; m1-p01-integration; m1-p01-handoff | m0-p03-handoff | Not run; evidence absent |
| [M1-P02](phase-02-protected-images-and-user-transitions.md) | M1-A02, M1-A03, M1-A06 | M1-T01, M1-T05, M1-T06, M1-T07 | m1-p02-decisions, m1-p02-images, m1-p02-transitions; m1-p02-integration; m1-p02-handoff | m1-p01-handoff | Not run; evidence absent |
| [M1-P03](phase-03-serial-cli-and-virtual-acceptance.md) | M1-A03, M1-A04, M1-A05, M1-A06 | M1-T01, M1-T02, M1-T03, M1-T04, M1-T05, M1-T06, M1-T07, M1-T08 | m1-p03-decisions, m1-p03-io, m1-p03-cli; m1-p03-integration; m1-p03-handoff | m1-p02-handoff | Not run; evidence absent |
| [M1-P04](phase-04-physical-t7500-qualification.md) | M1-A01, M1-A04, M1-A06 | M1-T01, M1-T02, M1-T03, M1-T04, M1-T05, M1-T06, M1-T07, M1-T08 | m1-p04-decisions, m1-p04-physical; m1-p04-integration; m1-p04-handoff | m1-p03-handoff | Not run; evidence absent |

The final virtual phase (Phase 3) reruns all M1 acceptance cases for milestone closure.
Earlier contract, fixture, model or hosted results remain partial where guest
integration is required. Scope exclusions and physical obligations in this
definition are unchanged. An acceptance reviewer must retain failure history,
record the accepted tested revision, and reopen gates on incompatible input
changes, missing required evidence or a violated invariant.

## Index

### Subdirectories

- None yet.

### Documents

- [Phase 1 — Kernel entry and memory foundation](phase-01-kernel-entry-and-memory-foundation.md) — Bring up the real ring-0 kernel and validated boot-memory state on the M0 fixture, with bounded diagnostics and no host OS inside the guest.
- [Phase 2 — Protected images and user transitions](phase-02-protected-images-and-user-transitions.md) — Install validated native images and demonstrate safe ring-3 execution, traps, and return with kernel-owned context and protected memory.
- [Phase 3 — Serial CLI and virtual acceptance](phase-03-serial-cli-and-virtual-acceptance.md) — Deliver the native user-mode atom prompt with real commands, bounded serial behavior, advancing time, and the complete virtual M1 evidence bundle.
- [Phase 4 — Physical T7500 qualification](phase-04-physical-t7500-qualification.md) — Repeat the single-CPU CLI qualification on the observed T7500 without confusing emulator evidence with physical support.

## Maintaining this index

Add every phase/supporting child to the inventory as it is written. Keep
artifact/test identities, M0 compatibility, M2 handoff, and virtual versus
physical qualification states consistent with the parent stream and governing
inquiry. Link observed evidence without rewriting an unrun test as a success.
