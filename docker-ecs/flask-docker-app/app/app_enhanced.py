from flask import Flask, request, jsonify
import redis, sqlite3, os
from datetime import datetime

app = Flask(__name__)

DATABASE = '/app/data/visitors.db'
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

def init_db():
    os.makedirs('/app/data', exist_ok=True)
    conn = sqlite3.connect(DATABASE)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS visitors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT,
        time TEXT
    )""")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    redis_client.incr("page_views")
    conn = sqlite3.connect(DATABASE)
    conn.execute("INSERT INTO visitors VALUES (NULL, ?, ?)",
                 (request.remote_addr, datetime.now()))
    conn.commit()
    conn.close()

    return f"Page Views: {redis_client.get('page_views')}"

@app.route('/health')
def health():
    return jsonify(status="ok", page_views=redis_client.get("page_views"))

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
