#!/usr/bin/env python3
import os
import time
import tempfile
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>Logging Application</h1>
    <p><a href="/write-temp">Write to /tmp</a></p>
    <p><a href="/write-app">Write to /app</a></p>
    <p><a href="/logs">View Logs</a></p>
    """

@app.route('/write-temp')
def write_temp():
    try:
        with open('/tmp/temp-log.txt', 'a') as f:
            f.write(f"Temp log entry at {time.ctime()}\n")
        return "Successfully wrote to /tmp"
    except Exception as e:
        return f"Error writing to /tmp: {str(e)}"

@app.route('/write-app')
def write_app():
    try:
        with open('/app/app-log.txt', 'a') as f:
            f.write(f"App log entry at {time.ctime()}\n")
        return "Successfully wrote to /app"
    except Exception as e:
        return f"Error writing to /app: {str(e)}"

@app.route('/logs')
def view_logs():
    logs = ""
    try:
        if os.path.exists('/tmp/temp-log.txt'):
            with open('/tmp/temp-log.txt', 'r') as f:
                logs += "<h3>Temp Logs:</h3><pre>" + f.read() + "</pre>"
    except:
        pass
    try:
        if os.path.exists('/app/app-log.txt'):
            with open('/app/app-log.txt', 'r') as f:
                logs += "<h3>App Logs:</h3><pre>" + f.read() + "</pre>"
    except:
        pass
    return logs if logs else "No logs found"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
