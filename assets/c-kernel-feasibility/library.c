#include "abi.h"
struct record apply(struct record value, callback function) {
    value.value = function(value.value);
    value.kind += 1;
    return value;
}
