from . import db
import datetime
from sqlalchemy.ext.hybrid import hybrid_property


class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200),unique=True ,nullable=False)
    isbn = db.Column(db.String(13),unique=True, nullable=False)
    pageCount = db.Column(db.Integer)
    isLent = db.Column(db.Boolean,default=False, nullable=False)
    addDate = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    latestLent = db.Column(db.DateTime)
    latestReturn = db.Column(db.DateTime)

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer = db.relationship('Customer', backref="books")

    @hybrid_property
    def isLent(self):
        # if it currently have a relation with customer meaning it has been lent out
        return not (self.customer is None)


class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200),unique=True ,nullable=False)
    mobile = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(100),unique=True, nullable=False)

class LentHistory(db.Model):
    __tablename__ = "lentHistory"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column('customer_id',db.Integer,db.ForeignKey('customer.id',ondelete='cascade'))
    book_id = db.Column('book_id',db.Integer,db.ForeignKey('book.id',ondelete='cascade'))
    lentDate = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    returnDate = db.Column(db.DateTime)

    book = db.relationship(Book, backref="customersLentHistory")
    customers = db.relationship(Customer, backref="booksLentHistory")
    
