from flask import Blueprint
from flask_restful import Api
from . import resources

auth_api_bp = Blueprint('auth_api', __name__)
auth_api = Api(auth_api_bp)


auth_api.add_resource(resources.UserRegistration, '/registration')
auth_api.add_resource(resources.UserListResource, '/users/')
auth_api.add_resource(resources.UserResource, '/users/<int:id>')
auth_api.add_resource(resources.UserLogin, '/login')
auth_api.add_resource(resources.UserLogoutAccess, '/logout/access')
auth_api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
auth_api.add_resource(resources.TokenRefresh, '/token/refresh')
