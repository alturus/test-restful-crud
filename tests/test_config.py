import os
import unittest
from datetime import timedelta
from app import create_app
from config import basedir


class TestDevelopmentConfig(unittest.TestCase):
    def setUp(self):
        self.app = create_app('development')

    def test_app_is_development(self):
        self.assertTrue(self.app.config['DEBUG'] is True)
        self.assertTrue(self.app.config['SECRET_KEY'] == 'my_precious_secret_key')
        self.assertTrue(self.app.config['JWT_SECRET_KEY'] == 'jwt-secret-string')
        self.assertTrue(
            self.app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///' + os.path.join(basedir, 'books.db')
        )


class TestTestingConfig(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')

    def test_app_is_testing(self):
        self.assertTrue(self.app.config['DEBUG'] is True)
        self.assertTrue(self.app.config['TESTING'] is True)
        self.assertTrue(self.app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] is False)
        self.assertTrue(self.app.config['SECRET_KEY'] == 'my_precious_secret_key')
        self.assertTrue(self.app.config['JWT_SECRET_KEY'] == 'jwt-secret-string')
        self.assertTrue(self.app.config['JWT_ACCESS_TOKEN_EXPIRES'] == timedelta(seconds=5))
        self.assertTrue(
            self.app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///' + os.path.join(basedir, 'books_test.db')
        )


class TestProductionConfig(unittest.TestCase):
    def setUp(self):
        self.app = create_app('production')

    def test_app_is_production(self):
        self.assertTrue(self.app.config['DEBUG'] is False)
        self.assertFalse(self.app.config['SECRET_KEY'] == 'my_precious_secret_key')
        self.assertFalse(self.app.config['JWT_SECRET_KEY'] == 'jwt-secret-string')
        self.assertFalse(
            self.app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///' + os.path.join(basedir, 'books.db')
        )
        self.assertFalse(self.app.config['ADMIN_USERNAME'] == 'admin')
        self.assertFalse(self.app.config['ADMIN_PASSWORD'] == 'password')


if __name__ == "__main__":
    unittest.main()
