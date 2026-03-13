from datetime import datetime, timezone
from app import db


class Email(db.Model):
    __tablename__="email"
    id = db.Column(db.Integer,primary_key=True)
    gmail_id = db.Column(db.String(255), nullable=False)
    sender = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=True)
    body = db.Column(db.Text, nullable=True)
    received_at = db.Column(db.DateTime,default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),nullable=False)
    
    attachments = db.relationship("Email_Attachment", backref="email", lazy=True)