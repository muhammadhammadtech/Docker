from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "This app will fail health checks"})

@app.route('/health')
def health_check():
    # Always return unhealthy status
    return jsonify({
        "status": "unhealthy",
        "error": "Deliberately failing for testing"
    }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
