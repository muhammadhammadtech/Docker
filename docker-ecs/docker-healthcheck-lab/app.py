from flask import Flask, jsonify
import os
import time
import random

app = Flask(__name__)

# Global variable to simulate application state
app_healthy = True
start_time = time.time()

@app.route('/')
def home():
    return jsonify({
        "message": "Hello from Docker Health Check Lab!",
        "status": "running",
        "uptime": int(time.time() - start_time)
    })

@app.route('/health')
def health_check():
    global app_healthy
    
    # Simulate random failures for testing
    if random.random() < 0.1:  # 10% chance of failure
        app_healthy = False
    
    if app_healthy:
        return jsonify({
            "status": "healthy",
            "timestamp": int(time.time()),
            "uptime": int(time.time() - start_time)
        }), 200
    else:
        return jsonify({
            "status": "unhealthy",
            "timestamp": int(time.time()),
            "error": "Application is experiencing issues"
        }), 500

@app.route('/make-unhealthy')
def make_unhealthy():
    global app_healthy
    app_healthy = False
    return jsonify({"message": "Application marked as unhealthy"})

@app.route('/make-healthy')
def make_healthy():
    global app_healthy
    app_healthy = True
    return jsonify({"message": "Application marked as healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
