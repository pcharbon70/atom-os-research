---
title: "Protected I/O and DMA ownership"
kind: note
created: "2026-09-02"
maturity: developing
tags:
  - architecture-support
  - capabilities
  - device-drivers
  - dma
  - iommu
  - operating-systems
aliases:
  - "Kernel DMA ownership protocol"
  - "Protected device I/O"
---

# Protected I/O and DMA ownership

The best initial implementation is **deny-by-default device isolation with one
IOMMU address space per indivisible requester set, explicit frame-epoch-bound
`DmaMapping` authority, and enforced CPU/device ownership transfer**.
Requester, endpoint, interrupt, and reset scopes remain independent objects.
Drivers run as unprivileged native I/O services, but a trusted mediator retains
raw DMA-issue
queues/doorbells unless hardware enforces their ranges and generations. The
kernel retains binding, IOMMU, interrupt-remapping, revocation, reset-lease, and
accounting authority. PCIe ATS, PRI, PASID/SVA, peer-to-peer DMA, and
application-owned hardware queues remain disabled until their extra caches and
completion protocols are implemented and verified.

This design does not equate “unmapped” with “safe to reuse.” Safe revocation is
a transaction: stop new publication, quiesce or reset the endpoint, complete
device and IOMMU invalidation, retire stale interrupts, acquire CPU cache
ownership where required, and only then scrub and reclaim memory. If any proof
is missing, memory remains pinned and the endpoint is quarantined.

The design is a proposal. IOMMU specifications, driver-isolation systems,
CleanQ, Thunderclap, Arrakis, and recoverable-driver research supply mechanisms
and evidence, but they do not prove this complete protocol on the target
machines.

## Question, scope, and operational standard

The question is:

> What smallest privileged mechanism can safely delegate high-throughput I/O
> to restartable services while preserving memory confidentiality, integrity,
> bounded resource use, and truthful revocation across coherent and
> non-coherent machines?

The component owns:

- validation and binding of component 0's normalized requester, MMIO,
  interrupt, reset, topology, and coherency descriptors into live protected-I/O
  objects;
- deny-by-default IOMMU and interrupt-remapping setup before an untrusted
  service can drive a device;
- capabilities for endpoints, domains, DMA memory, mappings, queues, and
  revocation;
- checked IOVA allocation, page pinning, access permissions, quotas, and
  generation-tagged mapping state;
- architecture-specific translation-cache and device-cache invalidation with
  completion evidence;
- coherent and non-coherent cache-ownership transitions;
- endpoint quiescence, reset, surprise-removal, fault, and quarantine state;
- stale-interrupt rejection and diagnostic fault attribution; and
- final memory scrub/reclamation when all relevant agents are excluded.

It does not own:

- device-class policy, filesystem/network protocol semantics, or a particular
  driver's descriptor format;
- BEAM mailbox, binary, garbage-collection, or supervision semantics;
- arbitrary direct access to physical addresses, MMIO, port I/O, or interrupt
  controllers by an actor or driver;
- a universal reset sequence—the device profile must supply and validate one;
- containment of a hostile DMA requester on a platform without a working
  isolation boundary; or
- a claim that IOMMU isolation makes a malicious driver harmless. A driver can
  still corrupt buffers deliberately delegated to its endpoint or violate a
  shared protocol.

A satisfactory implementation must pass this operational standard:

1. Before delegation, every DMA-capable requester is either blocked, attached
   to a kernel quarantine domain, or assigned to exactly one authorized domain.
   Unknown requester aliases fail closed.
2. A service can map only memory named by a live `DmaBufferCapability`, within
   its access, IOVA, pin, queue, and lifetime quotas. No public interface accepts
   a raw physical address as authority.
3. In the strict untrusted-driver profile, CPU and device ownership of a cache
   line or buffer never overlap: writable CPU aliases are revoked to remote-TLB
   completion before `DeviceOwned`, and restored only after trusted completion.
   A separate trusted-typestate profile may retain aliases, and a coherent-
   shared type may permit deliberate overlap; neither is mislabeled strict
   enforcement.
4. A stale descriptor, completion, fault, interrupt, mapping token, or device
   transaction from an earlier binding generation cannot authorize or complete
   work in a later generation.
5. Revocation does not report `Reclaimable` until device issue is stopped,
   in-flight access is accounted for, IOMMU and optional device translation
   caches are invalidated with completion evidence, and CPU cache ownership is
   restored where required.
6. Timeout or reset uncertainty yields `QuarantinedPinned`, not optimistic
   unmap and reuse. Recovery never depends on the failed driver cooperating.
7. The declared platform profile states whether the IOMMU covers every DMA
   path, whether interrupts are remapped, whether requester isolation is
   atomic, and whether peer-to-peer transactions can bypass control.
8. Intel VT-d, Arm SMMUv3, and RISC-V IOMMU backends can implement the common
   completion contract while preserving their distinct requester identifiers,
   queues, and invalidation rules.
9. Fault storms, pinning, IOVA consumption, command-queue use, outstanding
   operations, PRI requests, and interrupt rate are bounded and attributable.
10. Model, emulator, and hardware tests inject delayed DMA after unmap, stale
    ATS entries, reordered descriptor publication, reset failure, surprise
    removal, stale interrupts, and IOMMU command timeout.

## Evidence, synthesis, and proposal

| Status | Claim |
| --- | --- |
| Normative architecture fact | Intel VT-d, Arm SMMUv3, and the RISC-V IOMMU provide requester-scoped translation structures, translation-cache invalidation, fault reporting, and explicit synchronization mechanisms, but their identifiers and command/completion details differ. |
| Normative architecture fact | Device-side address-translation caches require their own invalidation protocol; changing a page table and invalidating only an IOMMU cache is insufficient when ATS-like facilities are enabled. |
| Reported security evidence | Thunderclap found exploitable weaknesses in operating-system IOMMU use and emphasized that hot-pluggable peripherals must be treated as potentially malicious DMA agents. |
| Reported systems evidence | CleanQ makes queue-buffer ownership transitions explicit and reports that a formal model can coexist with practical I/O performance. Its queue model is useful evidence, not a complete device-reset or IOMMU-revocation design. |
| Reported systems evidence | User-mode driver and direct-I/O systems show that device access can leave a monolithic kernel fast path, while also moving protocol validation and isolation obligations to memory mappings, queues, and the control plane. |
| Reported reliability evidence | Recoverable-driver work shows the value of isolating and restarting faulty drivers, but device state and outstanding DMA can prevent transparent recovery. |
| Synthesis | The protection object must be the entire indivisible requester group plus its memory, MMIO, interrupt, cache, reset, and transport paths—not a convenient PCI function number or one page table alone. |
| Project proposal | Delegate capabilities for bounded buffers and queues to an I/O service, retain lifecycle and revocation authority in the kernel, and model memory reuse as a completed ownership transfer. |
| Unverified | Actual requester grouping, reset coverage, coherency behavior, invalidation latency, fault containment, and throughput on each target platform. |

