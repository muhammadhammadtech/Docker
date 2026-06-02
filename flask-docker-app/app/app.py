from flask import Flask, request, jsonify
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = '/app/data/visitors.db'

def init_db():
    os.makedirs('/app/data', exist_ok=True)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT,
            visit_time TIMESTAMP,
            user_agent TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_visitor(ip_address, user_agent):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO visitors (ip_address, visit_time, user_agent) VALUES (?, ?, ?)",
        (ip_address, datetime.now(), user_agent)
    )
    conn.commit()
    conn.close()

def get_visitor_count():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM visitors")
    count = cursor.fetchone()[0]
    conn.close()
    return count

@app.route('/')
def home():
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    log_visitor(ip_address, user_agent)
    visitors = get_visitor_count()

    return f"""
    <h1>Flask Docker App</h1>
    <p>Status: Running in Docker</p>
    <p>Total Visitors: {visitors}</p>
    <p>Your IP: {ip_address}</p>
    """

@app.route('/health')
def health():
    return jsonify(status="healthy", visitors=get_visitor_count())

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
