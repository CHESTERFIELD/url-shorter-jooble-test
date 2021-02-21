from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .url import UrlModel
from .user import User

__all__ = ['UrlModel', 'User']
