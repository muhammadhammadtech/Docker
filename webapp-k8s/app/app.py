from flask import Flask
import os
import socket

app = Flask(__name__)

@app.route('/')
def hello():
    hostname = socket.gethostname()
    return f'''
    <html>
        <head><title>Docker + Kubernetes Demo</title></head>
        <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
            <h1 style="color: #2196F3;">Welcome to Docker + Kubernetes Integration!</h1>
            <h2 style="color: #4CAF50;">Container Hostname: {hostname}</h2>
            <p>This application is running in a Docker container managed by Kubernetes.</p>
            <p style="color: #666;">Lab 31: Docker and Kubernetes Integration</p>
        </body>
    </html>
    '''

@app.route('/health')
def health():
    return {'status': 'healthy', 'hostname': socket.gethostname()}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
