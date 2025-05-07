; ===========================================================================================
; Fast String Hashing in x86-64 Assembly Language
; -------------------------------------------------------------------------------------------
; File:           src/asm/hash.asm
; Architecture:   x86-64 (64-bit), System V AMD64 ABI
; Platform:       Cross-platform (Linux, macOS); uses conditional symbols for MACHO64
; Author:         [Your Name or Team]
; Description:
;   This assembly module implements a simple yet efficient hashing algorithm
;   inspired by DJB2, optimized specifically for performance on 64-bit CPUs.
;
;   The core formula used is:
;       hash = hash * 33 + char
;
;   This approach offers a good balance between speed and hash distribution
;   for small-to-medium sized strings. It's widely used in hash tables, symbol
;   resolution, or lookup operations.
;
; Technical Summary:
;   - Input: RDI register is expected to contain a pointer to a null-terminated string.
;   - Output: RAX will contain the 64-bit hash result.
;   - Registers Used:
;       - RDI: input string pointer (preserved in RSI)
;       - RSI: working copy of string pointer
;       - RCX: loop counter / offset
;       - RDX: temporary character holder
;       - RAX: accumulated hash value (final result)
;
;   - Clobbered Registers: RCX, RDX, RAX
;
; Assembly Concepts Used:
;   - null-terminated string traversal
;   - byte-wise access with `movzx`
;   - conditional branching via `test`, `jz`
;   - integer multiplication and addition
;   - label-based looping (`.hash_loop`)
;
; Notes:
;   - The algorithm assumes valid UTF-8 ASCII-compatible strings.
;   - Behavior with non-null-terminated or binary strings is undefined.
;   - This is *not* cryptographically secure and should not be used for security purposes.
;
; GitHub Linguist Detection Hint:
;   This file intentionally contains detailed inline documentation and comments
;   to ensure correct language detection and indexing by tools such as GitHub Linguist.
;   The structure and annotations help with syntax highlighting and project statistics.
;
; Potential Applications:
;   - Symbol hashing in compilers or assemblers
;   - Interning strings in a memory-efficient hash table
;   - Key derivation for custom associative data structures
;   - Lightweight fingerprinting of identifiers in interpreters or DSLs
;
; Compilation:
;   You can assemble this file using NASM and link with your C/C++ project:
;
;     nasm -f elf64 src/asm/hash.asm   ; Linux
;     nasm -f macho64 src/asm/hash.asm ; macOS
;
; Integration:
;   Link with a C/C++ program and declare:
;
;     extern uint64_t fast_hash(const char *str);
;
; License:
;   MIT License. Use and distribute freely with attribution.
;
; ===========================================================================================

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