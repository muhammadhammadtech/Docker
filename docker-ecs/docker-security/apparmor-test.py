#!/usr/bin/env python3
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>AppArmor Security Test</h1>
    <p><a href="/read-passwd">Try to read /etc/passwd</a></p>
    <p><a href="/read-shadow">Try to read /etc/shadow</a></p>
    <p><a href="/write-proc">Try to write to /proc</a></p>
    <p><a href="/list-root">Try to list root directory</a></p>
    """

@app.route('/read-passwd')
def read_passwd():
    try:
        with open('/etc/passwd', 'r') as f:
            content = f.read()
        return f"<pre>{content}</pre>"
    except Exception as e:
        return f"BLOCKED: {str(e)}"

@app.route('/read-shadow')
def read_shadow():
    try:
        with open('/etc/shadow', 'r') as f:
            content = f.read()
        return f"<pre>{content}</pre>"
    except Exception as e:
        return f"BLOCKED: {str(e)}"

@app.route('/write-proc')
def write_proc():
    try:
        with open('/proc/sys/kernel/hostname', 'w') as f:
            f.write('hacked')
        return "SUCCESS: Modified system hostname"
    except Exception as e:
        return f"BLOCKED: {str(e)}"

@app.route('/list-root')
def list_root():
    try:
        files = os.listdir('/')
        return f"<pre>{chr(10).join(files)}</pre>"
    except Exception as e:
        return f"BLOCKED: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
