---
title: "Networking and remote actor boundaries"
kind: note
created: "2026-09-06"
maturity: developing
tags:
  - capability-roadmap
  - proof-of-concept
  - requirements
aliases: []
---

# Networking and remote actor boundaries

Requirement R15, after M4. Add bounded communication between independently failing machines without confusing transport reliability with application outcome recovery.

## Evidence and alternatives

[QUIC's transport specification](../../30-sources/iyengar-thomson-2021-quic.md) defines stream/connection flow control and other resource limits. These do not bound all implementation buffers, cryptographic work or application queues, nor establish durable execution of a received request.

The [OTP signal reference](../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md) supplies relevant actor ordering semantics, but implementing a custom remote request service does not establish Erlang distribution-protocol compatibility.

Compare a reusable TCP/IP stack with a separately qualified secure channel against a QUIC implementation. TCP may reduce initial protocol breadth if a suitable stack is available; QUIC offers independent streams but adds substantial cryptographic, timer and connection-state machinery. No library or NIC has been selected or audited here. A first decision needs a dependency and licensing review of concrete candidates.

## Proposed integration boundary

Start with one NIC, one queue pair and finite copied packet buffers in an isolated native network service. A virtual NIC is a possible first device, but its descriptor, interrupt and DMA contract must be audited before granting it access. Do not inherit a host networking stack inside the guest without labeling that dependency.

Inventory packet allocation, timers, entropy, cryptography, checksum offloads, synchronization, threading, filesystem/certificate access and platform calls. Identify what runs in the driver, protocol service, runtime and kernel. Bound parser depth and work per dispatch before considering throughput optimization.

Maintain separate limits for RX/TX descriptors, packet buffers, connections, streams, handshake state, retransmission, timers, fragment/reassembly state, cryptographic input and application mailboxes. Apply admission before allocating from shared pools. A peer that never consumes data must not exhaust local recovery resources.

The initial protocol can be a small versioned request/reply service carrying explicit actor/service identities. Interoperability with upstream Erlang distribution is a separate compatibility profile and corpus; do not infer it from local BEAM execution.

## Identity, ordering and failure outcomes

Bind every remote reference to a peer identity, session incarnation and service generation. Authentication and replay resistance need qualified keys and entropy; a changing connection number alone is not a trusted identity.

State which messages preserve order and what reconnect means. Never redirect a delayed reply from an old session to a newly registered service by name alone. After connection loss, operations accepted by the peer may have taken effect.

Use request identities and an application outcome protocol when retrying effects. Without durable outcome retention, advertise at-most-one local admission or an indeterminate result as appropriate, not global exactly-once execution.

Do not introduce membership, leader election or consensus before the underlying peer/session, failure-detection and resource contracts are tested. A timeout is evidence of missing timely communication, not proof that the other machine is dead.

## Acceptance and next exploration

Select a concrete NIC and stack using an import/ownership matrix. Build two-node tests for loss, duplication, delay, reconnect, queue saturation, malformed lengths, handshake floods and one-sided restart. Include partitions during an accepted counter/job operation.

Verify interoperability against the selected protocol implementation, not only two copies of the same code. Retain packet traces with secrets removed, queue high-water marks and timed-out operations.

The next artifact is a stack/NIC selection record with a finite resource budget and session protocol. No remote actor, network driver or secure-channel test was run during this session.

## Connections

[DMA isolation](dma-driver-isolation-and-recovery.md), [authentication](authentication-and-administration-profile.md) and [durable outcomes](durable-state-and-crash-consistency.md) are dependencies of stronger network claims.
