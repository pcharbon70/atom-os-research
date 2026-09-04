---
title: "What contract should system-wide authentication and authorization provide?"
kind: inquiry
created: "2026-09-04"
status: open
tags:
  - authentication
  - authorization
  - capabilities
  - distributed-systems
  - operating-systems
  - security
aliases:
  - "Atom OS authentication and authorization contract"
---

# What contract should system-wide authentication and authorization provide?

## Why this matters

Authentication and authorization determine whether every other isolation,
recovery, update, persistence, networking, and administrative claim can be
trusted. A secure kernel can still host an insecure system if a spoofable UI,
overpowered policy service, stale distributed decision, bearer credential,
weak recovery path, or ambient shell privilege can mint or misuse authority.

The current synthesis proposes a two-plane architecture, but the concrete
deployment profile, native login ceremony, authority algebra, policy schema,
hardware roots, consistency bounds, and recovery model are still unimplemented
and therefore unresolved.

## Operational question

What minimal, testable contract lets Atom OS accept human, workload, node, and
recovery evidence; issue only justified attenuated authority; mediate every
protected effect; revoke and drain that authority under crash and partition;
and preserve useful audit evidence without placing identity policy or complex
protocol parsers in the privileged kernel?

An answer is adequate only if it specifies and tests:

- the exact principal, evidence, session, policy-query, grant, capability,
  revocation, completion, and audit schemas;
- the boot manifest and all roots of authority, including anonymous/bootstrap,
  update, storage-key, audit, debug, and recovery roots;
- complete mediation and non-amplification from boot through local and remote
  effects;
- authenticator enrollment, use, downgrade resistance, inventory, removal,
  lock/resume, logout, and separate credential/data/factory recovery;
- workload identity, measured boot, attestation appraisal, node join/removal,
  snapshot and clone behavior;
- policy semantics, atomic activation, relation consistency, cache keys,
  issuer fencing, replay consumption, and partition behavior;
- maximum stale-authority and revocation-exposure bounds per operation class;
- crash-consistent grant issue, idempotency consumption, effect admission,
  audit admission, quiescence, sanitization, and uncertainty reporting; and
- the exact hardware, compiler, runtime, policy, time, network, usability, and
  operational assumptions supporting each assurance claim.

The contract is falsified by any protected effect with no enforcement point,
any capability not rooted in the checked boot authority graph, any authority
amplification through transfer or restart, any unauthenticated path to a
non-public object, any policy or revocation failure that broadens authority,
any resource rename/recreation that resurrects a grant, any unbounded
pre-authentication or revocation work, or any recovery path that acts as an
unreported universal decryption or administrator key.

## Working hypotheses

- Authentication and rich policy belong in separately confined layer-4
  services; the layer-2 kernel should enforce only typed objects, capabilities,
  generations, budgets, admission, and revocation state.
- An explicit anonymous principal with manifest-declared public/bootstrap
  capabilities is safer and easier to test than a missing-login special case.
- Human login should be phishing-resistant public-key authentication over a
  protected Atom-specific ceremony; privileged actions need request-bound
  hardware-key step-up and sometimes threshold approval.
- PIDs, names, UIDs, paths, roles, attributes, certificates, and attestation
  measurements designate or describe; only a bounded capability presented at
  the effect boundary authorizes local execution.
- ReBAC should express ownership and sharing, RBAC should express job roles and
  separation of duty, ABAC should supply authoritative short-lived context,
  and a pure typed policy engine should compile the combination into
  capabilities.
- Remote proof should terminate at a confined gateway. Short-lived mutual-TLS
  workload credentials are the default between nodes; OAuth is an external
  federation profile; bearer JWTs are compatibility-only.
- Revocation needs local generations and anchors, bounded leases, ordered
  distributed watermarks, operation-specific in-flight semantics, and an
  explicit maximum exposure window. Offline authority cannot promise immediate
  global revocation or enforce a global consumptive quota.
- Recovery should authenticate a distinct principal and issue narrow one-shot
  authority. Credential recovery, data-key recovery, and destructive reset
  require separate designs and disclosure.
- Security services must be split so no one domain can edit policy, verify any
  identity, mint arbitrary grants, suppress revocation, delete audit, update
  the platform, and invoke recovery.

## Paths to explore

### Formal and executable models

