from marshmallow import fields
from app import db, ma
from .author import AuthorSchema


book_author = db.Table('book_author',
                       db.Column('author_id', db.Integer, db.ForeignKey('authors.id'), primary_key=True),
                       db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True),
                       )


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.Integer, unique=True, nullable=False)
    year = db.Column(db.Integer)
    authors = db.relationship('Author', secondary=book_author, lazy='subquery',
                              backref=db.backref('books', lazy=True))

    @classmethod
    def is_unique(cls, id, isbn):
        existing_book = cls.query.filter_by(isbn=isbn).first()
        if existing_book is None:
            return True

        if existing_book.id == id:
            return True
        else:
            return False


class BookSchema(ma.ModelSchema):
    authors = fields.Nested(AuthorSchema, many=True, exclude=('books',))
    url = ma.URLFor('api.bookresource', id='<id>', _external=True)

    class Meta:
        model = Book
