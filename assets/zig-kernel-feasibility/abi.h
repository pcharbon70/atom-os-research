#ifndef ATOM_ZIG_RESEARCH_ABI_H
#define ATOM_ZIG_RESEARCH_ABI_H
#include <stdint.h>
#include <stddef.h>
struct pair { uint32_t tag; uint64_t value; };
typedef uint64_t (*callback)(uint64_t);
_Static_assert(sizeof(struct pair) == 16, "pair size");
_Static_assert(_Alignof(struct pair) == 8, "pair alignment");
_Static_assert(offsetof(struct pair, value) == 8, "pair offset");
uint64_t c_add(uint64_t a, uint64_t b);
struct pair c_apply(struct pair p, callback cb);
uint64_t zig_callback(uint64_t n);
struct pair zig_roundtrip(struct pair p);
#endif
