---
title: "Freestanding build and static images"
kind: note
created: "2026-09-06"
maturity: developing
tags:
  - boot
  - proof-of-concept
  - requirements
aliases: []
---

# Freestanding build and static images

Requirement R02, M0–M1, extended at M3. The build must produce identifiable kernel and native CLI images, and later a bounded bundle of genuine compiler-produced BEAM modules. The first guest can use static images without a writable filesystem or general dynamic linker.

## Evidence and limits

[GCC's freestanding documentation](../../30-sources/gnu-project-2026-gcc-freestanding-environment.md) explicitly leaves startup and linking to the environment and requires memory-support routines. Thus a freestanding flag is only one part of the dependency contract.

The [ELF program-loading reference](../../30-sources/xinuos-2026-elf-program-loading.md) describes loadable segments, memory/file lengths, alignment and permissions. Its visible edition is 4.3 DRAFT. Atom should declare a stricter image subset rather than infer that every valid ELF image is acceptable.

The [AMD64 procedure ABI](../../30-sources/x86-psabi-project-2026-amd64-procedure-abi.md) provides the relevant calling-convention and stack model. Atom must separately specify its syscall ABI; neither a procedure ABI nor a Linux target triple supplies it. [NixOS's published deployment work](../../30-sources/dolstra-et-al-2008-nixos.md) provides implementation evidence for explicit build-input closures and immutable outputs; a declared input graph still requires reproduction checks. [SOURCE_DATE_EPOCH](../../30-sources/lamb-luo-2017-source-date-epoch.md) addresses timestamp variation, not the entire build environment.

## Proposed implementation profile

The user selected **Zig as the kernel language on 2026-09-08**, superseding
this report's earlier open language choice. The [Zig feasibility and C-interoperability
study](zig-kernel-language-feasibility-and-c-interoperability.md) supports starting
bounded M0 qualification with narrow audited C/assembly escape hatches. Zig
0.16.0 is the researched and locally probed candidate, not an accepted compiler
pin. Backend/linker, panic, allocation, helper closure and instruction/state
policy remain explicit decisions; the study's hosted/link probes are not M0
completion, a boot demonstration or a performance benchmark.

Target the [adopted T7500 / Intel x86-64 profile](dell-precision-t7500-target-and-minimal-qemu-profile.md), with a proposed static little-endian ELF64/AMD64 image subset and an explicitly recorded LP64 procedure convention. An integer-only bring-up narrows ordinary ABI state expectations; it is not full AMD64 psABI support. Audit generated instructions and linked helpers, and implement initialized FP/SIMD context ownership before admitting that state. Record stack alignment, kernel red-zone exclusion, optimization, code model, relocation policy, stack protection, exception/unwind policy and linker version. Do not inherit host-native instruction selection or a Linux syscall interface.

An image manifest should include source revision and local changes, tool identities, flags, link script, entry address, segment intervals, exported entry points, imports, stack/heap reservations and content hashes. Produce a link map and inspect undefined symbols. Every helper is either provided by reviewed guest code or rejected; host `malloc`, threads, clocks, files, entropy and signal services cannot leak into the guest through convenient libraries.

Prefer a single declared static ELF subset for native images, or a build-time conversion to a simpler flat descriptor. The conversion alternative reduces guest parsing but moves its correctness into the trusted build pipeline. In either case, the guest checks the descriptor's lengths, destinations and authority.

For ELF admission, require the declared class, endianness, machine and supported type; bounded program-header count; checked offset/size arithmetic; file size no greater than memory size; valid alignment; nonoverlapping destination policy; an executable entry within an admitted segment; and no unsupported interpreter, relocation, TLS or dynamic-link dependency. Apply page permissions deliberately and reject images that would require writable executable aliases. Zero-fill uninitialized memory before user access.

## Reproducibility and packaging

Pin the complete build environment, including generated tools and compiler support libraries. Control locale, timestamps, file order and path-dependent metadata. Do two clean builds in different absolute directories and compare kernel, CLI, firmware and BEAM hashes individually. A difference requires explanation at the artifact level; merely producing the same boot banner is insufficient.

Bundle service images and their authority/resource descriptors separately. A content hash identifies bytes; it does not authorize execution. At M3, record the OTP compiler, library versions and fixture hashes independently of the native compiler. The exact build of the semantic oracle belongs in the [BEAM profile](beam-profile-loader-and-conformance.md).

Keep source and dependency retrieval outside the measured guest boot path. A cached dependency is still an input that must be identified. Retain symbols separately if stripping is part of image production, and ensure they resolve against the executed artifact.

## Acceptance and failure tests

Build a corpus of truncated headers, overflowed intervals, invalid entry points, unsupported relocations and overlapping segments. Failed image preparation must release staged pages and publish no runnable context. Test a malformed boot-bundle count and wrong service hash. Check that initialized data is preserved, BSS is zero, stack alignment holds, and privilege state cannot be selected by an image field.

The decisive next work is a linker/startup smoke test and binary dependency census. Do not claim reproducibility, a safe loader or an executable version pin from this document alone.

## Connections

The [C feasibility assessment](c-kernel-language-feasibility-and-low-level-compatibility.md)
evaluates the alternative kernel language and C-component dependency contract
without changing the selected Zig decision or closing build qualification.

[Boot handoff](target-firmware-and-boot-handoff.md) establishes load ownership. [User protection](privilege-entry-memory-and-user-return.md) enforces the installed image. [Validation](models-fault-injection-and-measurement.md) defines retained build and run evidence.
