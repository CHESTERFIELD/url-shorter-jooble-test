from sqlalchemy.exc import IntegrityError

from bl.url_shorter_helper import UrlShorterHelper
from exceptions import ResourceExists
from models import UrlModel
from models import db


class UrlRepository:

    @staticmethod
    def create(full_url: str, life_period: int) -> dict:
        """ Create user """
        try:
            url_hash = UrlShorterHelper.get_unique_hash_url(full_url)
            url = UrlModel(full_url=full_url, url_hash=url_hash, life_period=life_period)
            db.session.add(url)
            db.session.commit()
            result = {
                'id': url.id,
                'full_url': url.full_url,
                'url_hash': url.url_hash,
                'created_at': str(url.created_at),
                'life_period': url.life_period
            }
        except IntegrityError:
            db.session.rollback()
            raise ResourceExists('url already exists')

        return result

    @staticmethod
    def get(url_hash: str) -> dict:
        """ Query a user by username """
        url = UrlModel.query.filter_by(url_hash=url_hash).first_or_404()
        result = {
            'id': url.id,
            'full_url': url.full_url,
            'url_hash': url.url_hash,
            'created_at': str(url.created_at),
            'life_period': url.life_period
        }
        return result
