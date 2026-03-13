from datetime import datetime, timezone

from app import db


class Permission(db.Model):
    __tablename__ ="permissions"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True, nullable = False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime,default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),nullable=False)

    roles = db.relationship("Role", secondary= "role_permissions", back_populates = "permissions")
