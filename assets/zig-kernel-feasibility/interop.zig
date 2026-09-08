const std = @import("std");
pub const panic = std.debug.FullPanic(struct {
    fn stop(_: []const u8, _: ?usize) noreturn { @trap(); }
}.stop);
const Pair = extern struct { tag: u32, value: u64 };
comptime {
    if (@sizeOf(Pair) != 16 or @alignOf(Pair) != 8 or @offsetOf(Pair, "value") != 8)
        @compileError("pair layout mismatch");
}
extern fn c_add(a: u64, b: u64) u64;
extern fn c_apply(p: Pair, cb: *const fn (u64) callconv(.c) u64) Pair;
export fn zig_callback(n: u64) u64 { return c_add(n, 2); }
export fn zig_roundtrip(p: Pair) Pair { return c_apply(p, &zig_callback); }
