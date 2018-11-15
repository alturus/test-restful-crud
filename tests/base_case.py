import unittest
import json
from app import create_app, db


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    @staticmethod
    def get_api_headers():
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def register_user(self, username, password):
        user = {
            'username': username,
            'password': password,
        }
        response = self.client.post(
            '/auth/registration',
            headers=self.get_api_headers(),
            data=json.dumps(user)
        )
        return response

    def get_headers_with_auth(self):
        response = self.register_user('user1', 'user1')
        access_token = json.loads(response.data.decode())['access_token']
        headers = self.get_api_headers()
        headers.update({
            'Authorization': 'Bearer {}'.format(access_token),
        })
        return headers

    def login_user(self, username, password):
        user = {
            'username': username,
            'password': password,
        }
        response = self.client.post(
            '/auth/login',
            headers=self.get_api_headers(),
            data=json.dumps(user)
        )
        return response
