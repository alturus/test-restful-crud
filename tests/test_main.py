import unittest
from tests.base_case import BaseTestCase


class TestMainApp(BaseTestCase):

    def test_index_page(self):
        response = self.client.get(
            '/',
        )
        data = response.data.decode()
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