## Threat model and trust boundary

### Agents that may fail

The baseline treats the driver service as buggy or malicious and the device as
buggy. A stricter profile also treats the device as actively malicious within
the electrical/interconnect behavior the platform's IOMMU is documented to
mediate. A compromised service may:

- forge or replay descriptors and completions;
- request excessive pinning, mappings, interrupts, or invalidations;
- access a delegated buffer outside its protocol phase;
- fail during revocation or reset;
- program a device to retain translations or issue delayed writes; and
- collude with another service through intentionally shared memory.

The privileged computing base includes the capability kernel, IOMMU and
interrupt-remapping backend, validated binding of component 0's endpoint
descriptors, cache-maintenance primitives, the endpoint-specific quiesce/reset
profile, and the platform firmware needed to make those mechanisms work.
Hardware descriptions are inputs to validate, not authority to trust blindly.

The baseline does not claim protection from physical attacks, malicious
firmware, an IOMMU implementation defect, a requester path that bypasses the
IOMMU, unisolated peer-to-peer routing, or a device that violates the physical
bus protocol. Those conditions select a weaker platform profile or make
untrusted delegation unavailable.

### Independent isolation, delivery, and reset scopes

IOMMU attachment, driver-visible function, interrupt containment, and reset
collateral are not assumed to have the same boundary. Component 0 supplies
normalized descriptors; this component validates and binds four independent
scope records. These records describe composition; they do not create parallel
owners for minimal-kernel authority objects:

```text
RequesterSet {
  requester_set_id, generation,
  requester_ids, iommu_path, peer_paths, isolation_evidence
}

DeviceEndpoint {
  endpoint_id, generation,
  device_functions, mmio_regions, queue_profiles, coherency_profile
}

InterruptSourceSet {
  interrupt_set_id, generation,
  interrupt_binding_views, remapping_path, containment_evidence
}

ResetDomain {
  reset_domain_id, generation, control_epoch,
  affected_endpoints, affected_requester_sets, reset_profile
}

EndpointBinding {
  binding_generation,
  requester_set, endpoint, interrupt_source_set, reset_domain
}
```

`RequesterSet` is the smallest unit the platform can attach independently to an
IOMMU domain; it may contain several enumerated functions or aliases.
`DeviceEndpoint` is the delegable MMIO/queue identity. Each member of an
`InterruptSourceSet` is a borrowed `InterruptBinding` view over an existing,
accounted `IRQBinding` aggregate; the set neither owns the view nor creates a
second interrupt authority or lifetime. The set may be shared or remapped
independently. `ResetDomain` records the actual
collateral scope and may be broader or narrower than one requester attachment.
If any boundary cannot distinguish two principals, all affected objects must be
assigned to one trust and recovery unit.

Each generation changes only when its own object is replaced or revalidated;
`binding_generation` changes whenever their composition changes. Hardware
requester, interrupt, and function numbers may be reused, but stale object
handles may not. An ordinary reset or reset-profile mutation requires both the
scoped `Reset`/`Quarantine` facet and the active manager's sealed, current
`ResetLease.Use(reset_domain, reset_epoch)`. Independent `ResetControl`
authority is held outside every affected driver and replaceable manager; it may
close a stale lease, advance the epoch, and install an escrowed successor
authority set, but it is not the credential used to execute an ordinary reset.

## Capability and resource model

### Capability types

Use typed objects with attenuated rights:

```text
EndpointCapability(endpoint, generation, rights)
  rights = Inspect | Bind | Configure | Submit | Revoke

RequesterSetCapability(requester_set, generation, rights)
InterruptSourceSetView(interrupt_set, generation,
                       borrowed_interrupt_binding_views)
ResetLease.Use(reset_domain, reset_epoch)
ResetControl(reset_domain, control_epoch,
             rights = Install | RevokeAndAdvance | Inspect)

DmaAddressSpace(address_space, attachment_generation, rights, quotas)
  rights = Map | Recover | Inspect

DmaBufferCapability(buffer, frame_authority_epoch, buffer_access_epoch,
                    byte_range, rights)
  rights = CpuRead | CpuWrite | DeviceRead | DeviceWrite | Share

DmaMapping(mapping, address_space, iova_range, access, generation,
           frame_authority_epoch, buffer_access_epoch,
           rights = Unmap | Invalidate | Inspect)
DeviceQueueLease(queue, binding_generation, ring_generation, rights)
InterruptBinding(irq_binding, source_incarnation,
                 route_generation, binding_generation)
```

The kernel retains final `Bind` and `Revoke`. The active reset manager outside
affected driver domains holds the current `ResetLease.Use` plus only the scoped
reset/profile facets it needs. A still more independent final controller holds
`ResetControl` and the precommitted escrow needed to replace that manager; the
two authorities are never collapsed into a copyable “control lease.” An I/O
service receives the smallest MMIO subset, `DeviceQueueLease`,
`InterruptBinding` view, and buffer/`DmaMapping` rights needed by its
device-class protocol. An allocator can mint a buffer capability without
revealing its physical pages. Every buffer and mapping binds the minimal
kernel's global frame-authority epoch. The mapping broker verifies ownership
and quota, pins the pages, chooses an IOVA, and returns an opaque `DmaMapping`.

`BufferAccessEpoch` is a protected per-range admission gate independent of the
frame's global authority epoch. Every CPU map, copy, transfer, and DMA-map
request must match the current buffer epoch and its `CpuOpen`, `DeviceOpen`, or
`Quarantined` state. Starting an exclusive transfer first advances the epoch to
`CpuClosing`, making all old `CpuRead`/`CpuWrite` facets stale; only then does it
drain existing aliases. CPU reacquisition advances to a fresh `CpuOpen` epoch
only after device exclusion completes.

