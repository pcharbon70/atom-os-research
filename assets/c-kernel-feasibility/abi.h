#ifndef ATOM_C_RESEARCH_ABI_H
#define ATOM_C_RESEARCH_ABI_H
#include <stddef.h>
#include <stdint.h>
struct record { uint32_t kind; uint64_t value; };
typedef uint64_t (*callback)(uint64_t);
_Static_assert(sizeof(struct record) == 16, "record size");
_Static_assert(_Alignof(struct record) == 8, "record alignment");
_Static_assert(offsetof(struct record, value) == 8, "record offset");
struct record apply(struct record value, callback function);
#endif
