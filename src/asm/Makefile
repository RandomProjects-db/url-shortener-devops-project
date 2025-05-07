# =============================================================================================
# Makefile for Building x86-64 Assembly Hash Library (Linux/macOS)
#
# Description:
#   This Makefile automates the process of compiling a DJB2-inspired hash function written in
#   x86-64 NASM assembly and wrapping it with a C interface for cross-platform dynamic linking.
#
#   It supports Linux and macOS targets by checking the system type using `uname`, and sets
#   flags accordingly for symbol naming, object format (`elf64` for Linux, `macho64` for macOS),
#   and dynamic library output naming conventions (`.so` vs `.dylib`).
#
# Components:
#   - Assembly Source: `hash.asm`
#   - C Wrapper: `hash.c` (compiled to `hash_wrapper.o`)
#   - Final Output: `libhash.so` (Linux) or `libhash.dylib` (macOS)
#
# Usage:
#   make         → Builds the shared library for your system
#   make clean   → Removes object and binary files
#   make test    → Builds and runs test script (requires `test_asm.py`)
#
# Tools Required:
#   - NASM assembler (for .asm file)
#   - GCC/Clang compiler (for .c file)
#   - Python 3 (optional, for test runner)
#
# =============================================================================================

UNAME_S := $(shell uname -s)
CC=gcc
ASM=nasm
CFLAGS=-fPIC -O3

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    ASMFLAGS = -f macho64 -DMACHO64
    LDFLAGS = -dynamiclib
    LIB = libhash.dylib
else
    ASMFLAGS = -f elf64
    LDFLAGS = -shared
    LIB = libhash.so
endif

all: $(LIB)

$(LIB): hash.o hash_wrapper.o
	$(CC) $(LDFLAGS) -o $@ $^

hash.o: hash.asm
	$(ASM) $(ASMFLAGS) -o $@ $<

hash_wrapper.o: hash.c
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	rm -f *.o *.so *.dylib

test: all
	python3 test_asm.py