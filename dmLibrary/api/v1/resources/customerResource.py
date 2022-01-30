
from flask import request, abort, jsonify, current_app
from flask_restful import Resource
from dmLibrary.api.masqlapi import masqlapi
from dmLibrary.database import db
from dmLibrary.database.models import Customer, Book
from dmLibrary.database.schemas import CustomerSchema,CustomerSchema
from dmLibrary.database.schemas import BookSchema,BookSchemaPOST
from dmLibrary.api.v1 import bp


apiHandle = masqlapi(db.session, Customer ,CustomerSchema, CustomerSchema)
bookHandle = masqlapi(db.session, Book ,BookSchema, BookSchemaPOST)

@bp.route('/customers', methods=['GET'])
def get_customer_resource():
    filters = request.args
    # check if query string is valid
    errors = CustomerSchema().validate(filters, partial=True)
    if errors:
        abort(400, str(errors))
    objs = apiHandle.get_many(**filters)
    return apiHandle.getMethod(objs, many=True)
    

@bp.route('/customers', methods=['POST'])
def post_customer_resource():
    return apiHandle.post(["name"])

@bp.route('/customers/<id>', methods=['PATCH'])
def patch_single_customer_resource(id):
    obj = apiHandle.get(id=id) or abort(404)
    return apiHandle.patch(obj)

@bp.route('/customers/<id>', methods=['DELETE'])
def delete_single_customer_resource(id):
    obj = apiHandle.get(id=id) or abort(404)
    return apiHandle.delete(obj)

@bp.route('/customers/<id>/lent', methods=['POST'])
def lent_book_resource(id):
    customer_obj = apiHandle.get(id=id) or abort(404)
    json = request.get_json()
    if not json:
        return {'message': 'Bad request', 'status_code': 400, 'status': 'failure', 'data': 'JSON input object is missing or cannot be parsed'}, 400

    book_id_list = json.get("book_id_list",[])
    if not book_id_list:
        return {'message': 'book_id_list is not provided in post body', 'status_code': 400, 'status': 'failure', 'data': ''}, 400
    
    newBooks = []
    for cur_id in book_id_list:
        cur_book = bookHandle.get(id=cur_id)
        if not cur_book:
            return {'message': f'book id:{cur_id} is invalid', 'status_code': 400, 'status': 'failure', 'data': None}, 400
        if cur_book.isLent:
            return {'message': f'book id:{cur_id} is currently being lent', 'status_code': 400, 'status': 'failure', 'data': None}, 400

        if customer_obj.books:
            customer_obj.books.append(cur_book)
        else:
            customer_obj.books = [cur_book]
    # specify list of books id

    return apiHandle.update(customer_obj)

# @bp.route('/customers/<id>/return', methods=['POST'])
# def return_book_resource(id):
#     # specify list of book id
#     pass

