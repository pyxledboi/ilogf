from flask import Flask, request
from datetime import datetime
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

# Tell Flask/Werkzeug to trust one proxy (Render’s load balancer).
# This makes request.remote_addr become the leftmost value in X-Forwarded-For.
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)

@app.route('/')
def log_ip():
    # Now request.remote_addr is real client IP (thanks to ProxyFix)
    ip = request.remote_addr  
    user_agent = request.headers.get('User-Agent', 'Unknown')
    timestamp = datetime.now().isoformat()
    print(f"{timestamp} - IP: {ip}, UA: {user_agent}")
    return "Gotcha 😉"

# Optional debug route: dumps all headers so you can verify what Render sends
@app.route('/debug')
def dump_headers():
    headers = "\n".join(f"{k}: {v}" for k, v in request.headers.items())
    print(f"---HEADER DUMP START---\n{headers}\n---HEADER DUMP END---")
    return "Check Render logs for headers"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
