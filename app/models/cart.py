from datetime import datetime, timezone

from app import db


class Cart(db.Model):
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)
    created_at = db.Column(db.DateTime,default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),nullable=False)

    items = db.relationship("CartItem",backref="cart",cascade="all, delete-orphan",lazy=True)