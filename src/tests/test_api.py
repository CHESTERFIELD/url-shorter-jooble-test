import random
import unittest
from main import app
import json
import faker


class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        self.test_client = app.test_client()
        self.faker = faker.Faker()

    def test_post_url_on_unique_hash_url(self):
        for _ in range(100000):
            response = self.test_client.post('/api/v1/url',
                                             content_type='application/json',
                                             data=json.dumps({'full_url': self.faker.url(), 'life_period': random.randrange(1, 365)}))
            self.assertEqual(response.status_code, 201)


if __name__ == "__main__":
    unittest.main()
