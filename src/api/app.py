from ctypes import CDLL, c_char_p, c_uint64
import os
import time  # Added for salting
from flask import Flask, request, redirect  # Added redirect
import redis

app = Flask(__name__)
redis_client = redis.Redis(
    host='redis-service',
    port=6379,
    password=os.environ.get("REDIS_PASSWORD"),
    decode_responses=True
)

# Load assembly library
try:
    lib_name = 'libhash.so'
    asm_lib = CDLL(os.path.join('/usr/local/lib', lib_name))
    asm_lib.hash_wrapper.argtypes = [c_char_p]
    asm_lib.hash_wrapper.restype = c_uint64
    print(f"✅ Assembly hash loaded: {lib_name}")
except Exception as e:
    print(f"❌ Assembly load failed: {e}")
    asm_lib = None

@app.route('/shorten', methods=['POST'])
def shorten_url():
    if request.method != 'POST':
        return {'error': 'Method not allowed'}, 405
    try:
        url = request.json.get('url')
        if not url:
            return {'error': 'URL is required'}, 400
        
        # Add salt using timestamp
        salted_url = f"{url}-{time.time()}"
        
        if asm_lib:
            raw_hash = asm_lib.hash_wrapper(salted_url.encode())
        else:
            raw_hash = hash(salted_url) & 0xFFFFFFFFFFFFFFFF
            
        short_hash = raw_hash % 10000
        # Set TTL (24 hours)
        redis_client.setex(short_hash, 86400, url)
        return {'short_url': f'{os.getenv("DOMAIN", "http://localhost:5050")}/{short_hash}'}
    except Exception as e:
        print(f"Error shortening URL: {e}")
        return {'error': str(e)}, 500

@app.route('/<short_hash>', methods=['GET'])
def redirect_to_url(short_hash):
    original_url = redis_client.get(short_hash)
    if original_url:
        return redirect(original_url, code=302)  # Proper redirect
    return {'error': 'URL not found'}, 404

@app.route('/')
def health_check():
    return {'status': 'ok'}, 200


# import platform
# from ctypes import CDLL, c_char_p, c_uint64
# import os

# lib_name = 'libhash.dylib' if platform.system() == 'Darwin' else 'libhash.so'
# lib_path = os.path.join(os.path.dirname(__file__), lib_name)
# asm_lib = CDLL(lib_path)
# asm_lib.hash_wrapper.argtypes = [c_char_p]
# asm_lib.hash_wrapper.restype = c_uint64



# def py_hash(s):
#     h = 0
#     for c in s.encode():
#         h = h * 33 + c
#     return h & 0xFFFFFFFFFFFFFFFF

# def test():
#     for s in ["hello", "world", "test", ""]:
#         asm = asm_lib.hash_wrapper(s.encode())
#         py = py_hash(s)
#         print(f"{s!r}: asm={asm} py={py} {'OK' if asm==py else 'FAIL'}")
#         assert asm == py

# if __name__ == "__main__":
#     test()