---
title: "Gateway session authentication and profile negotiation"
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

# Gateway session authentication and profile negotiation

This study decomposes [Distribution gateway and remote actor semantics](../distribution-gateway-and-remote-actor-semantics.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

PARTISAN makes topology replaceable; standard distribution documentation supplies interoperability behavior rather than automatic capability attenuation. [1](../../../30-sources/meiklejohn-et-al-2019-partisan.md), [2](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Gateway authentication, transport sessions and BEAM node-incarnation identity are distinct. Compatible sends do not acquire delivery-completion results.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own bounded handshake state, authenticated peer identity, selected protocol/profile, route authority and session epoch. A session is not established merely because a TCP or encrypted connection exists. Standard trusted distribution and a restricted Atom gateway are distinct profiles.

### Admission, transitions and completion

Negotiate supported features, limits and identity bindings before exposing routes. Admit only authorized operations and reserve control/data capacity. Bind subsequent frames to the authenticated session; close admission before draining on disconnect or policy revocation.

### Failure and adversarial behavior

Authentication alone does not authorize unrestricted node operations. Downgrade, replay and profile mismatch must fail without interning unbounded atoms or publishing routes. Kernel network/device isolation cannot stop an authorized gateway from exercising excessive application authority.

### Alternatives and unresolved tradeoffs

A standard OTP adapter maximizes interoperability but inherits its declared trust assumptions. A restricted protocol improves mediation but may not interoperate transparently. Document the distinction rather than relabeling a custom secure transport as standard distribution.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Replay a previous session handshake and frame sequence.
- Negotiate incompatible signal/ETF features and verify no route publication.
- Exhaust data credits while preserving bounded authenticated close/control handling.

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

1. [PARTISAN](../../../30-sources/meiklejohn-et-al-2019-partisan.md).
2. [OTP 29.0.6 managed-runtime documentation](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md).