For `EnforcedExclusive`, a malicious service does not receive an unrestricted
writable descriptor ring or doorbell capable of naming arbitrary DMA. A trusted
queue mediator owns those issue aliases, or a hardware virtual queue enforces
the capability-indexed ranges and generations. Direct raw queue/MMIO delegation
is admitted only as an explicitly weaker trusted-typestate profile or after
equivalent hardware enforcement is demonstrated.

Page-table memory, IOMMU command/event rings, interrupt-controller registers,
and reset controls are never mapped writable into the driver service.

### Quotas and accounting

Charge resources before publication and return the charge only after completed
revocation:

- pinned bytes and page count;
- IOVA extent and number of mapping records;
- active queue and descriptor count;
- outstanding device-owned buffer bytes;
- interrupt and fault rate;
- invalidation and command-queue occupancy;
- optional PRI/page-request credits; and
- quarantine-pinned memory after a failed endpoint.

Quarantine debt remains visible to the supervisor and system resource manager.
Hiding it as a successful unmap would permit a failed device to exhaust memory
through repeated restart attempts.

## Ownership state machines

### Endpoint lifecycle

```text
Denied
  -> QuiescentBound(binding_generation)
  -> Active
  -> Draining
  -> Resetting
  -> Denied(next_generation)

Draining/Resetting -> Quarantined(reason, pinned_resources)
Any state          -> RemovedUnknown(reason, pinned_resources)
```

`Denied` means all known requester IDs are blocked or attached to a domain with
no permitted mappings. `QuiescentBound` has a domain and interrupt containment
but cannot issue ordinary work. `Active` admits generation-tagged submissions.
`Draining` rejects new submissions. `Resetting` is endpoint-profile-specific.
Entering it validates the current sealed `ResetLease.Use` together with the
scoped `Reset` or `Quarantine` facet, then
coordinates every other binding named by the independent reset domain; it is
not implied by ownership of the requester set. `ResetControl` participates only
in takeover—closing an obsolete manager epoch and installing its escrowed
successor—not in this ordinary transition.
Only successful completion of the revocation ledger returns to `Denied`.

### Buffer and mapping ownership

Select one enforcement profile per buffer/ring type:

| Profile | CPU aliases while device owns data | Admitted principal |
| --- | --- | --- |
| `EnforcedExclusive` | All CPU aliases not required by a trusted mediator are closed and remotely invalidated before device ownership; before CPU reacquisition, device issue/translation authority for that operation is quiesced or revoked. Each direction gets a new access generation | Baseline for a malicious native driver |
| `TrustedTypestateExclusive` | Long-lived CPU aliases may remain, so exclusivity is a language/protocol promise rather than a protection fact | Audited memory-safe in-kernel or trusted service only |
| `CoherentShared` | Concurrent access is intentional; exact cache lines, atomics, producer/consumer fields, and visibility operations are specified | Explicit shared-ring protocol only |

The profile is part of the type and diagnostic record. Code may not infer
`EnforcedExclusive` merely because a token changed state.

For an exclusive device operation:

```text
CpuOwned
  -> MappedCpuOwned
  -> CpuClosing
  -> CpuAccessClosed
  -> Offered
  -> DeviceOwned
  -> Returned
  -> CpuReacquiring
  -> CpuOwned

MappedCpuOwned/CpuClosing/CpuAccessClosed/Offered/
DeviceOwned/Returned/CpuReacquiring
  -> Revoking
  -> TranslationPending
  -> Quiescent
  -> Unmapped
  -> ScrubbedOrReassigned

CpuClosing/CpuReacquiring/Revoking/TranslationPending
  -> QuarantinedPinned
```

`prepare_for_device` owns `CpuClosing`; its success record is the only path to
`CpuAccessClosed` and returns a `DeviceBufferToken` representing that closed
state. Acceptance by `publish_to_device` moves the protected token to
`Offered`; only successful descriptor publication and doorbell ordering moves
it to `DeviceOwned`. Cancellation may return the exact token in
`CpuAccessClosed` only when no device-visible publication occurred.

The IOMMU mapping lifetime and ownership lifetime are related but not
identical. Long-lived device mappings may amortize IOMMU work only for
`TrustedTypestateExclusive`, `CoherentShared`, or a strict hardware/mediator
profile that enforces per-operation device issue independently of the
malicious driver. Otherwise `EnforcedExclusive` closes device translation or
permission while the buffer is `CpuReacquiring` and before returning
`CpuOwned`. It also closes the malicious driver's CPU
aliases and reaches remote translation quiescence before device transfer; only
a trusted mediator's minimal alias may remain. Conversely, revocation may
remove device translation while physical pages remain pinned because earlier
transactions are not known to be drained.

Each transition names the agent allowed to initiate it and the evidence needed
to complete it. Queue indices alone are not evidence: a malicious service can
write arbitrary indices in its own memory.

### Queue ownership

Adapt the CleanQ idea to an endpoint generation:

```text
QueueEntryToken {
  queue_id,
  ring_generation,
  buffer_mapping_generation,
  buffer_access_epoch,
  frame_authority_epoch,
  byte_range,
  device_access,
  operation_generation,
}
```

At most one party owns an exclusive entry. Transfer is monotonic for that
operation generation:

```text
DriverAvailable -> DeviceOffered -> DeviceHeld -> DriverReturned
```

The producer writes descriptor contents, performs the backend's DMA publication
operation, and only then publishes ownership/doorbells. The consumer observes
ownership with the matching acquisition operation before reading contents.
Descriptor-memory order and device-MMIO order are separate contracts; a CPU
release store does not by itself order a posted MMIO doorbell on every ISA.

Shared coherent rings require a separate type whose fields, cache lines,
atomic operations, and producer/consumer ownership are specified. “Coherent”
does not make an underspecified lock-free ring correct.

## Core interfaces

The common interface should be narrow and split phase:

