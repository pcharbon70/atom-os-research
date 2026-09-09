---
title: "Remote PID/reference identity and route rebinding"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - actor-model
  - beam
  - managed-runtime
  - system-architecture
aliases: []
---

# Remote PID/reference identity and route rebinding

This study decomposes [Distribution gateway and remote actor semantics](../distribution-gateway-and-remote-actor-semantics.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

BEAM external identities include node creation; failure detection and transport replacement do not necessarily create a new remote actor. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md), [2](../../../30-sources/chandra-toueg-1996-failure-detectors.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Gateway authentication, transport sessions and BEAM node-incarnation identity are distinct. Compatible sends do not acquire delivery-completion results.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own a mapping from external PID/reference identity to authorized current route, with separate node creation and transport session generation. The same external term can remain valid across a reconnect to the same node incarnation; a restarted node is a different identity.

### Admission, transitions and completion

Resolve a send through the active authenticated route without rewriting term equality. Remove failed session bindings. Rebinding requires a peer with the same qualified node creation and fresh route authorization. Link/monitor relations terminated on disconnect are not automatically restored by rebinding.

### Failure and adversarial behavior

Treating every reconnect as a new PID breaks valid term identity; treating every node name as the same incarnation sends stale traffic to replacements. A noconnection observation reports relation loss, not proof that the remote process died.

### Alternatives and unresolved tradeoffs

Stable virtual-actor names can live above this service, but they are application identities resolved to particular actors, not substitutes for BEAM PID equality. A migration extension needs an explicit identity and ownership protocol.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Reconnect without node restart and preserve PID/reference equality while replacing route state.
- Restart under the same node name and reject old creation identifiers.
- Reconnect after monitor failure and verify no old monitor silently becomes active again.

Record the exact profile, tested revision, schedule/input bounds and resource
observations before claiming this contract holds. A semantic pass does not
establish latency or corruption containment.

## Connections

- [Component service index](README.md) — sibling responsibilities and shared boundaries.
- [Local order-preserving ingress](../signal-ingress-mailboxes-and-selective-receive/striped-ingress-order-and-node-reclamation.md) — a contract this service must compose with.
- [Disconnect knowledge and uncertainty](../failure-translation-and-the-otp-boundary/service-loss-uncertainty-and-supervisor-handoff.md) — a contract this service must compose with.
- [Open runtime inquiry](../../../40-inquiries/what-contract-should-the-managed-actor-runtime-provide.md) — unresolved design and evidence.
- [Research session](../../../50-journal/2026-09-09-managed-runtime-internal-services-deep-dive.md) — source manifest and reading limitations.

## Sources

1. [OTP 29.0.6 managed-runtime documentation](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md).
2. [Unreliable failure detectors](../../../30-sources/chandra-toueg-1996-failure-detectors.md).
