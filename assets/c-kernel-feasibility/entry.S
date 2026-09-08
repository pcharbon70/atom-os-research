.text
.global research_entry
.type research_entry, @function
research_entry:
    cli
1:
    hlt
    jmp 1b
.size research_entry, .-research_entry
.section .note.GNU-stack,"",@progbits
