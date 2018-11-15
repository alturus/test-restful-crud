import datetime
from marshmallow import fields
from app import db, ma


class BlacklistToken(db.Model):
    """Token Model for storing jti (JWT ID) of revoked tokens"""
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jti = db.Column(db.String(120), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, jti):
        self.jti = jti
        self.blacklisted_on = datetime.datetime.now()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)

    def __repr__(self):
        return '<id: jti: {}'.format(self.jti)


class BlacklistTokenSchema(ma.ModelSchema):
    tji = fields.String(required=True)
    blacklisted_on = fields.DateTime(dump_only=True)
