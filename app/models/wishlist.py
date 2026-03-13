from app import db
from datetime import datetime, timezone

class Wishlist(db.Model):
    __tablename__ = 'wishlists'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product_details.id'), nullable=False)
    created_at = db.Column(db.DateTime,default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),nullable=False)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id', name='unique_wishlist'),)
    product = db.relationship('Product', backref='wishlists')