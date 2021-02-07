from flask_restful import Api

from resources.url import UrlAPI


def create_api(app):
    api = Api(app)
    api.add_resource(UrlAPI, '/api/v1/url')
    return api
