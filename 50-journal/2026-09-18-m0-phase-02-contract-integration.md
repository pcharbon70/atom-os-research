---
title: "2026-09-18 — M0 phase 02 contract integration"
kind: journal
created: "2026-09-18"
tags:
  - implementation-planning
  - m0
  - proof-of-concept
  - zig
aliases: []
---

# 2026-09-18 — M0 phase 02 contract integration

The clean Kay OS revision
`f85571e2f2bb036c258fd596552731422cb41b38` passed all 24 registered M0
Phase 2 hosted contract, static-image, supply-chain, deterministic-media and
Phase 1 regression cases. The result supports `m0-p02-fixtures` and
`m0-p02-integration` within their declared pre-boot scope. On 2026-09-19, the
user/project owner selected **proceed** and accepted `m0-p02-handoff`. This run
does not demonstrate guest boot, ring-3 enforcement or the physical Dell
Precision T7500.

## Plan and acceptance baseline

- Milestone: [M0 — Boot inputs](../60-planning/01-proof-of-concept/m0-boot-inputs/README.md)
- Phase: [M0 Phase 2 — Boot, image, and interface contracts](../60-planning/01-proof-of-concept/m0-boot-inputs/phase-02-boot-image-and-interface-contracts.md)
- Tasks: `m0-p02-fixtures`, `m0-p02-integration`, evidence portion of
  `m0-p02-handoff`
- Artifact contributions: M0-A03 boot handoff; M0-A04 static image; M0-A05
  console/time authority contract
- Acceptance contributions: hosted/model portions of M0-T02, M0-T03 and M0-T04
- Case manifest: 24 exact positive, negative and regression IDs; SHA-256
  `4a373671781ae7297b511df7d82836f3b46000a542b6a8e3a882b85a26627194`

The accepted limits were declared before this run: Limine v12.9.0 and protocol
base revision 6, at most eight ELF load segments, fixed higher-half `ET_EXEC`,
64 MiB initial fixture memory, 256-byte console transfers, finite script
deadlines and exact case-result reconciliation. The run did not reinterpret an
unavailable guest or physical environment as a pass.

## Environment and provenance

