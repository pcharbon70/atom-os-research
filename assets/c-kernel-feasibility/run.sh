#!/usr/bin/env bash
# Research only; never execute the freestanding ELF or privileged functions.
set -euo pipefail
c_sources=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
c_out=$(mktemp -d /tmp/atom-c-probe.XXXXXX)
export ASDF_ZIG_VERSION=0.16.0
export ZIG_GLOBAL_CACHE_DIR="$c_out/global-cache"
export ZIG_LOCAL_CACHE_DIR="$c_out/local-cache"
cd "$c_out"
common=(-std=gnu11 -O2 -Wall -Wextra -Werror -march=nehalem -fcf-protection=none)
free=(-ffreestanding -mno-red-zone -mgeneral-regs-only -fno-stack-protector -fno-pic -fno-pie -fno-asynchronous-unwind-tables -fno-unwind-tables)
set -x
gcc --version
gcc -dumpmachine
zig version
zig cc --version
ld --version
sha256sum /usr/bin/gcc /usr/bin/ld /home/ducky/.asdf/installs/zig/0.16.0/zig "$c_sources"/*.c "$c_sources"/*.h "$c_sources"/*.S "$c_sources/run.sh"
gcc "${common[@]}" -c "$c_sources/library.c" -o host-gcc.o
zig cc "${common[@]}" -c "$c_sources/library.c" -o host-clang.o
gcc "${common[@]}" "$c_sources/host.c" host-clang.o -o gcc-client
zig cc "${common[@]}" "$c_sources/host.c" host-gcc.o -o clang-client
./gcc-client
./clang-client
for compiler in gcc clang; do
    if [[ "$compiler" == gcc ]]; then
        c_cmd=(gcc -m64)
    else
        c_cmd=(zig cc -target x86_64-freestanding-none)
    fi
    "${c_cmd[@]}" "${common[@]}" "${free[@]}" -c "$c_sources/library.c" -o "$compiler-library.o"
    "${c_cmd[@]}" "${common[@]}" "${free[@]}" -c "$c_sources/arch.c" -o "$compiler-arch.o"
    "${c_cmd[@]}" -c "$c_sources/entry.S" -o "$compiler-entry.o"
    ld -nostdlib -static -e research_entry -Ttext=0x100000 "$compiler-entry.o" "$compiler-library.o" "$compiler-arch.o" -o "$compiler-research.elf"
    readelf -h -l -d "$compiler-research.elf"
    nm -u "$compiler-research.elf"
    objdump -d "$compiler-arch.o"
    "${c_cmd[@]}" "${common[@]}" "${free[@]}" -c "$c_sources/helpers.c" -o "$compiler-helpers.o"
    nm -u "$compiler-helpers.o"
    if helper_diagnostic=$(ld -nostdlib -static -e research_entry "$compiler-entry.o" "$compiler-helpers.o" -o "$compiler-helper-failure.elf" 2>&1); then
        printf 'Unexpected helper-free link; inspect changed compiler behavior.\n'
        exit 1
    else
        printf '%s\n' "$helper_diagnostic"
        if [[ "$helper_diagnostic" != *"undefined reference to"*"__udivti3"* ]]; then
            printf 'Unexpected failure; not the required helper diagnostic.\n'
            exit 1
        fi
        printf 'PASS: omitted division helper is explicitly rejected.\n'
    fi
done
sha256sum gcc-client clang-client gcc-research.elf clang-research.elf
printf 'Research outputs retained at %s\n' "$c_out"
