from flask import Blueprint, jsonify, request,current_app, make_response
from app.models import ApproveKind
from app import db
import uuid
from app.utils import AuthUtil

approvekinds = Blueprint('approvekinds', __name__)

# handle 404
@approvekinds.errorhandler(404)
def invalid_route(e):
    f = open(str(current_app.config['LOGS_PATH']), 'a+')
    f.write(str(err))
    f.close()
    return jsonify({'status':-234,'error':'Seek failure'})

# routes
# RQST TYPES
@approvekinds.route('/api/v0/approvekinds', methods = ['GET'])
@AuthUtil.auth_required
def find_all(sess_instance_user):
    try:
        approvekinds = ApproveKind.query.all()
        rtn = []
        for approvekind in approvekinds:
            dt = {}
            dt['kind_type'] = approvekind.kind_type
            dt['kind_name'] = approvekind.kind_name
            dt['created_at'] = approvekind.created_at
            rtn.append(dt)
        return jsonify({'status':0,'data':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@approvekinds.route('/api/v0/approvekinds/<kind_type>', methods = ['GET'])
@AuthUtil.auth_required
def find_one(sess_instance_user,kind_type):
    try:
        approvekind = ApproveKind.query.filter_by(kind_type=kind_type).first()
        if not approvekind:
            return jsonify({'status':0,'data':None})
        rtn = []
        dt = {}
        dt['kind_type'] = approvekind.kind_type
        dt['kind_name'] = approvekind.kind_name
        dt['created_at'] = approvekind.created_at
        rtn.append(dt)            
        return jsonify({'status':0,'data':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@approvekinds.route('/api/v0/approvekinds', methods = ['POST'])
@AuthUtil.auth_required
def create_one(sess_instance_user):
    try:
        data = request.get_json()
        approvekind = ApproveKind(kind_type=data['kind_type'],kind_name=data['kind_name'])
        db.session.add(approvekind)
        db.session.commit()
        return jsonify({'status':0,'message':'Created!'})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@approvekinds.route('/api/v0/approvekinds/<kind_type>', methods = ['PUT'])
@AuthUtil.auth_required
def update_one(sess_instance_user,kind_type):
    try:
        approvekind = ApproveKind.query.filter_by(kind_type=kind_type).first()
        if not approvekind:
            return jsonify({'status':0,'data':None})
        data = request.get_json()
        approvekind.kind_type = data['kind_type']
        approvekind.kind_name = data['kind_name']
        db.session.commit()
        return jsonify({'status':0,'message':'Updated!'})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})