```text
bind_endpoint(endpoint_cap, service, isolation_profile)
  -> EndpointBinding | BindError

create_dma_address_space(binding, quotas)
  -> DmaAddressSpace | AddressSpaceError

map_dma(address_space, buffer_cap, byte_range, device_access, lifetime)
  -> Rejected(MapError) | Accepted(DmaMapOperation)

poll_dma_map(map_operation)
  -> Pending(stage)
   | Succeeded(DmaMapping)
   | Incomplete(observed, missing, quarantine)
   | QuarantinedPinned(reason)

prepare_for_device(mapping, byte_range, operation_generation)
  -> Rejected(OwnershipError) | Accepted(BufferTransferOperation)

poll_buffer_transfer(transfer_operation)
  -> Pending(stage) | Succeeded(DeviceBufferToken)
   | Incomplete(observed, missing, quarantine)

publish_to_device(queue_lease, device_buffer_token, descriptor)
  -> Rejected(QueueError, DeviceBufferToken)
   | Accepted(OperationToken<QueuePublication>)

cancel_publish_to_device(operation_token)
  -> CancellationSelected | TooLate(stage) | AlreadyTerminal(result)

poll_publish_to_device(operation_token)
  -> Pending(stage)
   | Succeeded(DeviceOperationToken)
   | Cancelled(DeviceBufferToken)
   | Incomplete(observed, missing, PinnedPublicationRecord)
   | QuarantinedPinned(reason, PinnedPublicationRecord)
   | Fatal(CrashRecord, PinnedPublicationRecord)

accept_completion(queue_lease, device_operation_token,
                  device_completion_token,
                  current_completion_facet)
  -> Rejected(CompletionError, DeviceOperationToken,
              DeviceCompletionToken)
   | Accepted(OperationToken<CompletionAcceptance>)

cancel_accept_completion(operation_token)
  -> CancellationSelected | TooLate(stage) | AlreadyTerminal(result)

poll_accept_completion(operation_token)
  -> Pending(stage)
   | Succeeded(ReturnedBufferToken)
   | Cancelled(DeviceOperationToken, DeviceCompletionToken)
   | Incomplete(observed, missing, PinnedCompletionRecord)
   | QuarantinedPinned(reason, PinnedCompletionRecord)
   | Fatal(CrashRecord, PinnedCompletionRecord)

prepare_for_cpu(returned_buffer_token, cpu_access)
  -> Rejected(OwnershipError) | Accepted(CpuReacquireOperation)

poll_cpu_reacquire(reacquire_operation)
  -> Pending(stage) | Succeeded(CpuBufferToken)
   | Incomplete(observed, missing, quarantine)

begin_revoke(binding_or_mapping, reason)
  -> Rejected(RevokeError) | Accepted(RevocationToken)

poll_revoke(revocation_token)
  -> Pending(stage) | MappingReclaimable | FrameRetypable
   | QuarantinedPinned(reason)
```

Every accepted operation has exactly one terminal result. Polling observes a
preallocated completion record; it does not block a privileged thread until a
hardware queue, remote CPU, device, or interconnect responds. Timeout yields
`Incomplete` or `QuarantinedPinned`, never an implied cancellation.

`DeviceQueueLease.Submit` and `.Doorbell` are borrowed, generation-checked
facets; a call does not transfer the lease itself. Before accepting publication,
the component copies and validates the descriptor into protected storage and
reserves its bounded queue slot and accounting credit. `Rejected` means that no
descriptor ownership bit, queue tail, or doorbell became device-visible, every
reservation was released, and the exact `DeviceBufferToken` remains with the
caller in `CpuAccessClosed`. `Accepted` consumes that token into the protected
operation record, moves the buffer to `Offered`, and leaves the caller only the
`OperationToken<QueuePublication>`. `Succeeded` replaces it with the sole
`DeviceOperationToken` for the now-`DeviceOwned` buffer. `Cancelled` can return
the original device-buffer authority only after proving no publication escaped
and rolling back the reservation. `Incomplete`, `QuarantinedPinned`, and
`Fatal` return no buffer authority: the operation record and buffer stay pinned
in the named protected ledger until a separate recovery protocol proves a safe
state.

Completion admission follows the same ownership rule. `Rejected` performs no
ownership transition, does not consume the one-shot `DeviceCompletionToken`,
and returns it with the exact `DeviceOperationToken`; the current completion
facet is borrowed, not transferred. `Accepted` moves both tokens into the protected
`OperationToken<CompletionAcceptance>`. `Succeeded` atomically consumes the
completion token and replaces the device-operation token with one
`ReturnedBufferToken` in
`Returned`. `Cancelled` returns both linear inputs only if it wins before the
evidence claim or ownership mutation. Every uncertain, quarantined, or fatal
terminal retains them in a protected pinned record and exposes no CPU-ownership
token. A cancellation request that arrives after the relevant visibility or
evidence point reports `TooLate`; it cannot manufacture a `Cancelled` terminal,
and the accepted operation continues to one sticky result.

A `DeviceCompletionToken` is protected, one-shot evidence minted by the minimal
kernel after either a controller/IOMMU record establishes the required
postcondition or a current, separately trusted queue-manager facet submits a
valid `CompletionAttestation`. An ordinary report or queue word from the
potentially malicious driver/device is only input to that validation and cannot
mint the token or CPU ownership. Under an actively malicious-device profile,
even a device-authored completion is insufficient unless a protected hardware
fence, quiescence, or reset contract excludes later access.

A `CompletionAttestation` is a sealed, one-shot record containing:

```text
manager_identity,
completion_session_epoch,
reset_control_epoch_or_none,
evidence_profile_and_class,
binding_generation,
queue_and_ring_generation,
operation_generation,
mapping_generation,
buffer_access_epoch,
frame_authority_epoch,
completed_byte_range
```

Manager takeover advances `completion_session_epoch` (and the reset-control
epoch when reset authority changes), invalidating every unconsumed attestation
from the old manager. Validation consumes the record atomically, so it cannot
complete a second operation or a replacement binding.

`map_dma` reports the exact alignment, boundary, maximum segment, and access
constraints. It does not silently widen a requested byte range to expose
unrelated data. If hardware translation granularity exceeds the requested
range, the allocator supplies exclusive padded storage or rejects the map.

`DeviceRead` means the device may read memory, and `DeviceWrite` means it may
write memory. These terms avoid API names whose “to/from” direction depends on
the speaker. Bidirectional mappings are exceptional and more expensive to
reason about.

Operations return explicit outcomes such as `QuotaExceeded`, `StaleGeneration`,
`EndpointDraining`, `UnsupportedIsolation`, `TranslationQueueFull`,
`InvalidationTimeout`, and `EndpointQuarantined`. Retrying is a policy decision
above this layer.

## Mapping and publication protocol

### Map

Before acceptance, the mapping broker validates domain, endpoint, service,
buffer, frame-authority epoch, access, and quotas, allocates a checked IOVA, and
constructs unpublished translation entries. Rejection returns every resource.
Acceptance atomically pins the frame, charges quota, and records a
`DmaMapOperation`; from that point the split-phase backend:

