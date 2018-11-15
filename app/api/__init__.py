from flask import Blueprint
from flask_cors import CORS
from flask_restful import Api
from .resources.books import BookListResource, BookResource
from .resources.authors import AuthorListResource, AuthorResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

cors = CORS(api_bp, resources={r"/api/*": {"origins": "*"}})

api.add_resource(AuthorListResource, '/authors/')
api.add_resource(AuthorResource, '/authors/<int:id>')
api.add_resource(BookListResource, '/books/')
api.add_resource(BookResource, '/books/<int:id>')
