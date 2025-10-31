from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Case(db.Model):
    __tablename__ = "cases"
    id = db.Column(db.String, primary_key=True)
    trade_id = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    status = db.Column(db.String, default="OPEN")
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "trade_id": self.trade_id,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
