import datetime

from sqlalchemy.dialects.postgresql import UUID
import uuid
from . import db


class UrlModel(db.Model):
    __tablename__ = 'urls'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    full_url = db.Column(db.String, unique=True, nullable=False)
    url_hash = db.Column(db.String, unique=True, nullable=False)
    full_url_title = db.Column(db.String, nullable=True, default=None)
    expire_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

