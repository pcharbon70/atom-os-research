---
title: "2026-09-21 — M0 phase 03 section 3.1 qualification"
kind: journal
created: "2026-09-21"
tags:
  - implementation-planning
  - m0
  - proof-of-concept
aliases: []
---

# 2026-09-21 — M0 phase 03 section 3.1 qualification

Section 3.1 produced and exercised the host acceptance harness, moved physical
inventory collection out of M0, and assembled a clean virtual M1 input bundle.
The run supports closing `m0-p03-harness` and `m0-p03-qualify`; it does not
close the phase integration or handoff tasks and demonstrates no guest boot,
native CLI, ring-3 transition, or physical Kay OS execution.

## Plan and acceptance baseline

The execution implements [M0 Phase 3 Section 3.1](../60-planning/01-proof-of-concept/m0-boot-inputs/phase-03-acceptance-harness-and-input-qualification.md)
at Kay OS revision `8206deb663ce9f651c140d8f08b76411f6c3a73b`.
Its stable task IDs are `m0-p03-harness`, `m0-p03-inventory`, and
`m0-p03-qualify`; the contributed artifacts are M0-A01 through M0-A07 and the
directly exercised case portion is M0-T05 plus the M0-T06 non-consumption
boundary.

The fixed harness limits were first output 5 seconds, response 2 seconds,
stall 3 seconds, total run 30 seconds, and cleanup grace 5 seconds. The test
oracle was the explicitly controlled `KAY-HARNESS/1` host fixture, not Kay OS,
Limine, QEMU serial output, or a delivered CLI. Physical observation remained
deferred to `m1-p04-inventory` and was prohibited from the virtual bundle.

## Environment and provenance

- Implementation repository: `https://pushin.eu/pcharbon70/kay-os.git`.
- Tested commit: `8206deb663ce9f651c140d8f08b76411f6c3a73b`; dirty-file count recorded by the bundle assembler: `0`.
- Harness interpreter: Python 3.12.12 at `/home/ducky/.asdf/installs/python/3.12.12/bin/python3`, SHA-256 `7960acf7a77624badfb1e4326dfa373a754854aaffb52420e641d53add83bea2`.
- Harness policy SHA-256: `9e2fc22ec257db2dbb122c32b0534a315542c49bee36b531ea3097edad3b6691`.
- Harness driver SHA-256: `b05cb600bd06ebd4864e53e41379bd2d162cc579b58ce644f24b8b3387424696`.
- Controlled fixture SHA-256: `374aa55d5bb9f13e7560843f437b7c32c2957ca51b3ae85dbcac7bb69e1a7f8c`.
- Evidence root: `/tmp/kay-m0-p03-section31-clean.FyJWsP`; this is local raw evidence outside Git, not a permanent archive attachment.
- M1 input manifest SHA-256: `abd5b99c7a90e7ec2bc78d54e08934c1668111c03071f87c55bb3fa9b7127694`.
- M1 bundle hash-list SHA-256: `ce2741675b48fdb0cd2b59637576ac3c9d853e18858dcaea42355573f1cdefb5`.

The run was hosted. It exercised process launch, PTY exchange, timing,
cleanup, evidence capture, publication-policy fixtures, and virtual bundle
assembly. QEMU, firmware, loader, and kernel were inputs copied by identity;
none was executed by this section-level test.

## Execution and results

| Task / case IDs | Fixture and exact command | Expected result | Actual observation | Result | Raw evidence / artifact identity |
| --- | --- | --- | --- | --- | --- |
| `m0-p03-harness`; `m0-p03-h01-success`; `m0-p03-n01`–`m0-p03-n08` | `python3 scripts/m0/verify-phase-03-section-31.py --output-dir /tmp/kay-m0-p03-section31-clean.FyJWsP/section31` | One success case passes; eight declared failure modes are detected; every process group is cleaned up. | All nine registered cases passed their expected interpretation. Negative driver exits were 20 through 26 as assigned; every row recorded `cleanup_complete=true`. | pass | `/tmp/kay-m0-p03-section31-clean.FyJWsP/section31/harness/case-results.tsv`; policy and tool hashes above |
| `m0-p03-inventory`; M0-T06 boundary | Same Section 3.1 verifier, using controlled safe, sensitive, and pending-review publication fixtures | Safe allowlisted data passes; identifier-like data and unapproved publication fail; retired physical-input bundle option is rejected. | All four boundary checks passed. No physical fixture was queried and no physical record was created. | pass | `/tmp/kay-m0-p03-section31-clean.FyJWsP/section31/case-results.tsv` |
| `m0-p03-qualify` | `python3 scripts/m0/assemble-m1-input-bundle.py --harness-evidence /tmp/kay-m0-p03-section31-clean.FyJWsP/section31/harness --output-dir /tmp/kay-m0-p03-section31-clean.FyJWsP/m1-input-bundle` | On a clean committed revision, copy the required virtual inputs and complete harness evidence; reject physical inventory as an input. | Bundle assembled at the exact clean commit with dirty count zero. Its manifest states `physical_inventory: not-consumed-owned-by-m1-p04-inventory`. | pass | Manifest SHA-256 `abd5b99c7a90e7ec2bc78d54e08934c1668111c03071f87c55bb3fa9b7127694`; bundle hash-list SHA-256 `ce2741675b48fdb0cd2b59637576ac3c9d853e18858dcaea42355573f1cdefb5` |
| `m0-p03-integration`; M0-T01–M0-T06 assembled rerun | Not run in Section 3.1 | Full phase driver reruns inherited M0 gates and final harness cases against one clean bundle. | Reserved for Section 3.2; no result inferred from component tests. | not run | No Section 3.2 artifact yet |

An earlier development run correctly reported
`pass-with-clean-bundle-pending` because the implementation worktree was still
dirty. The final assembler invocation above was deliberately repeated after
the Section 3.1 commit and accepted the clean revision. This preserves the
difference between development checks and qualification evidence.

## Review and handoff

The implementation agent reviewed the case table, tool identities, manifest,
dirty-state count and bundle hashes. Section 3.1 may proceed to the final
integration section. Independent final review, the assembled M0-T01–M0-T06
rerun, and the user/project-owner handoff decision remain pending, so Phase 3
and M0 remain open.

Changes to the fixed timing policy, protocol, required virtual-input list,
clean-tree rule, or physical-inventory exclusion reopen the affected Section
3.1 evidence. The tested commit above is not yet a merge revision. This
research record will necessarily be committed after the tested Kay OS commit;
neither future commit nor merge provenance is treated as tested here.

## Follow-ups

- Implement and run `m0-p03-integration` for all M0-T01 through M0-T06.
- Retain the full phase results and review decision before closing
  `m0-p03-handoff`.
- Collect a named physical fixture only under M1 Phase 4 and compare its
  external observation with Kay OS's own runtime discovery report.
