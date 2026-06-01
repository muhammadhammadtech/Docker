from flask import Flask, jsonify
import redis
import os
import socket

app = Flask(__name__)
redis_client = redis.Redis(host=os.getenv('REDIS_HOST', 'redis'), port=6379, decode_responses=True)

@app.route('/')
def hello():
    try:
        visits = redis_client.incr('visits')
        hostname = socket.gethostname()
        return jsonify({
            'message': 'Hello from Docker Swarm!',
            'hostname': hostname,
            'visits': visits,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'message': 'Hello from Docker Swarm!',
            'hostname': socket.gethostname(),
            'error': str(e),
            'status': 'error'
        })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
