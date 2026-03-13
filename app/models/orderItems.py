from app import db


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"),nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product_details.id"),nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    __table_args__ = (
        db.Index('idx_orderitem_order_id', 'order_id'),
        db.Index('idx_orderitem_product_id', 'product_id'),
    )

    # order = db.relationship("Order")
