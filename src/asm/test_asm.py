#!/usr/bin/env python3
"""
======================================================================
Unit Test Suite for x86-64 Assembly Hash Function (via C Wrapper)
======================================================================

This Python test script dynamically loads the shared hash library
built from NASM assembly and C wrapper, and runs unit tests to ensure
correct and deterministic behavior of the hashing function.

Features:
---------
- Uses Python's built-in `unittest` framework.
- Leverages `ctypes` to bind C ABI-compatible functions.
- Verifies:
    - Consistent hashing (same input gives same hash)
    - Hash uniqueness (different inputs give different hashes)

Requirements:
-------------
- Python 3.x
- Built shared library (`libhash.so` or `libhash.dylib`)
- Platform-compatible binary (macOS or Linux)

Usage:
------
$ python3 test_asm.py

If your system uses `.so` instead of `.dylib`, adjust `libname`.

File Structure:
---------------
/
├── hash.asm
├── hash.c
├── Makefile
├── libhash.dylib / libhash.so
└── test_asm.py  ← (this file)

License: MIT or public domain
"""

import ctypes, sys, unittest

class TestASMHash(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        libname = './libhash.dylib'
        cls.lib = ctypes.CDLL(libname)
        cls.lib.hash_wrapper.argtypes = [ctypes.c_char_p]
        cls.lib.hash_wrapper.restype = ctypes.c_uint64

    def test_hash_consistency(self):
        h1 = self.lib.hash_wrapper(b"test")
        h2 = self.lib.hash_wrapper(b"test")
        self.assertEqual(h1, h2)

    def test_hash_difference(self):
        h1 = self.lib.hash_wrapper(b"test1")
        h2 = self.lib.hash_wrapper(b"test2")
        self.assertNotEqual(h1, h2)

if __name__ == '__main__':
    unittest.main()
