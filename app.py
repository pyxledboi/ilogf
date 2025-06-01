from flask import Flask, request
from datetime import datetime
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
# Trust up to 2 proxies (Render’s load balancers), adjust if needed
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=2, x_proto=1, x_host=1, x_port=1, x_prefix=1)

@app.route('/')
def log_ip():
    # After ProxyFix, request.remote_addr should be the leftmost X-Forwarded-For
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    timestamp = datetime.now().isoformat()
    print(f"{timestamp} - IP: {ip}, UA: {user_agent}")
    return "Gotcha 😉"

@app.route('/debug')
def dump_headers():
    lines = [f"{k}: {v}" for k, v in request.headers.items()]
    dump = "\n".join(lines)
    print(f"--- HEADER DUMP ---\n{dump}\n--- END DUMP ---")
    return "Check logs for header dump."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
