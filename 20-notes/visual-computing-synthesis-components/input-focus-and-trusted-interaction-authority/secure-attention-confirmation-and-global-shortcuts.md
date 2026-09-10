---
title: "Secure attention, confirmation, and global shortcuts"
kind: note
created: "2026-09-10"
maturity: developing
tags:
  - secure-attention
  - trusted-path
  - visual-computing
aliases: []
---

# Secure attention, confirmation, and global shortcuts

This study decomposes [Input, focus, and trusted-interaction authority](../input-focus-and-trusted-interaction-authority.md).

Research question: Which interaction ceremonies must bypass ordinary clients,
and how are they bound to one principal, consequence, and current context?

## Research basis and status

Secure-interaction design emphasizes authentic parties and explicit authority.
Nitpicker and Qubes use trusted composition/labels to resist impersonation.
Android Protected Confirmation binds protected display and input to a
transaction message within a device-specific TEE profile.
[1](../../../30-sources/yee-2002-user-interaction-design-secure-systems.md)
[2](../../../30-sources/feske-helmuth-2005-nitpicker.md)
[3](../../../30-sources/qubes-project-2026-gui-virtualization.md)
[4](../../../30-sources/android-project-2026-protected-confirmation.md)

Atom's hardware-backed and accessible ceremony profiles remain unselected.

## Development

### Owned state and trust boundary

A trusted-path service owns reserved attention gestures, protected composition,
trusted origin markers, canonical consequence records, confirmation
generations, and shortcut namespace policy. Ordinary clients cannot intercept,
simulate, cover, or register the reserved path.

### Admission, transitions, and completion

Secure attention cancels ordinary capture, enters a fresh trusted generation,
renders the complete canonical prompt, and arms confirmation only after display
proof. Approval binds principal, operation digest, displayed consequence,
modality, generation, and expiry; any route, display, or policy change aborts.
Global shortcut allocation is namespaced and cannot shadow reserved gestures.

### Failure and adversarial behavior

Clickjacking, fake chrome, stale prompts, rapid replacement, inaccessible
confirmation, remote-seat substitution, and overload threaten authenticity.
Protected origin, full-render-before-arm, explicit remote policy, independent
recovery reserve, and alternate trusted modalities address the stated model.

### Alternatives and unresolved tradeoffs

Prompts inside application pixels are flexible but spoofable. Hardware TEE UI
can be narrow but inaccessible and device-specific. A small software trusted
path with optional hardware confirmation is preferred; ceremony usability and
Dell T7500 hardware support need separate evaluation.

## Verification obligations

- Reproduce overlay, occlusion, cursor hiding, target movement, and fake-system
  prompt attacks against each ceremony.
- Interrupt display, input, broker, policy, and hardware confirmation at every
  state; no partial ceremony may yield approval.
- Test comprehension and completion with keyboard, screen reader, switch,
  voice, low vision, and authorized remote administration.

## Connections

- [Internal-service index](README.md) — trusted-interaction decomposition.
- [Trusted-interaction broker](../../authentication-and-authorization-components/trusted-interaction-broker.md) — general authorization ceremony.
- [Research session](../../../50-journal/2026-09-10-visual-computing-internal-services-deep-dive.md) — evidence limits.

## Sources

1. [User interaction design for secure systems](../../../30-sources/yee-2002-user-interaction-design-secure-systems.md).
2. [Nitpicker](../../../30-sources/feske-helmuth-2005-nitpicker.md).
3. [Qubes GUI virtualization](../../../30-sources/qubes-project-2026-gui-virtualization.md).
4. [Android Protected Confirmation](../../../30-sources/android-project-2026-protected-confirmation.md).
