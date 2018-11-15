from functools import wraps
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    verify_jwt_in_request,
    get_jwt_claims,
    get_jwt_identity,
    get_raw_jwt,
)
from .model.user import User, UserSchema
from .model.blacklist_token import BlacklistToken
from app import db, jwt
from app.util import status

user_schema = UserSchema()


def admin_required(func):
    """Decorator to check for JWT, and to check a user has admin rights"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()

        if claims['admin'] is False:
            response = {'message': '{} does not have access'.format(claims['username'])}
            return response, status.HTTP_403_FORBIDDEN
        else:
            return func(*args, **kwargs)
    return wrapper


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    """Store data in JWT: username and admin rights"""
    claims = {
        'username': identity,
        'admin': False
    }
    user = User.find_by_username(identity)
    if user:
        claims['admin'] = user.is_admin

    return claims


class UserRegistration(Resource):
    def post(self):
        request_dict = request.get_json()

        if not request_dict:
            response = {'message': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST

        validate_errors = user_schema.validate(request_dict)
        if validate_errors:
            return validate_errors, status.HTTP_400_BAD_REQUEST

        username = request_dict['username']

        if not User.is_unique(id=0, username=username):
            response = {'error': 'An user with the same username already exists'}
            return response, status.HTTP_400_BAD_REQUEST

        try:
            user = User(
                username=username,
                password=request_dict['password'],
            )

            db.session.add(user)
            db.session.commit()

            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)

            response = {
                'message': 'User {} was created'.format(username),
                'access_token': access_token,
                'refresh_token': refresh_token,
            }

            return response, status.HTTP_201_CREATED

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {"error": str(e)}

            return response, status.HTTP_400_BAD_REQUEST


class UserLogin(Resource):
    def post(self):
        request_dict = request.get_json()

        if not request_dict:
            response = {'message': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST

        validate_errors = user_schema.validate(request_dict)
        if validate_errors:
            return validate_errors, status.HTTP_400_BAD_REQUEST

        username = request_dict['username']
        password = request_dict['password']

        current_user = User.find_by_username(username)

        if not current_user:
            response = {'message': 'User {} does not exist'.format(username)}
            return response, status.HTTP_404_NOT_FOUND

        if User.check_password(current_user.password, password):
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            response = {'message': 'Wrong credentials'}
            return response, status.HTTP_403_FORBIDDEN


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = BlacklistToken(jti=jti)

            db.session.add(revoked_token)
            db.session.commit()

            response = {'message': 'Access token has been revoked'}
            return response

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {"error": str(e)}
            return response, status.HTTP_400_BAD_REQUEST


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = BlacklistToken(jti=jti)

            db.session.add(revoked_token)
            db.session.commit()

            response = {'message': 'Refresh token has been revoked'}
            return response

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {"error": str(e)}
            return response, status.HTTP_400_BAD_REQUEST


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        username = get_jwt_identity()
        access_token = create_access_token(identity=username)

        response = {
            'username': username,
            'access_token': access_token
        }

        return response


class UserResource(Resource):
    @admin_required
    def get(self, id):
        user = User.query.get_or_404(id)
        result = user_schema.dump(user).data
        return result

    @admin_required
    def delete(self, id):
        user = User.query.get_or_404(id)
        try:
            db.session.delete(user)
            db.session.commit()

            response = {}

            return response, status.HTTP_204_NO_CONTENT

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {"error": str(e)}

            return response, status.HTTP_401_UNAUTHORIZED


class UserListResource(Resource):
    @admin_required
    def get(self):
        users = User.query.all()
        result = user_schema.dump(users, many=True).data

        return result
