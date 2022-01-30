
from flask import request, abort, jsonify, current_app
from flask_restful import Resource
import datetime
from sqlalchemy import desc
from dmLibrary.api.masqlapi import masqlapi
from dmLibrary.database import db
from dmLibrary.database.models import Customer, Book, LentHistory
from dmLibrary.database.schemas import CustomerSchema,CustomerSchema, BookSchema,BookSchemaPOST, LentHistorySchema, LentHistorySchemaPOST
from dmLibrary.api.v1 import bp


apiHandle = masqlapi(db.session, Customer ,CustomerSchema, CustomerSchema)
bookHandle = masqlapi(db.session, Book ,BookSchema, BookSchemaPOST)
lentHistoryHandle = masqlapi(db.session, LentHistory ,BookSchema, BookSchemaPOST)
def get_book_id_list(books):
    book_id_list = []
    for book in books:
        book_id_list.append(book.id)
    return book_id_list

def onlyinA(listA, listB):
    """ return element that's only in list A but not in B"""
    setA = set(listA)
    setB = set(listB)
    return list(setA.difference(setB))
    
        
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

        lent_data = {
                "book_id" : cur_id,
                "customer_id":id
            }
        cur_lentHistory = LentHistory(**lent_data)
        lentHistoryHandle.add(cur_lentHistory)

    # specify list of books id

    return apiHandle.update(customer_obj)

@bp.route('/customers/<id>/return', methods=['POST'])
def return_book_resource(id):
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
    

    # specify list of books id lent by current customer
    customer_book_id_list = get_book_id_list(customer_obj.books)

    # check if request contain only book lent by current customer
    wrong_book_id_list = onlyinA(book_id_list, customer_book_id_list)
    if wrong_book_id_list:
        return {'message': f'book id:{wrong_book_id_list} is not being lent by this customer', 'status_code': 400, 'status': 'failure', 'data': None}, 400

    # remove book being return from current customer
    for id in book_id_list:
        for i in range(len(customer_obj.books)):
            if id == customer_obj.books[i].id:
                del customer_obj.books[i]  
                query_data = {
                    "book_id":id,
                    "customer_id":customer_obj.id
                }
                cur_lentHistory = LentHistory.query.filter_by(**query_data).order_by(desc(LentHistory.lentDate)).first()
                cur_lentHistory.updateReturnDate()

    return apiHandle.update(customer_obj)

