---
title: "2026-09-21 — M0 phase 03 integration"
kind: journal
created: "2026-09-21"
tags:
  - implementation-planning
  - m0
  - proof-of-concept
aliases: []
---

# 2026-09-21 — M0 phase 03 integration

The clean Phase 3 driver passed all seven registered assembled results after
rerunning the 24-case Phase 2 gate, its Phase 1 regression, the nine-case host
harness, clean virtual M1 bundle assembly, and a missing-harness negative
probe. This closes `m0-p03-integration` at the tested revision. The
user/project-owner handoff decision remains pending, so Phase 3 and M0 are not
declared accepted by this record alone.

## Plan and acceptance baseline

The run implements [M0 Phase 3 Section 3.2](../60-planning/01-proof-of-concept/m0-boot-inputs/phase-03-acceptance-harness-and-input-qualification.md)
and evaluates M0-T01 through M0-T06 using Kay OS commit
`2d41f3975cbecb4e5ebcddb57840503898380dc8`. The exact Phase 3 manifest
contains seven rows: six assembled milestone results and one missing-harness
negative result. Required inherited observations remain owned by the Phase 2
manifest rather than being silently relabelled as new tests.

The predeclared Phase 3 limits were 600 seconds for Phase 2, 90 seconds for the
harness, 30 seconds for bundle assembly, and 10 seconds for the negative
probe. The inherited harness retained its 5/2/3/30/5-second
first-output/response/stall/total/cleanup policy. A pass was still explicitly
bounded to hosted input qualification: guest boot, native CLI, ring 3 and
physical Kay OS execution were false, and physical inventory consumption was
false.

## Environment and provenance

- Implementation repository: `https://pushin.eu/pcharbon70/kay-os.git`.
- Tested commit: `2d41f3975cbecb4e5ebcddb57840503898380dc8`; recorded dirty-file count: `0`.
- Successful raw evidence root: `/tmp/kay-m0-p03-integration.KtVmL3`.
- Preserved unsuccessful raw evidence root: `/tmp/kay-m0-p03-integration.MZjKqx`.
- Limine input archive: `/tmp/limine-binary-12.9.0.tar.xz`; detached signature: `/tmp/limine-binary-12.9.0.tar.xz.sig`; both were authenticated by the inherited Phase 2 gate.
- Zig: 0.16.0; QEMU: 8.2.2 Debian/Ubuntu build; `xorriso`: 1.5.6 from the locally extracted package runtime.
- Successful `xorriso` executable: `/tmp/kay-xorriso-root/usr/bin/xorriso`; its extracted shared-library directory was supplied through `LD_LIBRARY_PATH=/tmp/kay-xorriso-root/usr/lib/x86_64-linux-gnu`.
- Result JSON SHA-256: `40b915eaa5d9ecaf89a1340c6625425d32100742cec4d79a99cc5bfcf339e244`.
- Phase 3 result table SHA-256: `3cfb23bb620cf0eed303ee97f7fe49dde7329c36691175f893638a90f0b84a37`.
- Complete evidence hash-list SHA-256: `2a8e1f7e4f7f508fc44d4cdb5167481701d74e9a108e18757a3310a9fded51b9`.
- M1 input-manifest SHA-256: `065a6c2bd2f602b3f0be8c1469ce7a1bb34ef3c011216bcb33ebbf8a24ff5531`.
- M1 bundle hash-list SHA-256: `1c13c2f1278fb70c35d82e6af0ffdc83221734136efe122c13d43b4566b322b4`.
- Reproduced read-only ISO SHA-256: `3ffad1d85539911981121c65b8a4bdcfb7cd1d09fc14aa01fbb075debe74bc1f`.

The raw roots are local evidence outside Git and may not be durable across
host cleanup. Their critical result, manifest and bundle identities are
recorded above. No physical device was observed, booted or written.

## Execution and results

