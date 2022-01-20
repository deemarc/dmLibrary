import collections
import json

from . import ma
from .models import *
from flask_marshmallow import Marshmallow
from marshmallow import fields, Schema, validates_schema, ValidationError, pre_load, post_load,post_dump,validate,validates
from dmLibrary.external.googleBook import GoogleBook

# ======================== Book section ========================
class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book

class BookSchemaPOST(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        exclude = ('id',)

    @post_load
    def get_infofromISBN(self, data, **kwags):
        if (len(data['isbn']) != 10) and (len(data['isbn']) != 13):
            raise ValidationError('ISBN must be 10 or 13 characters', 'isbn')
        if not data['isbn'].isdigit():
            raise ValidationError('ISBN_10 contain only number', 'isbn')
        gb = GoogleBook()
        pageCount = gb.getPageCount(data['isbn'])

        if pageCount < 0:
            raise ValidationError('error getting pageCount from isbn', 'isbn')
        data["pageCount"] = pageCount
        return data

