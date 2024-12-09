from app import db
from datetime import datetime, timezone

class BlockedToken(db.Model):
    __tablename__ = 'blocked_tokens'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jti = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))  # Use timezone-aware datetime