- Implementation repository: [pcharbon70/kay-os](https://github.com/pcharbon70/kay-os)
- Tested revision: `f85571e2f2bb036c258fd596552731422cb41b38`
- Tested state: clean (`dirty_file_count=0`)
- Host: Linux x86-64
- Zig: 0.16.0, resolved binary SHA-256
  `2317bbb91798556d9d0f38aabdac23db83f0979b25f767259ae474546724087c`
- QEMU: 8.2.2, recorded for inherited baseline checks; no guest was started
- `xorriso`: 1.5.6 from a temporary extraction of Ubuntu packages under
  `/tmp/kay-xorriso-root`; the package was not installed system-wide because
  this session could not provide the required `sudo` password
- Limine: authenticated binary release v12.9.0, archive SHA-256
  `9a738586bff5790bd8bfef4a4868a2939cba3f81f22f121306d668c97f1c85d8`,
  signature SHA-256
  `c2ece24344e8b59350d8e7d9b70ce46b71f2c0cda3668096c14ff83f1f773e3d`,
  signing-key fingerprint `05D29860D0A0668AAEFB9D691F3C021BECA23821`
- Original evidence directory: `/tmp/kay-p02-final-clean.iOr4jf`
- Retained text evidence: [raw transcript](../assets/m0-phase-02-contract-integration/raw-transcript.txt)

The completed invocation was:

```sh
LD_LIBRARY_PATH=/tmp/kay-xorriso-root/usr/lib/x86_64-linux-gnu \
XORRISO=/tmp/kay-xorriso-root/usr/bin/xorriso \
  bash scripts/m0/verify-phase-02.sh \
  /tmp/kay-p02-final-clean.iOr4jf \
  /tmp/limine-binary-12.9.0.tar.xz \
  /tmp/limine-binary-12.9.0.tar.xz.sig
```

## Execution and results

| Task / case IDs | Fixture and exact command | Expected result | Actual observation | Result | Raw evidence / artifact identity |
| --- | --- | --- | --- | --- | --- |
| `m0-p02-fixtures`; `m0-p02-t01`–`t03`; `n01`–`n11`, `n14`–`n16` | Hosted Zig tests and emitted-policy reconciliation inside `verify-phase-02.sh` | Valid bounded contracts pass; malformed boot/image, authorization, buffer and time cases fail closed | All registered Zig cases passed; compiled authority/result tables matched the JSON manifest | pass | [Transcript](../assets/m0-phase-02-contract-integration/raw-transcript.txt); kernel ELF SHA-256 `e3b317cabe4fd16e573fc86477ae06a96e1cec9ed33178b1519c71185f06244e` |
| `m0-p02-integration`; `m0-p02-t04`, `t08` | Two independent absolute-directory builds plus host ELF audit | Byte-identical ELF; bounded two-segment static image accepted by the shared contract | Both ELFs matched; `segments=2`, entry `0xffffffff80000000`, physical range `0x200000..0x206000` | pass | [Transcript](../assets/m0-phase-02-contract-integration/raw-transcript.txt) |
| `m0-p02-t05`, `n12` | Pinned Limine archive, signature and vendored public key | Exact release authenticates; truncated signature is rejected | Detached signature valid with expected fingerprint; invalid signature rejected | pass | Archive/signature identities above and [transcript](../assets/m0-phase-02-contract-integration/raw-transcript.txt) |
| `m0-p02-t06`, `n13` | Two read-only BIOS ISO builds; missing-tool negative | Byte-identical ISOs; absent `xorriso` fails before construction | Both ISO hashes matched; missing tool was rejected | pass | ISO SHA-256 `3ffad1d85539911981121c65b8a4bdcfb7cd1d09fc14aa01fbb075debe74bc1f` |
| `m0-p02-t07` | Nested Phase 1 driver | All inherited build/baseline and failure-detection cases remain passing | Phase 1 returned pass on the same clean revision | pass | Fixture ELF SHA-256 `e94b127fcc4388e73b4620a8b0908dcdeed0c3a08fbf0052d92cce58a3baf31a` |
| Guest boot and kernel enforcement | Not part of the Phase 2 pre-boot driver | Remain explicitly outside this result | `guest_boot=not-tested`; `ring3_enforcement=not-tested` | not run | Deferred to M1 implementation/evidence |
| Physical Dell Precision T7500 | No physical access or device write in this run | Remain open for Phase 3 qualification | `physical_t7500=not-tested` | not run | `m0-p03-inventory` and later physical evidence remain open |

The driver returned zero at `2026-09-18T18:28:44Z`. Its exact result set was
reconciled against all 24 manifest records; absent, duplicate, empty or
non-passing observations would have failed the run.

## Review and handoff

An independent review first identified boot-map reconciliation, physical-range
overlap, manifest, authority-table, ELF-audit, tool-identity and Code Companion
gaps. Those findings were corrected before the clean run. The final independent
follow-up review of commit `f85571e2f2bb036c258fd596552731422cb41b38`
reported no remaining implementation blocker. It confirmed the compiled Zig
policy/JSON reconciliation and independent expectations, the two-segment Code
Companion description, and rejection of ELF segments extending beyond the
actual file. Its sole closeout request was to replace the guide's stale “clean
rerun pending” banner; that documentation-only correction is part of the later
Section 2.2 record commit.

The tested revision is the Section 2.1 implementation commit. This journal and
its retained transcript are later evidence-record changes; they do not imply
that a future merge revision was tested. The user/project owner accepted the
declared pre-boot scope and recorded **proceed** on 2026-09-19. Phase 2 is
complete, and Phase 3 may begin; all guest, ring-3, physical and full-M0 gates
remain assigned to their owning later work.

Changes to the Limine release/protocol, handoff schema, image subset, linker
layout, ABI/register policy, operation table, grants, bounds, time units, fault
policy, tool identities, case manifest or verification scripts reopen the
relevant evidence.

## Follow-ups

- Begin M0 Phase 3 only after reviewing its open decision register and entry
  dependencies.
- Keep guest enforcement and physical qualification open in their owning
  phases; do not reinterpret this hosted contract result as a boot.
