import unittest
import json
from tests.base_case import BaseTestCase


class APITestCase(BaseTestCase):

    def test_booklist_resource_get_and_post(self):
        # add a book (POST request)
        book = {
            "title": "The Hitchhiker's Guide to Python: Best Practices for Development",
            "isbn": 9781491933176,
            "year": 2016,
            "authors": [
                {"firstname": "Kenneth", "lastname": "Reitz"},
                {"firstname": "Tanya", "lastname": "Schlusser"}
            ]
        }
        headers_with_auth = self.get_headers_with_auth()
        response = self.client.post(
            '/api/v1/books/',
            headers=headers_with_auth,
            data=json.dumps(book)
        )
        self.assertEqual(response.status_code, 201)
        url = json.loads(response.data).get('url')
        self.assertIsNotNone(url)

        # add a book with isdn what already exists
        response = self.client.post(
            '/api/v1/books/',
            headers=headers_with_auth,
            data=json.dumps(book)
        )
        self.assertEqual(response.status_code, 400)
        error = json.loads(response.data).get('error')
        self.assertEqual(error, 'A book with the same ISBN already exists')

        # get all books (GET request)
        response = self.client.get(
            '/api/v1/books/',
            headers=self.get_api_headers(),
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        url = response_data[0].get('url')
        title = response_data[0].get('title')
        self.assertIsNotNone(url)
        self.assertEqual(title, "The Hitchhiker's Guide to Python: Best Practices for Development")

    def test_booklist_resource_creation_with_missed_field(self):
        book = {
            "title": "Python for 21 days",
        }
        headers_with_auth = self.get_headers_with_auth()
        response = self.client.post(
            '/api/v1/books/',
            headers=headers_with_auth,
            data=json.dumps(book)
        )
        self.assertEqual(response.status_code, 400)
        error = json.loads(response.data).get('isbn')[0]
        self.assertEqual(error, 'Missing data for required field.')

    def test_book_resource_get_delete_update(self):
        # add a book (POST request)
        book = {
            "title": "The Hitchhiker's Guide to Python: Best Practices for Development",
            "isbn": 9781491933176,
            "year": 2016,
            "authors": [
                {"firstname": "Kenneth", "lastname": "Reitz"},
                {"firstname": "Tanya", "lastname": "Schlusser"}
            ]
        }

        headers_with_auth = self.get_headers_with_auth()

        response = self.client.post(
            '/api/v1/books/',
            headers=headers_with_auth,
            data=json.dumps(book)
        )
        self.assertEqual(response.status_code, 201)
        url = json.loads(response.data).get('url')
        self.assertIsNotNone(url)

        # update the book
        book = {
            "title": "New Title",
            "authors": [{
                "firstname": "John",
                 "lastname": "Smith"
            }]
        }
        response = self.client.patch(
            '/api/v1/books/1',
            headers=headers_with_auth,
            data=json.dumps(book)
        )
        self.assertEqual(response.status_code, 200)
        url = json.loads(response.data).get('url')
        title = json.loads(response.data).get('title')
        self.assertEqual(title, 'New Title')
        self.assertIsNotNone(url)

        # book already exists
        book = {
            "isbn": 9781491933176
        }
        response = self.client.patch(
            '/api/v1/books/1',
            headers=headers_with_auth,
            data=json.dumps(book)
        )
        self.assertEqual(response.status_code, 400)
        error = json.loads(response.data).get('error')
        self.assertEqual(error, 'A book with the same ISBN already exists')

        # book with invalid field (validation)
        book = {
            "year": "year"
        }
        response = self.client.patch(
            '/api/v1/books/1',
            headers=headers_with_auth,
            data=json.dumps(book)
        )
        self.assertEqual(response.status_code, 400)
        year_field = json.loads(response.data).get('year')[0]
        self.assertEqual(year_field, 'Not a valid integer.')

        # book with invalid authors field (is not array)
        book = {
            "authors": {
                "firstname": "Dan"
            }
        }
        response = self.client.patch(
            '/api/v1/books/1',
            headers=headers_with_auth,
            data=json.dumps(book)
        )
        self.assertEqual(response.status_code, 400)
        error = json.loads(response.data).get('error')
        self.assertEqual(error, "'authors' field must be an array")

        # book with invalid authors field (missing lastname field)
        book = {
            "authors": [{
                "firstname": "Dan"
            }]
        }
        response = self.client.patch(
            '/api/v1/books/1',
            headers=headers_with_auth,
            data=json.dumps(book)
        )
        self.assertEqual(response.status_code, 400)
        lastname_field = json.loads(response.data).get('lastname')[0]
        self.assertEqual(lastname_field, 'Missing data for required field.')

        # delete the book
        response = self.client.delete(
            '/api/v1/books/1',
            headers=headers_with_auth
        )
        self.assertEqual(response.status_code, 204)

        # try to delete with wrong url
        response = self.client.delete(
            '/api/v1/books/2',
            headers=headers_with_auth
        )
        self.assertEqual(response.status_code, 404)

    def test_authorlist_resource_creation(self):
        author = {
            "firstname": "Kenneth",
            "lastname": "Reitz",
        }

        headers_with_auth = self.get_headers_with_auth()

        response = self.client.post(
            '/api/v1/authors/',
            headers=headers_with_auth,
            data=json.dumps(author)
        )
        self.assertEqual(response.status_code, 201)
        url = json.loads(response.data).get('url')
        self.assertIsNotNone(url)

        # add an author what already exist
        response = self.client.post(
            '/api/v1/authors/',
            headers=headers_with_auth,
            data=json.dumps(author)
        )
        self.assertEqual(response.status_code, 400)
        error = json.loads(response.data).get('error')
        self.assertEqual(error, 'An author with the same name already exists')

    def test_authorlist_resource_creation_with_missed_field(self):
        author = {
            "firstname": "Kenneth",
        }

        headers_with_auth = self.get_headers_with_auth()

        response = self.client.post(
            '/api/v1/authors/',
            headers=headers_with_auth,
            data=json.dumps(author)
        )
        self.assertEqual(response.status_code, 400)
        error = json.loads(response.data).get('lastname')[0]
        self.assertEqual(error, 'Missing data for required field.')

    def test_authorlist_resourse_get_all(self):
        author = {
            "firstname": "Kenneth",
            "lastname": "Reitz",
        }

        headers_with_auth = self.get_headers_with_auth()

        response = self.client.post(
            '/api/v1/authors/',
            headers=headers_with_auth,
            data=json.dumps(author)
        )
        self.assertEqual(response.status_code, 201)
        url = json.loads(response.data).get('url')
        self.assertIsNotNone(url)

        # get all authors
        response = self.client.get(
            '/api/v1/authors/',
            headers=self.get_api_headers()
        )
        self.assertEqual(response.status_code, 200)
        url = json.loads(response.data)[0].get('url')
        self.assertIsNotNone(url)

    def test_author_resource_get(self):
        author = {
            "firstname": "Kenneth",
            "lastname": "Reitz",
        }

        headers_with_auth = self.get_headers_with_auth()

        response = self.client.post(
            '/api/v1/authors/',
            headers=headers_with_auth,
            data=json.dumps(author)
        )
        self.assertEqual(response.status_code, 201)
        url = json.loads(response.data).get('url')
        self.assertIsNotNone(url)

        # get author
        response = self.client.get(
            '/api/v1/authors/1',
            headers=self.get_api_headers()
        )
        self.assertEqual(response.status_code, 200)
        url = json.loads(response.data).get('url')
        self.assertIsNotNone(url)

    def test_author_resource_delete(self):
        author = {
            "firstname": "Kenneth",
            "lastname": "Reitz",
        }

        headers_with_auth = self.get_headers_with_auth()

        response = self.client.post(
            '/api/v1/authors/',
            headers=headers_with_auth,
            data=json.dumps(author)
        )
        self.assertEqual(response.status_code, 201)
        url = json.loads(response.data).get('url')
        self.assertIsNotNone(url)

        response = self.client.delete(
            '/api/v1/authors/1',
            headers=headers_with_auth
        )
        self.assertEqual(response.status_code, 204)

        # try to delete with wrong url
        response = self.client.delete(
            '/api/v1/authors/2',
            headers=headers_with_auth
        )
        self.assertEqual(response.status_code, 404)

    def test_author_resource_update(self):
        # create author
        author = {
            "firstname": "Kenneth",
            "lastname": "Reitz",
        }

        headers_with_auth = self.get_headers_with_auth()

        response = self.client.post(
            '/api/v1/authors/',
            headers=headers_with_auth,
            data=json.dumps(author)
        )
        self.assertEqual(response.status_code, 201)
        url = json.loads(response.data).get('url')
        self.assertIsNotNone(url)

        # test author already exists
        response = self.client.patch(
            '/api/v1/authors/1',
            headers=headers_with_auth,
            data=json.dumps(author)
        )
        self.assertEqual(response.status_code, 400)
        error = json.loads(response.data).get('error')
        self.assertEqual(error, 'An author with the same name already exists')

        # test author update (patch request)
        author = {
            "lastname": "Reitzzz"
        }
        response = self.client.patch(
            '/api/v1/authors/1',
            headers=headers_with_auth,
            data=json.dumps(author)
        )
        self.assertEqual(response.status_code, 200)
        url = json.loads(response.data).get('url')
        self.assertIsNotNone(url)

        # test without data
        author = dict()
        response = self.client.patch(
            '/api/v1/authors/1',
            headers=headers_with_auth,
            data=json.dumps(author)
        )
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data).get('message')
        self.assertEqual(message, 'No input data provided')


if __name__ == "__main__":
    unittest.main()
