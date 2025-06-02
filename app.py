from flask import Flask, request
from datetime import datetime

app = Flask(__name__)
# Ensure logger prints INFO-level messages
app.logger.setLevel("INFO")

@app.route('/')
def log_ip():
    ip = (
        request.headers.get('True-Client-Ip')
        or request.headers.get('Cf-Connecting-Ip')
        or request.headers.get('X-Forwarded-For', '').split(',')[0].strip()
        or request.remote_addr
    )

    user_agent = request.headers.get('User-Agent', 'Unknown')
    timestamp = datetime.now().isoformat()
    # Use logger.info instead of print
    app.logger.info(f"{timestamp} - IP: {ip}, UA: {user_agent}")
    return f"Detected IP: {ip}", 200, {'Content-Type': 'text/plain'}

@app.route('/debug')
def dump_headers():
    headers = "\n".join(f"{k}: {v}" for k, v in request.headers.items())
    return headers, 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
