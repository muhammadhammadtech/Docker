#!/usr/bin/env python3
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>Signed Docker Image</h1>
    <p>This image has been cryptographically signed!</p>
    <p>Image integrity verified through Docker Content Trust</p>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
