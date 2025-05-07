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
