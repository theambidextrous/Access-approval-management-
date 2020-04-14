from flask import Blueprint, jsonify, request,current_app, make_response
from app.models import Approveserver,ApproveKind,ServerRequest
from app import db
import uuid
from app.utils import AuthUtil
from app.utils import SysAccess as sa

serverapprovals = Blueprint('serverapprovals', __name__)

# handle 404
@serverapprovals.errorhandler(404)
def invalid_route(e):
    f = open(str(current_app.config['LOGS_PATH']), 'a+')
    f.write(str(err))
    f.close()
    return jsonify({'status':-234,'error':'Seek failure'})

# routes
# SERVER APPROVALS
@serverapprovals.route('/api/v0/requests/server/approve', methods = ['GET'])
@AuthUtil.auth_required
def find_all(sess_instance_user):
    if not sess_instance_user.isadmin and not sess_instance_user.can_approve_vpn:
        return jsonify({'status':-236, 'error':'Permission denied'})
    try:
        approvals = Approveserver.query.all()
        if not approvals:
            return jsonify({'status':0,'data':None})
        rtn = []
        for approval in approvals:
            dt = {}
            dt['public_id'] = approval.public_id
            dt['request_id'] = approval.request_id
            dt['user_id'] = approval.user_id
            dt['approved_by'] = approval.approved_by
            dt['approved_as'] = approval.approve_as
            dt['remarks'] = approval.remarks
            dt['approved_at'] = approval.approved_at
            rtn.append(dt)
        return jsonify({'status':0,'data':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@serverapprovals.route('/api/v0/requests/server/approve/byuser/<user_id>', methods = ['GET'])
@AuthUtil.auth_required
def find_all_by_user(sess_instance_user, user_id):
    if not sess_instance_user.isadmin and sess_instance_user.public_id != user_id:
        return jsonify({'status':-236, 'error':'Permission denied'})
    try:
        approvals = Approveserver.query.filter_by(user_id=user_id)
        if not approvals:
            return jsonify({'status':0,'data':None})
        rtn = []
        for approval in approvals:
            dt = {}
            dt['public_id'] = approval.public_id
            dt['request_id'] = approval.request_id
            dt['user_id'] = approval.user_id
            dt['approved_by'] = approval.approved_by
            dt['approved_as'] = approval.approve_as
            dt['remarks'] = approval.remarks
            dt['approved_at'] = approval.approved_at
            rtn.append(dt)
        return jsonify({'status':0,'data':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@serverapprovals.route('/api/v0/requests/server/approve/byrequest/<request_id>', methods = ['GET'])
@AuthUtil.auth_required
def find_all_by_request(sess_instance_user, request_id):
    try:
        approvals = Approveserver.query.filter_by(request_id=request_id)
        if not approvals:
            return jsonify({'status':0,'data':None})
        rtn = []
        for approval in approvals:
            dt = {}
            dt['public_id'] = approval.public_id
            dt['request_id'] = approval.request_id
            dt['user_id'] = approval.user_id
            dt['approved_by'] = approval.approved_by
            dt['approved_as'] = approval.approve_as
            dt['remarks'] = approval.remarks
            dt['approved_at'] = approval.approved_at
            rtn.append(dt)
        return jsonify({'status':0,'data':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})


@serverapprovals.route('/api/v0/requests/server/approve/<public_id>', methods = ['GET'])
@AuthUtil.auth_required
def find_one(sess_instance_user,public_id):
    try:
        approval = Approveserver.query.filter_by(public_id=public_id).first()
        if not approval:
            return jsonify({'status':0,'data':None})
        rtn = []
        dt = {}
        dt['public_id'] = approval.public_id
        dt['request_id'] = approval.request_id
        dt['user_id'] = approval.user_id
        dt['approved_by'] = approval.approved_by
        dt['approved_as'] = approval.approve_as
        dt['remarks'] = approval.remarks
        dt['approved_at'] = approval.approved_at
        rtn.append(dt)            
        return jsonify({'status':0,'data':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@serverapprovals.route('/api/v0/requests/server/approve/byrequser', methods = ['GET'])
@AuthUtil.auth_required
def find_one_by_user_and_req(sess_instance_user):
    try:
        data = request.get_json()
        approval=Approveserver.query.filter_by(request_id=data['request_id'], approved_by=sess_instance_user.public_id).first()
        if not approval:
            return jsonify({'status':0,'approved_as':None})
        return jsonify({'status':0,'approved_as':approval.approve_as})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@serverapprovals.route('/api/v0/requests/server/approve/byrequser', methods = ['PUT'])
@AuthUtil.auth_required
def update_one_by_user_and_req(sess_instance_user):
    try:
        data = request.get_json()
        approval = Approveserver.query.filter_by(request_id=data['request_id'],approved_by=sess_instance_user.public_id).first()
        if not approval:
            return jsonify({'status':0,'data':None})
        approve_as = str(sess_instance_user.can_approve_svr_as)
        if data['flag'] == '0':
            approve_as = '00'
        approval.approve_as = approve_as
        approval.remarks = data['remarks']
        db.session.commit()
        return jsonify({'status':0,'message':'Approved successfully'})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

    
@serverapprovals.route('/api/v0/requests/server/approve', methods = ['POST'])
@AuthUtil.auth_required
def create_one(sess_instance_user): #
    if sess_instance_user.isadmin:
        return jsonify({'status':-236, 'error':'Approval Permissions Denied for Admins'})
    if sess_instance_user.can_approve_svr_as == 0:
        return jsonify({'status':-236, 'error':'Permission denied. No Approve Permissions assigned to you.'})
    try:
        approve_as = str(sess_instance_user.can_approve_svr_as)
        data = request.get_json()
        if data['flag'] == '0':
            approve_as = '00'
            srequest = ServerRequest.query.filter_by(request_id=data['request_id'],issubmitted=True).first()
            if not srequest:
                return jsonify({'status':-404, 'message':'Server resource not found'})
            srequest.issubmitted = False
        if sess_instance_user.public_id == data['user_id']:
            return jsonify({'status':-236, 'error':'Self Approval Prohibited'})
        elif sess_instance_user.can_approve_svr_as != int(data['approve_as']):
            return jsonify({'status':-236, 'error':'Invalid Values in payload ::' + str(data['approve_as'])})
        elif not sess_instance_user.can_approve_svr and not sa.can_approve(sess_instance_user.public_id, data['user_id']):
            return jsonify({'status':-236, 'error':'Permission denied. Only approvers & line managers can perform this action'})
        else:
            approval = Approveserver(public_id=str(uuid.uuid4()), request_id=data['request_id'], user_id=data['user_id'], approved_by=sess_instance_user.public_id, approve_as=approve_as, remarks=data['remarks'])
            db.session.add(approval)
            db.session.commit()
            sa.is_approved_svr(data['request_id'])
            return jsonify({'status':0,'message':'Approved!'})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params' + str(data)})
