from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import uuid
import datetime

DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/casemgr")
ALERT_THRESHOLD = float(os.getenv("ALERT_THRESHOLD", "100000.0"))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Trade(db.Model):
    __tablename__ = "trades"
    id = db.Column(db.String, primary_key=True)
    trade_id = db.Column(db.String, nullable=False)
    instrument = db.Column(db.String)
    amount = db.Column(db.Float)
    currency = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Alert(db.Model):
    __tablename__ = "alerts"
    id = db.Column(db.String, primary_key=True)
    trade_id = db.Column(db.String, nullable=False)
    reason = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

db.create_all()

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status":"ok"}), 200

@app.route("/trades", methods=["POST"])
def create_trade():
    payload = request.get_json()
    trade_id = payload.get("trade_id") or str(uuid.uuid4())
    trade = Trade(
        id=str(uuid.uuid4()),
        trade_id=trade_id,
        instrument=payload.get("instrument"),
        amount=float(payload.get("amount", 0)),
        currency=payload.get("currency", "USD")
    )
    db.session.add(trade)
    db.session.commit()

    # simple synchronous alert rule
    if trade.amount >= ALERT_THRESHOLD:
        alert = Alert(id=str(uuid.uuid4()), trade_id=trade.trade_id,
                      reason=f"Amount {trade.amount} >= threshold {ALERT_THRESHOLD}")
        db.session.add(alert)
        db.session.commit()
        # TODO: publish to Kafka / Event Hub / Notification service
        return jsonify({"trade_id": trade.trade_id, "alerted": True}), 201

    return jsonify({"trade_id": trade.trade_id, "alerted": False}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
