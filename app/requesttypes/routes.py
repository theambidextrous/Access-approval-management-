from flask import Blueprint, jsonify, request,current_app, make_response
from app.models import RequestType
from app import db
import uuid
from app.utils import AuthUtil

requesttypes = Blueprint('requesttypes', __name__)

# handle 404
@requesttypes.errorhandler(404)
def invalid_route(e):
    f = open(str(current_app.config['LOGS_PATH']), 'a+')
    f.write(str(err))
    f.close()
    return jsonify({'status':-234,'error':'Seek failure'})

# routes
# RQST TYPES
@requesttypes.route('/api/v0/requests/type', methods = ['GET'])
@AuthUtil.auth_required
def find_all(sess_instance_user):
    try:
        types = RequestType.query.all()
        rtn = []
        for type in types:
            dt = {}
            dt['type_id'] = type.type_id
            dt['type_name'] = type.type_name
            dt['created_at'] = type.created_at
            rtn.append(dt)
        return jsonify({'status':0,'data':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@requesttypes.route('/api/v0/requests/type/<type_id>', methods = ['GET'])
@AuthUtil.auth_required
def find_one(sess_instance_user,type_id):
    try:
        type = RequestType.query.filter_by(type_id=type_id).first()
        if not type:
            return jsonify({'status':0,'data':None})
        rtn = []
        dt = {}
        dt['type_id'] = type.type_id
        dt['type_name'] = type.type_name
        dt['created_at'] = type.created_at
        rtn.append(dt)            
        return jsonify({'status':0,'data':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@requesttypes.route('/api/v0/requests/type', methods = ['POST'])
@AuthUtil.auth_required
def create_one(sess_instance_user):
    try:
        data = request.get_json()
        gen_id = str(uuid.uuid4())
        type = RequestType(type_id=gen_id,type_name=data['type_name'])
        db.session.add(type)
        db.session.commit()
        return jsonify({'status':0, 'created_id':gen_id, 'message':'Created!'})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})
