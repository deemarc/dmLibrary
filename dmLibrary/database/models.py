from . import db


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    isbn = db.Column(db.String(13),unique=True, nullable=False)
    pageCount = db.Column(db.Integer)
#     industryIdentifiers = db.relationship('IndustryIdentifier', backref='books', lazy=True)
    
#     # author_id = sa.Column(sa.Integer, sa.ForeignKey("authors.id"))
#     # author = relationship("Author", backref=backref("books"))

# class IndustryIdentifier(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     __tablename__ = "industryIdentifiers"
#     book_id = db.Column(db.Integer, db.ForeignKey('books.id'),nullable=False)
