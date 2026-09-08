#!/usr/bin/env bash
# Research only: never executes the freestanding artifact or privileged code.
set -euo pipefail
probe_sources=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
probe_out=$(mktemp -d /tmp/atom-zig-probe.XXXXXX)
export ASDF_ZIG_VERSION=0.16.0
export ZIG_GLOBAL_CACHE_DIR="$probe_out/global-cache"
export ZIG_LOCAL_CACHE_DIR="$probe_out/local-cache"
cd "$probe_out"
set -x
zig version
zig cc --version
cc --version
ld --version
sha256sum /home/ducky/.asdf/installs/zig/0.16.0/zig "$probe_sources"/*.zig "$probe_sources"/*.c "$probe_sources"/*.h
zig build-obj "$probe_sources/interop.zig" -target x86_64-linux-gnu -mcpu=nehalem -O ReleaseSafe -fllvm -fno-compiler-rt -femit-bin=host-zig.o
cc -std=c11 -O2 -DHOST_TEST -no-pie "$probe_sources/interop.c" host-zig.o -o host-test
./host-test
zig build-obj "$probe_sources/interop.zig" -target x86_64-freestanding-none -mcpu=nehalem -O ReleaseSafe -fllvm -mno-red-zone -fno-stack-check -fno-stack-protector -fno-compiler-rt -femit-bin=free-zig.o
zig cc -target x86_64-freestanding-none -march=nehalem -ffreestanding -mno-red-zone -fno-stack-protector -fno-pic -O2 -c "$probe_sources/interop.c" -o free-c.o
zig build-obj "$probe_sources/arch.zig" -target x86_64-freestanding-none -mcpu=nehalem -O ReleaseSmall -fllvm -mno-red-zone -fno-stack-check -fno-stack-protector -fno-compiler-rt -femit-bin=arch.o
ld -nostdlib -static -e arch_halt -Ttext=0x100000 free-zig.o free-c.o arch.o -o research.elf
readelf -h -l -d research.elf
nm -u research.elf
objdump -d arch.o
timeout 180 zig translate-c -target x86_64-freestanding-none "$probe_sources/abi.h" | awk '/^pub const struct_pair/,/^};/; /^pub const callback/; /^pub extern fn/; /^pub const __VERSION__/; /unable to translate macro/'
if header_diagnostic=$(zig build-obj "$probe_sources/interop.zig" -target x86_64-freestanding-none -femit-h -fno-emit-bin 2>&1); then
    printf 'Header generation unexpectedly succeeded; review current compiler behavior.\n'
    exit 1
else
    printf '%s\n' "$header_diagnostic"
    if [[ "$header_diagnostic" != *"-femit-h is currently broken"* ]]; then
        printf 'Unexpected header-generation failure; not the known diagnostic.\n'
        exit 1
    fi
    printf 'OBSERVED: bare -femit-h rejected; retained as a limitation, not an ABI failure.\n'
fi
sha256sum host-test research.elf
printf 'Research outputs retained at %s\n' "$probe_out"
