
from flask import request, abort, jsonify, current_app
from flask_restful import Resource
from dmLibrary.api.masqlapi import masqlapi
from dmLibrary.database import db
from dmLibrary.database.models import Book
from dmLibrary.database.schemas import BookSchema,BookSchemaPOST
from dmLibrary.api.v1 import bp


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

@bp.route('/books/<id>', methods=['GET'])
def get_single_book_resource(id):
    obj = apiHandle.get(id=id)
    return apiHandle.getMethod(obj, many=False)
    

@bp.route('/books', methods=['POST'])
def post_book_resource():
    return apiHandle.post(["title","isbn"])

@bp.route('/books/<id>', methods=['PATCH'])
def patch_single_book_resource(id):
    obj = apiHandle.get(id=id) or abort(404)
    return apiHandle.patch(obj)

@bp.route('/books/<id>', methods=['DELETE'])
def delete_single_book_resource(id):
    obj = apiHandle.get(id=id) or abort(404)
    return apiHandle.delete(obj)
