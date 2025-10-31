from flask import Flask, request, jsonify
import psycopg2, os
from models import init_db

app = Flask(__name__)
DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/casemgr")

init_db(DB_URL)

@app.route("/cases", methods=["POST"])
def create_case():
    data = request.json
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO cases (trade_id, description, status) VALUES (%s, %s, %s) RETURNING id",
        (data["trade_id"], data["description"], "OPEN"),
    )
    case_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"case_id": case_id, "status": "created"}), 201

@app.route("/cases", methods=["GET"])
def list_cases():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT id, trade_id, description, status FROM cases")
    cases = [{"id": r[0], "trade_id": r[1], "description": r[2], "status": r[3]} for r in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(cases)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
