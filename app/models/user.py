from datetime import datetime, timezone

from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    is_active = db.Column(db.Boolean, nullable = False , server_default ="1")
    is_superadmin = db.Column(db.Boolean, nullable = False, server_default ="0")
    created_at = db.Column(db.DateTime,default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),nullable=False)
    updated_at = db.Column(db.DateTime,default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), onupdate=datetime.now(timezone.utc).replace(tzinfo=None),nullable=False)


    address = db.relationship("Address", backref="user", lazy=True)

    products = db.relationship("Product", backref="user", lazy=True)

    roles = db.relationship("Role", secondary="user_roles", back_populates="users")
    
    reviews = db.relationship("ProductReview", backref="user", lazy=True)

    __table_args__ = (
        db.Index('idx_user_is_active', 'is_active'),
        db.Index('idx_user_created_at', 'created_at'),
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def has_permission(self, permission):
        perm_name = permission.value if hasattr(permission, "value") else str(permission)
        for role in self.roles:
            
                for perm in role.permissions:
                    if perm.name == perm_name:
                        return True
        return False
