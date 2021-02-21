import datetime
from urllib.request import urlopen, Request
from uuid import UUID

from lxml.html import parse
from sqlalchemy.exc import IntegrityError

from bl.url_shorter_helper import UrlShorterHelper
from exceptions import ResourceExists
from models import UrlModel
from models import db


class UrlRepository:

    @staticmethod
    def create(full_url: str, life_period: int) -> UrlModel:
        """ Create url """
        try:
            current_date = datetime.date.today()
            expire_date = current_date + datetime.timedelta(days=life_period)

            url_hash = UrlShorterHelper.get_unique_hash_url(full_url)

            request = Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
            page = urlopen(request)
            p = parse(page)
            title = p.find(".//title").text

            url = UrlModel(full_url=full_url, url_hash=url_hash, expire_date=expire_date, full_url_title=title)
            db.session.add(url)
            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            raise ResourceExists('url already exists')

        return url

    @staticmethod
    def get(url_hash: str) -> UrlModel:
        """ Query a url by full_url """
        url = UrlModel.query.filter_by(url_hash=url_hash).first_or_404()

        return url

    @staticmethod
    def get_by_id(id: UUID) -> UrlModel:
        """ Query a url by id """
        url = UrlModel.query.filter_by(id=id).first_or_404()

        return url

    @staticmethod
    def get_exist_url(full_url: str) -> UrlModel:
        """ Query a url by full_url """
        url = UrlModel.query.filter_by(full_url=full_url).first()

        return url

    @staticmethod
    def list() -> list:
        return UrlModel.query.all()

    @staticmethod
    def delete(id: UUID) -> None:
        UrlModel.query.filter_by(id=id).delete()
        db.session.commit()

    @staticmethod
    def paginate(page: int, per_page: int) -> list:
        return UrlModel.query.paginate(page=page, per_page=per_page)
