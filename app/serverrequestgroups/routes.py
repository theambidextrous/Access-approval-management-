from flask import Blueprint, jsonify, request,current_app, make_response
from app.models import RequestGroup
from app import db
import uuid
from app.utils import AuthUtil

serverrequestgroups = Blueprint('serverrequestgroups', __name__)

# handle 404
@serverrequestgroups.errorhandler(404)
def invalid_route(e):
    f = open(str(current_app.config['LOGS_PATH']), 'a+')
    f.write(str(err))
    f.close()
    return jsonify({'status':-234,'error':'Seek failure'})

# routes
# RQST TYPES
@serverrequestgroups.route('/api/v0/serverrequests/groups', methods = ['GET'])
@AuthUtil.auth_required
def find_all(sess_instance_user):
    try:
        groups = RequestGroup.query.all()
        rtn = []
        for group in groups:
            dt = {}
            dt['group_id'] = group.group_id
            dt['group_name'] = group.group_name
            dt['created_at'] = group.created_at
            rtn.append(dt)
        return jsonify({'status':0,'data':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@serverrequestgroups.route('/api/v0/serverrequests/groups/<group_id>', methods = ['GET'])
@AuthUtil.auth_required
def find_one(sess_instance_user,group_id):
    try:
        group = RequestGroup.query.filter_by(group_id=group_id).first()
        if not group:
            return jsonify({'status':0,'data':None})
        rtn = []
        dt = {}
        dt['group_id'] = group.group_id
        dt['group_name'] = group.group_name
        dt['created_at'] = group.created_at
        rtn.append(dt)            
        return jsonify({'status':0,'data':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@serverrequestgroups.route('/api/v0/serverrequests/groups', methods = ['POST'])
@AuthUtil.auth_required
def create_one(sess_instance_user):
    try:
        data = request.get_json()
        group = RequestGroup(group_id=str(uuid.uuid4()),group_name=data['group_name'])
        db.session.add(group)
        db.session.commit()
        return jsonify({'status':0,'message':'Created!'})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})
