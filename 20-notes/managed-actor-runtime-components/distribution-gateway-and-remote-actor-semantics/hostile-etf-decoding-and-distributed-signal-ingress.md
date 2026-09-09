---
title: "Hostile ETF decoding and distributed signal ingress"
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

# Hostile ETF decoding and distributed signal ingress

This study decomposes [Distribution gateway and remote actor semantics](../distribution-gateway-and-remote-actor-semantics.md).
The question is how this service can own a narrow, testable contract without
silently widening compatibility, authority or the failure boundary.

## Research basis and status

A wire-format decoder and a safety policy are separate checks; structurally valid external terms can still exceed resources or invoke unsupported semantics. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-managed-runtime-documentation.md), [2](../../../30-sources/necula-1997-proof-carrying-code.md).

The protocols below are **proposed Atom OS architecture**, not upstream
implementation facts or completed tests. Gateway authentication, transport sessions and BEAM node-incarnation identity are distinct. Compatible sends do not acquire delivery-completion results.
This is full-system research, not a proof-of-concept phase or platform setup.

## Development

### Owned state and trust boundary

Own frame/decompression budgets, parser arena, provisional atoms, peer charge and decoded signal envelope. All lengths, nesting, big integers, binaries and function/reference encodings are untrusted. Native pointers and adapter authority have no wire representation.

### Admission, transitions and completion

Authenticate and frame before bounded decoding. Validate node creation, feature flags and allowed control operations; commit admitted atoms only after full validation and reservation. Publish through the same generation-aware signal ingress used locally, retaining the declared per-sender ordering scope.

### Failure and adversarial behavior

A compressed atom flood can consume permanent global state if decoding interns eagerly. A malformed fun or reference can cross into execution metadata. Dropping an admitted distributed relation signal without the profile's failure handling can leave false live state.

### Alternatives and unresolved tradeoffs

A generic ETF library reduces code duplication but its allocation, atom and depth policy must be audited. A restricted streaming decoder can reject earlier but still needs complete-frame ownership and rollback rules. Neither is trusted merely because it is written in a memory-safe language.

## Verification obligations

The following are unexecuted falsifiers, not passing acceptance evidence:

- Fuzz decompression ratio, term depth, atom growth and malformed PID/fun encodings.
- Reject unauthorized distribution control operations after valid authentication.
- Verify rejected frames return credits without mutating permanent atoms or actor relations.

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
2. [Proof-carrying code](../../../30-sources/necula-1997-proof-carrying-code.md).
