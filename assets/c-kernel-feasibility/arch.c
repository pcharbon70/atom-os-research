#include <stdint.h>
#include <stdatomic.h>
void port_write(uint16_t port, uint8_t value) {
    __asm__ volatile ("outb %0, %1" : : "a"(value), "Nd"(port));
}
uint32_t mmio_read(uintptr_t address) {
    return *(volatile uint32_t *)address;
}
uint64_t atomic_increment(_Atomic uint64_t *counter) {
    return atomic_fetch_add_explicit(counter, 1, memory_order_seq_cst);
}
// Compile/disassemble only: no installed IDT or validated real frame exists.
struct interrupt_frame { uint64_t rip, cs, rflags, rsp, ss; };
__attribute__((interrupt)) void interrupt_probe(struct interrupt_frame *frame) {
    (void)frame;
}
