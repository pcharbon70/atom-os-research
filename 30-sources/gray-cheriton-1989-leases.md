---
title: "Leases: An efficient fault-tolerant mechanism for distributed file cache consistency"
kind: source
created: "2026-09-04"
authors:
  - "Cary G. Gray"
  - "David R. Cheriton"
published: 1989
citation_key: "gray-cheriton-1989-leases"
container: "Proceedings of the Twelfth ACM Symposium on Operating Systems Principles"
edition: "SOSP '89, pages 202–210"
isbn: "0-89791-338-8"
doi: "10.1145/74850.74870"
url: "https://doi.org/10.1145/74850.74870"
accessed: "2026-09-04"
tags:
  - cache-consistency
  - distributed-systems
  - leases
  - time
aliases:
  - "Leases paper"
---

# Leases: An efficient fault-tolerant mechanism for distributed file cache consistency

## Reference

Cary G. Gray and David R. Cheriton. “[Leases: An Efficient Fault-Tolerant
Mechanism for Distributed File Cache
Consistency](https://www.andrew.cmu.edu/course/15-440/assets/READINGS/gray1989.pdf).”
*Proceedings of the Twelfth ACM Symposium on Operating Systems Principles
(SOSP '89)*, pages 202–210, 1989. DOI
[10.1145/74850.74870](https://doi.org/10.1145/74850.74870).

## Research question or contribution

The paper asks how a distributed cache can serve repeated reads without
contacting the primary on every access while preserving single-copy-like
consistency through client crashes, server crashes, lost messages, and network
partitions. It introduces bounded-duration leases: the server promises not to
change data during the holder's valid interval without first obtaining the
holder's approval.

## Method

The authors specify the lease protocol and failure assumptions, derive an
analytic model for server load and consistency delay, and apply a trace-driven
simulation using file-access characteristics from the V system. They compare
lease terms and discuss implementation optimizations. The measurements concern
file-cache reads and writes, not service leadership or external devices.

## Findings

- A lease is a time-bounded contract, not a heartbeat observation. The holder
  may use cached data while its local validity interval remains open; the
  server delays a conflicting change until holders approve or their leases are
  safely expired.
- Message loss, partitions, and crash-stop client or server failures need not
  violate the paper's consistency result when server writes persist across
  restart and its timing assumptions hold. An unreachable client delays a
  conflicting write only until the remaining lease bound elapses.
- Safety depends on clocks. A server clock that advances too quickly or a
  client clock that advances too slowly can create overlapping beliefs about
  validity. The minimum requirement is known bounded drift, with terms and
  communication delay accounted conservatively.
- Short leases can approach the load benefit of long leases for read-heavy
  workloads while reducing delay after client failure, server recovery, or
  false sharing. The reported V-derived example found a ten-second term within
  five percent of the infinite-term server load under that workload model.
- Write-heavy or broadly shared data may merit a zero-duration lease. Lease
  duration is therefore a workload and failure-bound decision, not one global
  constant.

## Relevance

The paper provides the minimum discipline for Atom OS cached registry entries,
configuration snapshots, credentials, and coordination leases: name the
grantor, resource, holder, generation, issue evidence, holder deadline, and
grantor deadline; state the drift and scheduling-pause bounds; and enter a
jeopardy state early enough to stop new effects before uncertainty can overlap
a successor.

Its result must not be overextended. A coordination lease can bound when a
holder may act, but an old holder or delayed message can still reach a storage,
device, network, or update sink. Exclusive effects therefore also carry a
monotonically increasing fence, and every sink durably rejects generations at
or below its accepted high-water value. Short validity improves recovery but
does not replace sink enforcement.

## Limits

The model excludes Byzantine failures, including dangerous clock behavior,
and assumes persistent server state. Its synchronization and delay assumptions
must be re-established for target Atom OS timekeeping, scheduler pauses, sleep
states, and network paths. Trace-driven simulation of V file access is not a
service-ownership benchmark. The paper does not address quorum
reconfiguration, authenticated lease proofs, revocation of copied secrets, or
the durable high-water state needed for fenced external effects.

## Derived work

- [Naming, registry, and local discovery](../20-notes/otp-like-system-services-components/naming-registry-and-local-discovery.md)
- [Configuration, workload identity, and secrets](../20-notes/otp-like-system-services-components/configuration-workload-identity-and-secrets.md)
- [Distributed membership, discovery, and authoritative coordination](../20-notes/otp-like-system-services-components/distributed-membership-discovery-and-authoritative-coordination.md)
- [OTP-like system-services contract inquiry](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
