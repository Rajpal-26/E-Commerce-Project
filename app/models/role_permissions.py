from datetime import datetime, timezone

from app import db


class Role_permission(db.Model):
    __tablename__ = "role_permissions"
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id", ondelete="CASCADE"), primary_key = True)
    permission_id = db.Column(db.Integer, db.ForeignKey("permissions.id", ondelete="CASCADE"), primary_key = True)
    created_at = db.Column(db.DateTime,default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),nullable=False)
