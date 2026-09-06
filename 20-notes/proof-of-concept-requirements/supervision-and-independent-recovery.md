---
title: "Supervision and independent recovery"
kind: note
created: "2026-09-06"
maturity: developing
tags:
  - operating-systems
  - proof-of-concept
  - requirements
aliases: []
---

# Supervision and independent recovery

Requirement R12, M2–M4. Demonstrate both actor-level supervision and recovery across a real protection boundary. A supervisor inside a crashed runtime cannot restart that runtime.

## Evidence and alternatives

[Herder and colleagues' MINIX work](../../30-sources/herder-et-al-2006-dependable-operating-system.md) demonstrates restricted user-space drivers and an external reincarnation service. Its limitations include failures of core services and loss of state; this is evidence for a topology, not proof of unlimited recovery.

The [OTP supervisor reference](../../30-sources/erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md) defines child specifications, restart strategies, shutdown and intensity behavior. Those semantics concern managed children within a working runtime, not recovery of the runtime's address space.

Use static launch and naming initially. Dynamic discovery, persistent registries and replacement of the recovery root can follow after the basic containment experiment.

## Proposed four-domain topology

Launch four Intel x86-64 ring-3 domains: CLI, outer recovery/control, project managed runtime and native test/I/O service. The ring-0 kernel enforces their memory and authority boundaries. Firmware and the host remain trusted dependencies outside this guest recovery claim.

Check a static launch graph for valid images, finite resource grants, permitted endpoints, dependency order and recovery ownership. Prevent cycles that require an unstarted child to initialize its own recovery authority.

The outer recovery service holds only the capabilities needed to launch, stop and inspect its configured children. Its CPU, memory, replacement capacity and fault delivery survive those children. The CLI can request a permitted named restart but cannot mint root authority or choose arbitrary executable memory.

The registry publishes a service identity and current generation after successful initialization. It is not merely a name-to-reused-slot table. A caller must distinguish replacement from continued execution of the original service.

## Recovery policy and observable outcomes

Separate four experiments:

1. A BEAM worker exits and its selected supervisor/restart policy replaces it inside the existing runtime.
2. The native service crashes or loops and outer recovery replaces its protection domain.
3. The whole runtime fails and outer recovery creates a fresh runtime generation.
4. The CLI fails and outer recovery restores the operator interface.

A volatile counter/job workload may reset state after replacement. Report this explicitly. A request accepted before failure may have an indeterminate effect; never translate every missing reply into “not executed.”

Use bounded restart intensity and backoff so a permanently bad image cannot consume all recovery CPU and slots. Define start timeout, readiness acknowledgement, shutdown deadline and escalation. A child that never cooperates must still be stoppable under the kernel lifecycle contract.

For M2–M4, failure of the kernel or outer recovery domain may trigger a documented machine reset. Do not advertise survival of every supervisor level. Later root takeover requires separate authority retirement and resource ownership protocols.

## Acceptance and remaining decisions

Exhaust a child while checking recovery's heartbeat and available reserves. Inject malformed fault reports, repeated crashes during startup, delayed readiness from an old generation and failures during cleanup. Verify that registry publication never exposes a half-initialized replacement.

Run 1,000 child restarts at fixed capacity and inspect reclaimed versus quarantined resources. A sequence of successful launches funded by monotonically consumed fresh memory fails the recovery criterion.

The CLI must demonstrate all four failure classes with real generation changes and bounded evidence. Trace who detected failure, who authorized stop/replacement, what state was lost and when the new service became callable.

The next artifact is the static authority/resource graph and recovery state machine. No restart topology or reserve isolation has yet been executed in this research session.

## Connections

[Lifecycle](domain-lifecycle-and-safe-reclamation.md), [accounting](resource-accounting-and-mailbox-overload.md), [CLI](serial-console-and-minimal-cli.md) and later [root survival](updates-and-recovery-root-survival.md) define the complete boundary.
