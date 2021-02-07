import random
import string
import unittest

from api import create_api
from app import create_app
import json
import faker

from models import db


class TestFlaskApi(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')
        self.api = create_api(self.app)
        self.test_client = self.app.test_client()
        self.db = db

    def test_post_url_on_unique_hash_url(self):
        for _ in range(100000):

            response = self.test_client.post('/api/v1/url',
                                             content_type='application/json',
                                             data=json.dumps({'full_url': fake_url(),
                                                              'life_period': random.randrange(1, 365)}))
            self.assertEqual(response.status_code, 201)

    def tearDown(self):
        # Delete Database table after the test is complete
        pass


def fake_url():
    domain = ''.join(random.choice(string.digits+string.ascii_letters) for _ in range(9))
    param1 = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(9))
    param2 = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(9))
    return "http://{domain}.com/?param1={param1}&param2={param2}".format(domain=domain, param2=param2, param1=param1)


if __name__ == "__main__":
    unittest.main()
