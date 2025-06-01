
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def log_ip():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    timestamp = datetime.now().isoformat()
    with open("logs.txt", "a") as log:
        log.write(f"{timestamp} - IP: {ip}, UA: {user_agent}\n")
    return "Gotcha 😉"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
