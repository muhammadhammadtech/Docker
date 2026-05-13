#!/usr/bin/env python3
import os
import getpass
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return f"""
    <h1>Docker Security Demo</h1>
    <p>Current User: {getpass.getuser()}</p>
    <p>User ID: {os.getuid()}</p>
    <p>Group ID: {os.getgid()}</p>
    <p>Working Directory: {os.getcwd()}</p>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