1. makes table writes visible under the IOMMU contract;
2. installs or updates the domain root/context;
3. submits required negative-cache or translation-cache invalidation;
4. records the backend's defined completion event without blocking the caller;
   and
5. publishes the opaque mapping capability only in the terminal `Succeeded`
   result.

Failure unwinds only state proved unobserved. If hardware may have observed a
partial change and completion cannot be established, the operation terminates
`Incomplete` or `QuarantinedPinned`; the endpoint/domain and frame remain
pinned rather than being reused.

### Give ownership to the device

For a device-read buffer on a non-coherent platform, clean dirty CPU cache
lines to the point required by the platform before descriptor publication. For
a device-write buffer, prevent dirty CPU lines from later overwriting device
results; the exact clean/invalidate sequence comes from the platform coherency
profile. In `EnforcedExclusive`, the transfer operation first closes the
`BufferAccessEpoch` admission gate, making every old CPU mapping/copy facet
stale, then closes extant untrusted aliases and obtains remote
`TranslationQuiescent` evidence before returning a `DeviceBufferToken` bound to
the new epoch. A mere typestate statement that the CPU “must not touch” the
range is insufficient.

After data and descriptor preparation, execute the architecture/device memory
publication primitive, publish the descriptor ownership bit or queue tail, and
then issue the correctly ordered doorbell. These effects occur only after
`publish_to_device` accepts and owns the `DeviceBufferToken`; the accepted
operation records the buffer, queue, binding, and publication generations.
Success returns the sole `DeviceOperationToken`. If observation cannot
establish whether any effect escaped, the terminal result keeps that authority
pinned rather than returning a retryable buffer token.

### Return ownership to the CPU

An interrupt is a hint to inspect a protected completion path, not proof of a
particular operation. The driver may report queue generation, descriptor
identity, bounds, device status, and operation token, but that report has no
completion authority. A protected hardware record or separately trusted queue
manager validates the device-specific postcondition so the minimal kernel can
mint a one-shot `DeviceCompletionToken`. Before acceptance,
`accept_completion` rejects stale/duplicate generations without consuming that
token or the `DeviceOperationToken`. After acceptance, its protected operation
owns both; terminal success consumes them and mints one `ReturnedBufferToken`
for the proved byte range. Cancellation can return them only before evidence
claim or ownership mutation, while uncertainty pins them without creating CPU
authority.

`prepare_for_cpu` then closes or quiesces device issue/translation authority as
required by `EnforcedExclusive`, performs non-coherent CPU cache acquisition,
and only after those split-phase obligations complete returns
`CpuBufferToken`. Thus the API and prose preserve the intermediate returned
state; they do not treat a device-authored queue word as CPU ownership.

Partial completion, short packets, scatter/gather chains, and devices that can
write metadata after a completion bit require device-class-specific evidence.
The common layer cannot infer this from an interrupt.

## Revocation is a completion protocol

### Revocation ledger

`begin_revoke` closes the logical gate immediately, then executes a durable,
profile-validated `RevocationPlan` dependency DAG. Its nodes include:

| Obligation node | Required evidence |
| --- | --- |
| Gate closed | endpoint/mapping generation advanced; all new submissions rejected |
| Buffer access closed | affected `BufferAccessEpoch` advanced so old CPU-map, copy, transfer, and DMA-map facets cannot start a new effect |
| Frame authority retired/quarantined (conditional) | only when the whole frame is being retyped/reassigned or uncertain access threatens it, the minimal kernel advances the global frame-authority epoch and closes every facet across all mappings |
| Driver issue frozen | writable queue, payload, MMIO, and doorbell aliases held by the affected driver are revoked to remote-TLB completion, or the holder domain is terminally stopped; descriptor publication is drained |
| Management route preserved | an independently owned interrupt or polling route remains able to report drain/reset completion and faults |
| Ordinary interrupt contained | driver route disabled or rebound; pending events tagged to old generation |
| Device quiesced | endpoint-specific stop/drain completed, or a reset with documented DMA-stop semantics completed |
| Page tables revoked | target mappings removed or domain changed to deny-all |
| IOMMU cache invalidated | required context/IOTLB invalidations accepted and completed |
| Device cache invalidated | ATS/device-TLB invalidation completed when that feature was enabled |
| Transport drained | previously accepted reads/writes and posted writes are completed or excluded by the device/interconnect profile |
| CPU ownership acquired | non-coherent cache state made safe for inspection/reuse |
| Interrupt epoch retired | no old event can complete a new operation |
| Memory sanitized | secrets scrubbed before transfer to another protection domain |
| Reclaimable | pins, IOVA, mappings, and accounting may be released |

The plan is not one universal sequence. A device that needs mappings to drain
places `Device quiesced` before `Page tables revoked`; a profile with an early
deny-all isolation switch may reverse those nodes; a drain reported by an
interrupt makes `Management route preserved` a predecessor of completion.
Plan validation rejects a cycle or any path that disables its own only
completion mechanism. Applicable nodes may not be omitted, and `Reclaimable`
depends on every one of them.

“Applicable” depends on the revocation target. Ordinary closure of one mapping
advances its mapping generation and affected buffer-access epoch but does not
invalidate unrelated legitimate facets to a shared frame. Endpoint teardown
closes every mapping in that binding. Global frame-authority retirement is
required only for frame retype/reassignment or escalation where the affected
range cannot be bounded. The terminal result distinguishes
`MappingReclaimable` from `FrameRetypable`.

A page-table update plus IOTLB invalidation prevents future translations; it
does not recall a transaction already translated or a posted write already
accepted by the fabric. Reclamation therefore still depends on device and
transport completion. The recovery ledger is owned outside the failed driver.
Quarantine advances the narrowest buffer/mapping admission epochs that contain
the uncertainty; if old access may reach the whole frame, it additionally
advances the global frame-authority epoch. In either case it denies every new
effect in the affected scope. Cross-principal frame reuse is possible only
after full quiescence and scrub, when the minimal kernel destroys/retypes the
frame under a fresh authority epoch.

### Timeout and reset failure

Every hardware command has a bounded software observation deadline. Timeout
does not prove failure before or after the operation; it creates uncertainty.
The response is:

1. close logical access and ordinary driver delivery, while preserving or
   rebinding the independent management completion/fault route;
2. attempt a stronger platform isolation/reset action if the endpoint profile
   authorizes one;
