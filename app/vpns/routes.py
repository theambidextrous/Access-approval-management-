from flask import Blueprint, jsonify, request,current_app, make_response
from app.models import Vpn, VpnRequest,Approvevpn
from app import db
import uuid
from datetime import datetime as dtm
from app.utils import AuthUtil

vpns = Blueprint('vpns', __name__)

# handle 404
@vpns.errorhandler(404)
def invalid_route(e):
    f = open(str(current_app.config['LOGS_PATH']), 'a+')
    f.write(str(err))
    f.close()
    return jsonify({'status':-234,'error':'Seek failure'})

# routes
# VPN REQUESTS
@vpns.route('/api/v0/requests/vpnrequests', methods = ['GET'])
@AuthUtil.auth_required
def find_all(sess_instance_user):
    if not sess_instance_user.isadmin and not sess_instance_user.can_approve_vpn:
        return jsonify({'status':-236, 'error':'Permission denied'})
    try:
        vpns = VpnRequest.query.filter_by(issubmitted = True)
        if not vpns:
            return jsonify({'status':0,'request_data':None})
        rtn = []
        for vpn in vpns:
            if sess_instance_user.isadmin or sess_instance_user.can_approve_vpn_as == 1:#line manager first one
                dt = {}
                isperp = False
                if vpn.access_start == vpn.access_end:
                    isperp = True
                dt['request_id'] = vpn.request_id
                dt['requested_by'] = vpn.user_id
                dt['general_note'] = vpn.general_note
                dt['confidentiality_note'] = vpn.confidentiality_note
                dt['access_start'] = vpn.access_start
                dt['access_end'] = vpn.access_end
                dt['isexpired'] = vpn.isexpired
                dt['isapproved'] = vpn.isapproved
                dt['issubmitted'] = vpn.issubmitted
                dt['isperpetual'] = isperp
                dt['created_at'] = vpn.created_at
                rtn.append(dt)
            else:
                approval = Approvevpn.query.filter(Approvevpn.approve_as != '00', Approvevpn.request_id == vpn.request_id).order_by(Approvevpn.approved_at.desc()).first() #latest approval on this request
                if approval:
                    latest_apr = str(approval.approve_as)
                    latest_apr_add_1 = str(int(approval.approve_as)+1)
                    latest_apr_add_2 = str(int(approval.approve_as)+2)
                    curr_usr_apr = str(sess_instance_user.can_approve_vpn_as)
                    if latest_apr >= curr_usr_apr or (curr_usr_apr == str('3') and latest_apr_add_2 == str('3')):
                        dt = {}
                        isperp = False
                        if vpn.access_start == vpn.access_end:
                            isperp = True
                        dt['request_id'] = vpn.request_id
                        dt['requested_by'] = vpn.user_id
                        dt['general_note'] = vpn.general_note
                        dt['confidentiality_note'] = vpn.confidentiality_note
                        dt['access_start'] = vpn.access_start
                        dt['access_end'] = vpn.access_end
                        dt['isexpired'] = vpn.isexpired
                        dt['isapproved'] = vpn.isapproved
                        dt['issubmitted'] = vpn.issubmitted
                        dt['isperpetual'] = isperp
                        dt['created_at'] = vpn.created_at
                        rtn.append(dt)
                    elif latest_apr >= curr_usr_apr or (curr_usr_apr == str('4') and latest_apr_add_1 == str('4')):
                        dt = {}
                        isperp = False
                        if vpn.access_start == vpn.access_end:
                            isperp = True
                        dt['request_id'] = vpn.request_id
                        dt['requested_by'] = vpn.user_id
                        dt['general_note'] = vpn.general_note
                        dt['confidentiality_note'] = vpn.confidentiality_note
                        dt['access_start'] = vpn.access_start
                        dt['access_end'] = vpn.access_end
                        dt['isexpired'] = vpn.isexpired
                        dt['isapproved'] = vpn.isapproved
                        dt['issubmitted'] = vpn.issubmitted
                        dt['isperpetual'] = isperp
                        dt['created_at'] = vpn.created_at
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

