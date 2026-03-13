from datetime import datetime, timezone

from app import db


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key = True, nullable= False)
    name = db.Column(db.String(50), unique = True, nullable = False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default= True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
                           onupdate=datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)

    users= db.relationship("User", secondary = "user_roles", back_populates= "roles")
    permissions = db.relationship("Permission", secondary = "role_permissions", back_populates = "roles")
    __table_args__ = (
        db.Index('idx_role_is_active', 'is_active'),
    )