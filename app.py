from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def log_ip():
    # 1) Check Cloudflare’s header
    cf_ip = request.headers.get('CF-Connecting-IP')
    if cf_ip:
        ip = cf_ip
    else:
        # 2) Fallback: use X-Forwarded-For (Render’s header), take first value
        forwarded = request.headers.get('X-Forwarded-For', '')
        ip = forwarded.split(',')[0].strip() if forwarded else request.remote_addr

    user_agent = request.headers.get('User-Agent', 'Unknown')
    timestamp = datetime.now().isoformat()
    print(f"{timestamp} - IP: {ip}, UA: {user_agent}")
    return "Gotcha 😉"

@app.route('/debug')
def dump_headers():
    # (Optional) Let’s see exactly what headers are coming through
    dump = "\n".join(f"{k}: {v}" for k, v in request.headers.items())
    print(f"--- HEADER DUMP ---\n{dump}\n--- END DUMP ---")
    return "Check logs for header dump."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
