#!/usr/bin/env python3
import os
import logging
from flask import Flask, jsonify
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Secure Production Application",
        "user": os.getenv('USER', 'unknown'),
        "uid": os.getuid(),
        "gid": os.getgid(),
        "timestamp": datetime.now().isoformat(),
        "security_features": [
            "Non-root user",
            "Read-only filesystem",
            "Dropped capabilities",
            "AppArmor protection",
            "Signed image"
        ]
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/security-test')
def security_test():
    tests = {}

    try:
        with open('/tmp/test-write', 'w') as f:
            f.write('test')
        tests['tmp_write'] = 'allowed'
        os.remove('/tmp/test-write')
    except:
        tests['tmp_write'] = 'denied'

    try:
        with open('/app/test-write', 'w') as f:
            f.write('test')
        tests['app_write'] = 'allowed'
        os.remove('/app/test-write')
    except:
        tests['app_write'] = 'denied'

    try:
        with open('/etc/passwd', 'r') as f:
            f.read(10)
        tests['passwd_read'] = 'allowed'
    except:
        tests['passwd_read'] = 'denied'

    return jsonify(tests)

if __name__ == '__main__':
    logger.info("Starting secure application")
    app.run(host='0.0.0.0', port=5000)
