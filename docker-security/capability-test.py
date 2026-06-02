#!/usr/bin/env python3
import os
import socket
import subprocess
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>Capability Testing</h1>
    <p><a href="/test-network">Test Network Capabilities</a></p>
    <p><a href="/test-process">Test Process Capabilities</a></p>
    <p><a href="/test-filesystem">Test Filesystem Capabilities</a></p>
    <p><a href="/capabilities">View Current Capabilities</a></p>
    """

@app.route('/capabilities')
def show_capabilities():
    try:
        result = subprocess.run(['capsh', '--print'],
                              capture_output=True, text=True)
        return f"<pre>{result.stdout}</pre>"
    except Exception as e:
        return f"Error checking capabilities: {str(e)}"

@app.route('/test-network')
def test_network():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('0.0.0.0', 80))
        sock.close()
        return "SUCCESS: Can bind to privileged port 80"
    except Exception as e:
        return f"FAILED: Cannot bind to privileged port: {str(e)}"

@app.route('/test-process')
def test_process():
    try:
        os.nice(-1)
        return "SUCCESS: Can change process priority"
    except Exception as e:
        return f"FAILED: Cannot change process priority: {str(e)}"

@app.route('/test-filesystem')
def test_filesystem():
    try:
        with open('/tmp/test-file', 'w') as f:
            f.write('test')
        os.chown('/tmp/test-file', 1000, 1000)
        return "SUCCESS: Can change file ownership"
    except Exception as e:
        return f"FAILED: Cannot change file ownership: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