| Task / case IDs | Fixture and exact command | Expected result | Actual observation | Result | Raw evidence / artifact identity |
| --- | --- | --- | --- | --- | --- |
| Attempt 1; `m0-p03-integration` | `XORRISO=/tmp/kay-xorriso-root/usr/bin/xorriso python3 scripts/m0/verify-phase-03.py /tmp/kay-m0-p03-integration.MZjKqx /tmp/limine-binary-12.9.0.tar.xz /tmp/limine-binary-12.9.0.tar.xz.sig` | Complete the phase or retain the exact bounded failure. | Contract work passed, but ISO construction stopped because the extracted executable could not load `libisoburn.so.1`. No Kay OS case was interpreted as failed. | fail | `/tmp/kay-m0-p03-integration.MZjKqx/phase-02/image-a.log` |
| M0-T01–M0-T06; `m0-p03-integration` | `LD_LIBRARY_PATH=/tmp/kay-xorriso-root/usr/lib/x86_64-linux-gnu XORRISO=/tmp/kay-xorriso-root/usr/bin/xorriso python3 scripts/m0/verify-phase-03.py /tmp/kay-m0-p03-integration.KtVmL3 /tmp/limine-binary-12.9.0.tar.xz /tmp/limine-binary-12.9.0.tar.xz.sig` | Require a clean revision; pass all inherited and Phase 3 cases; assemble the virtual bundle; consume no physical inventory. | 24 Phase 2 results, nine harness results and seven Phase 3 results passed. Bundle revision equalled the tested clean commit. | pass | Result and bundle hashes above; `/tmp/kay-m0-p03-integration.KtVmL3/case-results.tsv` |
| M0-T01 | Same successful command | Resolve signed inputs, exact environment, baseline and clean handoff. | Registered row `m0-p03-t01-complete-environment` passed. | pass | Phase 3 result-table hash above |
| M0-T02 | Same successful command | Reproduce clean kernel and read-only ISO outputs. | Registered row passed; inherited clean builds and two ISO builds were byte-identical. | pass | ISO SHA-256 above |
| M0-T03 | Same successful command | Accept the valid image and reject malformed handoff/image inputs. | Registered row passed from the emitted-image audit and inherited negative cases. | pass | 24-case Phase 2 result set under the successful evidence root |
| M0-T04 | Same successful command | Reconcile bounded operations, caller/endpoint/grant authority, time and failure contracts. | Registered row passed from the compiled policy and inherited positive/negative cases. | pass | 24-case Phase 2 result set under the successful evidence root |
| M0-T05 | Same successful command | Pass the controlled success path; detect all declared failures and cleanup; reject missing harness evidence. | One success, eight failure/cleanup cases and the missing-evidence probe passed. | pass | Nine-case harness table and Phase 3 result-table hash above |
| M0-T06 | Same successful command | Exclude physical inventory and preserve its M1 Phase 4 ownership. | Bundle manifest recorded `not-consumed-owned-by-m1-p04-inventory`; no physical-fixture file entered the virtual inputs. | pass | M1 input-manifest SHA-256 above |
| Code Companion | `KAY_MKDOCS=/tmp/kay-docs-venv/bin/mkdocs scripts/docs/verify-code-guide.sh` | Coverage, evolution metadata, links, navigation and strict HTML build pass. | Verification passed; MkDocs emitted its upstream future-version warning only. | pass | `/tmp/kay-code-guide-final.log` |

The failed attempt was corrected by completing the temporary package runtime,
not by changing any acceptance deadline, test case, Kay OS input, or expected
result. Its evidence remains separate from the successful clean run.

## Review and handoff

The implementation agent reviewed the exact result set, clean revision,
evidence boundary, hashes and failure history. The technical recommendation is
**proceed**: `m0-p03-integration` and the evidence-recording subtask are
complete, while final `m0-p03-handoff` acceptance remains assigned to the
user/project owner.

Any change to the selected compiler/firmware/loader inputs, Phase 2 contracts,
harness protocol or limits, required virtual-input list, clean-tree rule, or
physical-inventory exclusion reopens the relevant cases. The tested revision
is a feature-branch commit, not a merge revision. A later merge must be
recorded separately and is not automatically covered by this run.

## Follow-ups

- Obtain the user/project-owner proceed, revise, blocked, or independent-review
  decision for `m0-p03-handoff`.
- After merge, record merge provenance without relabelling this pre-merge run
  as merged-baseline evidence.
- Enter M1 only after the accepted handoff reproduces the immutable virtual
  input bundle; collect physical-fixture data solely in M1 Phase 4.