3. record requester, command, queue, mapping, and fault state;
4. keep affected pages and table structures pinned; and
5. publish `QuarantinedPinned` for supervisory policy.

A global IOMMU reset or bus reset can affect unrelated endpoints and is not an
automatic fallback. It requires a system-level recovery transaction.

### Surprise removal

Physical disappearance is not proof that transactions are drained. Mark the
binding generation dead, mask/remap interrupts, query the interconnect and
IOMMU fault state, apply the hot-remove/reset guarantees available to that
platform, and quarantine memory if those guarantees do not establish a safe
completion point.

## Cross-ISA implementation

The common semantics are “block, install, invalidate, synchronize, fault, and
attribute.” Backends must not erase the following differences:

| Concern | Intel VT-d | Arm SMMUv3 | RISC-V IOMMU |
| --- | --- | --- | --- |
| Request identity | PCI requester/source identity; scalable configurations may add process-address-space identity | StreamID selects a Stream Table Entry; SubstreamID may select a context | device context, with optional process-directory/process identity |
| Translation/control records | root/context and, by mode, PASID-related translation structures | stream table and context descriptors | device-context and optional process-directory tables |
| IOMMU invalidation | register or queued-invalidation operations for context/IOTLB and related caches | command queue operations for configuration, TLB, and ATC state | command queue `IOTINVAL` and related operations |
| Device translation cache | device-TLB invalidation when ATS is enabled | ATC invalidation when ATS is enabled | `ATS.INVAL` for device address-translation cache state |
| Completion primitive | queued wait/completion semantics after prior invalidations | `CMD_SYNC` and its configured completion mechanism | `IOFENCE.C` orders/completes prior commands under the specified contract |
| Fault/event path | DMA-remapping and interrupt-remapping fault records | event queue, global error records, and optional PRI queue | fault queue and command-queue status/error state |
| Initial profile | one requester group/domain, translated mode, interrupt remapping, ATS/PASID off | one StreamID group/domain, stage-1 or stage-2 policy selected explicitly, ATS/PRI off | one device context/domain, ATS/process identity off |

### Intel VT-d backend

Build tables in kernel-owned memory, derive requester groups from validated PCI
topology and alias rules, and use translated or deny-all entries rather than
pass-through for untrusted endpoints. Invalidation scope must cover every
changed context, IOTLB, interrupt-remapping, and optional device-TLB entry.
Queued invalidation completion is the backend evidence that earlier queued
invalidations reached their specified completion point; it is not proof that a
device-specific posted write was drained.

### Arm SMMUv3 backend

Validate StreamID coverage before enabling a service. Publish Stream Table and
Context Descriptor changes with the prescribed memory ordering, enqueue the
corresponding configuration/TLB command, and use `CMD_SYNC` completion rather
than command-queue consumption as the synchronization point. If ATS is enabled
later, include ATC invalidation and handle timeout as incomplete revocation.
Event and PRI records are untrusted inputs bounded by queue capacity and rate.

### RISC-V IOMMU backend

Use device contexts to select the domain and leave process-directory/ATS paths
disabled in the baseline. After table changes, issue the required `IOTINVAL`
scope followed by `IOFENCE.C` with the access-order operands required by the
transition: a device-read-only reclamation requests `PR`, while a range that
was device-write-accessible requests both `PR` and `PW` (as does bidirectional
access). These bits cover transactions already processed by the IOMMU; they do
not prove that a device or interconnect has stopped issuing or drained work, so
the profile retains a separate quiescence/transport node. If device address-
translation caching is later enabled, the
revocation transaction also includes `ATS.INVAL` and its required completion/
order. Command-queue head movement alone is not the common layer's completion
proof.

### IOMMU-independent semantic contract

The upper layer asks for operations such as:

```text
block_requesters(endpoint_generation)
install_translation(domain, map_generation)
invalidate_iommu(scope, generation)
invalidate_device_cache(scope, generation)
submit_translation_sync(generation)
  -> Rejected(reason) | Accepted(TranslationSyncOperation)
poll_translation_sync(operation)
  -> Pending | Succeeded(completion_scope)
   | Incomplete(observed, missing, quarantine)
read_and_ack_faults(budget)
```

Each backend documents which hardware state the completion covers and which
device/interconnect obligations remain. These are split-phase submissions and
completion observations, not blocking waits hidden behind `await`. A generic
`flush()` call would conceal the most important distinctions.

## Platforms without complete DMA isolation

Expose a truthful profile rather than silently weakening `ProtectedDma`:

```text
StrictIsolated
  // every requester path translated; interrupts contained; reset profile known

IsolatedNoDeviceCache
  // strict mapping isolation; ATS/PRI/PASID unavailable or forcibly disabled

TrustedDeviceCoherent
  // no hostile-device containment claim; coherent ownership protocol retained

TrustedDeviceBounce
  // trusted requester restricted by driver protocol to a bounce arena

NoDma
  // programmed I/O only
```

This hardware-isolation profile is composed with exactly one buffer-ownership
profile (`EnforcedExclusive`, `TrustedTypestateExclusive`, or
`CoherentShared`). `StrictIsolated` describes requester reach and reset/
interrupt containment; it does not by itself prove that a malicious CPU holder
lost an alias or that an operation-specific device access ended.

A bounce buffer can protect the rest of memory from an honest device that is
programmed to use only that arena and can limit accidental protocol exposure.
Without hardware DMA isolation it cannot stop a malicious requester from
issuing another physical address. Therefore `TrustedDeviceBounce` is not a
substitute for `StrictIsolated`, and an untrusted driver may be forbidden even
if copies are used.

For early prototypes, `NoDma` or a single audited trusted device with a fixed
reserved arena is preferable to advertising containment that the hardware does
not provide.

## Managed-runtime and capability-kernel boundary

Ordinary BEAM processes never receive MMIO, I/O-port, requester, interrupt,
IOMMU, or DMA mapping capabilities. A native I/O service owns the attenuated
endpoint interface and communicates with managed processes through bounded IPC
and explicitly owned shared buffers.

DMA pages are not ordinary movable actor-heap objects. The runtime may expose a
managed handle whose finalizer requests release, but finalization is neither
timely revocation nor hardware completion. The resource supervisor owns the
lease and can revoke it independently of actor garbage collection.

The kernel preserves the architecture's process-local managed execution and
garbage-collection contract by keeping collector policy outside privileged
code. It enforces only the memory, queue, capability, and endpoint boundaries
needed to prevent a native service or device from escaping its grant.

