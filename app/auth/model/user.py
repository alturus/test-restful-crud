import datetime
from marshmallow import fields, validate
from app import db, ma, bcrypt


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, username, password, admin=False):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode()
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    @property
    def is_admin(self):
        return self.admin

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def check_password(pw_hash, password):
        return bcrypt.check_password_hash(pw_hash, password)

    @classmethod
    def is_unique(cls, id, username):
        existing_user = cls.query.filter_by(username=username).first()
        if existing_user is None:
            return True

        if existing_user.id == id:
            return True
        else:
            return False


class UserSchema(ma.ModelSchema):
    username = fields.String(required=True, validate=validate.Length(3))
    password = fields.String(required=True, validate=validate.Length(3))
    registered_on = fields.DateTime(dump_only=True)
    url = ma.URLFor('auth_api.userresource', id='<id>', _external=True)
