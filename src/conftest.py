from flask_restful import Api
from app import create_app

from resources.url import UrlAPI


@pytest.fixture
def app():
    app = create_app()
    api = Api(app)
    api.add_resource(UrlAPI, '/api/v1/url', 'urls')
    return app