Supervision maps naturally onto explicit failure:

- a failed service process can be restarted after the old endpoint generation
  is closed and revocation completes;
- the new service receives fresh capabilities and queue generations rather
  than inheriting raw device state;
- an endpoint in `QuarantinedPinned` is a degraded resource requiring policy,
  not a silently restarted device; and
- callers receive failure for outstanding operations so application-level
  supervisors can retry, fail over, or shed load.

For high throughput, batch capability-validated buffer transfers and queue
notifications. Do not put one kernel transition on every packet if an owned
ring and bounded batch can preserve the same authority.

## Safety, security, and failure analysis

### Malicious shared protocols

An IOMMU limits address reach but not the meaning of shared bytes. Validate
descriptor length, offset, segment count, alignment, generation, and integer
arithmetic before granting or publishing ownership. Allocate metadata and data
so hardware translation granularity cannot expose neighboring principals.
Never let a device-supplied length select an unchecked CPU copy.

### ATS, PRI, PASID, and shared virtual addressing

These features may reduce translation overhead or enable fine-grained sharing,
but they add device caches, page-request traffic, process-identity binding,
fault races, and new denial-of-service surfaces. Enable them only in a later
profile with:

- bounded page-request credits and fault handling;
- generation binding between process address space and device context;
- device-cache invalidation in every unmap and process teardown;
- cancellation rules for requests racing revocation; and
- tests proving a stale process identity cannot reach a reused address space.

### Reset is not a universal proof

Function-level, bus-level, power, and firmware resets have different scope and
DMA-stop guarantees. A reset profile records the sequence, collateral domain,
completion indication, configuration that survives, and whether transactions
can remain in the fabric. Devices without adequate evidence cannot provide
automatic safe restart.

### Non-coherent memory

Cache maintenance is ownership transfer, not an optimization. Operations are
range-checked, aligned safely without touching another principal's cache line,
ordered with descriptor/doorbell publication, and paired with the declared
memory attributes. Mixed cacheability aliases are rejected. Failure to perform
the CPU-side acquisition after device write can expose stale data even when
IOMMU permissions were correct.

### Interrupts and faults

An interrupt carries endpoint, route, and binding generations. Masking a source
does not erase an already pending message; completion handlers reject stale
epochs. Fault and PRI queues have bounded drain budgets. Repeated faults first
throttle and then quarantine the endpoint rather than monopolizing a kernel
CPU.

### Peer-to-peer DMA

Peer traffic may bypass host memory translation or create authority not
represented by either endpoint's normal domain. Disable it by default. Later
support requires an explicit pair capability, validated path/isolation proof,
address aperture, ownership protocol, and joint revocation transaction.

### Confidentiality on reuse

After safe quiescence, scrub buffers before granting them to another protection
domain. Device-private memory and persistent queues may retain secrets across
reset; endpoint profiles must either sanitize them or declare that the device
cannot cross tenants without a stronger reset.

## Verification and benchmarks

### State-machine model

Model at least two endpoint generations, two domains, a driver, a device, an
IOMMU cache, an optional device cache, an interrupt route, CPU cache ownership,
and nondeterministic delayed transactions. Check:

- one exclusive owner per buffer range and operation generation;
- no device access outside a live authorized mapping;
- no reclaimed page is reachable from an old translation or in-flight access;
- stale completion/interrupt/fault records cannot advance a new operation;
- `Reclaimable` implies every applicable ledger stage completed;
- timeout can preserve liveness by quarantine without violating safety; and
- quota is conserved across failure and restart.

Inject ordering mistakes deliberately: publish a doorbell before descriptors,
skip a cache clean, observe a queue head before command completion, omit a
device-cache invalidation, reset while a posted write is pending, and reuse a
requester ID after hot removal.

### Emulator and device-model tests

Use IOMMU-capable virtual platforms for deterministic protocol tests, while
recording which behaviors are model assumptions. A hostile device model should:

- DMA one byte before and beyond every mapping boundary;
- delay writes until after unmap and service restart;
- retain an emulated ATS entry;
- duplicate, reorder, truncate, and fabricate completions;
- flood interrupts, faults, and page requests;
- ignore quiesce and fail reset; and
- issue from an alias requester identity.

Tests must verify denial and attribution, not merely absence of a host crash.

### Hardware qualification

For each board and device revision, record firmware/IOMMU version, topology,
requester group, coherency attributes, enabled features, reset mechanism, and
known errata. Qualification includes:

- DMA to an unmapped guard page before, during, and after domain changes;
- IOMMU and optional device-cache invalidation completion under load;
- non-coherent patterns that reveal dirty/stale cache lines;
- surprise removal and restart with outstanding traffic;
- interrupt-remapping and stale-event tests;
- fault isolation between two simultaneously active endpoints; and
- memory-pressure behavior when quarantine pins resources.

### Performance measurements

Report distributions and saturation points rather than one throughput number:

- map/unmap latency by page count and invalidation scope;
- buffer ownership-transfer latency, including cache maintenance;
- batch size versus packets/operations per second and tail latency;
- IOMMU command/fault queue occupancy and backpressure;
- interrupt versus polling cost and CPU use;
- IOTLB miss behavior and page-size trade-offs;
- service restart and full revocation time;
- copy/bounce, long-lived mapping, and direct-queue baselines; and
- cross-core and NUMA placement effects.

Measure security configurations actually proposed for use. A benchmark with
the IOMMU, interrupt remapping, or required cache maintenance disabled does not
establish the production design's performance.

## Staged implementation

### Stage 0: executable ownership model

Implement the capability types, endpoint/buffer state machines, generations,
quota ledger, and a fake device/IOMMU backend. Model-check safety and make
quarantine a first-class result before touching hardware.

### Stage 1: deny-by-default bring-up

Validate component 0's normalized requester sets and endpoints, block every
requester, reserve IOMMU tables and queues, contain interrupts, and expose
diagnostic faults. Use programmed I/O or one audited boot device while
validating that no unexpected requester can DMA.

### Stage 2: one strict domain and mediated queues

Support one device per isolation group with fixed long-lived DMA arenas,
read/write-minimal mappings, ATS/PRI/PASID and peer-to-peer disabled, and a
trusted queue mediator. Establish architecture invalidation completion and
non-coherent ownership transitions.

### Stage 3: unprivileged restartable I/O service

