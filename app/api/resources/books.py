from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from ..model.book import Book, BookSchema
from ..model.author import Author, AuthorSchema
from app.util import status
from app import db

book_schema = BookSchema()
author_schema = AuthorSchema()


class BookResource(Resource):
    def get(self, id):
        book = Book.query.get_or_404(id)
        result = book_schema.dump(book).data
        return result

    @jwt_required
    def patch(self, id):
        book = Book.query.get_or_404(id)
        book_dict = request.get_json()

        if not book_dict:
            response = {'message': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST

        if 'title' in book_dict:
            book.title = book_dict['title']

        if 'year' in book_dict:
            book.year = book_dict['year']

        if 'isbn' in book_dict:
            book_isbn = book_dict['isbn']

            if Book.is_unique(id=0, isbn=book_isbn):
                book.isbn = book_isbn
            else:
                response = {'error': 'A book with the same ISBN already exists'}
                return response, status.HTTP_400_BAD_REQUEST

        if 'authors' in book_dict:
            book_authors = book_dict['authors']

            if not isinstance(book_authors, list):
                response = {'error': "'authors' field must be an array"}
                return response, status.HTTP_400_BAD_REQUEST

            authors = []
            for author_dict in book_authors:
                validate_errors = author_schema.validate(author_dict)
                if validate_errors:
                    return validate_errors, status.HTTP_400_BAD_REQUEST

                author_firstname = author_dict['firstname']
                author_lastname = author_dict['lastname']
                author = Author.query.filter_by(firstname=author_firstname, lastname=author_lastname).first()

                if author is None:
                    # Create a new Author
                    author = Author(firstname=author_firstname, lastname=author_lastname)
                    db.session.add(author)
                    db.session.commit()

                authors.append(author)
            book.authors = authors

        dumped_book, dump_errors = book_schema.dump(book)

        if dump_errors:
            return dump_errors, status.HTTP_400_BAD_REQUEST

        validate_errors = book_schema.validate(dumped_book)
        if validate_errors:
            return validate_errors, status.HTTP_400_BAD_REQUEST

        try:
            db.session.commit()
            return self.get(id)

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {"error": str(e)}

            return response, status.HTTP_400_BAD_REQUEST

    @jwt_required
    def delete(self, id):
        book = Book.query.get_or_404(id)
        try:
            db.session.delete(book)
            db.session.commit()

            response = {}

            return response, status.HTTP_204_NO_CONTENT

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {"error": str(e)}

            return response, status.HTTP_401_UNAUTHORIZED


class BookListResource(Resource):
    def get(self):
        books = Book.query.all()
        result = book_schema.dump(books, many=True).data
        return result

    @jwt_required
    def post(self):
        request_dict = request.get_json()

        if not request_dict:
            response = {'message': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST

        validate_errors = book_schema.validate(request_dict)
        if validate_errors:
            return validate_errors, status.HTTP_400_BAD_REQUEST

        book_isbn = request_dict['isbn']

        if not Book.is_unique(id=0, isbn=book_isbn):
            response = {'error': 'A book with the same ISBN already exists'}
            return response, status.HTTP_400_BAD_REQUEST

        try:
            authors = []
            for author_dict in request_dict['authors']:
                author_firstname = author_dict['firstname']
                author_lastname = author_dict['lastname']
                author = Author.query.filter_by(firstname=author_firstname, lastname=author_lastname).first()

                if author is None:
                    # Create a new Author
                    author = Author(firstname=author_firstname, lastname=author_lastname)
                    db.session.add(author)

                authors.append(author)

            # Now that we are sure we have all authors
            # create a new Book
            book = Book(
                title=request_dict['title'],
                isbn=book_isbn,
                year=request_dict['year'],
            )
            book.authors = authors

            db.session.add(book)
            db.session.commit()

            query = Book.query.get(book.id)
            result = book_schema.dump(query).data

            return result, status.HTTP_201_CREATED

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {"error": str(e)}

            return response, status.HTTP_400_BAD_REQUEST
