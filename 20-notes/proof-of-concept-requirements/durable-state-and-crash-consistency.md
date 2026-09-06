---
title: "Durable state and crash consistency"
kind: note
created: "2026-09-06"
maturity: developing
tags:
  - capability-roadmap
  - proof-of-concept
  - requirements
aliases: []
---

# Durable state and crash consistency

Requirement R14, after M4. Recover useful service state across interruption, including interruption of recovery itself. This capability is not required for the initial volatile CLI/BEAM demonstration.

## Evidence, alternatives and a correction

[FSCQ](../../30-sources/chen-et-al-2015-fscq.md) uses crash-aware specifications over an asynchronous disk model and builds a synchronous transactional interface above it. Its proof assumptions and hosted implementation do not transfer automatically to a new storage driver.

[Pillai and colleagues](../../30-sources/pillai-et-al-2014-crash-consistent-applications.md) show that application persistence protocols depend on filesystem-specific ordering and atomicity behavior. Their crash-testing work motivates checking permitted persistence states rather than testing only clean shutdown.

This corrects the earlier [durable-state synthesis](../otp-like-system-services-components/durable-state-transactions-and-outcome-recovery.md), which described FSCQ as having a synchronous disk model. The distinction matters: an operation's synchronous interface can be implemented over an asynchronous substrate only through a specified protocol.

For a first durable service, compare a single-writer log with immutable checkpoints against integrating a general filesystem or transactional database. The log minimizes API breadth, but the project then owns recovery, checksums, allocation and format evolution. It is a proposed experiment, not an implemented storage system.

## Proposed backend and persistence contract

Select one concrete block or flash backend before defining “committed.” A virtual block device is a candidate, not a researched feature-negotiation or flush implementation in this session. Record device version, atomic write unit, alignment, volatile caches, completion meaning, ordering, flush/barrier behavior, discard and error reporting.

Separate process crash, guest reset, emulator termination, host crash and physical power loss. They exercise different persistence layers. Host filesystems and drive caches remain dependencies when the virtual disk is a host file.

A candidate log record contains format version, length, sequence/request identity, payload and integrity check. Specify whether checksums only detect corruption and how collisions or undetectable corruption affect the claim. Never treat a checksum as evidence that an acknowledged write reached stable media.

Define the durable commit point and acknowledge only after its required barrier. Checkpoints publish through a recoverable generation/selection protocol. Retain enough old state to recover if either the checkpoint or its selection metadata is torn or missing.

## Outcomes and recovery

Associate an application request identity with its committed result when retries need outcome recovery. A timeout after acceptance remains indeterminate until the durable outcome protocol resolves it. Exactly-once effects require appropriate application semantics and retention rules, not just a transport identifier.

Recovery must reject incomplete records safely, identify the last valid committed state and avoid replaying non-idempotent effects blindly. Define behavior for corruption that prevents distinguishing two candidate histories: stop for repair rather than inventing successful recovery.

Recovery writes are themselves crashable. Bound log scanning, checkpoint memory and recovery CPU; repeated failure must not force unbounded startup time or consume the outer recovery reserve.

## Acceptance and next exploration

First audit one backend's actual specification and negotiated features. Then build a small persistence simulator that enumerates allowed write loss, reordering and tearing around every barrier. Inject failure at every log, commit, checkpoint and recovery transition.

Retain a semantic oracle for acknowledged operations, possible unacknowledged effects and valid recovery states. Repeat against the actual virtual backend, clearly separating simulator coverage from device evidence.

The next artifact is the backend failure model plus an executable single-writer log/checkpoint protocol. No backend was selected or power-loss test run. This is the recommended next capability after M4 because it directly tests whether restart can restore useful state.

## Connections

[Independent recovery](supervision-and-independent-recovery.md) provides process replacement. [Updates](updates-and-recovery-root-survival.md) must preserve or migrate the durable format.
