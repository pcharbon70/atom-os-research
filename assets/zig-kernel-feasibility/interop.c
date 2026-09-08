#include "abi.h"
uint64_t c_add(uint64_t a, uint64_t b) { return a + b; }
struct pair c_apply(struct pair p, callback cb) {
    p.value = cb(p.value);
    p.tag += 1;
    return p;
}
#ifdef HOST_TEST
#include <stdio.h>
int main(void) {
    struct pair out = zig_roundtrip((struct pair){7, 40});
    if (out.tag != 8 || out.value != 42 || zig_callback(9) != 11) return 1;
    puts("PASS: C -> Zig -> C -> Zig callback; by-value struct and layout");
    return 0;
}
#endif
