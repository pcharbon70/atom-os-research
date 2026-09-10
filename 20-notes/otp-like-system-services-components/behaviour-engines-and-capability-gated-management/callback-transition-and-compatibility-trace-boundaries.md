---
title: "Callback transition and compatibility trace boundaries"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - otp
  - system-services
  - service-architecture
aliases: []
---

# Callback transition and compatibility trace boundaries

This study decomposes [Behaviour engines and capability-gated management](../behaviour-engines-and-capability-gated-management.md).

Research question: Which evidence is needed before replacing an engine callback and its state schema?

## Research basis and status

OTP exposes explicit code-change hooks; F1 illustrates why valid endpoints do not
imply safe intermediate schemas. [1](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md) [2](../../../30-sources/rae-et-al-2013-online-schema-change-f1.md)

The Development section is an Atom OS proposal, not a source guarantee or an
implemented result. Evidence applies only within each source's stated model;
the references below retain those limits.

## Development

### Owned state and trust boundary

The transition coordinator owns old/new callback digests, schema relation, saved
engine envelope and transition token. It does not own BEAM code loading, garbage
collection or stack safety; those remain managed-runtime contracts.

### Admission, transitions and completion

Close relevant admission, settle or explicitly retain outstanding calls, reach a
runtime-supported safe point and transform into private state. Validate timers,
deferred replies and event interpretation against the new schema. Publish callback
and engine-state identity together, then resume only with the matching token.

### Failure and adversarial behavior

An exception during transformation must leave an intact old state or a quarantined
target. A successful state conversion does not establish that old continuations or
queued messages remain meaningful. Purging old code cannot be used as a substitute
for enumerating those obligations.

### Alternatives and unresolved tradeoffs

Generation replacement offers a simpler failure boundary than in-place conversion
but requires state export and more resources. Strict OTP release behavior is
separately versioned and tested; native replacement is not automatically an
equivalent hot-code update.

## Verification obligations

These are unexecuted falsifiers, not passed tests:

- Retain an old-format postponed event and a deferred reply through transition; verify declared conversion or explicit rejection.
- Crash before and after callback/state publication and require a consistent pair on recovery, never mixed schema and code.

Any claimed result must identify the implementation revision, admitted state
bounds, trust and failure profile, injected schedule and raw outcome history.
Check both invariant preservation and progress under explicit assumptions.

## Connections

- [Internal-service index](README.md) — sibling responsibilities and scope.
- [Supervision and recovery policy](../supervision-and-recovery-policy/README.md) — owns restart admission, quarantine and escalation.
- [Observability, audit, alarms, and operator control](../observability-audit-alarms-and-operator-control/README.md) — separates diagnostic, audit and operator-control obligations.
- [Open Layer 4 inquiry](../../../40-inquiries/what-contract-should-the-otp-like-system-services-layer-provide.md) — unresolved architecture qualification.
- [Research session](../../../50-journal/2026-09-10-otp-system-services-internal-services-deep-dive.md) — sources, method and limitations.

## Sources

1. [OTP 29.0.6 system-services documentation](../../../30-sources/erlang-otp-team-2026-otp-29-0-6-system-services-documentation.md).
2. [Online schema change in F1](../../../30-sources/rae-et-al-2013-online-schema-change-f1.md).
