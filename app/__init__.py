from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from config import config

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    from .auth.model.blacklist_token import BlacklistToken
    return BlacklistToken.is_jti_blacklisted(jti)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from .main import main as main_bp
    app.register_blueprint(main_bp)

    from .auth import auth_api_bp
    app.register_blueprint(auth_api_bp, url_prefix='/auth')

    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    return app
