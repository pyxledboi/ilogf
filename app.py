from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def log_ip():
    # Prioritize True-Client-Ip (Cloudflare) or Cf-Connecting-Ip, then fallback to X-Forwarded-For
    ip = (
        request.headers.get('True-Client-Ip')
        or request.headers.get('Cf-Connecting-Ip')
        or request.headers.get('X-Forwarded-For', '').split(',')[0].strip()
        or request.remote_addr
    )

    user_agent = request.headers.get('User-Agent', 'Unknown')
    timestamp = datetime.now().isoformat()
    print(f"{timestamp} - IP: {ip}, UA: {user_agent}")
    return f"Detected IP: {ip}", 200, {'Content-Type': 'text/plain'}

@app.route('/debug')
def dump_headers():
    # Return all headers so you can inspect them directly
    headers = "\n".join(f"{k}: {v}" for k, v in request.headers.items())
    return headers, 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
