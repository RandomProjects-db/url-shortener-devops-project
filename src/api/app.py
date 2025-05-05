from flask import Flask, request
import redis
import os

app = Flask(__name__)
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

# Fix: Use environment variable for flexibility
DOMAIN = os.getenv('DOMAIN', 'http://localhost:5050')  # Default to 5050

@app.route('/shorten', methods=['POST'])
def shorten_url():
    url = request.json.get('url')
    short_hash = hash(url) % 10000
    redis_client.set(short_hash, url)
    return {'short_url': f'{DOMAIN}/{short_hash}'}  # Now uses correct port

@app.route('/<short_hash>')
def redirect(short_hash):
    url = redis_client.get(short_hash)
    return f'Redirecting to: {url}' if url else 'Not found', 200 if url else 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)