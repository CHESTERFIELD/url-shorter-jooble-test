import random
import string
import unittest

from api_creator import create_api
from app_creator import create_app
import json
import faker

from models import db


class TestFlaskApi(unittest.TestCase):
    """
        Test API for creating a new entity with a short URL
        For testing, paste in the working container with flask application command -
        cd src/ && python -m unittest tests.test_api
    """
    def setUp(self):
        self.app = create_app('test')
        self.api = create_api(self.app)
        self.test_client = self.app.test_client()
        self.db = db

    def test_api(self):
        # test post without data
        response = self.test_client.post('/api/v1/url',
                                         content_type='application/json',
                                         data={})
        self.assertEqual(response.status_code, 400)

        # test post with invalid url
        response = self.test_client.post('/api/v1/url',
                                         content_type='application/json',
                                         data=json.dumps({'full_url': 'httpss://ua.jooble.org/'}))
        self.assertEqual(response.status_code, 400)

        # test post with invalid life period
        response = self.test_client.post('/api/v1/url',
                                         content_type='application/json',
                                         data=json.dumps({'full_url': 'https://ua.jooble.org/',
                                                          'life_period': 1000}))
        self.assertEqual(response.status_code, 400)

        # common post request
        response = self.test_client.post('/api/v1/url',
                                         content_type='application/json',
                                         data=json.dumps({'full_url': 'https://ua.jooble.org/',
                                                          'life_period': random.randrange(1, 365)}))
        self.assertEqual(response.status_code, 201)

        # test post with exists url
        response = self.test_client.post('/api/v1/url',
                                         content_type='application/json',
                                         data=json.dumps({'full_url': 'https://ua.jooble.org/'}))
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        # Delete Database table after the test is complete
        pass


if __name__ == "__main__":
    unittest.main()
