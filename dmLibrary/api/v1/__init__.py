import socket
import os
import time
from flask import abort, Blueprint, current_app, request, url_for, jsonify
from dmLibrary.database import db
from apispec import APISpec

bp = Blueprint('api', __name__)

def test_engine(engine):
    """ Tests SQLAlchemy engine and returns response time """
    if not engine:
        return {'status': 'ERROR', 'error': 'No engine defined'}
    try:
        start = time.time()
        connection = engine.connect()
        if not connection.closed:
            connection.close()
        elapsed = '{:.3f}'.format(time.time() - start)
        return {
            'engine': str(engine),
            'label': getattr(engine, 'label', '<unknown>'),
            'status': 'OK',
            'time': elapsed
        }
    except Exception as err:
        return {'status': 'ERROR', 'error': str(err)}

@bp.teardown_request
def teardown(exception=None):
    # print("before tear down sessiion:{0}".format(str(db.session)))
    if exception:

        current_app.logger.error("teardown with error, error message: {0}".format(exception))
        current_app.error("teardown_request - rolling back active database sessions.")
        db.session.rollback()
        
    db.session.close()
    db.session.remove()

@bp.route("/<path:invalid_path>", methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE', 'OPTIONS'])
def route404(*args, **kwargs):
    """ Catch all route within blueprint to force use of 404 errorhandler. """
    abort(404)

@bp.route('/monitor', methods=['GET'])
def monitor():
    """ Global monitoring route """
    headers_list = request.headers.getlist("X-Forwarded-For")
    user_ip = headers_list[0] if headers_list else request.remote_addr
    poolid = pool_chk_in = pool_chk_out = None
    if db.session.bind :
        poolid = id(db.session.bind.pool)
        pool_chk_in =  db.session.bind.pool.checkedin()
        pool_chk_out =  db.session.bind.pool.checkedout()


    payload = {
        'app': current_app.name,
        'node': socket.gethostname().lower(),
        'status': 'OK',
        'proxy' : os.environ.get('proxy'),
        # 'cache' : CacheConfig.CACHE_TYPE ,
        #'debug' : config.get('DEBUG')
        'client_ip' : user_ip,
        'connection_pool' : {'id':poolid,
                           'checked_in' : pool_chk_in,
                           'checked_out' : pool_chk_out
        }
    }

    current_app.testing = True

    


    with current_app.app_context():

        payload['status'] = 'OK'
        payload['dependencies'] = {}

    #     # Blueprints for V3
    #     payload['v3']['dependencies']['admin_v3'] = test_blueprint(client, '/admin/v3')
    #     payload['v3']['dependencies']['api_v3'] = test_blueprint(client, '/api/v3')
    #     payload['v3']['dependencies']['ui_v3'] = test_blueprint(client, '/v3')

        # Engines for V1
        payload['dependencies']['engine'] = test_engine(db.session.bind)

        for k, v in payload['dependencies'].items():
            if v.get('status') != 'OK':
                payload['status'] = 'ERROR'
                payload['status'] = 'ERROR'
                # if 'engine' in k:
                #     db.configure()

        if payload['status'] == 'ERROR':
            return payload, 500

        return payload, 200

