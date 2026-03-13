from datetime import datetime, timezone

from app import db
from app.models.enums import OrderStatus, PaymentStatus


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    total_amount = db.Column(db.Float,nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey("address.id"), nullable=False)
    delivery_address = db.Column(db.Text, nullable = False)

    payment_mode = db.Column(db.String(50),nullable=True)
    payment_status = db.Column(db.Enum(PaymentStatus), default = PaymentStatus.PENDING, nullable = False)
    order_status = db.Column(db.Enum(OrderStatus), default = OrderStatus.PENDING, nullable = False)
    created_at = db.Column(db.DateTime,default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),nullable=False)

    order_items = db.relationship("OrderItem", backref="order", lazy=True)

    __table_args__ = (
        db.Index('idx_order_user_id', 'user_id'),
        db.Index('idx_order_address_id', 'address_id'),
        db.Index('idx_order_status', 'order_status'),
        db.Index('idx_order_payment_status', 'payment_status'),
        db.Index('idx_order_created_at', 'created_at'),
    )