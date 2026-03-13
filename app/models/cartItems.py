from datetime import timezone, datetime

from app import db


class CartItem(db.Model):
    __tablename__ = "cart_items"
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey("product_details.id"), nullable = False)
    quantity = db.Column(db.Integer , nullable = False , default = 1)
    price_at_time = db.Column(db.Float, nullable = False)

    created_at = db.Column(db.DateTime,default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),nullable=False)
    product = db.relationship("Product", backref="cart_items")

    __table_args__ = (
        db.UniqueConstraint("cart_id", "product_id", name="unique_cart_product"),
        db.Index('idx_cartitem_cart_id', 'cart_id'),
        db.Index('idx_cartitem_product_id', 'product_id'),
    )