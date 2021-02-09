import datetime

from sqlalchemy.exc import IntegrityError

from bl.url_shorter_helper import UrlShorterHelper
from exceptions import ResourceExists
from models import UrlModel
from models import db


class UrlRepository:

    @staticmethod
    def create(full_url: str, life_period: int) -> UrlModel:
        """ Create user """
        try:
            current_date = datetime.date.today()
            expire_date = current_date + datetime.timedelta(days=life_period)
            url_hash = UrlShorterHelper.get_unique_hash_url(full_url)
            url = UrlModel(full_url=full_url, url_hash=url_hash, expire_date=expire_date)
            db.session.add(url)
            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            raise ResourceExists('url already exists')

        return url

    @staticmethod
    def get(url_hash: str) -> UrlModel:
        """ Query a user by username """
        url = UrlModel.query.filter_by(url_hash=url_hash).first_or_404()

        return url

    @staticmethod
    def get_exist_url(full_url: str) -> UrlModel:
        """ Query a user by username """
        url = UrlModel.query.filter_by(full_url=full_url).first()

        return url

    @staticmethod
    def list() -> list:
        return UrlModel.query.all()