Move the driver into a native protection domain with attenuated interrupt and
buffer capabilities while a trusted mediator retains DMA-issue MMIO/queue
aliases for the strict profile. Delegate a raw virtual queue only where
hardware enforces its ranges and generations. Add bounded fault handling,
service-independent revocation, reset profiles, stale-generation tests, and
supervised restart.

### Stage 4: dynamic leases and zero-copy batching

Add checked dynamic mapping, scatter/gather, long-lived mapping with repeated
ownership transfer, bounded batches, and application-facing shared-buffer
handles. Demonstrate safe cancellation and resource recovery under load.

### Stage 5: optional advanced translation

Only after measurement and model extension, consider per-process device
identity, PRI, ATS, shared virtual addressing, direct application queues, or
peer-to-peer DMA. Each feature is a new protection profile with additional
completion obligations, not a transparent optimization flag.

## Alternatives and trade-offs

### Kernel-resident drivers

Kernel drivers simplify some call paths and can share internal APIs, but make a
memory-safety or protocol fault part of the privileged failure domain. A small
trusted boot driver may be a staging choice; it should use the same ownership
tokens so relocation to a service does not change semantics.

### Permanent mappings

Long-lived IOMMU mappings avoid invalidation on every operation and are a good
optimization for bounded pools only when a trusted mediator or hardware queue
mechanism enforces per-operation issue, or when the selected profile admits
trusted typestate/coherent sharing. They weaken temporal address revocation,
increase pinned-memory pressure, and are not an `EnforcedExclusive` boundary by
themselves. Quotas and generation-tagged queue transfer remain mandatory.

### Map/unmap per operation

Per-operation translation changes give smaller temporal exposure but add table
work, invalidation latency, and command-queue pressure. They still cannot
substitute for device completion and are unlikely to be the best packet-scale
path.

### Copying and bounce buffers

Copies simplify actor ownership, avoid pinning arbitrary managed memory, and
can reduce data exposure to a service. They cost memory bandwidth and latency.
On a no-IOMMU machine, they do not contain a hostile DMA requester.

### Direct application queues

Arrakis-style direct paths can reduce kernel mediation and context switching.
They require hardware virtualizable queues, safe per-principal reset, resource
limits, interrupt paths, and revocation. They are an optional later profile,
not the baseline for preserving supervision and fault containment.

### One shared IOMMU domain

A shared domain is easy to configure and maximizes buffer sharing, but a
compromised endpoint can access every page in that domain. Use it only when all
members are one trust principal and one restart unit; do not call it
least-privilege isolation.

## Unresolved questions

- Which first target exposes complete requester and interrupt isolation, and
  what firmware, bridge, or peer paths escape it?
- What is the smallest reset profile that establishes DMA quiescence for each
  initial device class?
- Can the first implementation rely entirely on long-lived bounded pools, or
  do any workloads require dynamic per-operation mappings?
- Which kernel component validates device-class completion without importing a
  large driver into the trusted computing base?
- How should pinned/quarantined memory pressure interact with supervisor
  restart limits and system admission control?
- What page sizes and IOVA strategy minimize IOTLB pressure without exposing
  adjacent principals through coarse translation granularity?
- Which non-coherent targets are in scope, and can cache-line exclusivity be
  enforced by the allocator without excessive fragmentation?
- Is interrupt remapping mandatory for every supported strict profile, or can
  a platform-specific controller capability provide equivalent containment?
- What formal relation connects the generic ownership model to each device's
  descriptor and completion protocol?
- Which advanced feature—multi-queue direct access, ATS, PRI, or PASID—earns
  its verification and recovery complexity first?

## Connections

- [Kernel hardware and architecture support layer](kernel-hardware-and-architecture-support-layer.md)
- [Typed kernel-facing architecture facade](typed-kernel-facing-architecture-facade.md)
- [Unsafe architecture-primitives capsule](unsafe-architecture-primitives-capsule.md)
- [Address translation and protection transitions](address-translation-and-protection-transitions.md)
- [Ordering, coherence, and code publication](ordering-coherence-and-code-publication.md)
- [Interrupt event fabric](interrupt-event-fabric.md)
- [Architecture faults and diagnostics](architecture-faults-and-diagnostics.md)
- [Logical-CPU coordination and lifecycle](logical-cpu-coordination-and-lifecycle.md)
- [Minimal privileged kernel layer](minimal-privileged-kernel-layer.md)

## Sources

### Architecture specifications and implementation contracts

- [Arm System Memory Management Unit Architecture Specification, SMMUv3](../30-sources/arm-2025-smmuv3-architecture.md)
- [Intel Virtualization Technology for Directed I/O Architecture Specification](../30-sources/intel-2024-vt-d-architecture.md)
- [RISC-V IOMMU Architecture Specification](../30-sources/risc-v-international-2026-iommu-architecture.md)
- [Linux kernel low-level core APIs](../30-sources/linux-kernel-community-2026-low-level-core-apis.md)

### Research evidence

- [CleanQ: a lightweight, uniform, formally specified interface for intra-machine data transfer](../30-sources/haecki-et-al-2019-cleanq.md)
- [Thunderclap: exploring vulnerabilities in operating system IOMMU protection via DMA from untrustworthy peripherals](../30-sources/markettos-et-al-2019-thunderclap.md)
- [Tolerating malicious device drivers in Linux](../30-sources/boyd-wickizer-zeldovich-2010-malicious-device-drivers.md)
- [Arrakis: the operating system is the control plane](../30-sources/peter-et-al-2014-arrakis.md)
- [A least-privilege memory protection model for modern hardware](../30-sources/achermann-et-al-2019-least-privilege-memory-protection.md)
- [Recovering device drivers](../30-sources/swift-et-al-2004-recovering-device-drivers.md)

## Current conclusion

Protected DMA is an ownership and completion protocol built on, but not
equivalent to, an IOMMU. The recommended baseline blocks every requester,
binds independent requester, endpoint, interrupt, and reset scopes to one
unprivileged I/O service, restricts access to capability-named buffers, and
uses `EnforcedExclusive` transfer for a malicious native driver. Mappings and
operations remain generation-tagged, and revocation is incomplete until the
profile's device, translation, cache, interrupt, frame-authority, and transport
obligations are discharged.

This structure preserves the capability-microkernel boundary and supports
supervised native I/O services without putting managed-runtime policy in the
kernel. Its decisive remaining work is empirical: validate isolation groups,
coherency, resets, invalidation completion, and failure behavior on the first
target hardware before calling the note stable.
