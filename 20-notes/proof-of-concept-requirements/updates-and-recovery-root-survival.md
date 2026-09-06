---
title: "Updates and recovery-root survival"
kind: note
created: "2026-09-06"
maturity: developing
tags:
  - capability-roadmap
  - proof-of-concept
  - requirements
aliases: []
---

# Updates and recovery-root survival

Requirement R19, after M4. Safely select and activate a new system image, preserve recoverable state, and define what happens when the recovery controller itself fails.

## Evidence and distinct mechanisms

[The Update Framework specification](../../30-sources/tuf-project-2026-specification-1-0-36.md) separates signed metadata roles, thresholds, versioning and freshness checks. It addresses trusted acquisition, not the complete installation, boot-selection or data-migration transaction.

[The firmware-update architecture](../../30-sources/moran-et-al-2021-firmware-update-architecture.md) discusses verification and recovery-image arrangements. It is architectural guidance, not a universally safe A/B activation protocol.

[FSCQ's crash-aware approach](../../30-sources/chen-et-al-2015-fscq.md) reinforces the need to include recovery interruptions in state-transition reasoning. Its filesystem proof does not establish Atom update correctness.

Compare immutable image replacement with in-place live patching. Prefer a proposed inactive-image/trial-boot approach first: it limits live mutation, but still requires durable selection, health confirmation and rollback rules.

## Proposed update state machine

Record trusted root metadata, accepted artifact identity, target hardware/profile, image generation and data-schema compatibility. Verify acquired metadata and content before granting an image execution authority. A valid signature alone does not prove freshness or compatibility.

Stage the new image outside the active slot, verify it, then publish a durable trial-selection record. Define exactly what survives interruption before and after each write. The boot selector must distinguish incomplete staging, an unconfirmed trial and a confirmed active image.

Use a bounded health-confirmation protocol that proves required services actually started. A banner printed by the new image is not sufficient. Maintain a prepositioned known-good recovery path with enough resources to execute.

Define trusted time or another explicit freshness strategy for metadata expiry. The initial PoC only has monotonic uptime; that does not automatically provide a trustworthy civil clock across resets.

## Data migration and rollback cutoff

Image rollback is unsafe if the new image has already written data the old image cannot interpret. Declare compatible schema ranges, migration ownership and the point after which old-image rollback is forbidden or requires data restoration.

Choose between backward-compatible writes, copy-on-write migration with a recoverable selection point, and a separately verified restoration path. Each has storage and failure costs. Do not promise arbitrary rollback merely because two executable slots exist.

Protect version/freshness state against the rollback threat in the chosen deployment profile. If malicious storage rollback is outside the initial threat model, state that exclusion instead of claiming hardware-backed anti-rollback.

## Recovery-root failure and takeover

M4 may reset the machine if outer recovery fails. Surviving that failure requires an independent controller or boot path with preassigned authority and capacity; spawning another process inside the failed controller's resource domain is insufficient.

A takeover must retire the old controller's execution and authority before enabling a conflicting replacement. Account for delayed commands, child ownership, outstanding faults, registry generations and reserved replacement slots. Two active controllers must not both believe they own the same lifecycle transitions.

Firmware or kernel compromise remains outside a user-space recovery service's power to repair unless an independently trusted mechanism exists.

## Acceptance and next exploration

Inject interruption at every acquisition, staging, selection, trial, confirmation and migration boundary, including recovery. Test expired metadata, old-but-valid signatures, wrong-platform images, failed health checks, full staging storage and failure of the recovery controller during child replacement.

Retain the boot decision, image/schema generations and authority-owner transitions for each case. The next artifact is a combined image/data/root-takeover state machine under one explicit threat and persistence model.

No updater, secure boot chain, anti-rollback mechanism or recovery-root replacement was implemented or tested here.

## Connections

[Durability](durable-state-and-crash-consistency.md), [authentication](authentication-and-administration-profile.md) and [independent recovery](supervision-and-independent-recovery.md) supply the required lower-level contracts.
