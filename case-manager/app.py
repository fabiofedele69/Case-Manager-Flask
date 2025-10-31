from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Case
import os
import uuid
import datetime

DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/casemgr")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/cases", methods=["GET"])
def get_cases():
    cases = Case.query.all()
    return jsonify([c.to_dict() for c in cases]), 200

@app.route("/cases", methods=["POST"])
def create_case():
    payload = request.get_json()
    case = Case(
        id=str(uuid.uuid4()),
        trade_id=payload.get("trade_id"),
        description=payload.get("description", "No description provided"),
        status="OPEN",
        created_at=datetime.datetime.utcnow(),
    )
    db.session.add(case)
    db.session.commit()
    return jsonify(case.to_dict()), 201

@app.route("/cases/<case_id>", methods=["PATCH"])
def update_case(case_id):
    case = Case.query.get(case_id)
    if not case:
        return jsonify({"error": "Case not found"}), 404

    payload = request.get_json()
    if "status" in payload:
        case.status = payload["status"]
    if "description" in payload:
        case.description = payload["description"]

    case.updated_at = datetime.datetime.utcnow()
    db.session.commit()
    return jsonify(case.to_dict()), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
