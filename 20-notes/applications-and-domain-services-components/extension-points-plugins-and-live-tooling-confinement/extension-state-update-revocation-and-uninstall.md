---
title: "Extension state, update, revocation, and uninstall"
kind: note
created: "2026-09-09"
maturity: developing
tags:
  - application-architecture
  - domain-modeling
  - system-architecture
aliases: []
---

# Extension state, update, revocation, and uninstall

This study decomposes [Extension points, plugins, and live-tooling confinement](../extension-points-plugins-and-live-tooling-confinement.md).

Research question: What survives an extension replacement, and what does revocation actually stop?

## Research basis and status

NixOS separates immutable configuration generations from mutable activation effects; selecting an old generation does not undo domain state. [1](../../../30-sources/dolstra-et-al-2008-nixos.md).

Crash-only design puts authoritative state outside replaceable components; restarting cannot repair every corruption or ambiguous effect. [2](../../../30-sources/candea-fox-2003-crash-only-software.md).

The model below is proposed Atom OS architecture, not a result demonstrated by
these sources. Layer 5 owns domain meaning; lower layers enforce authority,
durability and resource limits. This is full-system research, independent of
proof-of-concept plans, QEMU configuration and kernel-language implementation.

## Development

### Owned state and trust boundary

Own extension-private durable schema, host compatibility, invocation inventory and
uninstall retention policy. State is namespaced by extension, application generation
and authenticated realm. Host domain truth contains validated facts, not opaque
plugin memory or a promise to reload arbitrary old code.

### Admission, transitions and completion

Close old invocation admission, revoke relevant imports, finish or transfer accepted
responsibilities and prepare compatible state privately. Publish a replacement only
after validation and required quiescence. Uninstall explicitly retains, exports or
deletes user-authored data under policy while keeping necessary outcome and repair
evidence.

### Failure and adversarial behavior

Killing the host cannot prove an effect never occurred. An old result can arrive
after the new extension is active; generation checks prevent accidental acceptance.
Deleting old code may strand required compensation or state readers. Revocation
cannot retract information already disclosed to an extension.

### Alternatives and unresolved tradeoffs

Discarding derived caches makes replacement simple, but user-authored extension data
needs a different lifecycle. Retaining old generations eases compatibility yet
increases storage and attack surface. Research retirement conditions from
outstanding references and obligations rather than elapsed time alone.

## Verification obligations

These are unexecuted falsifiers, not passing tests:

- Revoke during computation and during a durably accepted effect; distinguish discardable output from persistent responsibility.
- Uninstall with old schema data and pending repair; verify the explicit export, retention and reader-code dependencies.

Record the exact protocol and storage profile, tested revision, input/history
bounds, observed results and residual uncertainty. A semantic test does not
establish a hard latency bound, physical durability or protection against a
compromised enforcement layer.

## Connections

- [Component service index](README.md) — sibling ownership and research boundaries.
- [Recipient-bound composition and installer retirement](../application-manifest-composition-and-authority-envelope/recipient-bound-composition-and-installer-retirement.md) — a cross-component contract this service must preserve.
- [Placement contracts and independent boundary selection](../cross-layer-placement-tenancy-overload-and-recovery-topology/placement-contracts-and-independent-boundary-selection.md) — a cross-component contract this service must preserve.
- [Open application inquiry](../../../40-inquiries/how-should-atom-os-structure-applications-and-domain-services.md) — unresolved evidence and competing designs.
- [Research session](../../../50-journal/2026-09-09-application-domain-internal-services-deep-dive.md) — exhaustive source manifest and reading limits.

## Sources

1. [NixOS](../../../30-sources/dolstra-et-al-2008-nixos.md).
2. [Crash-only software](../../../30-sources/candea-fox-2003-crash-only-software.md).
