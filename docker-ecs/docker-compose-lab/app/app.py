from flask import Flask, request, jsonify, session
import psycopg2
import redis
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_NAME = os.environ.get('DB_NAME', 'webapp')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASS = os.environ.get('DB_PASS', 'password')

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.route('/')
def home():
    views = r.incr('page_views')
    return jsonify({
        'message': 'Welcome to Multi-Container Web App!',
        'page_views': views,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/users', methods=['GET', 'POST'])
def users():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        data = request.get_json()
        cur.execute(
            "INSERT INTO users (name, email, created_at) VALUES (%s, %s, %s)",
            (data['name'], data['email'], datetime.now())
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'User created'}), 201

    cur.execute("SELECT name, email, created_at FROM users")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify({'users': [
        {'name': r[0], 'email': r[1], 'created_at': r[2].isoformat()}
        for r in rows
    ]})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})
