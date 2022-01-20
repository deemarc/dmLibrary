
from flask import request, abort, jsonify, current_app
from flask_restful import Resource
from dmLibrary.api.masqlapi import masqlapi
from dmLibrary.database import db
from dmLibrary.database.models import Book
from dmLibrary.database.schemas import BookSchema,BookSchemaPOST
from dmLibrary.api.v1 import bp
# from dmLibrary.api.schemas.schemas import IngredientSchema

# from dmLibrary.database.models import IngredientName
# from dmLibrary.api.apierror import ApiError
# from dmLibrary.api.resources.restive import Restive

# apiHandle = Restive(IngredientName,IngredientSchema)
apiHandle = masqlapi(db.session, Book ,BookSchema, BookSchemaPOST)

@bp.route('/books', methods=['GET'])
def get_book_resource():
    filters = request.args
    # check if query string is valid
    errors = BookSchema().validate(filters, partial=True)
    if errors:
        abort(400, str(errors))
    objs = apiHandle.get_many(**filters)
    return apiHandle.getMethod(objs, many=True)
    
    # def post(self):
    #     return apiHandle.post("title")

@bp.route('/books', methods=['POST'])
def post_baker_resource():
    return apiHandle.post(["title","ISBN_10"])

@bp.route('/books/<id>', methods=['DELETE'])
def delete_single_book_resource(id):
    obj = apiHandle.get(id=id) or abort(404)
    return apiHandle.delete(obj)