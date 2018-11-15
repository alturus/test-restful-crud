import unittest
import json
import time
from app import db
from app.auth.model.user import User
from tests.base_case import BaseTestCase


class TestAuthCase(BaseTestCase):

    def test_user_registration(self):
        username = 'user1'
        password = 'pass1'
        response = self.register_user(username, password)
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'User {} was created'.format(username))
        self.assertTrue(data['access_token'])
        self.assertTrue(data['refresh_token'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_registered_with_already_registered_user(self):
        # Initial user registration
        username = 'user1'
        password = 'pass1'
        self.register_user(username, password)

        # Attempt to register same user
        response = self.register_user(username, 'password')
        data = json.loads(response.data.decode())
        self.assertTrue(data['error'] == 'An user with the same username already exists')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_registered_user_login(self):
        # Initial user registration
        username = 'user1'
        password = 'pass1'
        self.register_user(username, password)

        # registered user login
        response = self.login_user(username, password)
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'], 'Logged in as {}'.format(username))
        self.assertTrue(data['access_token'])
        self.assertTrue(data['refresh_token'])
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_non_registered_user_login(self):
        username = 'user2'
        password = 'pass2'
        response = self.login_user(username, password)
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'User {} does not exist'.format(username))
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 404)

    def test_registered_user_login_with_wrong_password(self):
        # Initial user registration
        username = 'user1'
        password = 'pass1'
        self.register_user(username, password)

        response = self.login_user(username, 'pass2')
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'Wrong credentials')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 403)

    def test_invalid_user_login(self):
        # try login without any data
        response = self.client.post(
            '/auth/login',
            headers=self.get_api_headers(),
            data=json.dumps(dict())
        )
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'], 'No input data provided')
        self.assertEqual(response.status_code, 400)

        # try login with wrong data
        response = self.client.post(
            '/auth/login',
            headers=self.get_api_headers(),
            data=json.dumps(dict(user='test'))
        )
        data = json.loads(response.data.decode())
        self.assertEqual(data['username'][0], 'Missing data for required field.')
        self.assertEqual(data['password'][0], 'Missing data for required field.')
        self.assertEqual(response.status_code, 400)

    def test_valid_logout_access_and_refresh_tokens(self):
        # user registration
        username = 'user1'
        password = 'pass1'
        self.register_user(username, password)

        # user login
        response = self.login_user(username, password)
        data = json.loads(response.data.decode())
        access_token = data['access_token']
        refresh_token = data['refresh_token']
        self.assertTrue(data['message'] == 'Logged in as {}'.format(username))
        self.assertTrue(access_token)
        self.assertTrue(refresh_token)
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)

        # valid access token logout
        headers = self.get_api_headers()
        headers.update({
            'Authorization': 'Bearer {}'.format(access_token),
        })
        response = self.client.post(
            '/auth/logout/access',
            headers=headers,
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'Access token has been revoked')
        self.assertEqual(response.status_code, 200)

        # valid refresh token logout
        headers = self.get_api_headers()
        headers.update({
            'Authorization': 'Bearer {}'.format(refresh_token),
        })
        response = self.client.post(
            '/auth/logout/refresh',
            headers=headers,
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'Refresh token has been revoked')
        self.assertEqual(response.status_code, 200)

    def test_invalid_logout_access_token_then_refresh_token(self):
        # user registration
        username = 'user1'
        password = 'pass1'
        self.register_user(username, password)

        # user login
        response = self.login_user(username, password)
        data = json.loads(response.data.decode())
        access_token = data['access_token']
        refresh_token = data['refresh_token']
        self.assertTrue(data['message'] == 'Logged in as {}'.format(username))
        self.assertTrue(access_token)
        self.assertTrue(refresh_token)
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)

        time.sleep(6)

        # invalid access token logout
        headers = self.get_api_headers()
        headers.update({
            'Authorization': 'Bearer {}'.format(access_token),
        })
        response = self.client.post(
            '/auth/logout/access',
            headers=headers,
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'Token has expired')
        self.assertEqual(response.status_code, 401)

        # access token refresh
        headers.update({
            'Authorization': 'Bearer {}'.format(refresh_token),
        })
        response = self.client.post(
            '/auth/token/refresh',
            headers=headers,
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['username'] == username)
        access_token = data['access_token']
        self.assertEqual(response.status_code, 200)

        # valid access token logout with refreshed token
        headers.update({
            'Authorization': 'Bearer {}'.format(access_token),
        })
        response = self.client.post(
            '/auth/logout/access',
            headers=headers,
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'Access token has been revoked')
        self.assertEqual(response.status_code, 200)

    def test_get_admin_resource_without_admin_rights(self):
        # user registration
        username = 'user1'
        password = 'pass1'
        response = self.register_user(username, password)
        data = json.loads(response.data.decode())
        access_token = data['access_token']

        headers = self.get_api_headers()
        headers.update({
            'Authorization': 'Bearer {}'.format(access_token),
        })
        response = self.client.get(
            '/auth/users/',
            headers=headers,
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == '{} does not have access'.format(username))
        self.assertEqual(response.status_code, 403)

    def test_get_admin_resource_with_admin_rights(self):
        # create admin user
        username = 'admin'
        password = 'pass1'
        user = User(username, password, admin=True)
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()

        # admin user login
        response = self.login_user(username, password)
        data = json.loads(response.data.decode())
        access_token = data['access_token']
        self.assertTrue(data['message'] == 'Logged in as {}'.format(username))

        # access to UserList resource
        headers = self.get_api_headers()
        headers.update({
            'Authorization': 'Bearer {}'.format(access_token),
        })
        response = self.client.get(
            '/auth/users/',
            headers=headers,
        )
        data = json.loads(response.data.decode())
        self.assertEqual(data[0]['username'], username)
        self.assertTrue(data[0]['url'])
        self.assertEqual(response.status_code, 200)

        # access to User resource
        response = self.client.get(
            '/auth/users/1',
            headers=headers,
        )
        data = json.loads(response.data.decode())
        self.assertEqual(data['username'], username)
        self.assertTrue(data['password'])
        self.assertTrue(data['registered_on'])
        self.assertTrue(data['url'])
        self.assertEqual(response.status_code, 200)

        # delete user with admin rights
        response = self.client.delete(
            '/auth/users/1',
            headers=headers,
        )
        self.assertEqual(response.status_code, 204)

    def test_valid_blacklisted_token_logout(self):
        # user registration
        username = 'user1'
        password = 'pass1'
        response = self.register_user(username, password)
        data = json.loads(response.data.decode())
        access_token = data['access_token']
        refresh_token = data['refresh_token']

        # revoke access token
        headers = self.get_api_headers()
        headers.update({
            'Authorization': 'Bearer {}'.format(access_token),
        })
        response = self.client.post(
            '/auth/logout/access',
            headers=headers,
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'Access token has been revoked')
        self.assertEqual(response.status_code, 200)

        # invalid resource get with revoked token
        response = self.client.get(
            '/auth/users/',
            headers=headers,
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'Token has been revoked')
        self.assertEqual(response.status_code, 401)

        # revoke refresh token
        headers = self.get_api_headers()
        headers.update({
            'Authorization': 'Bearer {}'.format(refresh_token),
        })
        response = self.client.post(
            '/auth/logout/refresh',
            headers=headers,
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'Refresh token has been revoked')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
