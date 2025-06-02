from flask import Flask, request, Response
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def log_ip():
    # Check CF-Connecting-IP first
    cf_ip = request.headers.get('CF-Connecting-IP')
    if cf_ip:
        ip = cf_ip
    else:
        forwarded = request.headers.get('X-Forwarded-For', '')
        ip = forwarded.split(',')[0].strip() if forwarded else request.remote_addr

    ua = request.headers.get('User-Agent', 'Unknown')
    ts = datetime.now().isoformat()
    print(f"{ts} - IP: {ip}, UA: {ua}")
    return "Gotcha 😉"

@app.route('/debug')
def dump_headers():
    # Return all received headers so you can inspect them in-browser
    headers = "\n".join(f"{k}: {v}" for k, v in request.headers.items())
    return Response(headers, mimetype="text/plain")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
