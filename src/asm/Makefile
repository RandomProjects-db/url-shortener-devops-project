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