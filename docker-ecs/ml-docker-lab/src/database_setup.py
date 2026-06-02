import psycopg2
import os
import time

def wait_for_db(host, port, database, user, password):
    while True:
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password
            )
            conn.close()
            return
        except:
            print("Waiting for database...")
            time.sleep(2)

def create_tables():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "postgres"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "mldb"),
        user=os.getenv("DB_USER", "mluser"),
        password=os.getenv("DB_PASSWORD", "mlpassword")
    )

    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id SERIAL PRIMARY KEY,
            input JSONB,
            output JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    wait_for_db("postgres", 5432, "mldb", "mluser", "mlpassword")
    create_tables()
