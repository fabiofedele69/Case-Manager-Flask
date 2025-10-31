import psycopg2

def init_db(db_url):
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id SERIAL PRIMARY KEY,
            trade_id VARCHAR(50),
            description TEXT,
            status VARCHAR(20)
        );
        CREATE TABLE IF NOT EXISTS trades (
            trade_id VARCHAR(50) PRIMARY KEY,
            instrument VARCHAR(50),
            amount NUMERIC,
            currency VARCHAR(10)
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