- Use the [sixteen component implementation
  reports](../20-notes/authentication-and-authorization-components/README.md)
  as the initial state-machine and message-schema inventory, then check their
  shared generations, request digests, evidence revisions, permit receipts,
  issuer envelopes, revocation watermarks, and effect outcomes for gaps or
  contradictory ownership.
- Model the authority graph, attenuation order, transfer, generation reuse,
  delegation depth, budgets, revocation traversal, and bootstrap authority.
- Specify state machines for enrollment, login, session fixation prevention,
  step-up, lock, suspend, snapshot, logout, recovery, grant issue, policy
  activation, partition, audit outage, and effect completion.
- Build a small reference policy semantics and grant compiler, prove key
  properties, and differentially test the eventual implementation.

### Target and trusted interaction

- Select the first deployment profile and board, then inventory privilege
  modes, MMU/PMP, IOMMU, TPM or DICE, rollback-resistant state, entropy,
  trusted display/input, removable authenticators, suspend, and storage.
- Specify the native relying-party ID and canonical request encoding and model
  WebAuthn/CTAP composition, concurrent ceremonies, authenticator management,
  and downgrade.
- Prototype trusted paths for local, multi-seat, accessible, remote, and
  headless environments and test spoofing and coercion resistance with users.

### Policy, distribution, and failure

- Define entity, action, resource, relationship, attribute, obligation, and
  assurance schemas plus atomic model activation and rollback protection.
- Measure policy evaluation, causal-relation lookup, cache invalidation,
  revocation propagation, issuer fencing, replay-store availability, and
  audit-spool limits under load and partition.
- Fault-inject grant-issuer and resource crashes around durable release,
  idempotency consumption, effect commit, and audit admission.
- Decide which low-risk rules are monotonic enough for bounded-stale reads and
  which always require causally complete current state.

### Recovery, storage, and operations

- Choose explicit credential-recovery, encrypted-data-recovery, and factory-
  reset profiles and document every decryption authority.
- Exercise authenticator loss, quorum-member replacement, recovery-code use,
  cooling-off, owner notification, cancellation, break-glass, key rotation,
  audit outage, and boot rollback.
- Define session and key behavior across lock, suspend, hibernate, VM snapshot,
  restore, migration, and cloned instances.

## Findings

The current [authentication and authorization synthesis](../20-notes/authentication-and-authorization-across-the-five-layer-architecture.md)
finds that the strongest fit is an identity/policy control plane plus a
capability data plane. It defines the chain from evidence to mediated effect,
assigns responsibilities across all five layers, and proposes concrete query,
grant, revocation, recovery, audit, and failure contracts.

The [authentication and authorization map](../10-maps/authentication-and-authorization.md)
organizes the supporting primary research and standards. The [2026-09-04 research journal](../50-journal/2026-09-04-authentication-and-authorization-deep-dive.md)
records source versions, method, and evidence boundaries.

The [component implementation deep
dives](../20-notes/authentication-and-authorization-components/README.md)
now develop all sixteen proposed layer-4 services individually. Their shared
conclusion is that architectural separation must be enforced by distinct
unprivileged Layer-4 service domains isolated by Layer 2 and by narrowly
delegated facets, not merely by actor names or supervision inside one mutually
trusting runtime. Every service protocol has
typed negative and uncertain outcomes; outage, stale state, overload, restart,
or malformed input must never widen authority. The policy-enforcement point at
the resource remains authoritative even after a permit has been evaluated or
a grant has been compiled.

The [component research journal](../50-journal/2026-09-04-authentication-and-authorization-components-deep-dive.md)
records the exact new and reused evidence for that expansion, as well as the
cross-service lifecycle model, evaluation program, falsifiers, and unresolved
hardware, usability, consistency, and proof obligations.

The literature supports the components but does not settle their Atom-specific
composition. In particular, WebAuthn does not specify a native OS trusted path;
TPM/DICE and RATS do not decide resource policy; Cedar does not provide kernel
enforcement; Zanzibar's consistency design does not solve every offline or
consumptive authorization problem; and seL4 or CHERI proofs do not transfer to
this future system.

## Outcome

The inquiry remains open. The architecture is developed enough to guide a
formal model and first single-node prototype, but it should not be resolved
until one deployment profile has passed authority-graph modeling, trusted-path
testing, parser and policy fuzzing, crash/partition/revocation fault injection,
recovery drills, and end-to-end complete-mediation review.
