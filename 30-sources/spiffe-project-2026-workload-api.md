---
title: "The SPIFFE Workload API"
kind: source
created: "2026-09-03"
authors:
  - "SPIFFE Project"
published: null
citation_key: "spiffe-project-2026-workload-api"
container: "SPIFFE standards"
edition: "Git revision 99470b9abc825f14aa364dfa2c3b53b02ba5db5b; stable core with incubating WIT-SVID profile"
isbn: null
doi: null
url: "https://github.com/spiffe/spiffe/blob/99470b9abc825f14aa364dfa2c3b53b02ba5db5b/standards/SPIFFE_Workload_API.md"
accessed: "2026-09-03"
tags:
  - authentication
  - distributed-systems
  - service-identity
  - workload-identity
aliases:
  - "SPIFFE Workload API"
---

# The SPIFFE Workload API

## Reference

SPIFFE Project. “[The SPIFFE Workload
API](https://github.com/spiffe/spiffe/blob/99470b9abc825f14aa364dfa2c3b53b02ba5db5b/standards/SPIFFE_Workload_API.md).”
Living SPIFFE standard pinned at revision
`99470b9abc825f14aa364dfa2c3b53b02ba5db5b`, accessed 2026-09-03. The
[canonical moving document](https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE_Workload_API.md),
normative
[`workloadapi.proto`](https://github.com/spiffe/spiffe/blob/99470b9abc825f14aa364dfa2c3b53b02ba5db5b/standards/workloadapi.proto)
and the companion [Workload Endpoint
specification](https://github.com/spiffe/spiffe/blob/99470b9abc825f14aa364dfa2c3b53b02ba5db5b/standards/SPIFFE_Workload_Endpoint.md)
were also read to establish the transport and caller-identification assumptions.
The Workload API document is marked stable except for its incubating WIT-SVID
profile.

## Research question or contribution

What portable local interface lets a workload bootstrap, retrieve, refresh,
and validate SPIFFE identity material and trust bundles without embedding one
orchestrator's credential-delivery mechanism in the workload?

The standard defines interoperable gRPC and Protocol Buffers profiles for
X.509-SVID, JWT-SVID, and optionally WIT-SVID material. It specifies client and
server state transitions, full-snapshot streaming, redaction behavior, and
federated trust-bundle handling; it does not specify application authorization
policy.

## Method

This is a normative interoperability specification rather than an experiment.
The Workload API Markdown, its protocol definition, and the companion Workload
Endpoint requirements were read together. Normative requirements were
separated from reference state machines and implementation choices. No claim
about performance, availability, or one particular SPIRE deployment is inferred
from conformance language alone.

## Findings

- The API is served by a SPIFFE Workload Endpoint as a gRPC service defined in
  Protocol Buffers version 3. X.509-SVID and JWT-SVID profiles are mandatory
  for an implementation, although an operator may disable either; the current
  WIT-SVID profile is optional and incubating.
- Identity bootstrap deliberately has no direct client authentication handshake
  or pre-shared workload token. The local endpoint implementation must identify
  its caller out of band, for example from kernel socket/process information or
  trusted orchestrator placement. The companion endpoint specification prefers
  a Unix-domain socket, discourages one endpoint instance from spanning hosts,
  and permits TCP only where the network supplies strong caller attribution.
- Long-lived server streams distribute X.509 identity material and trust-bundle
  updates. Clients should reconnect after stream loss. Each streamed response
  is a complete snapshot rather than a delta, so an empty/default field replaces
  an old value and omitted previously present data is treated as redacted and
  removed. This avoids a separate anti-entropy protocol but makes correct
  snapshot replacement essential.
- An X.509 response can contain every SVID to which the caller is entitled,
  each SVID's certificate chain and unencrypted PKCS#8 private key, its trust-
  domain bundle, revocation lists, and authorized foreign bundles. These are
  sensitive local materials whose confinement is an endpoint and operating-
  system responsibility.
- JWT-SVID issuance is audience-bound. The API can validate a presented token
  for a requested audience or provide JWT trust bundles for a workload that
  performs validation itself. Validation must select the bundle matching the
  subject's trust domain; if no matching bundle exists, the peer is untrusted.
- Federated bundles enable credential authentication across explicitly supplied
  trust domains. A subsequently redacted bundle must stop being used; receiving
  a bundle is not a grant of arbitrary authority to every identity in that
  domain.
- X.509 and WIT responses may contain multiple identities. The first is the
  default for clients unaware of multiple identities, while operator-defined
  hints can guide aware clients. The standard leaves the choice of which
  identity to assume and the meaning of hints to site policy.
- Update timing is implementation-specific. The standard warns that clients
  which do not receive updates can become stale and unavailable, and that
  synchronized mass reloads can themselves cause outages; a server may apply
  jitter when pushing widespread updates.

## Relevance

The Workload API offers a model for an Atom OS local identity broker. The
broker can obtain generation-bound caller evidence from a trusted kernel or
orchestrator channel, bind it to a protected-domain incarnation, select the
identities that caller is entitled to receive, and stream complete credential
and trust snapshots through a confined local endpoint.
Explicit snapshot replacement and redaction are useful semantics for credential
rotation because clients do not have to infer whether a missing bundle is merely
an omitted delta.

SPIFFE also reinforces three separate system-service concepts. A service name
locates candidates, an SVID authenticates the instance presenting its key, and
a capability or authorization decision determines what that instance may do.
Authenticated identity is not authorization: validating an SVID must never be
treated as permission to invoke every operation or acquire a lease. The
authorization policy must separately bind the authenticated identity, requested
operation, resource scope, and current policy or fencing generation.

For Atom OS, trust domains could align with explicit distribution and
administrative scopes, with foreign bundles admitted only through deliberate
federation policy. Copying the exact gRPC wire format is not required. A native
interface could preserve caller attribution, full-snapshot replacement,
redaction, trust-domain constraints, and JWT-specific audience binding while
using capability-protected channels or non-exportable key handles where
hardware and compatibility permit.

## Limits

The standard is a living document; this note pins the revision read, and future
changes require a new provenance check. Its core is marked stable, but the
WIT-SVID profile is explicitly incubating. It provides neither
performance evaluation nor a liveness bound for issuance, rotation, revocation,
stream reconnection, or recovery when the local identity agent or upstream
authority is unavailable.

Caller authentication is intentionally out of scope for the Workload API and
depends on the endpoint implementation. Weak socket confinement, reused process
identifiers, forged orchestrator metadata, or an over-privileged identity agent
can therefore break the bootstrap trust boundary. The API also does not define
workload attestation, registration policy, application authorization, capability
delegation, service discovery, consensus membership, lease authority, or
Byzantine-fault handling.

The standard returns private-key bytes for the X.509 and WIT profiles. That is
an interoperability fact, not evidence that exporting raw keys is the best Atom
OS implementation. Key confinement or hardware-backed handles would require a
separate profile and compatibility analysis. Likewise, receiving a valid SVID
proves only what its issuer, validity interval, key possession, and selected
trust bundle establish; it does not prove that the principal is uncompromised
or currently authorized for an application operation.

## Derived work

- [OTP-like system services layer](../20-notes/otp-like-system-services-layer.md)
- [OTP-like system services map](../10-maps/otp-like-system-services.md)
- [OTP-like system-services contract inquiry](../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md)
- [2026-09-03 OTP-like system services deep dive](../50-journal/2026-09-03-otp-like-system-services-deep-dive.md)
