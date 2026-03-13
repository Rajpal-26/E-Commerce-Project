from app.extensions import db

class Product(db.Model):
    __tablename__ = "product_details"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), unique=False, nullable=False)
    model_number = db.Column(db.String(100),nullable=False,unique=True)
    specification = db.Column(db.String(100),nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    images = db.Column(db.JSON)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
    reviews = db.relationship("ProductReview", backref="product", lazy=True)

    __table_args__ = (
        db.Index('idx_product_user_id', 'user_id'),
        db.Index('idx_product_name', 'name'),
        db.Index('idx_product_stock', 'stock'),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "model_number": self.model_number,
            "specification": self.specification,
            "price": self.price,
            "stock": self.stock,
            "images": self.images

        }
        

