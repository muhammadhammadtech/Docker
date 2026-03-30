from flask import Flask, jsonify
import redis
import os
import socket

app = Flask(__name__)

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis'),
    port=6379,
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2
)

@app.route('/')
def hello():
    hostname = socket.gethostname()
    try:
        visits = redis_client.incr('visits')
        return jsonify({
            'message': 'Hello from Docker Swarm!',
            'hostname': hostname,
            'visits': visits,
            'status': 'success'
        })
    except redis.exceptions.RedisError as e:
        return jsonify({
            'message': 'Hello from Docker Swarm!',
            'hostname': hostname,
            'error': 'Redis connection failed',
            'details': str(e),
            'status': 'error'
        })

@app.route('/health')
def health():
    try:
        redis_client.ping()
        return jsonify({'status': 'healthy'})
    except redis.exceptions.RedisError:
        return jsonify({'status': 'unhealthy'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
