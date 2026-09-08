export fn port_write(port: u16, value: u8) void {
    asm volatile ("outb %[value], %[port]"
        :
        : [value] "{al}" (value), [port] "{dx}" (port),
    );
}
export fn mmio_read(address: usize) u32 {
    const reg: *volatile u32 = @ptrFromInt(address);
    return reg.*;
}
export fn atomic_increment(counter: *u64) u64 {
    return @atomicRmw(u64, counter, .Add, 1, .seq_cst);
}
// Compile/disassemble only. This is not a valid boot entry or interrupt stub.
export fn arch_halt() callconv(.naked) noreturn {
    asm volatile ("cli\n1: hlt\njmp 1b");
}
