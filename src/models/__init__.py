from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .url import UrlModel

__all__ = ['UrlModel']
