
from flask import request, abort, jsonify, current_app
from flask_restful import Resource
from dmLibrary.api.masqlapi import masqlapi
from dmLibrary.database import db
from dmLibrary.database.models import LentHistory
from dmLibrary.database.schemas import LentHistorySchema,LentHistorySchemaPOST
from dmLibrary.api.v1 import bp
from sqlalchemy import desc

apiHandle = masqlapi(db.session, LentHistory ,LentHistorySchema, LentHistorySchemaPOST)

@bp.route('/lentHistory', methods=['GET'])
def get_lentHistory_resource():
    filters = request.args
    # check if query string is valid
    errors = LentHistorySchema().validate(filters, partial=True)
    if errors:
        abort(400, str(errors))
    objs = apiHandle.get_many(**filters)
    return apiHandle.getMethod(objs, many=True)

