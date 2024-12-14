from flask import Blueprint, request, jsonify
from app.services.leave_request_service import request_leave,get_employee_leave_requests,get_all_leave_requests,update_leave_request_status
from flask_jwt_extended import jwt_required
bp = Blueprint('leave_request', __name__, url_prefix='/leave_request')
#  tạo đơn xin nghỉ.
@bp.route('/create', methods=['POST'])
def create_leave():
    data = request.get_json()
    return request_leave(data)

# Nhân viên xem đơn xin nghỉ
@bp.route('/employee_requests', methods=['GET'])
def employee_requests():
    id_employee = request.args.get('id_employee')
    if not id_employee:
        return jsonify({'error': 'Missing employee ID'}), 400

    response, status = get_employee_leave_requests(id_employee)
    return jsonify(response), status
@bp.route('/getAll', methods=['GET'])
@jwt_required()
def admin_requests():
    response, status = get_all_leave_requests()
    return jsonify(response), status
@bp.route('/approve/<int:request_id>', methods=['POST'])
@jwt_required()
def approve_request(request_id):
    response, status = update_leave_request_status(request_id, 'Approved')
    return jsonify(response), status

@bp.route('/reject/<int:request_id>', methods=['POST'])
@jwt_required()
def reject_request(request_id):
    response, status = update_leave_request_status(request_id, 'Rejected')
    return jsonify(response), status