from datetime import datetime, timezone
from sqlalchemy import UniqueConstraint
from app import db


class Address(db.Model):
    __tablename__ = "address"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    house_number = db.Column(db.String(50), nullable=True)
    street_name = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "house_number",
            "street_name",
            "city",
            "state",
            "pincode",
            name="unique_user_address"
        ),
        db.Index('idx_address_user_id', 'user_id'),
    )