; filepath: src/asm/hash.asm
BITS 64
section .text

%ifdef MACHO64
    global __fast_hash
__fast_hash:
%else
    global fast_hash
fast_hash:
%endif

    mov rsi, rdi
    xor rax, rax
    xor rcx, rcx

.hash_loop:
    movzx edx, byte [rsi + rcx]
    test dl, dl
    jz .done
    imul rax, rax, 33
    add rax, rdx
    inc rcx
    jmp .hash_loop

.done:
    ret