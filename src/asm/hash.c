/* =============================================================================================
 * File:        src/c/hash_wrapper.c
 * Title:       Hash Function Wrapper - C Interface for x86-64 Assembly Hash Routine
 * Description:
 *   This file provides a portable C interface to an optimized assembly-level string hash
 *   function defined in `src/asm/hash.asm`. It bridges the gap between high-level C code and
 *   low-level architecture-specific assembly using `extern` linkage.
 *
 *   The assembly function computes a simple yet effective string hash using the DJB2-inspired
 *   formula: `hash = hash * 33 + char`. It is designed for performance in tight loops,
 *   symbol resolution, and hash table indexing.
 *
 * Usage:
 *   Simply include this file or its prototype in your project and link the corresponding
 *   assembly file. This wrapper handles cross-platform symbol naming conventions.
 *
 * Features:
 *   - Supports both macOS (Mach-O) and Linux (ELF) binaries via `__APPLE__` preprocessor macro.
 *   - Ensures linkage to correct symbol (`_fast_hash` on macOS vs `fast_hash` on Linux).
 *   - Minimal overhead, inlined wrapper logic.
 *
 * Requirements:
 *   - The target architecture must be x86-64.
 *   - NASM is required to compile the `hash.asm` file.
 *   - Ensure the assembly object is correctly linked with this C file.
 *
 * Sample Compilation:
 *   Linux:
 *     nasm -f elf64 src/asm/hash.asm -o hash.o
 *     gcc -c src/c/hash_wrapper.c -o hash_wrapper.o
 *     gcc hash.o hash_wrapper.o -o hashtest
 *
 *   macOS:
 *     nasm -f macho64 src/asm/hash.asm -o hash.o
 *     clang -c src/c/hash_wrapper.c -o hash_wrapper.o
 *     clang hash.o hash_wrapper.o -o hashtest
 *
 * Sample Usage:
 *   #include <stdio.h>
 *   #include <stdint.h>
 *
 *   extern uint64_t hash_wrapper(const char *str);
 *
 *   int main() {
 *       const char *msg = "hello, world";
 *       printf("Hash: %llu\n", hash_wrapper(msg));
 *       return 0;
 *   }
 *
 * License:
 *   MIT License - Free to use, modify, and distribute.
 *
 * ============================================================================================= */

#include <stdint.h>

#if defined(__APPLE__)
extern uint64_t _fast_hash(const char *str);
#else
extern uint64_t fast_hash(const char *str);
#endif

uint64_t hash_wrapper(const char *str) {
#if defined(__APPLE__)
    return _fast_hash(str);
#else
    return fast_hash(str);
#endif
}