@vpns.route('/api/v0/requests/vpnrequests/<request_id>', methods = ['GET'])
@AuthUtil.auth_required
def find_one(sess_instance_user,request_id):
    try:
        vpn = VpnRequest.query.filter_by(request_id=request_id).first()
        if not vpn:
            return jsonify({'status':0,'request_data':None})
        rtn = []
        dt = {}
        isperp = False
        if vpn.access_start == vpn.access_end:
            isperp = True
        dt['request_id'] = vpn.request_id
        dt['requested_by'] = vpn.user_id
        dt['general_note'] = vpn.general_note
        dt['confidentiality_note'] = vpn.confidentiality_note
        dt['access_start'] = vpn.access_start
        dt['access_end'] = vpn.access_end
        dt['isexpired'] = vpn.isexpired
        dt['isapproved'] = vpn.isapproved
        dt['issubmitted'] = vpn.issubmitted
        dt['isperpetual'] = isperp
        dt['created_at'] = vpn.created_at
        rtn.append(dt)            
        return jsonify({'status':0,'request_data':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@vpns.route('/api/v0/requests/vpnrequests/user/<public_id>', methods = ['GET'])
@AuthUtil.auth_required
def find_one_by_user(sess_instance_user,public_id):
    try:
        vpns = VpnRequest.query.filter_by(user_id=public_id)
        if not vpns:
            return jsonify({'status':0,'request_data':None})
        rtn = []
        for vpn in vpns:
            dt = {}
            isperp = False
            if vpn.access_start == vpn.access_end:
                isperp = True
            dt['request_id'] = vpn.request_id
            dt['requested_by'] = vpn.user_id
            dt['general_note'] = vpn.general_note
            dt['confidentiality_note'] = vpn.confidentiality_note
            dt['access_start'] = vpn.access_start
            dt['access_end'] = vpn.access_end
            dt['isexpired'] = vpn.isexpired
            dt['isapproved'] = vpn.isapproved
            dt['issubmitted'] = vpn.issubmitted
            dt['isperpetual'] = isperp
            dt['created_at'] = vpn.created_at
            rtn.append(dt)            
        return jsonify({'status':0,'request_data':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@vpns.route('/api/v0/requests/vpnrequests', methods = ['POST'])
@AuthUtil.auth_required
def create_one(sess_instance_user):
    try:
        data = request.get_json()
        gen_id = str(uuid.uuid4())
        access_start = dtm.strptime(data['access_start'], '%d%m%Y').date()
        access_end = dtm.strptime(data['access_end'], '%d%m%Y').date()
        vrequest = VpnRequest(request_id=gen_id, user_id=data['user_id'], access_start=access_start,access_end=access_end)
        db.session.add(vrequest)
        db.session.commit()
        return jsonify({'status':0,'request_id':gen_id, 'message':'Your request has been created!'})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@vpns.route('/api/v0/requests/vpnrequests/<request_id>', methods = ['PUT'])
@AuthUtil.auth_required
def update_one(sess_instance_user, request_id):
    try:
        vrequest = VpnRequest.query.filter_by(request_id=request_id).first()
        if not vrequest:
            return jsonify({'status':-404, 'message':'Vpn request not found'})
        data = request.get_json()
        vrequest.access_start = data['access_start']
        vrequest.access_end = data['access_end']
        db.session.commit()
        return jsonify({'status':0,'message':'vpn request has been updated!'})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@vpns.route('/api/v0/requests/vpnrequests/submit/<request_id>', methods = ['PUT'])
@AuthUtil.auth_required
def submit_4_approval(sess_instance_user, request_id):
    try:
        vrequest = VpnRequest.query.filter_by(request_id=request_id,user_id=sess_instance_user.public_id,issubmitted=False).first()
        if not vrequest:
            return jsonify({'status':-404, 'message':'Vpn request not found'})
        vrequest.issubmitted = True
        db.session.commit()
        return jsonify({'status':0,'message':'Vpn request has been submitted for approval!'})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

#REPORTS
@vpns.route('/api/v0/requests/vpnrequests/reports/<search_creteria>', methods = ['GET'])
@AuthUtil.auth_required
def find_report(sess_instance_user, search_creteria):
    try:
        if not sess_instance_user.isadmin:
            return jsonify({'status':-236, 'error':'Permission denied'})
        rtn = []
        # search_creteria ===== vpn__172.... OR usr__dffjgjfgj..........
        search_c = search_creteria.split('__')
        search_type = search_c[0]
        search_item = search_c[1]
        if search_type == 'vpn':
            reports = Vpn.query.filter_by(server=search_item) 
            if not reports:
                return jsonify({'status':0,'data':None})
            for i in reports:
                dt = {}
                isperp = False
                if i.vpnrequest.access_start == i.vpnrequest.access_end:
                    isperp = True
                dt['server'] = i.server
                dt['requested_by'] = i.vpnrequest.user_id
                dt['preferred_id'] = 'N/A'
                dt['access_start'] = i.vpnrequest.access_start
                dt['access_end'] = i.vpnrequest.access_end
                dt['isexpired'] = i.vpnrequest.isexpired
                dt['isapproved'] = i.vpnrequest.isapproved
                dt['isperpetual'] = isperp
                dt['created_at'] = i.vpnrequest.created_at
                rtn.append(dt)
        elif search_type == 'usr':
            reports = Vpn.query.all()
            if not reports:
                return jsonify({'status':0,'data':None})
            for i in reports:
                dt = {}
                if i.vpnrequest.user_id == search_item:
                    isperp = False
                    if i.vpnrequest.access_start == i.vpnrequest.access_end:
                        isperp = True
                    dt['server'] = i.server
                    dt['requested_by'] = i.vpnrequest.user_id
                    dt['preferred_id'] = 'N/A'
                    dt['access_start'] = i.vpnrequest.access_start
                    dt['access_end'] = i.vpnrequest.access_end
                    dt['isexpired'] = i.vpnrequest.isexpired
                    dt['isapproved'] = i.vpnrequest.isapproved
                    dt['isperpetual'] = isperp
                    dt['created_at'] = i.vpnrequest.created_at
                    rtn.append(dt)
                else:
                    pass
        return jsonify({'status':0,'data':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})


# VPN REQUESTS INFO
@vpns.route('/api/v0/requests/vpninfo', methods = ['GET'])
@AuthUtil.auth_required
def vpn_find_all(sess_instance_user):
    if not sess_instance_user.isadmin and not sess_instance_user.can_approve_vpn:
        return jsonify({'status':-236, 'error':'Permission denied'})
    try:
        infs = Vpn.query.all()
        rtn = []
        for inf in infs:
            dt = {}
            dt['public_id'] = inf.public_id
            dt['server'] = inf.server
            dt['reason'] = inf.reason
            dt['access_type'] = inf.access_type
            dt['request_id'] = inf.req_id
            dt['created_at'] = inf.created_at
            rtn.append(dt)
        return jsonify({'status':0,'requests_info':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@vpns.route('/api/v0/requests/vpninfo/byserver', methods = ['GET'])
@AuthUtil.auth_required
def find_all_by_svr(sess_instance_user):
    if not sess_instance_user.isadmin and not sess_instance_user.can_approve_vpn:
        return jsonify({'status':-236, 'error':'Permission denied'})
    try:
        infs = Vpn.query.with_entities(Vpn.server).distinct()
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

@vpns.route('/api/v0/requests/vpninfo/<public_id>', methods = ['GET'])
@AuthUtil.auth_required
def vpn_find_one(sess_instance_user,public_id):
    try:
        inf = Vpn.query.filter_by(public_id=public_id).first()
        if not inf:
            return jsonify({'status':0,'request_info':None})
        rtn = []
        dt = {}
        dt['public_id'] = inf.public_id
        dt['server'] = inf.server
        dt['reason'] = inf.reason
        dt['access_type'] = inf.access_type
        dt['request_id'] = inf.req_id
        dt['created_at'] = inf.created_at
        rtn.append(dt)            
        return jsonify({'status':0,'request_data':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@vpns.route('/api/v0/requests/vpnrequestinfo/<request_id>', methods = ['GET'])
@AuthUtil.auth_required
def vpn_find_one_by_request(sess_instance_user,request_id):
    try:
        infs = Vpn.query.filter_by(req_id=request_id)
        if not infs:
            return jsonify({'status':0,'request_info':None})
        rtn = []
        for inf in infs:
            dt = {}
            dt['public_id'] = inf.public_id
            dt['server'] = inf.server
            dt['reason'] = inf.reason
            dt['access_type'] = inf.access_type
            dt['request_id'] = inf.req_id
            dt['created_at'] = inf.created_at
            rtn.append(dt)
        return jsonify({'status':0,'data':rtn})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@vpns.route('/api/v0/requests/vpninfo', methods = ['POST'])
@AuthUtil.auth_required
def vpn_create_one(sess_instance_user):
    try:
        data = request.get_json()
        vpn_info = Vpn(public_id=str(uuid.uuid4()),server=data['server'], reason=data['reason'],access_type=data['access_type'],req_id=data['request_id'])
        db.session.add(vpn_info)
        db.session.commit()
        return jsonify({'status':0,'message':'Vpn request info added successfully!'})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})

@vpns.route('/api/v0/requests/vpninfo/<public_id>', methods = ['PUT'])
@AuthUtil.auth_required
def vpn_update_one(sess_instance_user, public_id):
    try:
        vinfo = Vpn.query.filter_by(public_id=public_id).first()
        if not vinfo:
            return jsonify({'status':-404, 'message':'Vpn request info not found'})
        data = request.get_json()
        vinfo.server = data['server']
        vinfo.reason = data['reason']
        vinfo.access_type = data['access_type']
        vinfo.req_id = data['request_id']
        db.session.commit()
        return jsonify({'status':0,'message':'vpn request info has been updated!'})
    except Exception as err:
        f = open(str(current_app.config['LOGS_PATH']), 'a+')
        f.write(str(err))
        f.close()
        return jsonify({'status':-233,'error':'Invalid request payload params'})