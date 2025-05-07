; ========================================================
; Fast String Hash Algorithm (x86-64 Assembly)
; 
; Implements a DJB2-like hash optimized for x86-64:
;   hash = hash * 33 + char
;
; Calling Convention: System V AMD64 ABI
; Input:  RDI = null-terminated string pointer
; Output: RAX = 64-bit hash value
; Clobbers: RCX, RDX
; ========================================================

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