from flask import Blueprint, jsonify, request,current_app, make_response
from app.models import Server, ServerRequest,Approveserver
from app import db
from datetime import datetime as dtm
import uuid
from app.utils import AuthUtil

servers = Blueprint('servers', __name__)

# handle 404
@servers.errorhandler(404)
def invalid_route(e):
    f = open(str(current_app.config['LOGS_PATH']), 'a+')
    f.write(str(err))
    f.close()
    return jsonify({'status':-234,'error':'Seek failure'})

# routes
# SERVER REQUESTS
@servers.route('/api/v0/requests/serverrequests', methods = ['GET'])
@AuthUtil.auth_required
def find_all(sess_instance_user):
    if not sess_instance_user.isadmin and not sess_instance_user.can_approve_svr and sess_instance_user.can_approve_svr < 1:
        return jsonify({'status':-236, 'error':'Permission denied'})
    try:
        serverrequests = ServerRequest.query.filter_by(issubmitted = True)
        rtn = []
        for serverrequest in serverrequests:
            if sess_instance_user.isadmin or sess_instance_user.can_approve_svr_as == 1:#line manager first one
                dt = {}
                isperp = False
                if serverrequest.access_start == serverrequest.access_end:
                    isperp = True
                dt['request_id'] = serverrequest.request_id
                dt['request_type'] = serverrequest.request_type
                dt['request_group'] = serverrequest.request_group
                dt['requested_by'] = serverrequest.user_id
                dt['preferred_id'] = serverrequest.preferred_id
                dt['general_note'] = serverrequest.general_note
                dt['confidentiality_note'] = serverrequest.confidentiality_note
                dt['access_start'] = serverrequest.access_start
                dt['access_end'] = serverrequest.access_end
                dt['isexpired'] = serverrequest.isexpired
                dt['isapproved'] = serverrequest.isapproved
                dt['issubmitted'] = serverrequest.issubmitted
                dt['isperpetual'] = isperp
                dt['created_at'] = serverrequest.created_at
                rtn.append(dt)
            else:
                approval = Approveserver.query.filter(Approveserver.approve_as != '00', Approveserver.request_id == serverrequest.request_id).order_by(Approveserver.approved_at.desc()).first() #latest approval on this request
                if approval:
                    latest_apr = str(int(approval.approve_as)+1)
                    curr_usr_apr = str(sess_instance_user.can_approve_svr_as)
                    if latest_apr == curr_usr_apr or approval.approve_as >= curr_usr_apr:
                        dt = {}
                        isperp = False
                        if serverrequest.access_start == serverrequest.access_end:
                            isperp = True
                        dt['request_id'] = serverrequest.request_id
                        dt['request_type'] = serverrequest.request_type
                        dt['request_group'] = serverrequest.request_group
                        dt['requested_by'] = serverrequest.user_id
                        dt['preferred_id'] = serverrequest.preferred_id
                        dt['general_note'] = serverrequest.general_note
                        dt['confidentiality_note'] = serverrequest.confidentiality_note
                        dt['access_start'] = serverrequest.access_start
                        dt['access_end'] = serverrequest.access_end
                        dt['isexpired'] = serverrequest.isexpired
                        dt['isapproved'] = serverrequest.isapproved
                        dt['issubmitted'] = serverrequest.issubmitted
                        dt['isperpetual'] = isperp
                        dt['created_at'] = serverrequest.created_at
                        rtn.append(dt)
                    else:
                        pass
                else:
                    pass
        return jsonify({'status':0,'requests':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@servers.route('/api/v0/requests/serverrequests/<request_id>', methods = ['GET'])
@AuthUtil.auth_required
def find_one(sess_instance_user,request_id):
    try:
        serverrequest = ServerRequest.query.filter_by(request_id=request_id).first()
        if not serverrequest:
            return jsonify({'status':0,'request_data':None})
        rtn = []
        dt = {}
        isperp = False
        if serverrequest.access_start == serverrequest.access_end:
            isperp = True
        dt['request_id'] = serverrequest.request_id
        dt['request_type'] = serverrequest.request_type
        dt['request_group'] = serverrequest.request_group
        dt['requested_by'] = serverrequest.user_id
        dt['preferred_id'] = serverrequest.preferred_id
        dt['general_note'] = serverrequest.general_note
        dt['confidentiality_note'] = serverrequest.confidentiality_note
        dt['access_start'] = serverrequest.access_start
        dt['access_end'] = serverrequest.access_end
        dt['isexpired'] = serverrequest.isexpired
        dt['isapproved'] = serverrequest.isapproved
        dt['issubmitted'] = serverrequest.issubmitted
        dt['isperpetual'] = isperp
        dt['created_at'] = serverrequest.created_at
        rtn.append(dt)            
        return jsonify({'status':0,'request_data':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@servers.route('/api/v0/requests/serverrequests/user/<public_id>', methods = ['GET'])
@AuthUtil.auth_required
def find_one_by_user(sess_instance_user,public_id):
    try:
        serverrequests = ServerRequest.query.filter_by(user_id=public_id)
        if not serverrequests:
            return jsonify({'status':0,'request_data':None})
        rtn = []
        for serverrequest in serverrequests:
            dt = {}
            isperp = False
            if serverrequest.access_start == serverrequest.access_end:
                isperp = True
            dt['request_id'] = serverrequest.request_id
            dt['request_type'] = serverrequest.request_type
            dt['request_group'] = serverrequest.request_group
            dt['requested_by'] = serverrequest.user_id
            dt['preferred_id'] = serverrequest.preferred_id
            dt['general_note'] = serverrequest.general_note
            dt['confidentiality_note'] = serverrequest.confidentiality_note
            dt['access_start'] = serverrequest.access_start
            dt['access_end'] = serverrequest.access_end
            dt['isexpired'] = serverrequest.isexpired
            dt['isapproved'] = serverrequest.isapproved
            dt['issubmitted'] = serverrequest.issubmitted
            dt['isperpetual'] = isperp
            dt['created_at'] = serverrequest.created_at
            rtn.append(dt)            
        return jsonify({'status':0,'request_data':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@servers.route('/api/v0/requests/serverrequests', methods = ['POST'])
@AuthUtil.auth_required
def create_one(sess_instance_user):
    try:
        data = request.get_json()
        gen_id = str(uuid.uuid4())
        access_start = dtm.strptime(data['access_start'], '%d%m%Y').date()
        access_end = dtm.strptime(data['access_end'], '%d%m%Y').date()
        srequest = ServerRequest(request_id=gen_id,request_type=data['request_type'], request_group=data['request_group'],user_id=data['user_id'],preferred_id=data['preferred_id'],access_start=access_start,access_end=access_end)
        db.session.add(srequest)
        db.session.commit()
        return jsonify({'status':0,'message':'Your request has been created!', 'request_id':gen_id})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@servers.route('/api/v0/requests/serverrequests/<request_id>', methods = ['PUT'])
@AuthUtil.auth_required
def update_one(sess_instance_user, request_id):
    try:
        srequest = ServerRequest.query.filter_by(request_id=request_id).first()
        if not srequest:
            return jsonify({'status':-404, 'message':'Server request not found'})
        data = request.get_json()
        access_start = dtm.strptime(data['access_start'], '%d%m%Y').date()
        access_end = dtm.strptime(data['access_end'], '%d%m%Y').date()
        srequest.request_type = data['request_type']
        srequest.request_group = data['request_group']
        srequest.preferred_id = data['preferred_id']
        srequest.access_start = access_start
        srequest.access_end = access_end
        db.session.commit()
        return jsonify({'status':0,'message':'server request has been updated!'})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@servers.route('/api/v0/requests/serverrequests/submit/<request_id>', methods = ['PUT'])
@AuthUtil.auth_required
def submit_4_approval(sess_instance_user, request_id):
    try:
        srequest = ServerRequest.query.filter_by(request_id=request_id,user_id=sess_instance_user.public_id,issubmitted=False).first()
        if not srequest:
            return jsonify({'status':-404, 'message':'Server request not found'})
        srequest.issubmitted = True
        db.session.commit()
        return jsonify({'status':0,'message':'server request has been submitted for approval!'})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

#REPORTS
@servers.route('/api/v0/requests/serverrequests/reports/<search_creteria>', methods = ['GET'])
@AuthUtil.auth_required
def find_report(sess_instance_user, search_creteria):
    try:
        if not sess_instance_user.isadmin:
            return jsonify({'status':-236, 'error':'Permission denied'})
        rtn = []
        # search_creteria ===== svr__172.... OR usr__dffjgjfgj..........
        search_c = search_creteria.split('__')
        search_type = search_c[0]
        search_item = search_c[1]
        if search_type == 'svr':
            reports = Server.query.filter_by(server=search_item) 
            if not reports:
                return jsonify({'status':0,'data':None})
            for i in reports:
                dt = {}
                isperp = False
                if i.serverrequest.access_start == i.serverrequest.access_end:
                    isperp = True
                dt['server'] = i.server
                dt['requested_by'] = i.serverrequest.user_id
                dt['preferred_id'] = i.serverrequest.preferred_id
                dt['access_start'] = i.serverrequest.access_start
                dt['access_end'] = i.serverrequest.access_end
                dt['isexpired'] = i.serverrequest.isexpired
                dt['isapproved'] = i.serverrequest.isapproved
                dt['isperpetual'] = isperp
                dt['created_at'] = i.serverrequest.created_at
                rtn.append(dt)
        elif search_type == 'usr':
            reports = Server.query.all()
            if not reports:
                return jsonify({'status':0,'data':None})
            for i in reports:
                dt = {}
                if i.serverrequest.user_id == search_item:
                    isperp = False
                    if i.serverrequest.access_start == i.serverrequest.access_end:
                        isperp = True
                    dt['server'] = i.server
                    dt['requested_by'] = i.serverrequest.user_id
                    dt['preferred_id'] = i.serverrequest.preferred_id
                    dt['access_start'] = i.serverrequest.access_start
                    dt['access_end'] = i.serverrequest.access_end
                    dt['isexpired'] = i.serverrequest.isexpired
                    dt['isapproved'] = i.serverrequest.isapproved
                    dt['isperpetual'] = isperp
                    dt['created_at'] = i.serverrequest.created_at
                    rtn.append(dt)
                else:
                    pass
        return jsonify({'status':0,'data':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

# SERVER REQUESTS INFO
@servers.route('/api/v0/requests/serverrequestinfo', methods = ['GET'])
@AuthUtil.auth_required
def svr_find_all(sess_instance_user):
    if not sess_instance_user.isadmin and not sess_instance_user.can_approve_svr:
        return jsonify({'status':-236, 'error':'Permission denied'})
    try:
        infs = Server.query.all()
        rtn = []
        for inf in infs:
            dt = {}
            dt['public_id'] = inf.public_id
            dt['server'] = inf.server
            dt['reason'] = inf.reason
            dt['access_rights'] = inf.access_rights
            dt['access_matrix'] = inf.access_matrix
            dt['request_id'] = inf.req_id
            dt['created_at'] = inf.created_at
            rtn.append(dt)
        return jsonify({'status':0,'requests_info':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@servers.route('/api/v0/requests/serverrequestinfo/byserver', methods = ['GET'])
@AuthUtil.auth_required
def find_all_by_svr(sess_instance_user):
    if not sess_instance_user.isadmin and not sess_instance_user.can_approve_svr:
        return jsonify({'status':-236, 'error':'Permission denied'})
    try:
        infs = Server.query.with_entities(Server.server).distinct()
        rtn = []
        for inf in infs:
            dt = {}
            dt['server'] = inf.server
            rtn.append(dt)
        return jsonify({'status':0,'servers':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@servers.route('/api/v0/requests/serverrequestinfo/<public_id>', methods = ['GET'])
@AuthUtil.auth_required
def svr_find_one(sess_instance_user,public_id):
    try:
        inf = Server.query.filter_by(public_id=public_id).first()
        if not inf:
            return jsonify({'status':0,'request_info':None})
        rtn = []
        dt = {}
        dt['public_id'] = inf.public_id
        dt['server'] = inf.server
        dt['reason'] = inf.reason
        dt['access_rights'] = inf.access_rights
        dt['access_matrix'] = inf.access_matrix
        dt['request_id'] = inf.req_id
        dt['created_at'] = inf.created_at
        rtn.append(dt)            
        return jsonify({'status':0,'request_data':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@servers.route('/api/v0/requests/serverrequestinfo/byrequest/<request_id>', methods = ['GET'])
@AuthUtil.auth_required
def svr_find_one_by_request(sess_instance_user,request_id):
    try:
        infs = Server.query.filter_by(req_id=request_id)
        if not infs:
            return jsonify({'status':0,'request_info':None})
        rtn = []
        for inf in infs:
            dt = {}
            dt['public_id'] = inf.public_id
            dt['server'] = inf.server
            dt['reason'] = inf.reason
            dt['access_rights'] = inf.access_rights
            dt['access_matrix'] = inf.access_matrix
            dt['request_id'] = inf.req_id
            dt['created_at'] = inf.created_at
            rtn.append(dt)
        return jsonify({'status':0,'data':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@servers.route('/api/v0/requests/serverrequestinfo', methods = ['POST'])
@AuthUtil.auth_required
def svr_create_one(sess_instance_user):
    try:
        data = request.get_json()
        svr_info = Server(public_id=str(uuid.uuid4()),server=data['server'], reason=data['reason'],access_rights=data['access_rights'],req_id=data['request_id'])
        db.session.add(svr_info)
        db.session.commit()
        return jsonify({'status':0,'message':'Server access request info added successfully!'})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@servers.route('/api/v0/requests/serverrequestinfo/<public_id>', methods = ['PUT'])
@AuthUtil.auth_required
def svr_update_one(sess_instance_user, public_id):
    try:
        svrinfo = Server.query.filter_by(public_id=public_id).first()
        if not svrinfo:
            return jsonify({'status':-404, 'message':'Server request info not found'})
        data = request.get_json()
        svrinfo.server = data['server']
        svrinfo.reason = data['reason']
        svrinfo.access_rights = data['access_rights']
        svrinfo.req_id = data['request_id']
        db.session.commit()
        return jsonify({'status':0,'message':'Server access request info has been updated!'})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})