import uuid

from flask_restful import Resource, fields, marshal_with
from flask_restful import reqparse
from urllib.parse import urlparse
from repositories.url import UrlRepository


def url(full_url):
    """Return full_url if valid, raise an exception in other case."""
    # TODO need write correct validation
    result = urlparse(full_url)
    print(result)
    if result.path and result.scheme and result.netloc:
        return full_url
    else:
        raise ValueError('{} is not a valid email'.format(full_url))


post_reqparse = reqparse.RequestParser()
post_reqparse.add_argument('full_url', type=url, required=True, location='json')
post_reqparse.add_argument('life_period', type=int, default=90, choices=range(366)[1:], help='choice from 1 to 365',
                           location='json')


class DaysItem(fields.Raw):
    # TODO check how work with list of attributes
    def format(self, values):
        print(values)
        return 10


class UUIDItem(fields.Raw):
    def format(self, value):
        return str(uuid.UUID(value))


url_fields = {
    'id': UUIDItem(attribute='id'),
    'full_url': fields.String,
    'url_hash': fields.String,
    'life_period': fields.Integer,
    'left_days': DaysItem(attribute=['life_period', 'created_at']),
    'created_at': fields.DateTime,
}


class UrlAPI(Resource):
    @marshal_with(url_fields)
    def post(self):
        args = post_reqparse.parse_args()
        print(args)
        result = UrlRepository.create(full_url=args['full_url'], life_period=args['life_period'])
        return result
