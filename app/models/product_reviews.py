from datetime import datetime
from app.extensions import db
from datetime import timezone

class ProductReview(db.Model):
    __tablename__ = 'product_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product_details.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime,default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),nullable=False)
    updated_at = db.Column(db.DateTime,default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), onupdate=datetime.now(timezone.utc).replace(tzinfo=None),nullable=False)

    __table_args__ = (
    db.UniqueConstraint('user_id', 'product_id', name='unique_user_product_review'),
    )
    