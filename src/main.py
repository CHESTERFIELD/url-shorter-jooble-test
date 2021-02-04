from flask_restful import Api

from app import create_app
from flask_migrate import Migrate
from models import db
from repositories.url import UrlRepository
from resources.url import UrlAPI
from flask import redirect

app = create_app()

migrate = Migrate(app, db)
print(app.config)


@app.route('/<short_url>')
def hello_world(short_url):
    url = UrlRepository.get(url_hash=short_url)
    return redirect(url['full_url']), 301


# API
api = Api(app)
api.add_resource(UrlAPI, '/api/v1/url')
# api.add_resource(UrlAPI, '/<str:short_url>')
