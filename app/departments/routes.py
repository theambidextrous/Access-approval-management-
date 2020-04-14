from flask import Blueprint, jsonify, request,current_app, make_response
from app.models import Department
from app import db
import uuid
from app.utils import AuthUtil

departments = Blueprint('departments', __name__)

# handle 404
@departments.errorhandler(404)
def invalid_route(e):
    f = open(str(current_app.config['LOGS_PATH']), 'a+')
    f.write(str(err))
    f.close()
    return jsonify({'status':-234,'error':'Seek failure'})

# routes
# RQST TYPES
@departments.route('/api/v0/departments', methods = ['GET'])
@AuthUtil.auth_required
def find_all(sess_instance_user):
    try:
        departments = Department.query.all()
        rtn = []
        for department in departments:
            dt = {}
            dt['dept_id'] = department.dept_id
            dt['dept_name'] = department.dept_name
            dt['line_manager'] = department.line_manager
            dt['created_at'] = department.created_at
            rtn.append(dt)
        return jsonify({'status':0,'data':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@departments.route('/api/v0/departments/<dept_id>', methods = ['GET'])
@AuthUtil.auth_required
def find_one(sess_instance_user,dept_id):
    try:
        department = Department.query.filter_by(dept_id=dept_id).first()
        if not department:
            return jsonify({'status':0,'data':None})
        rtn = []
        dt = {}
        dt['dept_id'] = department.dept_id
        dt['dept_name'] = department.dept_name
        dt['line_manager'] = department.line_manager
        dt['created_at'] = department.created_at
        rtn.append(dt)            
        return jsonify({'status':0,'data':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@departments.route('/api/v0/departments', methods = ['POST'])
@AuthUtil.auth_required
def create_one(sess_instance_user):
    try:
        data = request.get_json()
        department = Department(dept_id=str(uuid.uuid4()),dept_name=data['dept_name'],line_manager=data['line_manager'])
        db.session.add(department)
        db.session.commit()
        return jsonify({'status':0,'message':'Created!'})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@departments.route('/api/v0/departments/<dept_id>', methods = ['PUT'])
@AuthUtil.auth_required
def update_one(sess_instance_user,dept_id):
    try:
        department = Department.query.filter_by(dept_id=dept_id).first()
        if not department:
            return jsonify({'status':0,'data':None})
        data = request.get_json()
        department.dept_name = data['dept_name']
        department.line_manager = data['line_manager']
        db.session.commit()
        return jsonify({'status':0,'message':'Updated!'})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})
