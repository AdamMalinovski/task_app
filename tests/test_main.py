from api.main import app

from unittest import TestCase

class TestHome(TestCase):
    def test_home(self):
        with app.test_client() as c:
            response = c.get('/')

            self.assertEqual(response.status_code, 200)