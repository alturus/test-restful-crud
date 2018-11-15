from marshmallow import fields
from app import db, ma


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(40), nullable=False)
    firstname = db.Column(db.String(20), nullable=False)

    @classmethod
    def is_unique(cls, id, firstname, lastname):
        existing_author = cls.query.filter_by(firstname=firstname, lastname=lastname).first()
        if existing_author is None:
            return True

        if existing_author.id == id:
            return True
        else:
            return False


class AuthorSchema(ma.ModelSchema):
    books = fields.Nested('BookSchema', many=True, exclude=('authors',))
    url = ma.URLFor('api.authorresource', id='<id>', _external=True)

    class Meta:
        model = Author
