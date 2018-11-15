from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from ..model.author import Author, AuthorSchema
from app.util import status
from app import db

author_schema = AuthorSchema()


class AuthorResource(Resource):
    def get(self, id):
        author = Author.query.get_or_404(id)
        result = author_schema.dump(author).data
        return result

    @jwt_required
    def patch(self, id):
        author = Author.query.get_or_404(id)
        author_dict = request.get_json()

        if not author_dict:
            response = {'message': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST

        author_firstname = author_dict.get('firstname', author.firstname)
        author_lastname = author_dict.get('lastname', author.lastname)

        if Author.is_unique(id=0, firstname=author_firstname, lastname=author_lastname):
            author.firstname = author_firstname or author.firstname
            author.lastname = author_lastname or author.lastname
        else:
            response = {'error': 'An author with the same name already exists'}
            return response, status.HTTP_400_BAD_REQUEST

        dumped_author, dump_errors = author_schema.dump(author)

        if dump_errors:
            return dump_errors, status.HTTP_400_BAD_REQUEST

        validate_errors = author_schema.validate(dumped_author)
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
        author = Author.query.get_or_404(id)

        try:
            db.session.delete(author)
            db.session.commit()

            response = {}

            return response, status.HTTP_204_NO_CONTENT

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {"error": str(e)}

            return response, status.HTTP_401_UNAUTHORIZED


class AuthorListResource(Resource):
    def get(self):
        authors = Author.query.all()
        results = author_schema.dump(authors, many=True).data
        return results

    @jwt_required
    def post(self):
        request_dict = request.get_json()

        if not request_dict:
            response = {'message': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST

        validate_errors = author_schema.validate(request_dict)
        if validate_errors:
            return validate_errors, status.HTTP_400_BAD_REQUEST

        author_firstname = request_dict['firstname']
        author_lastname = request_dict['lastname']

        if not Author.is_unique(id=0, firstname=author_firstname, lastname=author_lastname):
            response = {'error': 'An author with the same name already exists'}
            return response, status.HTTP_400_BAD_REQUEST

        try:
            author = Author(
                firstname=author_firstname,
                lastname=author_lastname,
            )

            db.session.add(author)
            db.session.commit()

            query = Author.query.get(author.id)
            result = author_schema.dump(query).data

            return result, status.HTTP_201_CREATED

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {"error": str(e)}

            return response, status.HTTP_400_BAD_REQUEST
