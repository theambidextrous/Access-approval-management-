from flask import Blueprint, jsonify, request,current_app, make_response
from app.models import Right
from app import db
import uuid
from app.utils import AuthUtil

serverrights = Blueprint('serverrights', __name__)

# handle 404
@serverrights.errorhandler(404)
def invalid_route(e):
    f = open(str(current_app.config['LOGS_PATH']), 'a+')
    f.write(str(err))
    f.close()
    return jsonify({'status':-234,'error':'Seek failure'})

# routes
# RQST TYPES
@serverrights.route('/api/v0/serverrequests/rights', methods = ['GET'])
@AuthUtil.auth_required
def find_all(sess_instance_user):
    try:
        rights = Right.query.all()
        rtn = []
        for right in rights:
            dt = {}
            dt['right_id'] = right.right_id
            dt['right_name'] = right.right_name
            dt['created_at'] = right.created_at
            rtn.append(dt)
        return jsonify({'status':0,'data':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@serverrights.route('/api/v0/serverrequests/rights/<right_id>', methods = ['GET'])
@AuthUtil.auth_required
def find_one(sess_instance_user,right_id):
    try:
        right = Right.query.filter_by(right_id=right_id).first()
        if not right:
            return jsonify({'status':0,'data':None})
        rtn = []
        dt = {}
        dt['right_id'] = right.right_id
        dt['right_name'] = right.right_name
        dt['created_at'] = right.created_at
        rtn.append(dt)            
        return jsonify({'status':0,'data':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@serverrights.route('/api/v0/serverrequests/rights', methods = ['POST'])
@AuthUtil.auth_required
def create_one(sess_instance_user):
    try:
        data = request.get_json()
        right = Right(right_id=str(uuid.uuid4()),right_name=data['right_name'])
        db.session.add(right)
        db.session.commit()
        return jsonify({'status':0,'message':'Created!'})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})
