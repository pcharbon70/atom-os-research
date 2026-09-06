---
title: "Models, fault injection, and measurement"
kind: note
created: "2026-09-06"
maturity: developing
tags:
  - operating-systems
  - proof-of-concept
  - requirements
aliases: []
---

# Models, fault injection, and measurement

Requirement R13, M0–M4. Turn the research into falsifiable contracts and retained evidence. Structural archive validation and published precedents do not establish that Atom boots or contains faults.

## Evidence and assurance limits

[Newcombe and colleagues](../../30-sources/newcombe-et-al-2015-aws-formal-methods.md) report finding design errors with formal models; they also distinguish design reasoning from implementation correctness. [TLC configuration documentation](../../30-sources/tlaplus-project-2026-tlc-model-configuration.md) explains invariant, temporal-property and state-space settings. State constraints can suppress behavior, so a passing bounded run must report its restrictions.

[QEMU record/replay and debugging documentation](../../30-sources/qemu-project-2026-debugging-and-record-replay.md) supplies useful execution-control mechanisms with configuration and device limitations. A deterministic replay configuration is not interchangeable with every normal emulator run.

Use small models, host-side fake backends and actual guest tests together. None substitutes for the others.

## Minimum model suite

Model the selected single-CPU, server-funded profile rather than the entire eventual kernel. Check:

- unauthorized or stale capabilities cannot admit new work, while previously admitted effects remain tracked;
- free, owned, reserved and quarantined resources conserve configured capacity;
- closing a domain disables new admission before cleanup begins;
- reply, cancellation, timeout and peer death select one terminal transport disposition;
- reuse requires the profile's execution, translation and reference quiescence;
- child exhaustion cannot consume or revoke recovery's reserve.

Declare object counts, identifier widths, queue capacities and scheduler/event assumptions. Include wraparound with deliberately tiny generations. Separate safety from liveness: eventual cleanup may require fairness, available recovery budget and a functioning timer. A fairness assumption cannot be used to wish away a permanently stuck device or disabled interrupt.

Retain model source, configuration, explored-state counts, properties, counterexamples and fixes. Replay counterexamples against a fake backend where possible. A finite-state pass is not an unbounded proof or a proof that C/Rust/assembly implements the transitions.

## Reproducible harness and stage gates

M0 retains exact toolchain/firmware/emulator identities, clean build/run commands, symbols, serial capture and a host watchdog with failing exit status. A second clean build must reproduce artifacts or identify permitted nondeterminism.

M1 submits help, version and uptime, validates the prompt and parser error cases, and checks timer progress while idle. M2 adds unauthorized mapping/capability/buffer tests, exhaustion, non-yielding domains, model traces and stale-handle tests. M3 runs the declared compiled-BEAM corpus and GC tests through the guest CLI, not only in a hosted interpreter.

M4 separately injects CLI, actor, native-service and whole-runtime failure. Test delayed/duplicate replies, timer cancellation, failed construction, cleanup interruption, fixed-capacity repeated restart and quota failures during fault reporting.

The [T7500-oriented Intel x86-64 fixture](dell-precision-t7500-target-and-minimal-qemu-profile.md) adopts one virtual CPU and 128 MiB RAM for initial tests. Workload sizes remain proposals: 128 actors, one million transient allocations and 1,000 child restarts. Smaller limits are essential for reaching failure paths. Freeze workload seeds and policy values before comparing builds.

## Measurement protocol

Predeclare p99 and maximum-observed targets for CLI response, heartbeat delay, timer delivery, GC, fault delivery and recovery. Identify each interval's endpoints and clock. Define treatment of timed-out or missing samples; excluding them from a percentile would hide failures.

Retain raw observations, sample counts, warmup policy, workload/live-set conditions, host configuration and emulator acceleration. Report CPU consumption and permitted kernel/interrupt overrun separately from wall-clock delay. Label maxima as maximum observed, not worst-case bounds.

Separate same-runtime actor progress from independent-domain progress. A responsive recovery heartbeat during a stalled GC is useful containment evidence, not a passing actor-latency test.

## Acceptance and next exploration

The next deliverable is an executable gate manifest connecting every requirement to a test, fixture, threshold and evidence path. Start the serial harness alongside boot bring-up; create lifecycle models before optimizing transport.

This session performed literature and archive analysis only. No model checker, guest kernel, conformance corpus, fault campaign or timing benchmark was executed.

## Connections

The [requirements index](README.md) maps each readiness requirement to its report. [Build](freestanding-build-and-static-images.md), [time](time-preemption-and-cpu-budgets.md) and [recovery](supervision-and-independent-recovery.md) define the first integration gates.
