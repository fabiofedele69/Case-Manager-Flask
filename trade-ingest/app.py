from flask import Flask, request, jsonify
import os
import psycopg2

app = Flask(__name__)
DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/casemgr")
ALERT_THRESHOLD = float(os.getenv("ALERT_THRESHOLD", "100000"))

def get_db_conn():
    return psycopg2.connect(DB_URL)

@app.route("/trades", methods=["POST"])
def ingest_trade():
    data = request.json
    amount = data.get("amount", 0)
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO trades (trade_id, instrument, amount, currency) VALUES (%s, %s, %s, %s)",
        (data["trade_id"], data["instrument"], amount, data["currency"]),
    )
    conn.commit()
    cur.close()
    conn.close()

    alert = amount > ALERT_THRESHOLD
    return jsonify({"status": "ingested", "alert": alert}), 201

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
