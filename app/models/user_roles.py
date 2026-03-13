from datetime import datetime, timezone

from app import db
from app.models import roles, user


class User_role(db.Model):
    __tablename__ = "user_roles"
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id", ondelete ="CASCADE"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    assigned_at = db.Column(db.DateTime,default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),nullable=False)
    
