#include "abi.h"
#include <stdio.h>
static uint64_t add_two(uint64_t value) { return value + 2; }
int main(void) {
    struct record result = apply((struct record){7, 40}, add_two);
    if (result.kind != 8 || result.value != 42) return 1;
    puts("PASS: mixed-compiler C record argument/result and callback");
    return 0;
}
