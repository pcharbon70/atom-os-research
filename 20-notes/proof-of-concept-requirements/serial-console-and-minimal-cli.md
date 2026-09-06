---
title: "Serial console and minimal CLI"
kind: note
created: "2026-09-06"
maturity: developing
tags:
  - boot
  - proof-of-concept
  - requirements
aliases: []
---

# Serial console and minimal CLI

Requirement R04, first delivered at M1 and extended through M3. Boot into a native user-space command loop over a serial byte interface. Its usefulness is operational: it should expose the kernel and services as they become real, with bounded input and visible failure outcomes.

## Evidence and placement

The [xv6 console chapter](../../30-sources/cox-et-al-2026-xv6-risc-v-book.md) demonstrates buffered UART I/O and wakeups. Its sleep/wakeup discussion explains the lost-event race between testing a condition and becoming a waiter. Atom can reuse that reasoning while placing line editing and command parsing in user space.

[twilco's first-party UART walkthrough](../../30-sources/twilco-2019-risc-v-uart-driver.md) is useful evidence for inspecting a generated DTB and validating startup/linker assumptions. Its initial driver is intentionally incomplete and avoids interrupts. It is not an implementation of the CLI's idle-progress requirement.

These RISC-V examples supply queue/startup reasoning, not the active board's
UART discovery or register-address contract. The [T7500 profile](dell-precision-t7500-target-and-minimal-qemu-profile.md)
requires an explicitly configured virtual serial port and separately verified
physical serial/debug transport. Do not copy a generated DTB address into the
PC backend.

A polled early diagnostic console is reasonable scaffolding. For delivery, choose interrupt-driven buffered input, or explicitly bounded polling with scheduler-controlled waits. Neither a UART receive wait nor a saturated transmit buffer may keep the privileged kernel in an unbounded loop.

## Proposed command and byte protocol

The first CLI offers exactly `help`, `version` and `uptime`. `help` describes admitted syntax; `version` identifies executed kernel and CLI artifacts; `uptime` reports elapsed time in a declared unit through the kernel interface. The prompt is `atom>`. Shell pipelines, arbitrary executable paths and expression evaluation are unnecessary.

Adopt a proposed initial maximum of 256 input bytes excluding the terminator, an ASCII command vocabulary, a fixed argument count and a bounded output formatter. These are test-profile choices, not empirical capacity results. Define CR, LF and CRLF handling, backspace/delete at an empty line, tabs, NUL and other control bytes. Unknown commands and invalid arguments produce a bounded diagnostic and return to the prompt.

On overlong input, discard the remainder of that line through its delimiter and report one error. Do not interpret a truncated prefix as a destructive command. Reset parser state after disconnect or CLI replacement; stale bytes from an old command must not acquire authority in a new session.

At M2, `mem`, `ps` and `services` obtain versioned bounded snapshots. Distinguish kernel execution domains from BEAM actors so `ps` does not imply that every actor is a kernel thread. `restart <service>` accepts only configured service names and requests the independent recovery service to act. The CLI never receives arbitrary physical-memory or root-capability access.

At M3, `beam-profile` prints the implemented compatibility identifier and exclusions. `run <module>` chooses from the immutable boot bundle, checks its manifest, and starts an actual managed workload. A failed load returns an error without installing partial exports. Commands for unavailable mechanisms remain absent or explicitly unsupported.

## Scheduling, authority and observability

The kernel's byte transport validates user buffers and bounds work per call. Command parsing, editing and formatting belong to the CLI domain. Separate receive and transmit capacity; account both. A shared output service should preserve record boundaries or identify the writer so diagnostics do not masquerade as command responses.

Use level/state-based readiness: the waiter checks the queue and registers its wait atomically relative to event delivery, then rechecks after wakeup. Notifications can coalesce, so one notification cannot be treated as exactly one received byte. Timer progress and other domains must continue during idle input and output backpressure.

The first local development console trusts the host operator. That is not a human-login implementation. Remote exposure and credentials require the later [administration profile](authentication-and-administration-profile.md). Diagnostic output should not disclose capability secrets or arbitrary guest memory.

## Acceptance and remaining work

An unattended serial harness must submit all three M1 commands and verify both responses and return to the prompt. Include blank lines, CRLF, repeated backspace, maximum-length input, overflow followed by a valid command, malformed arguments, byte floods and transmit stalls. Use a separate heartbeat or timer counter to detect starvation.

Crash the CLI deliberately. M1 may follow a documented diagnostic halt/reset policy; M2 requires independent replacement and a new service generation. Exercise `restart` while the target has accepted a request and make the possible indeterminate result visible.

The next artifact is the byte/syscall contract plus a host parser harness and a real guest command session. No command implementation or serial experiment was produced in this research session.

## Connections

[Time and budgets](time-preemption-and-cpu-budgets.md) makes input waits responsive. [Independent recovery](supervision-and-independent-recovery.md) owns replacement. [Integrated validation](models-fault-injection-and-measurement.md) defines the retained transcript.
